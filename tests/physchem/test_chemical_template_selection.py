"""Protecting scoped chemical transfer without certifying unrelated components."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from tests.physchem.test_chemical_template import (
    PROVENANCE,
    _source,
    _stereo_template,
    _template,
)


def component_case():
    source = msm.merge([_source(frames=2), _source(frames=2)])
    source.topology.atoms["atom_name"] = ["outside"] * 6 + ["target"] * 6
    state = source.chemical_states._states[0]
    state.set_atom_attribute("formal_charge", [1], atom_indices=[0])
    source.chemical_states.append_state()
    source.interactions = {
        "old": msm.Interactions.from_records(
            [],
            n_atoms=12,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    return source, _template()


def options(template, **extra):
    return dict(
        template=template,
        atom_correspondence=np.column_stack((np.arange(6), np.arange(6, 12))),
        template_provenance=PROVENANCE,
        selection=np.arange(6, 12),
        **extra,
    )


@pytest.mark.parametrize("form", ["native", "topology", "h5msm"])
@pytest.mark.parametrize(
    "selection", [[11, 9, 7, 6, 10, 8, 8], 'atom_name == "target"']
)
def test_component_application_preserves_outside_state_pose_and_completeness(
    tmp_path,
    form,
    selection,
):
    source, template = component_case()
    original = source.copy()
    if form == "native":
        molecular_system = source
    elif form == "topology":
        molecular_system = source.topology
    else:
        molecular_system = tmp_path / "source.h5msm"
        msm.convert(source, to_form=molecular_system)
    args = options(template)
    args["selection"] = selection
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        assessment = msm.physchem.assess_chemical_template(molecular_system, **args)
        assert assessment["status"] == "compatible"
        output = msm.physchem.apply_chemical_template(molecular_system, **args)
    result, report = output["molecular_system"], output["report"]
    selected = result.chemical_states._states[0]
    assert report["coverage"]["scope"] == "selected_component"
    assert report["coverage"]["result_connectivity_completeness"] == "partial"
    assert selected.connectivity_completeness == "partial"
    assert selected.atom_attributes["formal_charge"].iloc[6:].tolist() == [0] * 6
    assert selected.atom_attributes["formal_charge"].iloc[0] == 1
    assert selected.atom_attributes["formal_charge"].iloc[1:6].isna().all()
    assert selected.atom_attributes["is_aromatic"].iloc[:6].isna().all()
    assert selected.bonds["bond_order"].iloc[:5].isna().all()
    assert selected.bonds["bond_order"].iloc[5:].tolist() == [1] * 5
    np.testing.assert_array_equal(report["source"]["atom_indices"], np.arange(6, 12))
    np.testing.assert_array_equal(
        report["atom_correspondence"], args["atom_correspondence"]
    )
    np.testing.assert_array_equal(
        report["source_bond_correspondence"],
        np.column_stack((np.arange(10), np.arange(10))),
    )
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(result.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        original.chemical_states._states[0].atom_attributes,
    )
    for field in ("atom_attributes", "bonds"):
        pd.testing.assert_frame_equal(
            getattr(result.chemical_states._states[1], field),
            getattr(original.chemical_states._states[1], field),
        )
    if form != "topology":
        for field in ("coordinates", "box", "time"):
            before, after = (
                getattr(source.structures, field),
                getattr(result.structures, field),
            )
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(before), msm.pyunitwizard.get_value(after)
            )
            assert msm.pyunitwizard.get_unit(before) == msm.pyunitwizard.get_unit(after)
        assert report["invalidated_analysis_names"] == ["old"]
        assert result.interactions["old"].evaluated_structure_indices.size == 0
    assert source.interactions["old"].evaluated_structure_indices.tolist() == [0, 1]
    path = tmp_path / "prepared.h5msm"
    msm.convert(result, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.chemical_states._states[0].connectivity_completeness == "partial"
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes, selected.atom_attributes
    )
    # Native/H5MSM assignments do not make the entire unprepared graph recognizable.
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_hbond_sites(result, method="smarts_donor_acceptor")


@pytest.mark.parametrize(
    "selection", [[6, 7, 8, 9, 10], [5, 7, 8, 9, 10, 11], [], [[6], [7]]]
)
def test_map_must_exhaust_exactly_the_selected_full_source_indices(selection):
    source, template = component_case()
    args = options(template)
    args["selection"] = selection
    before = deepcopy(source.chemical_states._states[0].atom_attributes)
    with pytest.raises(ArgumentError):
        msm.physchem.apply_chemical_template(source, **args)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )


def test_stored_cross_boundary_bond_is_unassessed_without_mutation():
    source, template = component_case()
    state = source.chemical_states._states[0]
    state.bonds = state.bonds.reindex(range(len(state.bonds) + 1))
    state.bonds.loc[len(state.bonds) - 1, ["atom1_index", "atom2_index"]] = [0, 6]
    state.bonds["atom1_index"] = state.bonds["atom1_index"].astype("int64")
    state.bonds["atom2_index"] = state.bonds["atom2_index"].astype("int64")
    before = state.bonds.copy(deep=True)
    report = msm.physchem.assess_chemical_template(source, **options(template))
    assert report["status"] == "unassessed"
    assert report["coverage"]["boundary"] == "external_relationships"
    assert report["coverage"]["external_source_bond_indices"].tolist() == [10]
    assert any(
        item["reason_code"] == "external_relationship_outside_scope"
        for item in report["issues"]
    )
    with pytest.raises(StructuralInconsistencyError) as error:
        msm.physchem.apply_chemical_template(source, **options(template))
    assert error.value.report["status"] == "unassessed"
    pd.testing.assert_frame_equal(state.bonds, before)


def test_selected_missing_bond_completion_remains_unassessed_without_mutation():
    source, template = component_case()
    state = source.chemical_states._states[0]
    state.bonds = state.bonds.drop(index=5).reset_index(drop=True)
    args = options(template, connectivity_policy="complete_from_template")
    before = state.bonds.copy(deep=True)
    assessment = msm.physchem.assess_chemical_template(source, **args)
    assert assessment["status"] == "unassessed"
    assert any(
        item["reason_code"] == "selected_graph_completion_outside_scope"
        for item in assessment["issues"]
    )
    assert assessment["coverage"]["missing_source_atom_pairs"].tolist() == [[6, 7]]
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **args)
    pd.testing.assert_frame_equal(state.bonds, before)
    assert len(state.bonds) == 9


@pytest.mark.parametrize("completeness", ["unavailable", "partial", "complete"])
def test_subset_retains_existing_global_status_and_noop_coverage(completeness):
    source, template = component_case()
    source.chemical_states._states[0].connectivity_completeness = completeness
    prepared = msm.physchem.apply_chemical_template(source, **options(template))[
        "molecular_system"
    ]
    assert prepared.chemical_states._states[0].connectivity_completeness == completeness
    prepared.interactions = source.interactions
    repeated = msm.physchem.apply_chemical_template(prepared, **options(template))
    assert repeated["report"]["assigned_fields"] == []
    assert repeated["report"]["invalidated_analysis_names"] == []
    assert repeated["molecular_system"].interactions[
        "old"
    ].evaluated_structure_indices.tolist() == [0, 1]


def test_selected_bond_stereo_references_use_full_source_axis():
    template = _stereo_template()
    target = _source(template, frames=2)
    target.topology.atoms = target.topology.atoms.iloc[::-1].reset_index(drop=True)
    target.chemical_states._states[0].bonds.drop(
        columns=["stereochemistry", "stereo_atom1_index", "stereo_atom2_index"],
        inplace=True,
    )
    source = msm.merge([_source(frames=2), target])
    result = msm.physchem.apply_chemical_template(
        source,
        template=template,
        selection=[6, 7, 8, 9],
        atom_correspondence=[[0, 9], [1, 8], [2, 7], [3, 6]],
        template_provenance=dict(PROVENANCE, hydrogen_policy="stored_counts"),
    )["molecular_system"]
    bonds = result.chemical_states.get_bonds()
    central = bonds[(bonds.atom1_index == 7) & (bonds.atom2_index == 8)].iloc[0]
    assert central.stereochemistry == "E"
    assert central.stereo_atom1_index == 6
    assert central.stereo_atom2_index == 9
    assert bonds.iloc[:5].stereochemistry.isna().all()


def test_unrelated_noncovalent_chemistry_stays_outside_template_scope():
    source, template = component_case()
    state = source.chemical_states._states[0]
    state.bonds.loc[0, "bond_type"] = "dative"
    before = state.bonds.iloc[:5].copy(deep=True)
    result = msm.physchem.apply_chemical_template(source, **options(template))[
        "molecular_system"
    ]
    pd.testing.assert_frame_equal(
        result.chemical_states.get_bonds().iloc[:5][before.columns],
        before,
    )
