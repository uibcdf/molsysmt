"""Compare exact-name references rather than projecting chemical parents."""

import warnings

import numpy as np
import pytest

from molsysmt import _ackredit
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.element.group.amino_acid import (
    get_expected_heavy_atoms as heavy,
)
from molsysmt.element.group.amino_acid import (
    get_expected_hydrogens as hydrogens,
)
from molsysmt.element.group.amino_acid import (
    get_group_db,
)

STATES = {
    "GLH": ({"OE1", "OE2"}, {"N1", "N2", "C1"}, {"HE2"}, set()),
    "HID": ({"ND1", "NE2"}, {"P"}, {"HD1"}, {"HE2"}),
    "HIE": ({"ND1", "NE2"}, {"P"}, {"HE2"}, {"HD1"}),
    "HIP": ({"ND1", "NE2"}, {"P", "O1P", "O2P", "O3P"}, {"HD1", "HE2"}, set()),
    "ASH": ({"OD1", "OD2"}, {"P"}, {"HD2"}, set()),
    "CYM": ({"SG"}, {"CD"}, set(), {"HG", "HG1"}),
    "CYX": ({"SG"}, {"CD"}, set(), {"HG", "HG1"}),
    "LYN": ({"NZ"}, {"NT"}, {"HZ1", "HZ2"}, {"HZ3"}),
}


@pytest.mark.parametrize("name,expected", STATES.items())
@pytest.mark.parametrize("pH", [2.0, 12.0])
def test_amber_state_uses_verified_connectivity_and_preserves_named_sidechain(
    name, expected, pH
):
    present, absent, required_h, forbidden_h = expected
    atoms = heavy(name, naming_scheme="amber")
    hs = set(hydrogens(name, naming_scheme="amber", pH=pH))
    assert present <= atoms
    assert not absent & atoms
    assert required_h <= hs
    assert not forbidden_h & hs
    assert "OXT" not in atoms


@pytest.mark.parametrize("name", STATES)
@pytest.mark.parametrize("function", [heavy, hydrogens])
def test_bare_ambiguous_reference_requires_context(name, function):
    with pytest.raises(ArgumentError) as error:
        function(name)
    assert error.value.extra["argument"] == "naming_scheme"


@pytest.mark.parametrize("name", ["HID", "HIP", "ASH", "CYX", "LYN"])
@pytest.mark.parametrize("scheme", ["ccd", "legacy"])
@pytest.mark.parametrize("function", [heavy, hydrogens])
def test_other_vocabulary_cannot_reuse_the_amber_state_reference(
    name, scheme, function
):
    assert function(name, naming_scheme=scheme) is None


@pytest.mark.parametrize("name", STATES)
@pytest.mark.parametrize("terminal", ["is_n_terminal", "is_c_terminal"])
def test_named_state_terminal_completion_is_explicitly_unassessed(name, terminal):
    assert hydrogens(name, naming_scheme="amber", **{terminal: True}) is None


@pytest.mark.parametrize("name", ["MSE", "SEP", "TPO", "MLY"])
def test_modified_heavy_reference_never_authorizes_parent_hydrogens(name):
    assert heavy(name) is not None
    assert hydrogens(name) is None
    assert heavy(name, naming_scheme="amber") is None


@pytest.mark.parametrize("function", [heavy, hydrogens])
@pytest.mark.parametrize("bad", ["N", 5, [["N"]], [None], np.ma.array(["N"])])
def test_invalid_atom_lists_are_rejected_at_the_public_boundary(function, bad):
    with pytest.raises(ArgumentError) as error:
        function("ALA", present_atom_names=bad)
    assert error.value.extra["argument"] == "present_atom_names"


@pytest.mark.parametrize("function", [heavy, hydrogens])
@pytest.mark.parametrize("bad", ["true", 1, None])
def test_standard_skip_contract_is_boolean(function, bad):
    with pytest.raises(ArgumentError) as error:
        function("ALA", skip_digestion=bad)
    assert error.value.extra["argument"] == "skip_digestion"


@pytest.mark.parametrize("function", [heavy, hydrogens])
def test_unknown_profile_is_not_a_legacy_fallback(function):
    with pytest.raises(ArgumentChoiceError):
        function("ALA", naming_scheme="invented")


@pytest.mark.parametrize("bad", [True, float("nan"), float("inf"), "7.4", None])
def test_ph_requires_a_finite_dimensionless_number(bad):
    with pytest.raises(ArgumentError) as error:
        hydrogens("ALA", pH=bad)
    assert error.value.extra["argument"] == "pH"


@pytest.mark.parametrize("flag", ["is_n_terminal", "is_c_terminal", "is_disulfide"])
def test_context_flags_are_boolean(flag):
    with pytest.raises(ArgumentError) as error:
        hydrogens("ALA", **{flag: 1})
    assert error.value.extra["argument"] == flag


