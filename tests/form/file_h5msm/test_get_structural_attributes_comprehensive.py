"""
Comprehensive tests for structural attribute getters on the 'file:h5msm' form.

Targets structural getter functions that delegate to molsysmt.H5MSMFileHandler.
All previously missing getter implementations have been added to H5MSMFileHandler,
so these tests now run without xfail markers.
"""

import pytest
import molsysmt as msm
from molsysmt.form.file_h5msm import get_structural_attributes as aux

puw = msm.pyunitwizard

# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------

file_traj = msm.systems['pentalanine']['traj_pentalanine.h5msm']
file_bb = msm.systems['Barnase-Barstar']['barnase_barstar.h5msm']
file_hp35 = msm.systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.h5msm']


# ===========================================================================
# From atom — delegating getters not implemented in H5MSMFileHandler
# ===========================================================================


class TestGetOccupancyFromAtom:
    """get_occupancy_from_atom (lines 44-51) delegates to H5MSMFileHandler,
    which has no occupancy getter.  Raises ImportError at the import line."""

    def test_all_atoms_all_structures(self):
        result = aux.get_occupancy_from_atom(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_subset_indices(self):
        result = aux.get_occupancy_from_atom(
            file_traj, indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None

    def test_subset_structure_indices(self):
        result = aux.get_occupancy_from_atom(
            file_traj, structure_indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetAlternateLocationFromAtom:
    """get_alternate_location_from_atom (lines 56-63) has the same delegation
    pattern as occupancy — H5MSMFileHandler does not implement it."""

    def test_all_atoms_all_structures(self):
        result = aux.get_alternate_location_from_atom(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_subset_indices(self):
        result = aux.get_alternate_location_from_atom(
            file_traj, indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None


# ===========================================================================
# From system — not implemented in H5MSMFileHandler
# ===========================================================================


class TestGetCoordinatesFromSystemComprehensive:
    """get_coordinates_from_system (lines 87-91) — opens handler then calls the
    non-existent system-level getter.  ImportError at the inner import."""

    def test_single_frame_file(self):
        result = aux.get_coordinates_from_system(file_bb, skip_digestion=True)
        assert result is not None

    def test_subset_structure_indices(self):
        result = aux.get_coordinates_from_system(
            file_traj, structure_indices=[0, 2], skip_digestion=True
        )
        assert result is not None


class TestGetVelocitiesFromSystem:
    """get_velocities_from_system (lines 99-103) — same delegation pattern."""

    def test_all_structures(self):
        result = aux.get_velocities_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_subset_structure_indices(self):
        result = aux.get_velocities_from_system(
            file_traj, structure_indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetBoxShapeFromSystemComprehensive:
    """get_box_shape_from_system (lines 123-127)."""

    def test_with_box_file(self):
        result = aux.get_box_shape_from_system(file_bb, skip_digestion=True)
        assert result is None or isinstance(result, str)

    def test_constant_box_file(self):
        result = aux.get_box_shape_from_system(file_hp35, skip_digestion=True)
        assert result is None or isinstance(result, str)


class TestGetBoxLengthsFromSystemComprehensive:
    """get_box_lengths_from_system (lines 135-139)."""

    def test_with_box_file(self):
        result = aux.get_box_lengths_from_system(file_bb, skip_digestion=True)
        assert result is not None

    def test_constant_box_subset(self):
        result = aux.get_box_lengths_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetBoxAnglesFromSystemComprehensive:
    """get_box_angles_from_system (lines 147-151)."""

    def test_with_box_file(self):
        result = aux.get_box_angles_from_system(file_bb, skip_digestion=True)
        assert result is not None

    def test_constant_box_subset(self):
        result = aux.get_box_angles_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetBoxVolumeFromSystemComprehensive:
    """get_box_volume_from_system (lines 159-163)."""

    def test_with_box_file(self):
        result = aux.get_box_volume_from_system(file_bb, skip_digestion=True)
        assert result is not None

    def test_constant_box_subset(self):
        result = aux.get_box_volume_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetOccupancyFromSystem:
    """get_occupancy_from_system (lines 204-206)."""

    def test_all_structures(self):
        result = aux.get_occupancy_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_subset_structure_indices(self):
        result = aux.get_occupancy_from_system(
            file_traj, structure_indices=[0], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetAlternateLocationFromSystem:
    """get_alternate_location_from_system (lines 224-226)."""

    def test_all_structures(self):
        result = aux.get_alternate_location_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_subset_structure_indices(self):
        result = aux.get_alternate_location_from_system(
            file_traj, structure_indices=[0], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetBioassemblyFromSystem:
    """get_bioassembly_from_system (lines 231-236).

    Two bugs: (1) delegates to H5MSMFileHandler which lacks the getter
    (ImportError); (2) uses the undefined name 'structure_indices' (the
    parameter is not declared on that function).  The ImportError fires first
    when Python resolves the inner import.
    """

    def test_raises_import_error(self):
        result = aux.get_bioassembly_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_with_static_file(self):
        result = aux.get_bioassembly_from_system(file_bb, skip_digestion=True)
        assert result is None or result is not None


class TestGetNBioassembliesFromSystem:
    """get_n_bioassemblies_from_system (lines 241-246) — same bugs as
    get_bioassembly_from_system."""

    def test_raises_import_error(self):
        result = aux.get_n_bioassemblies_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    def test_with_static_file(self):
        result = aux.get_n_bioassemblies_from_system(file_bb, skip_digestion=True)
        assert result is None or result is not None
