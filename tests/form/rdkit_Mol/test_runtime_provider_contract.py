"""Ground the optional RDKit floor in public native chemistry and geometry routes."""

import tomllib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from packaging.requirements import Requirement

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture
def chem():
    return pytest.importorskip("rdkit.Chem")


def _chemical_atoms(molsys):
    return msm.get(
        molsys,
        element="atom",
        formal_charge=True,
        atom_is_aromatic=True,
        n_unpaired_electrons=True,
        n_implicit_hydrogens=True,
        n_explicit_hydrogens=True,
        allows_implicit_hydrogens=True,
        atom_stereochemistry=True,
    )


def test_optional_requirement_excludes_the_pre_coordinate_array_api():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        item
        for item in map(Requirement, project["optional-dependencies"]["soft"])
        if item.name.lower() == "rdkit"
    )
    assert requirement.specifier.contains("2024.3.4")
    assert requirement.specifier.contains("2025.9.5")
    for version in ("2023.9.1", "2024.3.3"):
        assert not requirement.specifier.contains(version), (
            "Native coordinate export and coordinate CIP analysis use "
            "Conformer.SetPositions, first exposed in RDKit 2024.03.4."
        )
    assert not any(
        Requirement(raw).name.lower() == "rdkit" for raw in project["dependencies"]
    )


@pytest.mark.parametrize("layout", ["fortran", "strided"])
@pytest.mark.parametrize("unit, scale", [("angstrom", 10.0), ("pm", 1000.0)])
def test_native_coordinate_roundtrip_preserves_noncontiguous_inputs_and_units(
    chem, layout, unit, scale
):
    expected_nm = np.array([[0.1, -0.2, 0.3], [1.2, 0.5, -0.1], [-0.4, 0.6, 0.2]])
    if layout == "fortran":
        backing = np.asfortranarray(expected_nm * scale)
        values = backing
    else:
        backing = np.full((6, 3), -99.0)
        backing[::2] = expected_nm * scale
        values = backing[::2]
    assert not values.flags.c_contiguous
    backing_before = backing.copy()
    molsys = msm.convert(chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    molsys.structures.append(coordinates=puw.quantity(values[None], unit))
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_bonds = molsys.chemical_states.get_bonds().copy(deep=True)
    before_chemistry = _chemical_atoms(molsys)
    before_coordinates = puw.get_value(
        molsys.structures.coordinates, to_unit="nm"
    ).copy()

    exported = msm.convert(molsys, to_form="rdkit.Mol")
    assert exported.GetNumAtoms() == 3
    assert exported.GetNumBonds() == 2
    assert exported.GetNumConformers() == 1
    np.testing.assert_allclose(
        exported.GetConformer().GetPositions(), expected_nm * 10.0, atol=1e-13
    )
    recovered = msm.convert(exported, to_form="molsysmt.MolSys")
    assert recovered.structures.coordinates.shape == (1, 3, 3)
    np.testing.assert_allclose(
        puw.get_value(recovered.structures.coordinates, to_unit="nm"),
        expected_nm[None],
        atol=1e-13,
    )
    np.testing.assert_array_equal(backing, backing_before)
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.coordinates, to_unit="nm"), before_coordinates
    )
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(molsys.chemical_states.get_bonds(), before_bonds)
    assert _chemical_atoms(molsys) == before_chemistry


def test_native_anchors_and_supplied_maps_preserve_chemistry_and_inputs(chem):
    molsys = msm.convert(chem.MolFromSmiles("CC"), to_form="molsysmt.MolSys")
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_bonds = molsys.chemical_states.get_bonds().copy(deep=True)
    before_chemistry = _chemical_atoms(molsys)
    anchors = np.array([[0, 1]], dtype=np.int64)
    candidates = np.array([[[0, 0], [1, 1]]], dtype=np.int64)
    anchored = msm.chemical_states.get_atom_correspondences(
        molsys, fixed_atom_correspondence=anchors, max_matches=1
    )
    supplied = msm.chemical_states.get_atom_correspondences(
        molsys, candidate_atom_correspondences=candidates
    )
    np.testing.assert_array_equal(anchored["atom_correspondences"], [[[0, 1], [1, 0]]])
    np.testing.assert_array_equal(supplied["atom_correspondences"], candidates)
    assert anchored["search_complete"] and supplied["search_complete"]
    np.testing.assert_array_equal(anchors, [[0, 1]])
    np.testing.assert_array_equal(candidates, [[[0, 0], [1, 1]]])
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(molsys.chemical_states.get_bonds(), before_bonds)
    assert _chemical_atoms(molsys) == before_chemistry


def test_native_atomic_descriptor_sums_match_complete_molecule_scores(chem):
    molsys = msm.convert(chem.MolFromSmiles("CCO"), to_form="molsysmt.MolSys")
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_bonds = molsys.chemical_states.get_bonds().copy(deep=True)
    before_chemistry = _chemical_atoms(molsys)
    molecular_tpsa = puw.get_value(msm.physchem.get_tpsa(molsys), to_unit="angstrom**2")
    atomic_tpsa = puw.get_value(
        msm.physchem.get_tpsa(molsys, element="atom"), to_unit="angstrom**2"
    )
    molecular_logp = msm.physchem.get_lipophilicity(molsys)
    atomic_logp = msm.physchem.get_lipophilicity(molsys, element="atom")
    assert np.shape(molecular_tpsa) == np.shape(molecular_logp) == (1,)
    assert np.shape(atomic_tpsa) == np.shape(atomic_logp) == (3,)
    np.testing.assert_allclose(molecular_tpsa, [20.23], atol=1e-12)
    np.testing.assert_allclose(atomic_tpsa.sum(), molecular_tpsa[0], atol=1e-12)
    np.testing.assert_allclose(molecular_logp, [-0.0014], atol=1e-12)
    np.testing.assert_allclose(atomic_logp.sum(), molecular_logp[0], atol=1e-12)
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(molsys.chemical_states.get_bonds(), before_bonds)
    assert _chemical_atoms(molsys) == before_chemistry


def test_native_coordinate_cip_distinguishes_mirrors_without_editing_source(chem):
    molsys = msm.convert(chem.MolFromSmiles("FC(Cl)(Br)I"), to_form="molsysmt.MolSys")
    positions_angstrom = np.array(
        [[1, 1, 1], [0, 0, 0], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]], dtype=float
    )
    coordinates_pm = np.stack([positions_angstrom, -positions_angstrom]) * 100.0
    input_before = coordinates_pm.copy()
    molsys.structures.append(coordinates=puw.quantity(coordinates_pm, "pm"))
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_bonds = molsys.chemical_states.get_bonds().copy(deep=True)
    before_chemistry = _chemical_atoms(molsys)
    before_coordinates = puw.get_value(
        molsys.structures.coordinates, to_unit="nm"
    ).copy()
    labels = []
    for structure_index in (0, 1):
        result = msm.physchem.get_cip_stereochemistry(
            molsys, structure_indices=[structure_index], from_coordinates=True
        )
        assert result["structure_index"] == structure_index
        assert result["evidence"] == "coordinates"
        labels.append(result["atom_stereochemistry"][1])
    assert set(labels) == {"R", "S"}
    np.testing.assert_array_equal(coordinates_pm, input_before)
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.coordinates, to_unit="nm"), before_coordinates
    )
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(molsys.chemical_states.get_bonds(), before_bonds)
    assert _chemical_atoms(molsys) == before_chemistry
