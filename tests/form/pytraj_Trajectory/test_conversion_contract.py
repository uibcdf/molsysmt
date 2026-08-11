import os
import subprocess
import sys

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt import systems
from molsysmt.form.pytraj_Trajectory._runtime import (
    has_unsafe_frame_finalizer,
)


pytraj = pytest.importorskip("pytraj")


@pytest.fixture(scope="module")
def pdb_file():
    return systems["chicken villin HP35"]["1vii.pdb"]


@pytest.fixture(scope="module")
def pytraj_trajectory(pdb_file):
    if has_unsafe_frame_finalizer():
        pytest.skip("the installed PyTraj extension has the obsolete finalizer")
    return msm.convert(pdb_file, to_form="pytraj.Trajectory")


def test_an_incompatible_pytraj_build_is_rejected_without_a_native_abort(pdb_file):
    script = f"""
import molsysmt as msm
msm.convert({str(pdb_file)!r}, to_form='pytraj.Trajectory')
"""
    environment = os.environ.copy()
    environment["PYTHONFAULTHANDLER"] = "1"
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=300,
        env=environment,
    )

    assert result.returncode not in {-6, -11, 134, 139}
    if has_unsafe_frame_finalizer():
        assert result.returncode != 0
        assert "obsolete Frame.__del__ finalizer" in result.stderr
    else:
        assert result.returncode == 0, result.stderr


def test_pdb_to_pytraj_topology_uses_the_optional_default(pdb_file):
    topology = msm.convert(pdb_file, to_form="pytraj.Topology")

    assert topology.n_atoms == 596


def test_pdb_to_pytraj_trajectory_is_usable(pytraj_trajectory):
    assert msm.get_form(pytraj_trajectory) == "pytraj.Trajectory"
    assert pytraj_trajectory.n_frames == 1
    assert pytraj_trajectory.n_atoms == 596
    assert pytraj_trajectory[0].n_atoms == 596
    assert np.isfinite(pytraj.rmsd(pytraj_trajectory, ref=0)).all()


def test_pdb_to_pytraj_trajectory_applies_atom_selection(pdb_file):
    if has_unsafe_frame_finalizer():
        pytest.skip("the installed PyTraj extension has the obsolete finalizer")

    trajectory = msm.convert(
        pdb_file,
        to_form="pytraj.Trajectory",
        selection=[0, 2, 4],
    )

    assert trajectory.xyz.shape == (1, 3, 3)


def test_pdb_to_pytraj_trajectory_preserves_requested_structure_order():
    if has_unsafe_frame_finalizer():
        pytest.skip("the installed PyTraj extension has the obsolete finalizer")

    pdb_file = systems["Trp-Cage"]["1l2y.pdb"]
    source = msm.convert(pdb_file, to_form="molsysmt.MolSys")
    trajectory = msm.convert(
        pdb_file,
        to_form="pytraj.Trajectory",
        structure_indices=[19, 0],
    )
    expected = puw.get_value(
        source.structures.coordinates[[19, 0], :, :],
        to_unit="angstrom",
    )

    assert trajectory.xyz.shape == (2, 304, 3)
    assert np.allclose(trajectory.xyz, expected)


def test_native_without_a_box_produces_a_nonperiodic_trajectory(pdb_file):
    if has_unsafe_frame_finalizer():
        pytest.skip("the installed PyTraj extension has the obsolete finalizer")

    source = msm.convert(pdb_file, to_form="molsysmt.MolSys")
    source.structures.box = None
    trajectory = msm.convert(source, to_form="pytraj.Trajectory")

    assert trajectory.unitcells is None


def test_pytraj_trajectory_roundtrip_preserves_basic_data(pytraj_trajectory):
    output = msm.convert(pytraj_trajectory, to_form="molsysmt.MolSys")

    assert output.topology.n_atoms == pytraj_trajectory.n_atoms
    assert output.structures.coordinates.shape == pytraj_trajectory.xyz.shape
    assert np.allclose(
        puw.get_value(output.structures.coordinates, to_unit="angstrom"),
        pytraj_trajectory.xyz,
    )
    assert output.structures.box.shape == (1, 3, 3)


def test_pytraj_trajectory_delivers_coordinates_and_box(pytraj_trajectory):
    coordinates = msm.get(
        pytraj_trajectory,
        element="atom",
        coordinates=True,
    )
    box = msm.get(pytraj_trajectory, element="system", box=True)

    assert coordinates.shape == (1, 596, 3)
    assert box.shape == (1, 3, 3)


def test_pytraj_trajectory_uses_the_native_topology_pipe(pytraj_trajectory):
    atom_names, bonded_atoms = msm.get(
        pytraj_trajectory,
        element="atom",
        atom_name=True,
        bonded_atoms=True,
    )

    assert len(atom_names) == 596
    assert len(bonded_atoms) == 596
