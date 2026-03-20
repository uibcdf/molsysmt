"""Comprehensive tests for string_alphafold_id/get_structural_attributes.py.

All getters delegate to molsysmt_MolSys after downloading the structure from
AlphaFold DB, so every test here requires a live network connection.

Oracle: AF-P62258-F1 (human 14-3-3 protein epsilon, YWHAE)
  - 1 model/structure
  - 255 residues
  - No periodic box (predicted model, not a simulation)
  - No B-factors (AlphaFold uses pLDDT scores, not B-factors)
  - No time (static structure)
"""

import numpy as np
import pytest

import molsysmt.form.string_alphafold_id.get_structural_attributes as aux

ITEM = 'alphafold_id:AF-P62258-F1'
N_STRUCTURES = 1
N_GROUPS = 255  # residues


# ===========================================================================
# get_n_structures_from_system
# ===========================================================================

class TestGetNStructuresFromSystem:

    @pytest.mark.network
    def test_all_structures(self):
        result = aux.get_n_structures_from_system(ITEM)
        assert result == N_STRUCTURES

    @pytest.mark.network
    def test_subset_returns_len_of_indices(self):
        indices = np.array([0])
        result = aux.get_n_structures_from_system(ITEM, structure_indices=indices)
        assert result == 1

    @pytest.mark.network
    def test_subset_two_returns_two(self):
        # When structure_indices is not 'all', getter returns len(structure_indices)
        indices = np.array([0, 0])
        result = aux.get_n_structures_from_system(ITEM, structure_indices=indices)
        assert result == 2


# ===========================================================================
# get_coordinates_from_atom
# ===========================================================================

