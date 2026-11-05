"""Keep construction labels, chemistry references and declared naming coherent."""

import copy
import importlib

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import _ackredit
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    NotImplementedMethodError,
)
from molsysmt.native import Topology

STATES = {
    "GLH": ({"HE2"}, set()),
    "HID": ({"HD1"}, {"HE2"}),
    "HIE": ({"HE2"}, {"HD1"}),
    "HIP": ({"HD1", "HE2"}, set()),
    "ASH": ({"HD2"}, set()),
    "CYM": (set(), {"HG", "HG1"}),
    "CYX": (set(), {"HG", "HG1"}),
    "LYN": ({"HZ2", "HZ3"}, {"HZ1"}),
}


@pytest.mark.parametrize(
    "text,expected",
    [
        ("AG", ["ALA", "GLY"]),
        ("AlaGly", ["ALA", "GLY"]),
        ("amino_acids_1:ALA", ["ALA", "LEU", "ALA"]),
        ("amino_acids_3:ALA", ["ALA"]),
    ],
)
def test_string_sequence_syntax_is_explicit_and_output_has_known_producer_context(
    text, expected
):
    output = msm.build.build_peptide(text)
    assert output.topology.groups.group_name.tolist() == expected
    assert output.topology.group_naming_schemes == ("amber",) * len(expected)


@pytest.mark.parametrize("state", STATES)
def test_reviewed_named_states_require_explicit_source_context(state):
    with pytest.raises(ArgumentError) as error:
        msm.build.build_peptide("amino_acids_3:ALA" + state + "ALA")
    assert error.value.extra["argument"] == "naming_scheme"


@pytest.mark.parametrize("state", STATES)
def test_constructed_state_layout_is_recognized_without_adding_or_removing_alias_hydrogens(
    state,
):
    output = msm.build.build_peptide(
        "amino_acids_3:ALA" + state + "ALA", from_naming_scheme="amber"
    )
    selected = output.topology.atoms.group_index == 1
    names = output.topology.atoms.loc[selected, "atom_name"].tolist()
    required, excluded = STATES[state]
    assert required <= set(names)
    assert not excluded.intersection(names)
    expected = msm.element.group.amino_acid.get_expected_hydrogens(
        state, present_atom_names=names, naming_scheme="amber", pH=12.0
    )
    assert set(expected) == {name for name in names if name.startswith("H")}
    added = msm.build.add_missing_hydrogens(output, engine="MolSysMT", pH=7.4)
    pd.testing.assert_frame_equal(added.topology.atoms, output.topology.atoms)
    reconciled = msm.build.reconcile_protonation(output, pH=7.4)
    pd.testing.assert_frame_equal(reconciled.topology.atoms, output.topology.atoms)
    assert reconciled.topology.group_naming_schemes == ("amber",) * 3


@pytest.mark.parametrize("state", ["GLH", "HID", "HIP", "LYN"])
def test_declared_amber_caps_keep_their_methyl_hydrogens(state):
    source = msm.build.build_peptide(
        "amino_acids_3:ACE" + state + "NME", from_naming_scheme="amber"
    )
    result = msm.build.add_missing_hydrogens(source, engine="MolSysMT")
    pd.testing.assert_frame_equal(source.topology.atoms, result.topology.atoms)
    assert source.topology.group_naming_schemes == result.topology.group_naming_schemes


@pytest.mark.parametrize("state", ["HID", "HIP", "ASH", "CYX", "LYN"])
@pytest.mark.parametrize("scheme", ["ccd", "legacy"])
def test_non_amber_meaning_never_selects_same_spelled_amber_construction(state, scheme):
    with pytest.raises(NotImplementedMethodError):
        msm.build.build_peptide(
            "amino_acids_3:ALA" + state + "ALA", from_naming_scheme=scheme
        )


@pytest.mark.parametrize("text", ["amino_acids_3:MSE", "amino_acids_1:X"])
def test_unassessed_construction_never_substitutes_a_parent_or_unknown_symbol(text):
    with pytest.raises(NotImplementedMethodError):
        msm.build.build_peptide(text)