def test_heavy_conflict_is_not_replaced_by_the_first_catalogue_variant():
    assert heavy("ALA", ["N", "CA", "invented"]) is None
    assert hydrogens("ALA", ["N", "CA", "invented"]) is None
    assert heavy("GLH", ["N", "CA", "N1"], naming_scheme="amber") is None
    assert hydrogens("GLH", ["N", "CA", "N1"], naming_scheme="amber") is None


def test_raw_catalogue_is_not_rewritten_or_reordered():
    before = get_group_db("GLH")
    assert "N1" in before["topology"][0]["atoms"]
    assert "OE2" in heavy("GLH", naming_scheme="amber")
    assert get_group_db("GLH") == before


def test_caller_names_and_reference_outputs_are_independent():
    names = np.array(["N", "CA", "C", "O", "CB"], dtype=object)
    names.flags.writeable = False
    first = heavy("ALA", names)
    first.add("not a reference atom")
    assert "not a reference atom" not in heavy("ALA", names)
    np.testing.assert_array_equal(names, ["N", "CA", "C", "O", "CB"])


def test_optional_attribution_failure_preserves_expected_atoms(monkeypatch):
    def broken():
        raise RuntimeError("controlled attribution failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings(record=True):
        assert "OE2" in heavy("GLH", naming_scheme="amber")
        assert "HE2" in hydrogens("GLH", naming_scheme="amber")


def test_state_inventory_credits_verification_data_without_running_an_engine():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("atom references"):
        with ackredit.capture("reference") as capture:
            assert "HE2" in hydrogens("GLH", naming_scheme="amber")
        items = capture.attribution.to_dict()["items"]
        assert all(item["type"] == "dataset" for item in items)
        assert any(
            item["id"].startswith("dataset:meeko-residue-templates:") for item in items
        )
        assert any(
            item["id"].startswith("dataset:molsysmt-amino-acid-catalogue:")
            for item in items
        )


@pytest.mark.parametrize(
    "conflict", ["heavy_edge", "hydrogen_count", "hydrogen_parent"]
)
def test_state_verification_rejects_conflicting_bundled_graphs(monkeypatch, conflict):
    import copy

    from molsysmt._private import amino_acid_templates as references
    from molsysmt._private.smonitor import StructuralInconsistencyError

    variant = copy.deepcopy(get_group_db("GLH")["topology"][2])
    if conflict == "heavy_edge":
        variant["bonds"] = [p for p in variant["bonds"] if set(p) != {"CD", "OE2"}]
    elif conflict == "hydrogen_count":
        variant["atoms"].remove("HE2")
        variant["bonds"] = [p for p in variant["bonds"] if "HE2" not in p]
    else:
        variant["bonds"] = [
            ["HE2", "OE1"] if "HE2" in p else p for p in variant["bonds"]
        ]
    monkeypatch.setattr(references, "_catalogue", lambda name: (variant,))
    references._verified_state_variants.cache_clear()
    try:
        with pytest.raises(StructuralInconsistencyError):
            heavy("GLH", naming_scheme="amber")
    finally:
        references._verified_state_variants.cache_clear()


@pytest.mark.parametrize("dispatcher", [False, True])
@pytest.mark.parametrize("name", ["GLH", "HIP", "ASH", "CYM", "LYN"])
def test_reference_bond_maps_use_the_exact_named_state(dispatcher, name):
    import molsysmt as msm

    tool = (
        msm.element.group.get_bonded_atom_pairs
        if dispatcher
        else msm.element.group.amino_acid.get_bonded_atom_pairs
    )
    hs = hydrogens(name, naming_scheme="amber")
    names = sorted(heavy(name, naming_scheme="amber")) + hs
    indices = np.arange(50, 50 + len(names), dtype=np.int64)
    pairs = tool(name, names, atom_indices=indices, naming_scheme="amber")
    assert pairs
    local = {n: int(i) for n, i in zip(names, indices)}
    for h in hs:
        incident = [p for p in pairs if local[h] in p]
        assert len(incident) == 1
        other = next(i for i in incident[0] if i != local[h])
        assert names[other - 50] not in hs


@pytest.mark.parametrize("dispatcher", [False, True])
def test_reference_bond_queries_require_context_before_catalogue_access(dispatcher):
    import molsysmt as msm

    tool = (
        msm.element.group.get_bonded_atom_pairs
        if dispatcher
        else msm.element.group.amino_acid.get_bonded_atom_pairs
    )
    with pytest.raises(ArgumentError):
        tool("GLH", ["N", "CA"])
    assert tool("GLH", "N", atom_indices=50, naming_scheme="amber") == []
