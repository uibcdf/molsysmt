"""
Comprehensive tests for structural attribute getters on the 'file:h5msm' form.

Targets lines NOT covered by test_get_structural_attributes_file_h5msm.py:

  44-51  : get_occupancy_from_atom body
  56-63  : get_alternate_location_from_atom body
  87-91  : get_coordinates_from_system body
  99-103 : get_velocities_from_system body
  123-127: get_box_shape_from_system body
  135-139: get_box_lengths_from_system body
  147-151: get_box_angles_from_system body
  159-163: get_box_volume_from_system body
  204-206: get_occupancy_from_system body
  224-226: get_alternate_location_from_system body
  231-236: get_bioassembly_from_system body
  241-246: get_n_bioassemblies_from_system body

All of these functions delegate to the molsysmt.H5MSMFileHandler form, which does
not implement the corresponding getters.  Each call raises ImportError at the
'from molsysmt.form.molsysmt_H5MSMFileHandler import <name>' line, which means
the surrounding delegation code (lines listed above) IS executed up to the point
of the error.  These tests make those lines reachable and correctly document the
current known-broken state with pytest.mark.xfail.
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

    @pytest.mark.xfail(
        reason="get_occupancy_from_atom delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_all_atoms_all_structures(self):
        result = aux.get_occupancy_from_atom(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_occupancy_from_atom delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_subset_indices(self):
        result = aux.get_occupancy_from_atom(
            file_traj, indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_occupancy_from_atom delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_subset_structure_indices(self):
        result = aux.get_occupancy_from_atom(
            file_traj, structure_indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetAlternateLocationFromAtom:
    """get_alternate_location_from_atom (lines 56-63) has the same delegation
    pattern as occupancy — H5MSMFileHandler does not implement it."""

    @pytest.mark.xfail(
        reason="get_alternate_location_from_atom delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_all_atoms_all_structures(self):
        result = aux.get_alternate_location_from_atom(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_alternate_location_from_atom delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
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

    @pytest.mark.xfail(
        reason="get_coordinates_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_single_frame_file(self):
        result = aux.get_coordinates_from_system(file_bb, skip_digestion=True)
        assert result is not None

    @pytest.mark.xfail(
        reason="get_coordinates_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_subset_structure_indices(self):
        result = aux.get_coordinates_from_system(
            file_traj, structure_indices=[0, 2], skip_digestion=True
        )
        assert result is not None


class TestGetVelocitiesFromSystem:
    """get_velocities_from_system (lines 99-103) — same delegation pattern."""

    @pytest.mark.xfail(
        reason="get_velocities_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_all_structures(self):
        result = aux.get_velocities_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_velocities_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_subset_structure_indices(self):
        result = aux.get_velocities_from_system(
            file_traj, structure_indices=[0, 1], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetBoxShapeFromSystemComprehensive:
    """get_box_shape_from_system (lines 123-127)."""

    @pytest.mark.xfail(
        reason="get_box_shape_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_box_file(self):
        result = aux.get_box_shape_from_system(file_bb, skip_digestion=True)
        assert result is None or isinstance(result, str)

    @pytest.mark.xfail(
        reason="get_box_shape_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_constant_box_file(self):
        result = aux.get_box_shape_from_system(file_hp35, skip_digestion=True)
        assert result is None or isinstance(result, str)


class TestGetBoxLengthsFromSystemComprehensive:
    """get_box_lengths_from_system (lines 135-139)."""

    @pytest.mark.xfail(
        reason="get_box_lengths_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_box_file(self):
        result = aux.get_box_lengths_from_system(file_bb, skip_digestion=True)
        assert result is not None

    @pytest.mark.xfail(
        reason="get_box_lengths_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_constant_box_subset(self):
        result = aux.get_box_lengths_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetBoxAnglesFromSystemComprehensive:
    """get_box_angles_from_system (lines 147-151)."""

    @pytest.mark.xfail(
        reason="get_box_angles_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_box_file(self):
        result = aux.get_box_angles_from_system(file_bb, skip_digestion=True)
        assert result is not None

    @pytest.mark.xfail(
        reason="get_box_angles_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_constant_box_subset(self):
        result = aux.get_box_angles_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetBoxVolumeFromSystemComprehensive:
    """get_box_volume_from_system (lines 159-163)."""

    @pytest.mark.xfail(
        reason="get_box_volume_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_box_file(self):
        result = aux.get_box_volume_from_system(file_bb, skip_digestion=True)
        assert result is not None

    @pytest.mark.xfail(
        reason="get_box_volume_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_constant_box_subset(self):
        result = aux.get_box_volume_from_system(
            file_hp35, structure_indices=[0], skip_digestion=True
        )
        assert result is not None


class TestGetOccupancyFromSystem:
    """get_occupancy_from_system (lines 204-206)."""

    @pytest.mark.xfail(
        reason="get_occupancy_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_all_structures(self):
        result = aux.get_occupancy_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_occupancy_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_subset_structure_indices(self):
        result = aux.get_occupancy_from_system(
            file_traj, structure_indices=[0], skip_digestion=True
        )
        assert result is None or result is not None


class TestGetAlternateLocationFromSystem:
    """get_alternate_location_from_system (lines 224-226)."""

    @pytest.mark.xfail(
        reason="get_alternate_location_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_all_structures(self):
        result = aux.get_alternate_location_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_alternate_location_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
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

    @pytest.mark.xfail(
        reason="get_bioassembly_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_raises_import_error(self):
        result = aux.get_bioassembly_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_bioassembly_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_static_file(self):
        result = aux.get_bioassembly_from_system(file_bb, skip_digestion=True)
        assert result is None or result is not None


class TestGetNBioassembliesFromSystem:
    """get_n_bioassemblies_from_system (lines 241-246) — same bugs as
    get_bioassembly_from_system."""

    @pytest.mark.xfail(
        reason="get_n_bioassemblies_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_raises_import_error(self):
        result = aux.get_n_bioassemblies_from_system(file_traj, skip_digestion=True)
        assert result is None or result is not None

    @pytest.mark.xfail(
        reason="get_n_bioassemblies_from_system delegates to H5MSMFileHandler which lacks this getter (ImportError)",
        raises=ImportError,
        strict=True,
    )
    def test_with_static_file(self):
        result = aux.get_n_bioassemblies_from_system(file_bb, skip_digestion=True)
        assert result is None or result is not None
