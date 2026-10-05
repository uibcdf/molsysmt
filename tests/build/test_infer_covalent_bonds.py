"""Checking applied native candidates, original domains and persisted evidence."""

import builtins
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def _source(n_structures=1):
    builder = msm.MolSysBuilder()
    names = ["N", "CA", "C", "O", "CB", "H", "HN1"]
    atoms = [
        builder.add_atom(atom_name=name, atom_type=element)
        for name, element in zip(names, ["N", "C", "C", "O", "C", "H", "H"])
    ]
    builder.add_group(atoms, group_name="ALA", group_id="100")
    if n_structures:
        builder.set_coordinates(puw.quantity(np.zeros((n_structures, 7, 3)), "nm"))
    return builder.build()


EXPECTED = [[0, 1], [0, 5], [1, 2], [1, 4], [2, 3]]


def _pairs(molsys, state=0):
    return (
        molsys.chemical_states.get_bonds(chemical_state=state)[
            ["atom1_index", "atom2_index"]
        ]
        .to_numpy(dtype=np.int64)
        .tolist()
    )


def test_applied_pairs_and_provenance_are_literal_without_source_mutation(tmp_path):
    source = _source()
    source.topology.add_bonds([[2, 3]])
    msm.set(
        source,
        element="bond",
        bond_type="covalent",
        bond_order=2,
        bond_evidence="explicit",
    )
    before = source.topology.bonds.copy(deep=True)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    with puw.context(standard_units=["pm", "ps"]):
        result = msm.build.infer_covalent_bonds(source, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert _pairs(output) == EXPECTED
    assert report["n_added_bonds"] == 4
    assert report["candidate_method_indices"].tolist() == [0, 1, 0, 0, 0]
    assert report["candidate_method_indices"].dtype == np.int8
    assert report["source_bond_correspondence"].tolist() == [[0, 4]]
    assert output.topology.bonds["evidence"].tolist() == ["inferred"] * 4 + ["explicit"]
    assert pd.isna(output.topology.bonds.loc[0, "bond_order"])
    assert output.topology.bonds.loc[4, "bond_order"] == 2
    assert report["connectivity_completeness"] == "partial"
    assert (
        report["hydrogen_groups"][0]["hydrogen_coverage"]["issues"][0]["atom_name"]
        == "HN1"
    )
    assert (
        output.chemical_states.get_preparation_history()[0]["index_scope"]
        == "operation"
    )
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), coordinates
    )
    pd.testing.assert_frame_equal(source.topology.bonds, before)
    assert source.chemical_states.get_preparation_history() == ()
    report["added_bond_indices"][:] = -1
    history = output.chemical_states.get_preparation_history()
    assert history[0]["report"]["added_bond_indices"].tolist() == [0, 1, 2, 3]
    filename = str(tmp_path / "inferred.h5msm")
    msm.convert(output, to_form=filename)
    loaded = msm.convert(filename, to_form="molsysmt.MolSys")
    assert _pairs(loaded) == EXPECTED
    assert (
        loaded.chemical_states.get_preparation_history()[0]["report"]["software"]
        == history[0]["report"]["software"]
    )
    assert loaded.topology.bonds["provenance_index"].iloc[:4].tolist() == [0] * 4


@pytest.mark.parametrize(
    "selection,expected", [([5, 0, 5], [[0, 5]]), ([5], []), ([], [])]
)
def test_selected_candidates_keep_the_full_source_system(selection, expected):
    result = msm.build.infer_covalent_bonds(
        _source(), selection=selection, return_report=True
    )
    assert _pairs(result["molecular_system"]) == expected
    assert result["molecular_system"].get_n_atoms() == 7
    assert result["report"]["added_bonded_atom_pairs"].shape == (len(expected), 2)


def test_merging_inferred_graphs_offsets_current_history_references_without_rewriting_records():
    first = msm.build.infer_covalent_bonds(_source())
    second = msm.build.infer_covalent_bonds(msm.build.infer_covalent_bonds(_source()))
    merged = msm.merge([first.topology, second.topology])
    assert merged.bonds["provenance_index"].tolist() == [0] * 5 + [1] * 5
    history = merged._chemical_states_domain.get_preparation_history()
    assert len(history) == 3
    assert all(record["output"]["n_atoms"] == 7 for record in history)
    assert history[1]["report"]["added_bond_indices"].tolist() == list(range(5))
    assert second.topology.bonds["provenance_index"].tolist() == [0] * 5


def test_topology_input_needs_no_fabricated_structure():
    output = msm.build.infer_covalent_bonds(_source(n_structures=0).topology)
    assert _pairs(output) == EXPECTED
    report = output.chemical_states.get_preparation_history()[0]["report"]
    assert report["structure_index"] is None
    assert report["n_structures"] == 0


def test_only_selected_state_changes_and_all_structure_coordinates_survive():
    source = _source(n_structures=3)
    source.chemical_states.append_state()
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    result = msm.build.infer_covalent_bonds(
        source, chemical_state="structure", structure_indices=1, return_report=True
    )
    output = result["molecular_system"]
    assert _pairs(output, 0) == []
    assert _pairs(output, 1) == EXPECTED
    assert output.chemical_states.reference_chemical_state_index == 0
    assert result["report"]["structure_index"] == 1
    assert output.structures.n_structures == 3
    assert len(output.chemical_states.get_preparation_history(chemical_state=1)) == 1
    with pytest.raises(StructuralInconsistencyError):
        msm.build.infer_covalent_bonds(
            source, chemical_state="structure", structure_indices=2
        )
    assert _pairs(source, 1) == []


def test_changed_graph_invalidates_named_occurrences_but_no_addition_retains_them():
    source = _source()
    analysis = msm.Interactions.from_records(
        [
            dict(
                structure_index=0,
                interaction_type="test",
                evidence="synthetic",
                participants=[
                    dict(role="a", atom_indices=[0]),
                    dict(role="b", atom_indices=[1]),
                ],
            )
        ],
        n_atoms=7,
        n_structures=1,
        evaluated_structure_indices=[0],
        method="synthetic",
    )
    source.interactions = {"synthetic": analysis}
    result = msm.build.infer_covalent_bonds(source, return_report=True)
    output = result["molecular_system"]
    assert result["report"]["invalidated_analysis_names"] == ["synthetic"]
    assert output.interactions["synthetic"].query().n_interactions == 0
    assert source.interactions["synthetic"].query().n_interactions == 1
    output.interactions = {"synthetic": deepcopy(source.interactions["synthetic"])}
    unchanged = msm.build.infer_covalent_bonds(output, return_report=True)
    assert unchanged["report"]["n_added_bonds"] == 0
    assert unchanged["report"]["invalidated_analysis_names"] == []
    assert (
        unchanged["molecular_system"].interactions["synthetic"].query().n_interactions
        == 1
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"method": "unknown"},
        {"skip_digestion": "yes"},
        {"return_report": "yes"},
        {"selection": [-1]},
        {"structure_indices": [3]},
    ],
)
def test_public_validation_rejects_invalid_requests(kwargs):
    with pytest.raises(ArgumentError):
        msm.build.infer_covalent_bonds(_source(), **kwargs)


def test_pdb_form_agnostic_application_blocks_openmm_imports(tmp_path, monkeypatch):
    filename = str(tmp_path / "ala.pdb")
    msm.convert(_source(), to_form=filename)
    original = builtins.__import__

    def reject(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("Explicit native inference must not import OpenMM")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject)
    assert _pairs(msm.build.infer_covalent_bonds(filename)) == EXPECTED
