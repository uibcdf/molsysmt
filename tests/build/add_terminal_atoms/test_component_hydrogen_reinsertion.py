"""Checking the public mapped-H workflow without a competing reinsertion engine."""

import re
from copy import deepcopy
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
)
from tests.build.add_missing_hydrogens.test_fixed_state import hydrogenate, prepared
from tests.physchem import test_chemical_template_est as est_controls

DATA = est_controls.DATA
est_case = est_controls.est_case


def _attach_generated_hydrogens(
    source, hydrogenated, report, source_indices, *, attribute_policy="strict"
):
    """Execute the recipe using public tools, with explicit map/inventory checks."""
    source_indices = np.asarray(source_indices, dtype=np.int64)
    n_original = len(source_indices)
    if (
        source_indices.ndim != 1
        or len(np.unique(source_indices)) != n_original
        or np.any(source_indices < 0)
        or np.any(source_indices >= msm.get(source, n_atoms=True))
    ):
        raise ValueError(
            "The declared component-to-source map must be one-to-one and in range."
        )
    pairs = report["parent_hydrogen_pairs"]
    np.testing.assert_array_equal(
        report["atom_correspondence"],
        np.column_stack((np.arange(n_original), np.arange(n_original))),
    )
    np.testing.assert_array_equal(
        pairs[:, 1], np.arange(n_original, hydrogenated.get_n_atoms())
    )
    old_coordinates = msm.get(source, selection=source_indices, coordinates=True)
    retained_coordinates = msm.get(
        hydrogenated, selection=np.arange(n_original), coordinates=True
    )
    if not np.array_equal(
        msm.pyunitwizard.get_value(old_coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(retained_coordinates, to_unit="nm"),
    ):
        raise ValueError(
            "The retained component pose does not match the declared source map."
        )
    implicit, explicit = msm.get(
        source,
        selection=source_indices,
        n_implicit_hydrogens=True,
        n_explicit_hydrogens=True,
    )
    expected = np.asarray(implicit, dtype=np.int64) + np.asarray(
        explicit, dtype=np.int64
    )
    if not np.array_equal(expected, np.bincount(pairs[:, 0], minlength=n_original)):
        raise ValueError(
            "Generated H do not materialize the declared source inventory."
        )
    atoms = pairs[:, 1]
    fields = dict(
        formal_charge="formal_charge",
        atom_is_aromatic="is_aromatic",
        n_unpaired_electrons="n_unpaired_electrons",
        n_implicit_hydrogens="n_implicit_hydrogens",
        n_explicit_hydrogens="n_explicit_hydrogens",
        allows_implicit_hydrogens="allows_implicit_hydrogens",
        atom_stereochemistry="stereochemistry",
    )
    values = msm.get(hydrogenated, selection=atoms, **{name: True for name in fields})
    types, names = msm.get(
        hydrogenated, selection=atoms, atom_type=True, atom_name=True
    )
    records = [
        dict(
            parent_atom_index=int(source_indices[parent]),
            atom_type=types[k],
            atom_name=names[k],
            chemical_attributes={
                field: column[k] for field, column in zip(fields.values(), values)
            },
        )
        for k, (parent, _) in enumerate(pairs)
    ]
    result = msm.build.add_terminal_atoms(
        source,
        records,
        msm.get(hydrogenated, selection=atoms, coordinates=True),
        attribute_policy=attribute_policy,
    )
    affected_parents = np.unique(source_indices[pairs[:, 0]])
    if len(affected_parents):
        msm.set(
            result["molecular_system"],
            selection=affected_parents,
            n_implicit_hydrogens=np.zeros(len(affected_parents), dtype=int),
            n_explicit_hydrogens=np.zeros(len(affected_parents), dtype=int),
        )
    return result


def _complex(smiles):
    ligand = prepared(
        smiles,
        [[0.0, 0.0, 0.0], [1.4, 0.0, 0.0]] if smiles == "CO" else [[0.0, 0.0, 0.0]],
    )
    builder = msm.MolSysBuilder()
    # This ID collides with the isolated methanol engine's first generated H ID.
    builder.add_atom(atom_type="He", atom_name="outside", atom_id="2")
    builder.add_group([0], group_name="outside", group_id="outside")
    builder.set_coordinates(msm.pyunitwizard.quantity([[[1.0, 1.0, 1.0]]], "nm"))
    source = msm.merge([builder.build(), ligand])
    source.interactions = {
        "original": msm.Interactions.from_records(
            [],
            n_atoms=source.get_n_atoms(),
            n_structures=1,
            evaluated_structure_indices=[0],
            method="control",
        )
    }
    indices = np.arange(1, source.get_n_atoms(), dtype=np.int64)
    return source, ligand, indices


@pytest.mark.parametrize("smiles,formal_charge", [("CO", 0), ("[NH4+]", 1)])
@pytest.mark.parametrize("source_form", ["native", "h5msm"])
def test_reinsertion_preserves_original_axis_and_materializes_counts(
    tmp_path, smiles, formal_charge, source_form
):
    source, ligand, indices = _complex(smiles)
    before = source.copy()
    generated = hydrogenate(ligand)
    molecular_system = source
    if source_form == "h5msm":
        molecular_system = tmp_path / "source.h5msm"
        msm.convert(source, to_form=molecular_system)
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = _attach_generated_hydrogens(
            molecular_system,
            generated["molecular_system"],
            generated["report"],
            indices,
        )
    output = result["molecular_system"]
    n_old = source.get_n_atoms()
    assert output.get_n_atoms() == n_old + 4
    ids = output.topology.atoms.atom_id.tolist()
    assert len(ids) == len(set(ids)) and all(isinstance(value, str) for value in ids)
    pd.testing.assert_frame_equal(
        output.topology.atoms.iloc[:n_old], before.topology.atoms, check_dtype=False
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm")[
            :, :n_old
        ],
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="nm"),
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    old_fields = before.chemical_states._states[0].atom_attributes.columns
    pd.testing.assert_frame_equal(
        output.chemical_states._states[0].atom_attributes.iloc[:1][old_fields],
        before.chemical_states._states[0].atom_attributes.iloc[:1],
    )
    assert output.chemical_states._states[0].connectivity_completeness == "partial"
    implicit, explicit = msm.get(
        output, selection=indices, n_implicit_hydrogens=True, n_explicit_hydrogens=True
    )
    assert list(implicit) == list(explicit) == [0] * len(indices)
    assert (
        int(
            sum(
                msm.get(
                    output,
                    selection=np.r_[indices, np.arange(n_old, n_old + 4)],
                    formal_charge=True,
                )
            )
        )
        == formal_charge
    )
    mapped_pairs = generated["report"]["parent_hydrogen_pairs"].copy()
    mapped_pairs[:, 0] = indices[mapped_pairs[:, 0]]
    mapped_pairs[:, 1] = np.arange(n_old, n_old + 4)
    np.testing.assert_array_equal(result["report"]["parent_atom_pairs"], mapped_pairs)
    assert output.interactions["original"].evaluated_structure_indices.size == 0
    assert (
        output.interactions["original"].atom_source_indices.tolist()
        == list(range(n_old)) + [-1] * 4
    )
    assert source.interactions["original"].evaluated_structure_indices.tolist() == [0]
    path = tmp_path / "reinserted.h5msm"
    msm.convert(output, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        output.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("invalid", ["duplicate", "reordered", "counts"])
def test_malformed_map_or_inventory_leaves_input_unchanged(invalid):
    source, ligand, indices = _complex("CO")
    generated = hydrogenate(ligand)
    if invalid == "duplicate":
        indices[:] = 1
    elif invalid == "reordered":
        indices = indices[::-1]
    else:
        msm.set(source, selection=[1], n_implicit_hydrogens=[0])
    before = source.copy()
    with pytest.raises(ValueError):
        _attach_generated_hydrogens(
            source, generated["molecular_system"], generated["report"], indices
        )
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )


