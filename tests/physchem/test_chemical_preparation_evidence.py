"""Protecting retained construction and representation evidence across workflows."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from tests.native.test_preparation_history import assert_tree
from tests.physchem.test_normalize_aromatic_bond_orders import declared_source


def test_factory_retains_explicit_choices_data_and_detached_producer(monkeypatch):
    monkeypatch.setattr(msm, "__version__", "factory.producer")
    definition = msm.physchem.get_peptide_chemical_template(
        ["CYX", "HIE", "CYX"],
        "amine",
        "carboxylic_acid",
        disulfide_group_pairs=[[0, 2]],
    )
    template = definition["template"]
    history = template.chemical_states.get_preparation_history()
    assert len(history) == 1
    assert history[0]["index_scope"] == "operation"
    assert history[0]["output"] == dict(
        n_atoms=template.get_n_atoms(),
        n_bonds=len(template.chemical_states.get_bonds()),
        chemical_state_index=0,
    )
    report = history[0]["report"]
    assert report["schema"] == "molsysmt.peptide_template@1"
    assert report["status"] == "constructed"
    assert report["n_indexed_hydrogens"] == 0
    assert report["unassessed_checks"] == [
        "stereochemistry",
        "environmental_protonation",
        "geometry",
        "force_field_coverage",
    ]
    provenance = report["template_provenance"]
    assert provenance["residue_names"] == ["CYX", "HIE", "CYX"]
    assert provenance["n_terminal_state"] == "amine"
    assert provenance["c_terminal_state"] == "carboxylic_acid"
    assert provenance["disulfide_group_pairs"] == [[0, 2]]
    assert (
        provenance["software"] == report["software"] == {"molsysmt": "factory.producer"}
    )
    assert provenance["source"]["sha256"] == (
        "535dc75a2cc5db579a3114090c9ab1273892c556cb7cc1a850ce2c4cd57c7cde"
    )
    assert provenance["curation"]["rdkit_version"] == "2025.09.5"
    assert report["units"] == {"formal_charge": "elementary_charge"}
    assert_tree(report, definition["report"])
    assert_tree(provenance, definition["template_provenance"])
    definition["template_provenance"]["residue_names"][0] = "edited"
    definition["report"]["disulfide_bond_pairs"][:] = -1
    history[0]["report"]["software"]["molsysmt"] = "edited"
    retained = template.chemical_states.get_preparation_history()[0]["report"]
    assert retained["template_provenance"]["residue_names"] == ["CYX", "HIE", "CYX"]
    assert retained["software"]["molsysmt"] == "factory.producer"
    assert (retained["disulfide_bond_pairs"] >= 0).all()
    assert template.structures is None


@pytest.mark.parametrize("route", ["copy", "dict", "h5msm", "states_h5msm"])
def test_factory_and_normalization_evidence_survives_another_reader_version(
    tmp_path, monkeypatch, route
):
    monkeypatch.setattr(msm, "__version__", "construction.producer")
    source, aromatic = declared_source()
    original = source.chemical_states.get_preparation_history()
    monkeypatch.setattr(msm, "__version__", "normalization.producer")
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        output = msm.physchem.normalize_aromatic_bond_orders(source)
    normalized = output["molecular_system"]
    history = normalized.chemical_states.get_preparation_history()
    assert_tree(history[:-1], original)
    assert_tree(source.chemical_states.get_preparation_history(), original)
    assert [item["report"]["software"]["molsysmt"] for item in history] == [
        "construction.producer",
        "normalization.producer",
    ]
    report = history[-1]["report"]
    assert_tree(report, output["report"])
    np.testing.assert_array_equal(report["bond_indices"], aromatic)
    np.testing.assert_array_equal(report["original_bond_orders"], [1, 2, 1, 2, 1, 2])
    assert np.isnan(report["original_fractional_bond_orders"]).all()
    assert report["original_bond_orders"].dtype == np.float64
    assert report["invalidated_analysis_names"] == ["empty"]
    monkeypatch.setattr(msm, "__version__", "reader.version")
    if route == "copy":
        restored = normalized.copy().chemical_states
    elif route == "dict":
        payload = msm.convert(
            normalized.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        )
        restored = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    else:
        path = tmp_path / "evidence.h5msm"
        if route == "h5msm":
            msm.convert(normalized, to_form=path)
            loaded = msm.convert(path, to_form="molsysmt.MolSys")
            restored = loaded.chemical_states
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
                msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
            )
        else:
            msm.h5msm.write_layers(path, chemical_states=normalized.chemical_states)
            restored = msm.h5msm.read_layers(path)["chemical_states"]
    assert_tree(restored.get_preparation_history(), history)
    output["report"]["bond_indices"][:] = -1
    assert_tree(normalized.chemical_states.get_preparation_history(), history)


def test_unchanged_normalization_records_one_operation_and_preserves_analyses():
    source, _ = declared_source()
    source.chemical_states.append_state()
    history0 = source.chemical_states.get_preparation_history(0)
    history1 = source.chemical_states.get_preparation_history(1)
    first = msm.physchem.normalize_aromatic_bond_orders(source, chemical_state=0)
    normalized = first["molecular_system"]
    normalized.interactions = source.interactions
    second = msm.physchem.normalize_aromatic_bond_orders(normalized)
    repeated = second["molecular_system"]
    assert second["report"]["status"] == "unchanged"
    assert second["report"]["invalidated_analysis_names"] == []
    assert repeated.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]
    retained = repeated.chemical_states.get_preparation_history(0)
    assert len(retained) == len(history0) + 2
    assert_tree(retained[:-1], normalized.chemical_states.get_preparation_history(0))
    assert_tree(retained[-1]["report"], second["report"])
    assert retained[-1]["output"]["chemical_state_index"] == 0
    assert_tree(repeated.chemical_states.get_preparation_history(1), history1)
    assert_tree(source.chemical_states.get_preparation_history(0), history0)


def test_normalization_failure_does_not_append_or_partially_change_source():
    source, aromatic = declared_source()
    state = source.chemical_states._states[0]
    state.bonds.at[int(aromatic[-1]), "bond_order"] = 3
    original = state.bonds.copy(deep=True)
    history = source.chemical_states.get_preparation_history()
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.normalize_aromatic_bond_orders(source)
    assert_tree(source.chemical_states.get_preparation_history(), history)
    pd.testing.assert_frame_equal(state.bonds, original)
    assert source.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]


def test_extraction_keeps_original_construction_and_normalization_domains(tmp_path):
    source, _ = declared_source()
    normalized = msm.physchem.normalize_aromatic_bond_orders(source)["molecular_system"]
    history = normalized.chemical_states.get_preparation_history()
    subset = msm.extract(normalized, selection=[0, 1], structure_indices=[1])
    assert subset.get_n_atoms() == 2
    assert_tree(subset.chemical_states.get_preparation_history(), history)
    assert all(item["output"]["n_atoms"] == source.get_n_atoms() for item in history)
    assert history[-1]["report"]["bonded_atom_pairs"].max() >= subset.get_n_atoms()
    path = tmp_path / "historical-subset.h5msm"
    msm.convert(subset, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert_tree(loaded.chemical_states.get_preparation_history(), history)


def test_application_retains_factory_version_without_implicitly_importing_reference_history(
    monkeypatch,
):
    monkeypatch.setattr(msm, "__version__", "original.factory")
    definition = msm.physchem.get_peptide_chemical_template(
        ["GLY"], "amine", "carboxylate"
    )
    template = definition["template"]
    source = template.copy()
    reference_history = template.chemical_states.get_preparation_history()
    monkeypatch.setattr(msm, "__version__", "application.producer")
    applied = msm.physchem.apply_chemical_template(
        source,
        template=template,
        atom_correspondence=np.column_stack((np.arange(source.get_n_atoms()),) * 2),
        template_provenance=definition["template_provenance"],
    )["molecular_system"]
    history = applied.chemical_states.get_preparation_history()
    assert len(history) == 2
    assert_tree(history[:1], reference_history)
    assert history[-1]["report"]["software"] == {"molsysmt": "application.producer"}
    assert history[-1]["report"]["template_provenance"]["software"] == {
        "molsysmt": "original.factory"
    }
    assert_tree(template.chemical_states.get_preparation_history(), reference_history)
    # Archiving reference evidence is explicit and keeps its original template axes.
    assert applied.chemical_states.append_preparation_history(reference_history) == (2,)
    assert_tree(
        applied.chemical_states.get_preparation_history()[-1:], reference_history
    )
