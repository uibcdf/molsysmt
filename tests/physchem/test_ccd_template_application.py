"""Applying generic CCD references to pinned deposited molecular systems."""

import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

DATA = Path(__file__).parent / "data" / "chemical_templates"


@pytest.fixture(params=["1hsg", "1stp"])
def deposited(request):
    manifest = json.loads((DATA / "ccd_reference_inputs.json").read_text())
    record = manifest["deposited_structures"][request.param]
    path = DATA / record["file"]
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == record["sha256"]
    assert (
        hashlib.sha256(gzip.decompress(raw)).hexdigest()
        == record["uncompressed_sha256"]
    )
    source = msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    source = msm.extract(source, structure_indices=[0, 0, 0])
    reference = manifest["components"][record["component_id"]]
    ccd = DATA / reference["file"]
    assert hashlib.sha256(ccd.read_bytes()).hexdigest() == reference["sha256"]
    return source, record, ccd


@pytest.mark.parametrize("form", ["native", "h5msm", "permuted"])
def test_deposited_template_assignment_retains_pose_axes_and_outside_chemistry(
    deposited, form, tmp_path
):
    source, record, ccd = deposited
    if form == "permuted":
        source = msm.permute_atoms(
            source, atom_indices=np.arange(source.get_n_atoms())[::-1]
        )
    selection = msm.select(source, selection=f"group_index == {record['group_index']}")
    assert len(selection) == record["n_selected_atoms"]
    if form != "permuted":
        np.testing.assert_array_equal(selection, record["atom_indices"])
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.chemical_states.get_bonds().copy(deep=True)
    before_attrs = source.chemical_states._states[0].atom_attributes.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    input_system = source
    if form == "h5msm":
        input_system = tmp_path / "observed.h5msm"
        msm.convert(source, to_form=input_system)
        input_digest = hashlib.sha256(input_system.read_bytes()).hexdigest()
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        reference = msm.physchem.get_chemical_template(record["component_id"], ccd)
        mapping = msm.topology.get_atom_name_correspondence(
            reference["template"],
            reference_molecular_system=input_system,
            reference_selection=selection,
        )
        options = dict(
            template=reference["template"],
            atom_correspondence=mapping,
            template_provenance=reference["template_provenance"],
            selection=selection,
        )
        assessment = msm.physchem.assess_chemical_template(input_system, **options)
        assert assessment["status"] == "compatible"
        result = msm.physchem.apply_chemical_template(input_system, **options)
    prepared = result["molecular_system"]
    assert result["report"]["status"] == "applied"
    assert prepared is not source
    assert prepared.get_n_atoms() == source.get_n_atoms()
    assert msm.get(prepared, n_structures=True) == 3
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(prepared.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before_bonds)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before_attrs
    )
    for system in (source, prepared):
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(system.structures.coordinates, to_unit="nm"),
            coordinates,
        )
    if form == "h5msm":
        assert hashlib.sha256(input_system.read_bytes()).hexdigest() == input_digest
    outside = np.setdiff1d(np.arange(source.get_n_atoms()), selection)
    after_attrs = prepared.chemical_states._states[0].atom_attributes
    for field in after_attrs:
        if field in before_attrs:
            pd.testing.assert_series_equal(
                after_attrs[field].iloc[outside], before_attrs[field].iloc[outside]
            )
        else:
            assert after_attrs[field].iloc[outside].isna().all()
    original_outside = ~(
        before_bonds.atom1_index.isin(selection)
        & before_bonds.atom2_index.isin(selection)
    )
    after_bonds = prepared.chemical_states.get_bonds()
    pd.testing.assert_frame_equal(
        after_bonds.loc[original_outside, before_bonds.columns],
        before_bonds.loc[original_outside],
    )
    assert prepared.chemical_states._states[0].connectivity_completeness == "partial"
    target = tmp_path / "assigned.h5msm"
    msm.convert(prepared, to_form=target)
    restored = msm.convert(target, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(
        restored.chemical_states._states[0].atom_attributes, after_attrs
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        coordinates,
    )
    assert restored.chemical_states._states[0].connectivity_completeness == "partial"


def test_reference_chemistry_cannot_overwrite_a_conflicting_observed_charge(deposited):
    source, record, ccd = deposited
    reference = msm.physchem.get_chemical_template(record["component_id"], ccd)
    selection = msm.select(source, selection=f"group_index == {record['group_index']}")
    mapping = msm.topology.get_atom_name_correspondence(
        reference["template"],
        reference_molecular_system=source,
        reference_selection=selection,
    )
    charges = pd.array([pd.NA] * source.get_n_atoms(), dtype="Int64")
    charges[int(mapping[0, 1])] = 1
    source.chemical_states._states[0].set_atom_attribute("formal_charge", charges)
    before_charges = source.chemical_states._states[
        0
    ].atom_attributes.formal_charge.copy(deep=True)
    options = dict(
        template=reference["template"],
        atom_correspondence=mapping,
        template_provenance=reference["template_provenance"],
        selection=selection,
    )
    assert (
        msm.physchem.assess_chemical_template(source, **options)["status"] == "conflict"
    )
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **options)
    pd.testing.assert_series_equal(
        source.chemical_states._states[0].atom_attributes.formal_charge, before_charges
    )