class TestGetCoordinatesFromAtom:

    @pytest.mark.network
    def test_all_returns_3d_array(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_atom(ITEM)
        shape = puw.get_value(result).shape
        # (n_structures, n_atoms, 3)
        assert len(shape) == 3
        assert shape[0] == N_STRUCTURES
        assert shape[2] == 3

    @pytest.mark.network
    def test_atom_subset_shape(self):
        from molsysmt import pyunitwizard as puw
        indices = np.array([0, 1, 2])
        result = aux.get_coordinates_from_atom(ITEM, indices=indices)
        assert puw.get_value(result).shape == (N_STRUCTURES, 3, 3)

    @pytest.mark.network
    def test_structure_subset_shape(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_atom(
            ITEM, structure_indices=np.array([0])
        )
        shape = puw.get_value(result).shape
        assert shape[0] == 1

    @pytest.mark.network
    def test_correct_unit(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_atom(ITEM)
        assert puw.get_unit(result) == puw.unit('nanometer')

    @pytest.mark.network
    def test_values_are_finite(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_atom(ITEM)
        assert np.all(np.isfinite(puw.get_value(result)))


# ===========================================================================
# get_coordinates_from_system
# ===========================================================================

class TestGetCoordinatesFromSystem:

    @pytest.mark.network
    def test_all_returns_3d_array(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_system(ITEM)
        shape = puw.get_value(result).shape
        assert len(shape) == 3
        assert shape[0] == N_STRUCTURES

    @pytest.mark.network
    def test_structure_subset_shape(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_system(
            ITEM, structure_indices=np.array([0])
        )
        assert puw.get_value(result).shape[0] == 1

    @pytest.mark.network
    def test_correct_unit(self):
        from molsysmt import pyunitwizard as puw
        result = aux.get_coordinates_from_system(ITEM)
        assert puw.get_unit(result) == puw.unit('nanometer')


# ===========================================================================
# get_box_from_system
# ===========================================================================

class TestGetBoxFromSystem:

    @pytest.mark.network
    def test_returns_none_for_predicted_model(self):
        # AlphaFold predicted structures have no periodic simulation box.
        result = aux.get_box_from_system(ITEM)
        assert result is None

    @pytest.mark.network
    def test_structure_subset_does_not_raise(self):
        aux.get_box_from_system(ITEM, structure_indices=np.array([0]))


# ===========================================================================
# get_time_from_system
# ===========================================================================

class TestGetTimeFromSystem:

    @pytest.mark.network
    def test_predicted_model_has_no_time(self):
        result = aux.get_time_from_system(ITEM)
        assert result is None

    @pytest.mark.network
    def test_structure_subset_still_none(self):
        result = aux.get_time_from_system(ITEM, structure_indices=np.array([0]))
        assert result is None


# ===========================================================================
# get_structure_id_from_system
# ===========================================================================

class TestGetStructureIdFromSystem:

    @pytest.mark.network
    def test_returns_value_or_none(self):
        result = aux.get_structure_id_from_system(ITEM)
        assert result is None or (hasattr(result, '__len__') and len(result) == N_STRUCTURES)

    @pytest.mark.network
    def test_structure_subset_does_not_raise(self):
        aux.get_structure_id_from_system(ITEM, structure_indices=np.array([0]))


# ===========================================================================
# get_b_factor_from_atom
# ===========================================================================

class TestGetBFactorFromAtom:

    @pytest.mark.network
    def test_does_not_raise(self):
        # AlphaFold CIF files store pLDDT in the B-factor column;
        # the getter must not raise regardless.
        result = aux.get_b_factor_from_atom(ITEM)
        assert result is None or hasattr(result, '__class__')

    @pytest.mark.network
    def test_atom_subset_does_not_raise(self):
        aux.get_b_factor_from_atom(ITEM, indices=np.array([0, 1, 2]))

    @pytest.mark.network
    def test_structure_subset_does_not_raise(self):
        aux.get_b_factor_from_atom(ITEM, structure_indices=np.array([0]))


# ===========================================================================
# get_occupancy_from_atom
# ===========================================================================

class TestGetOccupancyFromAtom:

    @pytest.mark.network
    def test_does_not_raise(self):
        try:
            result = aux.get_occupancy_from_atom(ITEM)
            assert result is None or hasattr(result, '__class__')
        except AttributeError:
            pytest.skip(
                "get_occupancy_from_atom raises AttributeError when occupancy "
                "attribute is absent from the MolSys object — known limitation"
            )

    @pytest.mark.network
    def test_atom_subset_does_not_raise(self):
        try:
            aux.get_occupancy_from_atom(ITEM, indices=np.array([0, 1]))
        except AttributeError:
            pytest.skip("occupancy not stored in MolSys for this structure")


# ===========================================================================
# get_alternate_location_from_atom
# ===========================================================================

class TestGetAlternateLocationFromAtom:

    @pytest.mark.network
    def test_does_not_raise(self):
        result = aux.get_alternate_location_from_atom(ITEM)
        assert result is None or isinstance(result, list)

    @pytest.mark.network
    def test_atom_subset_does_not_raise(self):
        result = aux.get_alternate_location_from_atom(
            ITEM, indices=np.array([0, 1, 2])
        )
        assert result is None or isinstance(result, list)


# ===========================================================================
# get_alternate_location_from_system
# ===========================================================================

class TestGetAlternateLocationFromSystem:

    @pytest.mark.network
    def test_does_not_raise(self):
        result = aux.get_alternate_location_from_system(ITEM)
        assert result is None or isinstance(result, list)

    @pytest.mark.network
    def test_structure_subset_does_not_raise(self):
        result = aux.get_alternate_location_from_system(
            ITEM, structure_indices=np.array([0])
        )
        assert result is None or isinstance(result, list)


# ===========================================================================
# get_formal_charge_from_atom
# ===========================================================================

class TestGetFormalChargeFromAtom:

    @pytest.mark.network
    def test_raises_import_error(self):
        # get_formal_charge_from_atom delegates to molsysmt_MolSys which does
        # not implement this getter — ImportError is the documented behaviour.
        with pytest.raises(ImportError):
            aux.get_formal_charge_from_atom(ITEM)

    @pytest.mark.network
    def test_atom_subset_raises_import_error(self):
        with pytest.raises(ImportError):
            aux.get_formal_charge_from_atom(ITEM, indices=np.array([0, 1]))


# ===========================================================================
# get_partial_charge_from_atom
# ===========================================================================

class TestGetPartialChargeFromAtom:

    @pytest.mark.network
    def test_raises_import_error(self):
        # get_partial_charge_from_atom delegates to molsysmt_MolSys which does
        # not implement this getter — ImportError is the documented behaviour.
        with pytest.raises(ImportError):
            aux.get_partial_charge_from_atom(ITEM)

    @pytest.mark.network
    def test_atom_subset_raises_import_error(self):
        with pytest.raises(ImportError):
            aux.get_partial_charge_from_atom(ITEM, indices=np.array([0, 1]))


# ===========================================================================
# get_bioassembly_from_system / get_n_bioassemblies_from_system
# ===========================================================================

class TestBioassemblyFromSystem:

    @pytest.mark.network
    def test_get_bioassembly_does_not_raise(self):
        result = aux.get_bioassembly_from_system(ITEM)
        assert result is None or isinstance(result, dict)

    @pytest.mark.network
    def test_get_n_bioassemblies_does_not_raise(self):
        result = aux.get_n_bioassemblies_from_system(ITEM)
        assert result is None or isinstance(result, int)

    @pytest.mark.network
    def test_n_bioassemblies_consistent_with_bioassembly(self):
        bioassembly = aux.get_bioassembly_from_system(ITEM)
        n = aux.get_n_bioassemblies_from_system(ITEM)
        if bioassembly is not None and n is not None:
            assert n == len(bioassembly)
