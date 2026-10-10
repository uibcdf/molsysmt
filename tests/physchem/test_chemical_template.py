"""Protecting explicit template transfer, unresolved chemistry and source poses."""

import subprocess
import sys
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology

PROVENANCE = dict(
    identity="methanol independent control",
    version="1",
    source_uri="fixture:methanol",
    checksum="declared:fixture-1",
    hydrogen_policy="explicit_atoms",
)


def _template():
    topology = Topology(n_atoms=6)
    topology.atoms["atom_type"] = ["C", "O", "H", "H", "H", "H"]
    topology.atoms["atom_id"] = ["carbon", "oxygen", "h1", "h2", "h3", "h4"]
    topology.atoms["atom_name"] = ["C", "O", "HC1", "HC2", "HC3", "HO"]
    topology.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 0, 0, 0, 1],
            atom2_index=[1, 2, 3, 4, 5],
            bond_order=[1] * 5,
            bond_type=["covalent"] * 5,
            is_aromatic=[False] * 5,
            evidence=["explicit"] * 5,
        )
    )
    state = topology._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    for field, value in (
        ("formal_charge", 0),
        ("is_aromatic", False),
        ("n_unpaired_electrons", 0),
        ("n_implicit_hydrogens", 0),
        ("n_explicit_hydrogens", 0),
        ("allows_implicit_hydrogens", False),
    ):
        state.set_atom_attribute(field, [value] * 6)
    return topology


def _source(template=None, *, frames=3):
    template = _template() if template is None else template
    source = msm.convert(template, to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    state.atom_attributes = pd.DataFrame(index=range(source.get_n_atoms()))
    state.bonds.drop(
        columns=[
            c
            for c in ("bond_type", "bond_order", "is_aromatic", "joins_components")
            if c in state.bonds
        ],
        inplace=True,
    )
    state.bonds["evidence"] = "inferred"
    state.connectivity_completeness = "partial"
    if frames:
        n_atoms = source.get_n_atoms()
        source.structures.append(
            coordinates=msm.pyunitwizard.quantity(
                np.arange(frames * n_atoms * 3, dtype=float).reshape(frames, n_atoms, 3)
                / 10,
                "angstrom",
            ),
            box=msm.pyunitwizard.quantity(
                np.tile(np.eye(3), (frames, 1, 1)) * 10, "angstrom"
            ),
            time=msm.pyunitwizard.quantity(np.arange(frames) * 2, "fs"),
        )
    return source


def _options(source, template=None, correspondence=None, **extra):
    return dict(
        template=_template() if template is None else template,
        atom_correspondence=np.column_stack((np.arange(6), np.arange(6)))
        if correspondence is None
        else correspondence,
        template_provenance=PROVENANCE,
        **extra,
    )


def _chemistry(source):
    return msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()


def test_permuted_transfer_preserves_every_pose_and_source_identity():
    template = _template()
    order = [3, 1, 4, 0, 2, 5]
    source = _source(template)
    source.topology.atoms = source.topology.atoms.iloc[order].copy()
    source.topology.atoms.reset_index(drop=True, inplace=True)
    # Independent source ordering: H, O, H, C, H, H. Do not let an extraction
    # implementation define the oracle for the explicit map being tested.
    source.topology.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 1, 1, 2, 3],
            atom2_index=[3, 3, 5, 3, 4],
            evidence=["inferred"] * 5,
        )
    )
    correspondence = np.column_stack((np.arange(6), np.argsort(order)))
    before = _chemistry(source)
    atoms = source.topology.atoms.copy(deep=True)
    structures = {
        field: deepcopy(getattr(source.structures, field))
        for field in ("coordinates", "box", "time")
    }
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        assessment = msm.physchem.assess_chemical_template(
            source, **_options(source, template, correspondence)
        )
        assert assessment["status"] == "compatible"
        output = msm.physchem.apply_chemical_template(
            source, **_options(source, template, correspondence)
        )
    prepared = output["molecular_system"]
    assert output["report"]["status"] == "applied"
    assert prepared is not source
    np.testing.assert_equal(_chemistry(source), before)
    pd.testing.assert_frame_equal(prepared.topology.atoms, atoms)
    for field in ("coordinates", "box", "time"):
        np.testing.assert_equal(
            msm.pyunitwizard.get_value(getattr(prepared.structures, field)),
            msm.pyunitwizard.get_value(structures[field]),
        )
        assert msm.pyunitwizard.get_unit(
            getattr(prepared.structures, field)
        ) == msm.pyunitwizard.get_unit(structures[field])
    assert prepared.structures.n_structures == 3
    state = prepared.chemical_states._states[0]
    assert state.connectivity_completeness == "complete"
    assert state.atom_attributes["formal_charge"].tolist() == [0] * 6
    assert state.bonds["bond_order"].tolist() == [1] * 5
    assert state.bonds["evidence"].tolist() == ["inferred"] * 5
    # Independent methanol controls: one indexed OH donor, one oxygen acceptor.
    sites = msm.interactions.hbonds.get_hbond_sites(prepared)
    assert sites["donor_hydrogen_pairs"].tolist() == [[1, 5]]
    assert sites["acceptor_atom_indices"].tolist() == [1]
    output["report"]["template_provenance"]["identity"] = "edited"
    assert PROVENANCE["identity"] == "methanol independent control"
    assert (
        template._chemical_states_domain._states[0].bonds["evidence"].tolist()
        == ["explicit"] * 5
    )


