"""
Contract and parity tests for biopython.PDBStructure form.

biopython.PDBStructure is a Bio.PDB.Structure.Structure object.  The
creation path is molsysmt.MolSys → biopython.PDBStructure.

Oracle: builder_pdb_molsys (4 atoms: N/CA/C/O, 2 groups ALA+HOH, 1 chain A,
2 bonds).  Using the deterministic Builder oracle avoids dependency on PDB
file parsers.

Contract: a MolSys can be converted to biopython.PDBStructure and back.
Parity: the roundtrip preserves atom count, group count, chain count, atom
names, and group names.
"""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(scope="module")
def source_topology(_base_builder_pdb_molsys):
    return _base_builder_pdb_molsys.topology


@pytest.fixture(scope="module")
def bio_structure(_base_builder_pdb_molsys):
    return msm.convert(_base_builder_pdb_molsys, to_form="biopython.PDBStructure")


@pytest.fixture(scope="module")
def roundtrip_topology(bio_structure):
    return msm.convert(bio_structure, to_form="molsysmt.Topology")


# ---------------------------------------------------------------------------
# Contract: MolSys → biopython.PDBStructure is created
# ---------------------------------------------------------------------------


def test_bio_structure_is_created(bio_structure):
    from Bio.PDB.Structure import Structure

    assert isinstance(bio_structure, Structure)


def test_bio_structure_atom_count(bio_structure):
    assert len(list(bio_structure.get_atoms())) == 4


def test_bio_structure_chain_count(bio_structure):
    assert len(list(bio_structure.get_chains())) == 1


# ---------------------------------------------------------------------------
# Parity: biopython.PDBStructure → molsysmt.Topology preserves topology
# ---------------------------------------------------------------------------


def test_parity_atom_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_atoms == source_topology.n_atoms


def test_parity_group_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_groups == source_topology.n_groups


def test_parity_chain_count(roundtrip_topology, source_topology):
    assert roundtrip_topology.n_chains == source_topology.n_chains


def test_parity_atom_names(roundtrip_topology, source_topology):
    assert (
        roundtrip_topology.atoms["atom_name"].tolist()
        == source_topology.atoms["atom_name"].tolist()
    )


def test_parity_group_names(roundtrip_topology, source_topology):
    assert (
        roundtrip_topology.groups["group_name"].tolist()
        == source_topology.groups["group_name"].tolist()
    )


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
@pytest.mark.parametrize(
    "target", ["molsysmt.MolSys", "molsysmt.Topology", "molsysmt.Structures"]
)
def test_selected_native_conversion_keeps_model_and_atom_correspondence(
    bio_structure, target, length, time
):
    source = bio_structure.copy()
    shifted = source[0].copy()
    shifted.id = 1
    for atom in shifted.get_atoms():
        atom.coord = atom.coord + np.array([10.0, 20.0, 30.0])
    source.add(shifted)
    source_xyz = np.array(
        [[atom.coord.copy() for atom in model.get_atoms()] for model in source]
    )
    source_names = [atom.name for atom in source[0].get_atoms()]
    arguments = {"selection": [3, 1]}
    if target != "molsysmt.Topology":
        arguments["structure_indices"] = [1, 0]
    with msm.pyunitwizard.context(standard_units=[length, time, "radians"]):
        result = msm.convert(source, to_form=target, **arguments)
        assert msm.get_form(result) == target
        # Native inventory is source-sorted; a Structures-only selection retains order.
        selected = [3, 1] if target == "molsysmt.Structures" else [1, 3]
        if target != "molsysmt.Structures":
            topology = result.topology if target == "molsysmt.MolSys" else result
            assert topology.atoms["atom_name"].tolist() == [
                source_names[ii] for ii in selected
            ]
            assert all(isinstance(value, str) for value in topology.atoms["atom_id"])
        if target != "molsysmt.Topology":
            xyz = msm.get(result, element="atom", coordinates=True)
            assert xyz.shape == (2, 2, 3)
            assert msm.pyunitwizard.check(xyz, dimensionality={"[L]": 1})
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(xyz, to_unit="angstroms"),
                source_xyz[[1, 0]][:, selected],
                rtol=0,
                atol=1e-12,
            )
    np.testing.assert_array_equal(
        np.array([[atom.coord for atom in model.get_atoms()] for model in source]),
        source_xyz,
    )
