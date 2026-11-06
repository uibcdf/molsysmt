"""Keep naming recognition independent of exact chemistry and stable membership."""

import importlib

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.native import MolSys, Topology

parent = msm.element.group.amino_acid.get_standard_name
recognize = msm.element.group.amino_acid.is_amino_acid
kind = msm.element.group.get_group_type_from_group_name


@pytest.mark.parametrize(
    "name,scheme,expected_parent,expected_kind",
    [
        ("GLH", "amber", "GLU", "amino acid"),
        ("GLH", "legacy", "GLN", "amino acid"),
        ("HID", "amber", "HIS", "amino acid"),
        ("HID", "ccd", None, "small molecule"),
        ("ASH", "amber", "ASP", "amino acid"),
        ("ASH", "ccd", None, "small molecule"),
        ("CYX", "amber", "CYS", "amino acid"),
        ("CYX", "ccd", None, "small molecule"),
        ("XAA", "sequence", None, "amino acid"),
        ("XAA", "ccd", None, "small molecule"),
        ("XLE", "sequence", None, "amino acid"),
        ("XLE", "ccd", None, "small molecule"),
        ("MSE", "ccd", "MET", "amino acid"),
        ("SEP", "ccd", "SER", "amino acid"),
        ("ALA", None, None, "amino acid"),
    ],
)
def test_public_interpretations_share_reviewed_meanings(
    name, scheme, expected_parent, expected_kind
):
    assert parent(name, naming_scheme=scheme) == expected_parent
    assert kind(name, naming_scheme=scheme) == expected_kind
    assert recognize(name, naming_scheme=scheme) == (expected_kind == "amino acid")


@pytest.mark.parametrize("function", [parent, recognize, kind])
@pytest.mark.parametrize(
    "name", ["GLH", "HID", "ASH", "CYX", "HIP", "LYN", "XAA", "XLE"]
)
def test_ambiguous_scalar_queries_require_context(function, name):
    with pytest.raises(ArgumentError) as error:
        function(name)
    assert error.value.extra["argument"] == "naming_scheme"


@pytest.mark.parametrize("function", [parent, recognize, kind])
@pytest.mark.parametrize("bad", ["unknown", "AMBER", 1, ["amber"], False])
def test_invalid_profiles_use_argdigest_diagnostics(function, bad):
    with pytest.raises(ArgumentChoiceError) as error:
        function("ALA", naming_scheme=bad)
    assert error.value.extra["argument"] == "naming_scheme"


@pytest.mark.parametrize("function", [parent, recognize, kind])
@pytest.mark.parametrize("bad", ["true", 1, None])
def test_skip_digestion_is_boolean_at_each_public_boundary(function, bad):
    with pytest.raises(ArgumentError) as error:
        function("ALA", skip_digestion=bad)
    assert error.value.extra["argument"] == "skip_digestion"


@pytest.mark.parametrize("missing", [None, pd.NA, np.nan])
def test_missing_group_labels_do_not_invent_identity(missing):
    assert parent(missing) is None
    assert kind(missing) == "unknown"


def test_unassessed_default_names_do_not_activate_legacy_parents():
    assert parent("PCA") is None
    assert parent("PCA", naming_scheme="legacy") == "GLU"
    assert kind("PCA") == "unknown"
    assert not recognize("PCA")
    with pytest.raises(ArgumentError):
        parent("PCA", naming_scheme="amber")
    assert kind("PCA", naming_scheme="amber") == "unknown"
    assert not recognize("PCA", naming_scheme="amber")