@pytest.mark.parametrize(
    "form", ["molsysmt.Topology", "molsysmt.MolSys", "molsysmt.TopologyDict"]
)
def test_molecular_input_keeps_exact_names_and_source_metadata_without_parent_projection(
    form,
):
    source = msm.convert(
        "amino_acids_3:ALAGLHALA",
        to_form="molsysmt.Topology",
        from_naming_scheme="amber",
    )
    source = msm.convert(source, to_form=form)
    topology = (
        source
        if isinstance(source, Topology)
        else msm.convert(source, to_form="molsysmt.Topology")
    )
    before = topology.groups.copy()
    result = msm.build.build_peptide(source)
    assert result.topology.groups.group_name.tolist() == ["ALA", "GLH", "ALA"]
    assert msm.convert(result, to_form="string:amino_acids_1") == "AEA"
    pd.testing.assert_frame_equal(before, topology.groups, check_frame_type=False)
    assert topology.group_naming_schemes == ("amber",) * 3
    assert topology.n_atoms == 0


def test_conflicting_source_override_is_rejected_without_editing_declarations():
    source = msm.convert(
        "amino_acids_3:HIP", to_form="molsysmt.Topology", from_naming_scheme="ccd"
    )
    with pytest.raises(ArgumentError) as error:
        msm.build.build_peptide(source, from_naming_scheme="amber")
    assert error.value.extra["argument"] == "from_naming_scheme"
    assert source.group_naming_schemes == ("ccd",)


@pytest.mark.parametrize("form", ["molsysmt.Topology", "molsysmt.TopologyDict"])
def test_topology_outputs_preserve_generated_context_through_transport(form, tmp_path):
    source = msm.build.build_peptide(
        "amino_acids_3:ALAHIDALA", from_naming_scheme="amber", to_form=form
    )
    topology = msm.convert(source, to_form="molsysmt.Topology")
    assert topology.group_naming_schemes == ("amber",) * 3
    filename = msm.convert(topology, to_form=str(tmp_path / "peptide.h5msm"))
    loaded = msm.convert(filename, to_form="molsysmt.Topology")
    assert loaded.group_naming_schemes == ("amber",) * 3
    assert loaded.groups.group_name.tolist() == ["ALA", "HID", "ALA"]


@pytest.mark.parametrize("state", ["GLH", "HIP", "CYM", "LYN"])
def test_missing_construction_database_uses_verified_state_variant_instead_of_first_raw_compound(
    monkeypatch, state
):
    module = importlib.import_module("molsysmt.build.build_peptide")
    monkeypatch.setattr(module, "_get_peptide_builder_templates", lambda: {})
    with pytest.warns(UserWarning, match="fallback topology"):
        output = msm.build.build_peptide(
            "amino_acids_3:ALA" + state + "ALA", from_naming_scheme="amber"
        )
    names = set(
        output.topology.atoms.loc[output.topology.atoms.group_index == 1, "atom_name"]
    )
    assert {"N", "CA", "C", "O"} <= names
    assert not {"N1", "N2", "O1P", "NT"}.intersection(names)
    if state == "GLH":
        assert {"OE1", "OE2", "HE2"} <= names
    if state == "LYN":
        assert {"NZ", "HZ1", "HZ2"} <= names and "HZ3" not in names


def test_native_construction_credits_data_without_claiming_an_executed_external_engine():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("peptide construction"), ackredit.capture("build") as run:
        msm.build.build_peptide("AG")
    items = run.attribution.to_dict()["items"]
    assert any(
        item["id"].startswith("dataset:molsysmt-peptide-builder:") for item in items
    )
    assert all(item["type"] == "dataset" for item in items)


