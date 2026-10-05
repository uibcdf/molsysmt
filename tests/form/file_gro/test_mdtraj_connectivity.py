"""Keeping GRO connectivity consistent across native and MDTraj conversions."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture
def acidic_peptide_gro(tmp_path):
    # Heavy-atom ASH/GLH templates are connected by C(2)--N(8), 0.13 nm apart.
    groups = [
        (7, "ASH", ["N", "CA", "C", "O", "CB", "CG", "OD1", "OD2"]),
        (8, "GLH", ["N", "CA", "C", "O", "CB", "CG", "CD", "OE1", "OE2"]),
    ]
    coordinates = np.array(
        [
            [0.10, 0.20, 0.20],
            [0.20, 0.20, 0.20],
            [0.30, 0.20, 0.20],
            [0.30, 0.30, 0.20],
            [0.20, 0.10, 0.20],
            [0.20, 0.00, 0.20],
            [0.10, 0.00, 0.20],
            [0.30, 0.00, 0.20],
            [0.43, 0.20, 0.20],
            [0.53, 0.20, 0.20],
            [0.63, 0.20, 0.20],
            [0.63, 0.30, 0.20],
            [0.53, 0.10, 0.20],
            [0.53, 0.00, 0.20],
            [0.53, 0.00, 0.30],
            [0.43, 0.00, 0.30],
            [0.63, 0.00, 0.30],
        ]
    )
    structures = []
    for structure_index in range(3):
        lines = [f"Acidic peptide t= {structure_index * 2.0}", "17"]
        atom_index = 0
        for group_id, group_name, names in groups:
            for atom_name in names:
                xyz = coordinates[atom_index] + structure_index * 0.1
                lines.append(
                    f"{group_id:5d}{group_name:<5}{atom_name:>5}{41 + atom_index:5d}"
                    f"{xyz[0]:8.3f}{xyz[1]:8.3f}{xyz[2]:8.3f}"
                )
                atom_index += 1
        lines.append("5.0 5.0 5.0")
        structures.append("\n".join(lines) + "\n")
    path = tmp_path / "acidic.gro"
    path.write_text("".join(structures))
    return path, coordinates


def bond_pairs(topology):
    return {
        tuple(sorted((bond.atom1.index, bond.atom2.index))) for bond in topology.bonds
    }


EXPECTED_PAIRS = {
    (0, 1),
    (1, 2),
    (2, 3),
    (1, 4),
    (4, 5),
    (5, 6),
    (5, 7),
    (2, 8),
    (8, 9),
    (9, 10),
    (10, 11),
    (9, 12),
    (12, 13),
    (13, 14),
    (14, 15),
    (14, 16),
}


@pytest.mark.parametrize("target", ["mdtraj.Topology", "mdtraj.Trajectory"])
def test_gro_mdtraj_retains_supported_acidic_group_connectivity(
    acidic_peptide_gro, target
):
    pytest.importorskip("mdtraj")
    path, _ = acidic_peptide_gro
    result = msm.convert(path, to_form=target)
    topology = result.topology if target == "mdtraj.Trajectory" else result
    assert bond_pairs(topology) == EXPECTED_PAIRS
    assert len(topology.find_molecules()) == 1
    assert [group.name for group in topology.residues] == ["ASH", "GLH"]
    assert [str(group.resSeq) for group in topology.residues] == ["7", "8"]
    assert [str(atom.serial) for atom in topology.atoms] == [
        str(i) for i in range(41, 58)
    ]


def test_gro_mdtraj_preserves_nonconsecutive_structures_and_selected_bonds(
    acidic_peptide_gro,
):
    pytest.importorskip("mdtraj")
    path, coordinates = acidic_peptide_gro
    selected = [0, 1, 2, 8]
    with msm.pyunitwizard.context(standard_units=["angstrom", "fs"]):
        result = msm.convert(
            path,
            to_form="mdtraj.Trajectory",
            selection=selected,
            structure_indices=[2, 0],
        )
    assert result.xyz.shape == (2, 4, 3)
    np.testing.assert_allclose(
        result.xyz,
        np.stack([coordinates[selected] + 0.2, coordinates[selected]]),
        atol=1e-7,
    )
    np.testing.assert_allclose(result.time, [4.0, 0.0])
    np.testing.assert_allclose(result.unitcell_vectors, [np.eye(3) * 5] * 2)
    assert bond_pairs(result.topology) == {(0, 1), (1, 2), (2, 3)}


def test_gro_native_separates_consecutive_different_groups_with_same_label(tmp_path):
    path = tmp_path / "same-label.gro"
    path.write_text(
        "Different groups with repeated labels\n2\n"
        "    7NA      NA   41   0.100   0.200   0.300\n"
        "    7CL      CL   42   0.400   0.500   0.600\n"
        "5.0 5.0 5.0\n"
    )
    result = msm.convert(path, to_form="molsysmt.Topology", get_missing_bonds=False)
    assert result.groups.group_id.tolist() == ["7", "7"]
    assert result.groups.group_name.tolist() == ["NA", "CL"]
    assert result.atoms.group_index.tolist() == [0, 1]


def test_bundled_nglview_gro_uses_native_connectivity():
    pytest.importorskip("mdtraj")
    topology = msm.convert(
        msm.systems["nglview"]["md_1u19.gro"], to_form="mdtraj.Topology"
    )
    assert topology.n_atoms == 5547
    assert topology.n_residues == 349
    # This pins the native candidate profile, not chemical validation of all edges.
    assert topology.n_bonds == 5632
    assert len(topology.find_molecules()) == 1