@pytest.mark.parametrize(
    "change", ["element", "isotope", "charge", "radical", "stereo", "graph"]
)
def test_conflicts_fail_before_mutation_and_return_a_detached_report(change):
    template, source = _template(), _source()
    state = source.chemical_states._states[0]
    if change == "element":
        source.topology.atoms.loc[0, "atom_type"] = "N"
    elif change == "isotope":
        source.topology.atoms.loc[0, "isotope"] = 13
        template.atoms.loc[0, "isotope"] = 14
    elif change == "charge":
        state.set_atom_attribute("formal_charge", [1, None, None, None, None, None])
    elif change == "radical":
        state.set_atom_attribute(
            "n_unpaired_electrons", [1, None, None, None, None, None]
        )
    elif change == "stereo":
        state.set_atom_attribute("stereochemistry", ["R", None, None, None, None, None])
        template._chemical_states_domain._states[0].set_atom_attribute(
            "stereochemistry", ["S", None, None, None, None, None]
        )
    elif change == "graph":
        state.bonds.at[0, "atom2_index"] = 5
    before = _chemistry(source)
    assert (
        msm.physchem.assess_chemical_template(source, **_options(source, template))[
            "status"
        ]
        == "conflict"
    )
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **_options(source, template))
    assert error.value.report["status"] == "conflict"
    np.testing.assert_equal(_chemistry(source), before)


@pytest.mark.parametrize(
    "mapping",
    [
        None,
        [[0, 0]],
        [[0, 0], [0, 1]],
        [[0, 0], [1, 0]],
        np.column_stack((np.arange(6), np.arange(1, 7))),
        np.eye(6),
        [[True, False]],
        np.column_stack((np.arange(6.0), np.arange(6.0))),
    ],
)
def test_missing_nonexhaustive_duplicate_or_invalid_maps_are_argument_errors(mapping):
    source = _source()
    options = _options(source)
    options["atom_correspondence"] = mapping
    with pytest.raises(ArgumentError):
        msm.physchem.apply_chemical_template(source, **options)


def test_explicit_hydrogen_atoms_cannot_be_supplied_by_a_template_map():
    source = msm.extract(_source(), selection=[0, 1])
    with pytest.raises(ArgumentError):
        msm.physchem.apply_chemical_template(
            source, **_options(source, correspondence=[[0, 0], [1, 1]])
        )


@pytest.mark.parametrize(
    "change",
    [
        "reference",
        "template_field",
        "complete",
        "disconnected",
        "dative",
        "cut",
        "aromatic",
        "isotope",
    ],
)
def test_unresolved_scope_or_chemistry_is_not_compatible(change):
    source, template = _source(), _template()
    state, ref = (
        source.chemical_states._states[0],
        template._chemical_states_domain._states[0],
    )
    if change == "reference":
        source.chemical_states.append_state()
        source.chemical_states._reference_index = None
    elif change == "template_field":
        ref.atom_attributes.drop(columns="formal_charge", inplace=True)
    elif change == "complete":
        ref.connectivity_completeness = "partial"
    elif change == "disconnected":
        state.bonds.drop(index=4, inplace=True)
        state.bonds.reset_index(drop=True, inplace=True)
    elif change == "dative":
        ref.bonds.at[0, "bond_type"] = "dative"
    elif change == "cut":
        ref.bonds.at[0, "joins_components"] = False
    elif change == "aromatic":
        state.set_atom_attribute("is_aromatic", [True, None, None, None, None, None])
    elif change == "isotope":
        template.atoms.loc[0, "isotope"] = 13
    report = msm.physchem.assess_chemical_template(source, **_options(source, template))
    assert report["status"] in {"unassessed", "conflict"}
    assert report["issues"]
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **_options(source, template))
    assert error.value.report["status"] == report["status"]