@pytest.mark.parametrize("failure", [False, True])
def test_optional_attribution_absence_or_failure_preserves_construction(
    monkeypatch, failure
):
    def backend():
        if failure:
            raise RuntimeError("controlled construction attribution failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    if failure:
        with pytest.warns(Warning, match="controlled construction attribution failure"):
            result = msm.build.build_peptide("AG")
    else:
        result = msm.build.build_peptide("AG")
    assert result.topology.groups.group_name.tolist() == ["ALA", "GLY"]


def test_coverage_identifies_additional_atom_layout_source():
    system = msm.build.build_peptide(
        "amino_acids_3:ALAHIDALA", from_naming_scheme="amber"
    )
    report = msm.build.get_residue_chemical_coverage(system)["groups"][1]
    assert report["hydrogens"]["status"] == "unassessed"
    assert report["hydrogens"]["reason_code"] == "ambiguous_hydrogen_template_variants"
    assert any(
        not c["missing_atom_names"] and not c["unexpected_atom_names"]
        for c in report["hydrogens"]["candidates"]
    )
    sources = report["template"]["variant_sources"].values()
    assert any(
        source["resource"].endswith("peptide_builder/amber14sb.json.gz")
        for source in sources
    )
    assert any(
        source["resource"].endswith("amino_acids/H.pkl.gz") for source in sources
    )


def test_conflicting_construction_layout_cannot_hide_behind_a_valid_catalogue(
    monkeypatch,
):
    from molsysmt._private import amino_acid_templates, peptide_builder_data
    from molsysmt._private.smonitor import StructuralInconsistencyError

    original = peptide_builder_data.atom_variant

    def corrupt(name):
        variant = copy.deepcopy(original(name))
        variant["bonds"] = [
            pair for pair in variant["bonds"] if set(pair) != {"CD", "OE2"}
        ]
        return variant

    monkeypatch.setattr(peptide_builder_data, "atom_variant", corrupt)
    amino_acid_templates._verified_state_variants.cache_clear()
    try:
        with pytest.raises(StructuralInconsistencyError):
            msm.element.group.amino_acid.get_expected_heavy_atoms(
                "GLH", naming_scheme="amber"
            )
    finally:
        amino_acid_templates._verified_state_variants.cache_clear()


@pytest.mark.parametrize(
    "kwargs", [dict(skip_digestion=1), dict(from_naming_scheme="invented")]
)
def test_new_arguments_are_validated_at_public_boundary(kwargs):
    expected = ArgumentChoiceError if "from_naming_scheme" in kwargs else ArgumentError
    with pytest.raises(expected):
        msm.build.build_peptide("AG", **kwargs)


def test_group_declaration_does_not_force_one_atom_naming_layout_on_caps():
    source = msm.build.build_peptide("ACEALANME")
    mapping = {"H1": "HH31", "H2": "HH32", "H3": "HH33"}
    mask = source.topology.atoms.group_index == 0
    source.topology.atoms.loc[mask, "atom_name"] = source.topology.atoms.loc[
        mask, "atom_name"
    ].map(lambda name: mapping.get(name, name))
    result = msm.build.add_missing_hydrogens(source, engine="MolSysMT")
    pd.testing.assert_frame_equal(source.topology.atoms, result.topology.atoms)


def test_h5msm_source_reads_exact_group_context_without_materializing_structures(
    tmp_path, monkeypatch
):
    topology = msm.convert(
        "amino_acids_3:ALAGLHALA",
        to_form="molsysmt.Topology",
        from_naming_scheme="amber",
    )
    filename = msm.convert(topology, to_form=str(tmp_path / "source.h5msm"))
    from molsysmt import h5msm

    original = h5msm.read_layers

    def topology_only(*args, **kwargs):
        assert kwargs["layers"] == ["topology"]
        return original(*args, **kwargs)

    monkeypatch.setattr(h5msm, "read_layers", topology_only)
    result = msm.build.build_peptide(filename)
    assert result.topology.groups.group_name.tolist() == ["ALA", "GLH", "ALA"]
    assert result.topology.group_naming_schemes == ("amber",) * 3


def test_unsupported_source_context_is_rejected_before_optional_engine_or_construction_data(
    monkeypatch,
):
    module = importlib.import_module("molsysmt.build.build_peptide")

    def forbidden(*args, **kwargs):
        pytest.fail("construction began before validating the source context")

    monkeypatch.setattr(module, "_get_peptide_builder_templates", forbidden)
    monkeypatch.setattr("molsysmt.third_party.tleap.TLeap", forbidden)
    for engine in ("MolSysMT", "LEaP"):
        with pytest.raises(NotImplementedMethodError):
            msm.build.build_peptide(
                "amino_acids_3:HIP", from_naming_scheme="ccd", engine=engine
            )


def test_amber_cap_preparation_credits_the_layout_data_it_uses():
    ackredit = pytest.importorskip("ackredit")
    source = msm.build.build_peptide("ACEALANME")
    with ackredit.session("cap preparation"), ackredit.capture("prepare") as run:
        msm.build.add_missing_hydrogens(source, engine="MolSysMT")
    items = run.attribution.to_dict()["items"]
    assert any(
        item["id"].startswith("dataset:molsysmt-peptide-builder:") for item in items
    )
    assert all(item["type"] == "dataset" for item in items)
