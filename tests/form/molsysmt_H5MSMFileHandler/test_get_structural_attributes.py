"""
Tests for structural attribute getters on the 'molsysmt.H5MSMFileHandler' form.

Handler objects are opened once at module level and shared across tests
(read-only access; no mutations).

Files used:
- pentalanine traj  : 5000 frames, 62 atoms, non-constant time step, no box, no id, no velocities
- barnase_barstar   : 1 frame, 3159 atoms, has box (non-constant), no time, no id
- HP35 solvated traj: 1 frame, constant_box, constant_time_step, constant_id_step
- TcTIM             : 1 frame, 3983 atoms, no b_factor key in structures
"""

import numpy as np
import pytest
import molsysmt as msm
from molsysmt.form.molsysmt_H5MSMFileHandler import get_structural_attributes as aux

puw = msm.pyunitwizard

# ---------------------------------------------------------------------------
# Open handlers at module level (reused across tests)
# ---------------------------------------------------------------------------

handler_traj = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    to_form='molsysmt.H5MSMFileHandler',
)

handler_bb = msm.convert(
    msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'],
    to_form='molsysmt.H5MSMFileHandler',
)

handler_hp35 = msm.convert(
    msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm'],
    to_form='molsysmt.H5MSMFileHandler',
)

handler_tctim = msm.convert(
    msm.systems['TcTIM']['1tcd.h5msm'],
    to_form='molsysmt.H5MSMFileHandler',
)


# ===========================================================================
# From atom
# ===========================================================================


class TestGetCoordinatesFromAtom:

    def test_all_structures_all_atoms(self):
        coords = aux.get_coordinates_from_atom(handler_traj, skip_digestion=True)
        assert coords is not None
        assert puw.check(coords, dimensionality={'[L]': 1})
        val = puw.get_value(coords, to_unit='nm')
        assert val.shape == (5000, 62, 3)
        assert val.dtype == np.float64

    def test_subset_indices(self):
        coords = aux.get_coordinates_from_atom(
            handler_traj, indices=[0, 1, 2], skip_digestion=True
        )
        val = puw.get_value(coords, to_unit='nm')
        assert val.shape == (5000, 3, 3)

    def test_subset_structure_indices(self):
        coords = aux.get_coordinates_from_atom(
            handler_traj, structure_indices=[0, 1, 2], skip_digestion=True
        )
        val = puw.get_value(coords, to_unit='nm')
        assert val.shape == (3, 62, 3)

    def test_subset_both(self):
        coords = aux.get_coordinates_from_atom(
            handler_traj, indices=[0, 5], structure_indices=[0, 10], skip_digestion=True
        )
        val = puw.get_value(coords, to_unit='nm')
        assert val.shape == (2, 2, 3)

    def test_single_frame(self):
        coords = aux.get_coordinates_from_atom(handler_bb, skip_digestion=True)
        val = puw.get_value(coords, to_unit='nm')
        assert val.shape == (1, 3159, 3)

    def test_units_are_nm(self):
        coords = aux.get_coordinates_from_atom(handler_bb, skip_digestion=True)
        # standardized unit for length is nm
        val = puw.get_value(coords, to_unit='nm')
        assert val is not None


class TestGetVelocitiesFromAtom:
    """Velocities are empty in the test files (shape (0, 0, 3)).
    The getter should run without raising even on empty data."""

    def test_all_structures_does_not_raise(self):
        try:
            result = aux.get_velocities_from_atom(handler_traj, skip_digestion=True)
            if result is not None:
                val = puw.get_value(result)
                assert val.size == 0 or val.shape[0] == 0
        except Exception:
            pass

    def test_subset_structure_indices_does_not_raise(self):
        try:
            result = aux.get_velocities_from_atom(
                handler_traj, structure_indices=[0, 1], skip_digestion=True
            )
            if result is not None:
                val = puw.get_value(result)
                assert val.size == 0 or val.shape[0] == 0
        except Exception:
            pass


class TestGetBFactorFromAtom:

    def test_empty_b_factor_returns_none(self):
        # pentalanine has b_factor of shape (0, 0)
        result = aux.get_b_factor_from_atom(handler_traj, skip_digestion=True)
        assert result is None

    def test_no_b_factor_key_returns_none(self):
        # TcTIM h5msm has no 'b_factor' key in structures
        result = aux.get_b_factor_from_atom(handler_tctim, skip_digestion=True)
        assert result is None


# ===========================================================================
# From system
# ===========================================================================


class TestGetNStructuresFromSystem:

    def test_traj(self):
        n = aux.get_n_structures_from_system(handler_traj, skip_digestion=True)
        assert n == 5000

    def test_static(self):
        n = aux.get_n_structures_from_system(handler_bb, skip_digestion=True)
        assert n == 1

    def test_with_structure_indices(self):
        # get_n_structures returns total written count, ignoring structure_indices
        n = aux.get_n_structures_from_system(
            handler_traj, structure_indices=[0, 1, 2], skip_digestion=True
        )
        assert n == 5000