def test_selected_nonreference_state_and_frame_associations_are_preserved():
    source = _source()
    original = source.chemical_states._states[0].copy()
    source.chemical_states._append_state(original.copy())
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    template = _template()
    template._chemical_states_domain._append_state(
        template._chemical_states_domain._states[0].copy()
    )
    before = source.chemical_states._states[0].bonds.copy(deep=True)
    output = msm.physchem.apply_chemical_template(
        source,
        **_options(source, template, chemical_state=1, template_chemical_state=1),
    )
    prepared = output["molecular_system"]
    assert prepared.chemical_states.reference_chemical_state_index == 0
    pd.testing.assert_frame_equal(prepared.chemical_states._states[0].bonds, before)
    assert (
        prepared.chemical_states._states[1].atom_attributes["formal_charge"].tolist()
        == [0] * 6
    )
    np.testing.assert_equal(
        prepared._structure_chemical_state_indices,
        source._structure_chemical_state_indices,
    )
    assert source.chemical_states._states[1].atom_attributes.empty


def test_h5msm_inputs_and_public_roundtrip_preserve_applied_values(tmp_path):
    source = _source()
    path = tmp_path / "partial.h5msm"
    msm.h5msm.write(source, str(path))
    output = msm.physchem.apply_chemical_template(path, **_options(source))
    target = tmp_path / "prepared.h5msm"
    msm.convert(
        output["molecular_system"], to_form="file:h5msm", output_filename=str(target)
    )
    loaded = msm.convert(str(target), to_form="molsysmt.MolSys")
    assert (
        loaded.chemical_states._states[0].atom_attributes["formal_charge"].tolist()
        == [0] * 6
    )
    assert loaded.chemical_states._states[0].connectivity_completeness == "complete"
    np.testing.assert_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )


def test_real_ackredit_reuses_records_in_enclosing_workflow_and_failure_never_credits():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("preparation"):
        with ackredit.scope("consumer.prepare"):
            first = msm.physchem.apply_chemical_template(_source(), **_options(None))
            second = msm.physchem.apply_chemical_template(_source(), **_options(None))
        items = first["report"]["attribution"]["items"]
        assert items == second["report"]["attribution"]["items"]
        assert items[0]["roles"] == ["executed_software"]
        assert items[0]["id"] in ackredit.get_used_items()
        assert (
            "molsysmt.physchem.apply_chemical_template"
            in ackredit.current_session().usage_tree["consumer.prepare"]["children"]
        )
    with ackredit.session("failed preparation"):
        template = _template()
        template._chemical_states_domain._states[
            0
        ].connectivity_completeness = "partial"
        with pytest.raises(StructuralInconsistencyError):
            msm.physchem.apply_chemical_template(_source(), **_options(None, template))
        assert not ackredit.get_used_items()


@pytest.mark.parametrize("strict_warnings", [False, True])
def test_optional_attribution_failure_does_not_change_completed_preparation(
    monkeypatch,
    strict_warnings,
):
    import warnings
    from contextlib import nullcontext

    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def failed():
        raise RuntimeError("controlled provider failure")

    monkeypatch.setattr(_ackredit, "backend", failed)
    with warnings.catch_warnings():
        if strict_warnings:
            warnings.simplefilter("error", AckreditTrackingWarning)
        expected_warning = (
            nullcontext() if strict_warnings else pytest.warns(AckreditTrackingWarning)
        )
        with expected_warning:
            output = msm.physchem.apply_chemical_template(_source(), **_options(None))
    assert output["report"]["status"] == "applied"
    assert output["report"]["attribution"]["items"]


@pytest.mark.parametrize(
    "argument,value",
    [
        ("chemical_state", "structure"),
        ("template_chemical_state", "structure"),
        ("skip_digestion", "yes"),
        ("template_provenance", {}),
        ("template_chemical_state", -1),
    ],
)
def test_invalid_public_arguments_are_rejected(argument, value):
    options = _options(None)
    options[argument] = value
    with pytest.raises(ArgumentError):
        msm.physchem.assess_chemical_template(_source(), **options)