def mixed_topology(*, atoms=True):
    topology = Topology(
        n_atoms=4 if atoms else 0, n_groups=4, n_molecules=1, n_entities=1, n_chains=1
    )
    topology.groups["group_name"] = pd.array(["ASH"] * 4, dtype="string")
    topology.groups["group_id"] = pd.array(["a", "b", "c", "d"], dtype="string")
    topology.groups["group_type"] = pd.array(["unknown"] * 4, dtype="string")
    topology.groups["molecule_index"] = pd.array([0] * 4, dtype="Int64")
    topology.molecules["molecule_id"] = pd.array(["m"], dtype="string")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.chains["chain_id"] = pd.array(["A"], dtype="string")
    topology.set_group_naming_schemes(["amber", "ccd", None, "legacy"])
    if atoms:
        topology.atoms["atom_id"] = ["a", "b", "c", "d"]
        topology.atoms["atom_name"] = ["N"] * 4
        topology.atoms["group_index"] = pd.array([3, 1, 0, 2], dtype="Int64")
        topology.atoms["chain_index"] = pd.array([0] * 4, dtype="Int64")
    else:
        topology.set_chain_groups([[0, 1, 2, 3]])
    return topology


@pytest.mark.parametrize("atoms", [True, False])
def test_rebuilding_types_uses_per_group_context_and_preserves_membership(atoms):
    topology = mixed_topology(atoms=atoms)
    names = topology.groups[["group_id", "group_name", "molecule_index"]].copy()
    molecules = topology.molecules.copy()
    chains = topology.chains.copy()
    topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    assert topology.groups["group_type"].tolist() == [
        "amino acid",
        "small molecule",
        "unknown",
        "amino acid",
    ]
    pd.testing.assert_frame_equal(
        names, topology.groups[names.columns], check_frame_type=False
    )
    pd.testing.assert_frame_equal(molecules, topology.molecules, check_frame_type=False)
    pd.testing.assert_frame_equal(chains, topology.chains, check_frame_type=False)
    assert topology.group_naming_schemes == ("amber", "ccd", None, "legacy")
    assert topology.n_atoms == (4 if atoms else 0)


@pytest.mark.parametrize("as_molsys", [True, False])
def test_nonconsecutive_redefinition_never_groups_by_label_alone(as_molsys):
    topology = mixed_topology()
    source = MolSys._from_partial_domains(topology=topology) if as_molsys else topology
    assert msm.element.group.get_group_type(
        source, selection=[3, 1, 0], redefine_types=True
    ) == ["amino acid", "small molecule", "amino acid"]
    assert msm.element.group.get_group_type(
        source, selection=[2, 0, 1], element="atom", redefine_types=True
    ) == ["amino acid", "amino acid", "small molecule"]
    assert topology.groups["group_type"].tolist() == ["unknown"] * 4
    if as_molsys:
        assert source.structures is source.chemical_states is None


def test_declaration_supports_projection_without_silently_rewriting_stored_types():
    topology = mixed_topology(atoms=False)
    assert (
        msm.convert(topology, to_form="string:amino_acids_1", group_indices=[0, 3])
        == "DD"
    )
    with pytest.raises(ArgumentError):
        msm.convert(topology, to_form="string:amino_acids_1", group_indices=[2])
    assert topology.groups["group_type"].tolist() == ["unknown"] * 4


def test_raw_openmm_inventory_preserves_ambiguous_labels_without_assuming_amber():
    from openmm.app import Topology, element

    external = Topology()
    chain = external.addChain("A")
    for label in ("HID", "ASH", "ALA"):
        group = external.addResidue(label, chain)
        external.addAtom("N", element.nitrogen, group)
    native = msm.convert(external, to_form="molsysmt.Topology")
    assert native.groups["group_name"].tolist() == ["HID", "ASH", "ALA"]
    assert native.groups["group_type"].tolist() == ["unknown", "unknown", "amino acid"]
    assert native.group_naming_schemes == (None, None, None)
    assert (
        msm.convert(native, to_form="string:amino_acids_1", from_naming_scheme="amber")
        == "HDA"
    )
    assert native.groups["group_type"].tolist() == ["unknown", "unknown", "amino acid"]