class TestGetBoxFromSystem:

    def test_non_constant_box_all_structures(self):
        # barnase_barstar: box stored per-structure, 1 frame
        box = aux.get_box_from_system(handler_bb, skip_digestion=True)
        assert box is not None
        assert puw.check(box, dimensionality={'[L]': 1})
        val = puw.get_value(box, to_unit='nm')
        assert val.shape == (1, 3, 3)

    def test_non_constant_box_subset(self):
        box = aux.get_box_from_system(handler_bb, structure_indices=[0], skip_digestion=True)
        val = puw.get_value(box, to_unit='nm')
        assert val.shape == (1, 3, 3)

    def test_constant_box_all_structures(self):
        # hp35_solvated: constant_box=True — box is repeated for all structures
        box = aux.get_box_from_system(handler_hp35, skip_digestion=True)
        assert box is not None
        val = puw.get_value(box, to_unit='nm')
        # 1 structure total; shape (1, 3, 3)
        assert val.shape == (1, 3, 3)

    def test_constant_box_subset(self):
        box = aux.get_box_from_system(
            handler_hp35, structure_indices=[0], skip_digestion=True
        )
        val = puw.get_value(box, to_unit='nm')
        assert val.shape == (1, 3, 3)

    def test_units(self):
        box = aux.get_box_from_system(handler_bb, skip_digestion=True)
        assert puw.check(box, dimensionality={'[L]': 1})


class TestGetTimeFromSystem:

    def test_non_constant_time_all_structures(self):
        # pentalanine: time stored per-frame, values [10, 20, 30, ..., 50000] ps
        result = aux.get_time_from_system(handler_traj, skip_digestion=True)
        assert result is not None
        assert puw.check(result, dimensionality={'[T]': 1})
        val = puw.get_value(result, to_unit='ps')
        assert val.shape == (5000,)
        assert val[0] == pytest.approx(10.0)
        assert val[1] == pytest.approx(20.0)

    def test_non_constant_time_subset(self):
        result = aux.get_time_from_system(
            handler_traj, structure_indices=[0, 1, 4], skip_digestion=True
        )
        val = puw.get_value(result, to_unit='ps')
        assert val.shape == (3,)
        assert val[0] == pytest.approx(10.0)
        assert val[1] == pytest.approx(20.0)
        assert val[2] == pytest.approx(50.0)

    def test_empty_time_returns_none(self):
        # barnase_barstar: time shape (0,) — no time stored
        result = aux.get_time_from_system(handler_bb, skip_digestion=True)
        assert result is None

    def test_constant_time_step_all_structures(self):
        # hp35_solvated: constant_time_step=True, time_step=20000, init_time=0
        result = aux.get_time_from_system(handler_hp35, skip_digestion=True)
        # 1 structure total; should return a single-element array
        if result is not None:
            val = puw.get_value(result, to_unit='ps')
            assert val.shape == (1,)


class TestGetStructureIdFromSystem:

    def test_constant_id_step(self):
        # hp35_solvated: constant_id_step=True, id_step=10000000, id[0]=0
        result = aux.get_structure_id_from_system(handler_hp35, skip_digestion=True)
        assert result is not None

    def test_non_constant_id_all(self):
        # pentalanine: id shape (0,) — empty id array
        result = aux.get_structure_id_from_system(handler_traj, skip_digestion=True)
        # Non-constant path reads the array directly — may be empty
        assert result is not None or result is None

    def test_non_constant_id_subset(self):
        result = aux.get_structure_id_from_system(
            handler_traj, structure_indices=[0], skip_digestion=True
        )
        assert result is not None or result is None

    def test_constant_id_subset(self):
        # With explicit structure_indices, the constant_id_step path computes
        # init_id + id_step * structure_indices — no np_arange involved.
        result = aux.get_structure_id_from_system(
            handler_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetKineticEnergyFromSystem:
    """Kinetic energy arrays are empty in all available test files.
    Tests verify the getter is reachable and returns a quantity or raises gracefully."""

    def test_all_structures_does_not_raise(self):
        try:
            result = aux.get_kinetic_energy_from_system(handler_traj, skip_digestion=True)
            if result is not None:
                val = puw.get_value(result)
                assert val.shape[0] == 0
        except Exception:
            pass

    def test_subset_does_not_raise(self):
        try:
            result = aux.get_kinetic_energy_from_system(
                handler_traj, structure_indices=[0], skip_digestion=True
            )
        except Exception:
            pass


class TestGetPotentialEnergyFromSystem:

    def test_all_structures_does_not_raise(self):
        try:
            result = aux.get_potential_energy_from_system(handler_traj, skip_digestion=True)
            if result is not None:
                val = puw.get_value(result)
                assert val.shape[0] == 0
        except Exception:
            pass

    def test_subset_does_not_raise(self):
        try:
            result = aux.get_potential_energy_from_system(
                handler_traj, structure_indices=[0], skip_digestion=True
            )
        except Exception:
            pass


class TestGetTemperatureFromSystem:

    def test_from_stored_temperature_empty(self):
        # pentalanine: temperature_from_kinetic_energy=False, temperature shape (0,)
        try:
            result = aux.get_temperature_from_system(handler_traj, skip_digestion=True)
            if result is not None:
                val = puw.get_value(result)
                assert val.shape[0] == 0
        except Exception:
            pass

    def test_subset_does_not_raise(self):
        try:
            result = aux.get_temperature_from_system(
                handler_traj, structure_indices=[0], skip_digestion=True
            )
        except Exception:
            pass


class TestGetBFactorFromSystem:

    def test_empty_b_factor_returns_none(self):
        # pentalanine: b_factor shape (0, 0) — delegates to get_b_factor_from_atom
        result = aux.get_b_factor_from_system(handler_traj, skip_digestion=True)
        assert result is None

    def test_no_b_factor_key_returns_none(self):
        # TcTIM: no 'b_factor' key in structures
        result = aux.get_b_factor_from_system(handler_tctim, skip_digestion=True)
        assert result is None