def _stereo_template():
    template = _template().extract(atom_indices=[0, 1, 2, 3])
    template.atoms["atom_type"] = ["F", "C", "C", "Cl"]
    template.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 1, 2],
            atom2_index=[1, 2, 3],
            bond_order=[1, 2, 1],
            bond_type=["covalent"] * 3,
            is_aromatic=[False] * 3,
            stereochemistry=[None, "E", None],
            stereo_atom1_index=[None, 0, None],
            stereo_atom2_index=[None, 3, None],
        )
    )
    state = template._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    state.set_atom_attribute("n_implicit_hydrogens", [0, 1, 1, 0])
    state.set_atom_attribute("allows_implicit_hydrogens", [False, True, True, False])
    return template


def test_stereo_reference_atoms_follow_reversed_bond_endpoint_orientation():
    template = _stereo_template()
    source = _source(template)
    source.topology.atoms = source.topology.atoms.iloc[::-1].reset_index(drop=True)
    source.chemical_states._states[0].bonds.drop(
        columns=["stereochemistry", "stereo_atom1_index", "stereo_atom2_index"],
        inplace=True,
    )
    options = _options(source, template, [[0, 3], [1, 2], [2, 1], [3, 0]])
    options["template_provenance"] = dict(PROVENANCE, hydrogen_policy="stored_counts")
    prepared = msm.physchem.apply_chemical_template(source, **options)[
        "molecular_system"
    ]
    bonds = prepared.chemical_states._states[0].bonds
    assert bonds.loc[1, "stereochemistry"] == "E"
    # Source endpoint 1 neighbors 0; endpoint 2 neighbors 3, after reversal.
    assert bonds.loc[1, "stereo_atom1_index"] == 0
    assert bonds.loc[1, "stereo_atom2_index"] == 3
    assert prepared.chemical_states._states[0].atom_attributes[
        "n_implicit_hydrogens"
    ].tolist() == [0, 1, 1, 0]


@pytest.mark.parametrize("references", [[0, 0], [1, 3], [3, 0], [-1, 3], [0, 9]])
def test_invalid_stereo_references_fail_before_any_assignment(references):
    template = _stereo_template()
    source = _source(template, frames=0)
    before = _chemistry(source)
    for field, value in zip(("stereo_atom1_index", "stereo_atom2_index"), references):
        template._chemical_states_domain._states[0].bonds.loc[1, field] = value
    options = _options(source, template, np.column_stack((np.arange(4), np.arange(4))))
    options["template_provenance"] = dict(PROVENANCE, hydrogen_policy="stored_counts")
    report = msm.physchem.assess_chemical_template(source, **options)
    assert report["status"] == "conflict"
    assert "invalid_stereo_reference_atoms" in {
        i["reason_code"] for i in report["issues"]
    }
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **options)
    np.testing.assert_equal(_chemistry(source), before)


def test_chemical_changes_invalidate_only_returned_copy_and_idempotence_preserves_analysis():
    source = _source()
    analysis = msm.Interactions.from_records(
        [
            dict(
                structure_index=1,
                interaction_type="pair",
                participants=[
                    dict(role="first", atom_indices=[0]),
                    dict(role="second", atom_indices=[1]),
                ],
            )
        ],
        n_atoms=6,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="control",
    )
    source.interactions = {"control": analysis}
    output = msm.physchem.apply_chemical_template(source, **_options(source))
    prepared = output["molecular_system"]
    assert output["report"]["invalidated_analysis_names"] == ["control"]
    assert prepared.interactions["control"].evaluated_structure_indices.size == 0
    np.testing.assert_equal(
        source.interactions["control"].evaluated_structure_indices, [0, 1, 2]
    )
    assert (
        source.interactions["control"]
        .query(structure_indices=[1])
        .to_dict()["occurrence_indices"]
        .size
        == 1
    )
    # Recompute/attach an analysis on the prepared chemistry, then repeat preparation.
    prepared.interactions = {"control": analysis}
    repeated = msm.physchem.apply_chemical_template(prepared, **_options(prepared))
    assert repeated["report"]["assigned_fields"] == []
    assert repeated["report"]["invalidated_analysis_names"] == []
    np.testing.assert_equal(
        repeated["molecular_system"]
        .interactions["control"]
        .evaluated_structure_indices,
        [0, 1, 2],
    )