def test_repeating_materialized_component_is_a_noop_with_evaluated_coverage():
    source, ligand, indices = _complex("CO")
    generated = hydrogenate(ligand)
    output = _attach_generated_hydrogens(
        source, generated["molecular_system"], generated["report"], indices
    )["molecular_system"]
    output.interactions = {
        "fresh": msm.Interactions.from_records(
            [],
            n_atoms=output.get_n_atoms(),
            n_structures=1,
            evaluated_structure_indices=[0],
            method="control",
        )
    }
    repeated = hydrogenate(generated["molecular_system"])
    extended_map = np.r_[indices, np.arange(source.get_n_atoms(), output.get_n_atoms())]
    result = _attach_generated_hydrogens(
        output, repeated["molecular_system"], repeated["report"], extended_map
    )
    assert result["report"]["status"] == "unchanged"
    assert result["report"]["parent_atom_pairs"].shape == (0, 2)
    assert result["molecular_system"].interactions[
        "fresh"
    ].evaluated_structure_indices.tolist() == [0]
    pd.testing.assert_frame_equal(
        result["molecular_system"].chemical_states._states[0].atom_attributes,
        output.chemical_states._states[0].atom_attributes,
    )


def test_real_est_reinsertion_preserves_partial_complex_and_source_pose(
    est_case, tmp_path
):
    ligand, manifest = est_case
    source = msm.convert(DATA / "1qku.cif.gz", to_form="molsysmt.MolSys")
    indices = np.asarray(manifest["source_atom_indices"], dtype=np.int64)
    mapping = np.asarray(manifest["atom_correspondence"], dtype=np.int64)
    full_map = mapping.copy()
    full_map[:, 1] = indices[mapping[:, 1]]
    args = dict(
        template=DATA / "est_template.h5msm",
        template_provenance=manifest["template_provenance"],
    )
    prepared_source = msm.physchem.apply_chemical_template(
        source, atom_correspondence=full_map, selection=indices, **args
    )["molecular_system"]
    isolated = msm.physchem.apply_chemical_template(
        ligand, atom_correspondence=mapping, **args
    )["molecular_system"]
    with pytest.warns(StructuralAttributeDropWarning, match="b_factor"):
        generated = hydrogenate(isolated, attribute_policy="intersection")
    assert generated["report"]["n_added_hydrogens"] == 24
    before = prepared_source.copy()
    original_report = deepcopy(generated["report"])
    with pytest.raises(StructuralInconsistencyError, match="b_factor"):
        _attach_generated_hydrogens(
            prepared_source, generated["molecular_system"], generated["report"], indices
        )
    with pytest.warns(StructuralAttributeDropWarning, match="b_factor"):
        result = _attach_generated_hydrogens(
            prepared_source,
            generated["molecular_system"],
            generated["report"],
            indices,
            attribute_policy="intersection",
        )
    output = result["molecular_system"]
    assert output.get_n_atoms() == 6620, (
        output.get_n_atoms(),
        len(result["report"]["parent_atom_pairs"]),
        prepared_source.get_n_atoms(),
    )
    assert result["report"]["dropped_attributes"] == ["b_factor"]
    assert output.chemical_states._states[0].connectivity_completeness == "partial"
    pd.testing.assert_frame_equal(
        output.topology.atoms.iloc[:6596],
        source.topology.atoms,
        check_dtype=False,
        check_frame_type=False,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm")[
            :, :6596
        ],
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    outside = np.setdiff1d(np.arange(6596), indices)
    pd.testing.assert_frame_equal(
        output.chemical_states._states[0].atom_attributes.iloc[outside],
        before.chemical_states._states[0].atom_attributes.iloc[outside],
    )
    pd.testing.assert_frame_equal(
        prepared_source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        generated["report"]["parent_hydrogen_pairs"],
        original_report["parent_hydrogen_pairs"],
    )
    full_ligand = msm.extract(output, selection=np.r_[indices, np.arange(6596, 6620)])
    full_ligand = msm.physchem.apply_chemical_template(
        full_ligand,
        template=generated["molecular_system"],
        atom_correspondence=np.column_stack((np.arange(44), np.arange(44))),
        template_provenance=dict(
            identity="explicit-H EST control",
            version="1",
            source_uri="fixture:EST-hydrogen-addition",
            checksum="declared:retained-producer-report",
            hydrogen_policy="explicit_atoms",
        ),
    )["molecular_system"]
    assert msm.physchem.get_aromatic_rings(full_ligand)["atom_indices"].tolist() == [
        0,
        1,
        2,
        4,
        5,
        10,
    ]
    assert (
        msm.physchem.get_hydrogen_inventory(full_ligand)[
            "missing_hydrogen_counts"
        ].tolist()
        == [0] * 44
    )
    path = tmp_path / "est-original-axis.h5msm"
    msm.convert(output, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.get_n_atoms() == 6620
    assert loaded.chemical_states._states[0].connectivity_completeness == "partial"
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        output.chemical_states._states[0].atom_attributes,
    )


