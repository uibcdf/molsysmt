"""Testing the contractual read scope of the file:gro adapter."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


GRO_TEXT = """Two-atom triclinic GRO fixture
    2
    7LIG     C1   41   0.100   0.200   0.300  0.0100  0.0200  0.0300
    7LIG     O2   42   0.400   0.500   0.600 -0.0100 -0.0200 -0.0300
   2.00000   3.00000   4.00000   0.10000   0.20000   0.30000   0.40000   0.50000   0.60000
"""


@pytest.fixture
def gro_path(tmp_path):
    """Writing a deterministic GRO fixture."""

    path = tmp_path / "triclinic.gro"
    path.write_text(GRO_TEXT, encoding="utf-8")
    return path


@pytest.fixture
def gro_molsys(gro_path):
    """Reading the deterministic GRO fixture without bond inference."""

    return msm.convert(
        gro_path,
        to_form="molsysmt.MolSys",
        get_missing_bonds=False,
    )


def test_file_gro_reads_topology_with_string_ids(gro_molsys):
    assert gro_molsys.topology.n_atoms == 2
    assert gro_molsys.topology.n_groups == 1
    assert gro_molsys.topology.atoms["atom_id"].tolist() == ["41", "42"]
    assert gro_molsys.topology.groups["group_id"].tolist() == ["7"]
    assert gro_molsys.topology.atoms["atom_name"].tolist() == ["C1", "O2"]


def test_file_gro_reads_coordinates_velocities_and_triclinic_box(gro_molsys):
    np.testing.assert_allclose(
        puw.get_value(gro_molsys.structures.coordinates, to_unit="nm"),
        [[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]],
    )
    np.testing.assert_allclose(
        puw.get_value(gro_molsys.structures.velocities, to_unit="nm/ps"),
        [[[0.01, 0.02, 0.03], [-0.01, -0.02, -0.03]]],
    )
    np.testing.assert_allclose(
        puw.get_value(gro_molsys.structures.box, to_unit="nm"),
        [[[2.0, 0.1, 0.2], [0.3, 3.0, 0.4], [0.5, 0.6, 4.0]]],
    )


def test_file_gro_applies_atom_and_structure_subsets(gro_path):
    output = msm.convert(
        gro_path,
        to_form="molsysmt.MolSys",
        selection=[1],
        structure_indices=[0],
        get_missing_bonds=False,
    )

    assert output.topology.atoms["atom_id"].tolist() == ["42"]
    assert output.structures.coordinates.shape == (1, 1, 3)
    assert output.structures.velocities.shape == (1, 1, 3)
    assert output.structures.box.shape == (1, 3, 3)


def test_file_gro_matches_openmm_for_coordinates_and_box(gro_path, gro_molsys):
    openmm = pytest.importorskip("openmm")
    openmm_gro = openmm.app.GromacsGroFile(str(gro_path))

    expected_coordinates = np.asarray(
        openmm_gro.getPositions(asNumpy=True).value_in_unit(openmm.unit.nanometer)
    )
    expected_box = np.asarray(
        openmm_gro.getPeriodicBoxVectors().value_in_unit(openmm.unit.nanometer)
    )

    np.testing.assert_allclose(
        puw.get_value(gro_molsys.structures.coordinates, to_unit="nm")[0],
        expected_coordinates,
    )
    np.testing.assert_allclose(
        puw.get_value(gro_molsys.structures.box, to_unit="nm")[0],
        expected_box,
    )