def test_declared_heavy_only_template_transfers_counts_without_adding_hydrogen_atoms():
    template = _template().extract(atom_indices=[0, 1])
    ref = template._chemical_states_domain._states[0]
    ref.connectivity_completeness = "complete"
    ref.set_atom_attribute("n_implicit_hydrogens", [3, 1])
    ref.set_atom_attribute("allows_implicit_hydrogens", [True, True])
    source = _source(template)
    options = _options(source, template, [[0, 0], [1, 1]])
    options["template_provenance"] = dict(PROVENANCE, hydrogen_policy="stored_counts")
    result = msm.physchem.apply_chemical_template(source, **options)
    assert result["report"]["coverage"]["explicit_hydrogen_atom_indices"].size == 0
    assert result["molecular_system"].get_n_atoms() == 2
    assert result["molecular_system"].chemical_states._states[0].atom_attributes[
        "n_implicit_hydrogens"
    ].tolist() == [3, 1]
    # Counts cannot silently change the explicit-atoms policy.
    options["template_provenance"] = PROVENANCE
    assert (
        msm.physchem.assess_chemical_template(source, **options)["status"] == "conflict"
    )


def test_optional_ackredit_absence_keeps_portable_attribution(monkeypatch):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    output = msm.physchem.apply_chemical_template(_source(), **_options(None))
    assert output["report"]["status"] == "applied"
    assert output["report"]["attribution"]["items"][0]["version"] == msm.__version__


def test_native_preparation_needs_neither_rdkit_nor_ackredit():
    script = """
import importlib.abc
import runpy
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit', 'ackredit'}:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0, Absent())
fixture = runpy.run_path('tests/physchem/test_chemical_template.py')
msm = fixture['msm']
source = fixture['_source']()
output = msm.physchem.apply_chemical_template(source, **fixture['_options'](source))
assert output['report']['status'] == 'applied'
assert output['report']['attribution']['items']
source.topology.remove_bonds([4])
output = msm.physchem.apply_chemical_template(
    source, **fixture['_options'](source), connectivity_policy='complete_from_template')
assert output['report']['status'] == 'applied'
assert len(output['report']['added_bonds']) == 1
assert output['molecular_system'].get_n_atoms() == 6
assert 'rdkit' not in sys.modules and 'ackredit' not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr


@pytest.mark.parametrize(
    "change", ["negative", "outside", "self", "duplicate", "fractional"]
)
def test_invalid_stored_endpoints_are_rejected_before_connectivity_kernel(change):
    source = _source()
    state = source.chemical_states._states[0]
    if change == "duplicate":
        state.bonds = pd.concat([state.bonds, state.bonds.iloc[[0]]], ignore_index=True)
    else:
        state.bonds["atom1_index"] = state.bonds["atom1_index"].astype(object)
        state.bonds.loc[0, "atom1_index"] = {
            "negative": -1,
            "outside": 6,
            "self": 1,
            "fractional": 0.5,
        }[change]
    report = msm.physchem.assess_chemical_template(source, **_options(source))
    assert report["status"] == "conflict"
    assert "invalid_stored_relationship" in {i["reason_code"] for i in report["issues"]}
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **_options(source))


def test_declared_benzene_transfer_and_kekule_normalization_remains_unassessed():
    template = _template()
    template.atoms["atom_type"] = ["C"] * 6
    template.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 0, 1, 2, 3, 4],
            atom2_index=[1, 5, 2, 3, 4, 5],
            bond_type=["covalent"] * 6,
            is_aromatic=[True] * 6,
        )
    )
    ref = template._chemical_states_domain._states[0]
    ref.connectivity_completeness = "complete"
    ref.set_atom_attribute("is_aromatic", [True] * 6)
    ref.set_atom_attribute("n_implicit_hydrogens", [1] * 6)
    ref.set_atom_attribute("allows_implicit_hydrogens", [True] * 6)
    source = _source(template, frames=0)
    options = _options(source, template)
    options["template_provenance"] = dict(
        PROVENANCE, identity="benzene control", hydrogen_policy="stored_counts"
    )
    prepared = msm.physchem.apply_chemical_template(source, **options)[
        "molecular_system"
    ]
    rings = msm.physchem.get_aromatic_rings(prepared)
    assert rings["atom_offsets"].tolist() == [0, 6]
    assert sorted(rings["atom_indices"].tolist()) == list(range(6))
    # Same cyclic graph with declared alternating orders requires normalization;
    # it must not be silently treated as proven equivalent or an ordinary conflict.
    state = source.chemical_states._states[0]
    state.set_atom_attribute("is_aromatic", [False] * 6)
    state.bonds["is_aromatic"] = [False] * 6
    state.bonds["bond_order"] = [1, 2, 2, 1, 2, 1]
    report = msm.physchem.assess_chemical_template(source, **options)
    assert report["status"] == "unassessed"
    assert "aromatic_representation_requires_normalization" in {
        issue["reason_code"] for issue in report["issues"]
    }
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **options)