def test_private_rebuild_never_calls_public_name_query(monkeypatch):
    module = importlib.import_module("molsysmt.element.group.get_group_type")

    def forbid(*args, **kwargs):
        pytest.fail("Native inference must not re-enter the public query layer.")

    monkeypatch.setattr(module, "get_group_type_from_group_name", forbid)
    monkeypatch.setattr(msm.element.group, "get_group_type_from_group_name", forbid)
    topology = mixed_topology()
    topology.rebuild_groups(redefine_ids=False, redefine_types=True)
    assert topology.groups["group_type"].tolist() == [
        "amino acid",
        "small molecule",
        "unknown",
        "amino acid",
    ]


@pytest.mark.parametrize(
    "label,expected", [("HOH", "water"), ("NA", "ion"), ("ACE", "terminal capping")]
)
def test_independent_non_peptide_catalogs_are_not_parent_templates(label, expected):
    assert parent(label, naming_scheme="amber") is None
    assert kind(label, naming_scheme="amber") == expected


def test_declared_ccd_non_peptide_cannot_be_overridden_by_atom_name_heuristic():
    topology = Topology(n_atoms=5, n_groups=1)
    topology.atoms["atom_name"] = ["N", "CA", "C", "O", "CB"]
    topology.atoms["group_index"] = pd.array([0] * 5, dtype="Int64")
    topology.groups["group_name"] = ["HID"]
    topology.set_group_naming_schemes("ccd")
    assert msm.element.group.get_group_type(topology, redefine_types=True) == [
        "small molecule"
    ]


def test_all_group_redefinition_is_a_query_without_copy_or_public_dispatch(monkeypatch):
    topology = mixed_topology()

    def forbid(*args, **kwargs):
        pytest.fail("A type query must not copy or re-enter the dispatch layer.")

    monkeypatch.setattr(topology, "copy", forbid)
    monkeypatch.setattr(msm, "get", forbid)
    assert msm.element.group.get_group_type(topology, redefine_types=True) == [
        "amino acid",
        "small molecule",
        "unknown",
        "amino acid",
    ]
    assert topology.groups["group_type"].tolist() == ["unknown"] * 4


def test_missing_type_can_be_projected_from_an_explicit_assessed_declaration():
    topology = Topology(n_groups=1)
    topology.groups["group_name"] = ["GLH"]
    topology.set_group_naming_schemes("amber")
    assert msm.convert(topology, to_form="string:amino_acids_1") == "E"
    assert topology.groups["group_type"].isna().all()


def test_uninitialized_group_labels_and_types_remain_missing_not_literal_nan():
    topology = Topology(n_groups=2)
    assert topology.groups["group_name"].isna().all()
    assert topology.groups["group_type"].isna().all()
    assert msm.element.group.get_group_type(topology) == ["unknown", "unknown"]


@pytest.mark.parametrize(
    "function,expected", [(parent, "HIS"), (recognize, True), (kind, "amino acid")]
)
def test_optional_attribution_failure_preserves_recognition(
    function, expected, monkeypatch
):
    from molsysmt import _ackredit

    def unavailable():
        raise RuntimeError("Controlled optional-provider failure")

    monkeypatch.setattr(_ackredit, "backend", unavailable)
    assert function("HID", naming_scheme="amber") == expected


def test_non_peptide_recognition_credits_its_ccd_data_not_a_molecular_engine():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("CCD recognition"):
        with ackredit.capture("recognition") as capture:
            assert not recognize("HID", naming_scheme="ccd")
        items = capture.attribution.to_dict()["items"]
        assert {item["id"] for item in items} == {"rcsb-ccd-group-names-20261104"}


def test_direct_module_import_is_the_supported_classifier():
    from molsysmt.element.group.get_group_type_from_group_name import (
        get_group_type_from_group_name,
    )

    assert get_group_type_from_group_name is kind
    assert msm.element.group.get_group_type_from_group_name is kind
    assert get_group_type_from_group_name("ALA") == "amino acid"