def test_cookbook_reinsertion_blocks_execute_on_the_pinned_real_control(
    est_case, tmp_path, monkeypatch
):
    _, manifest = est_case
    source = msm.convert(DATA / "1qku.cif.gz", to_form="molsysmt.MolSys")
    indices = np.asarray(manifest["source_atom_indices"], dtype=np.int64)
    mapping = np.asarray(manifest["atom_correspondence"], dtype=np.int64)
    full_map = mapping.copy()
    full_map[:, 1] = indices[mapping[:, 1]]
    template = DATA / "est_template.h5msm"
    updated = msm.physchem.apply_chemical_template(
        source,
        template=template,
        template_provenance=manifest["template_provenance"],
        atom_correspondence=full_map,
        selection=indices,
    )["molecular_system"]
    page = (
        Path(__file__).resolve().parents[3]
        / "docs/content/user/cookbook/applying_chemical_templates.md"
    )
    section = (
        page.read_text()
        .split("(cookbook-component-hydrogen-reinsertion)=", 1)[1]
        .split("## Handling unresolved cases", 1)[0]
    )
    blocks = re.findall(r"```python\n(.*?)```", section, re.S)
    assert len(blocks) == 2
    namespace = dict(
        msm=msm,
        molsys_A=updated,
        template=template,
        template_provenance=manifest["template_provenance"],
        source_atom_indices=indices,
        atom_correspondence=mapping,
    )
    monkeypatch.chdir(tmp_path)
    with pytest.warns(StructuralAttributeDropWarning, match="b_factor"):
        for block in blocks:
            exec(compile(block, str(page), "exec"), namespace)
    loaded = msm.convert(
        tmp_path / "complex_with_generated_hydrogens.h5msm", to_form="molsysmt.MolSys"
    )
    assert loaded.get_n_atoms() == 6620
    assert loaded.chemical_states._states[0].connectivity_completeness == "partial"
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm")[
            :, :6596
        ],
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    implicit, explicit = msm.get(
        loaded, selection=indices, n_implicit_hydrogens=True, n_explicit_hydrogens=True
    )
    assert implicit == explicit == [0] * 20
