import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pyunitwizard as puw

@pytest.fixture
def pentalanine_tier1_forms():
    """Provides a dictionary of pentalanine in Tier 1 forms."""
    base_file = systems['pentalanine']['traj_pentalanine.h5']
    forms = {
        'molsysmt.MolSys': msm.convert(base_file, to_form='molsysmt.MolSys'),
        'openmm.Topology': msm.convert(base_file, to_form='openmm.Topology'),
        'mdtraj.Trajectory': msm.convert(base_file, to_form='mdtraj.Trajectory'),
    }
    return forms

def test_get_atom_name_parity(pentalanine_tier1_forms):
    """Verify that atom names are identical across all Tier 1 forms."""
    
    results = {}
    for form_name, item in pentalanine_tier1_forms.items():
        results[form_name] = msm.get(item, element='atom', name=True)
    
    # Compare all against the native MolSys
    native_names = results['molsysmt.MolSys']
    for form_name, names in results.items():
        assert names == native_names, f"Atom name discrepancy in {form_name}"

def test_get_coordinates_parity(pentalanine_tier1_forms):
    """Verify that coordinates match within tolerance across Tier 1 forms."""
    
    results = {}
    for form_name, item in pentalanine_tier1_forms.items():
        # Coordinates should come out standardized in nanometers (MolSysMT standard)
        res = msm.get(item, element='atom', coordinates=True)
        if res is not None:
            results[form_name] = res
    
    if 'molsysmt.MolSys' not in results:
        return

    native_coords = puw.get_value(results['molsysmt.MolSys'], to_unit='nm')
    
    for form_name, coords in results.items():
        val = puw.get_value(coords, to_unit='nm')
        # Using a strict tolerance for Tier 1 parity
        np.testing.assert_allclose(val, native_coords, atol=1e-5, 
                                   err_msg=f"Coordinate discrepancy in {form_name}")

def test_get_n_atoms_parity(pentalanine_tier1_forms):
    """Verify that n_atoms is consistent."""
    
    for form_name, item in pentalanine_tier1_forms.items():
        n_atoms = msm.get(item, element='system', n_atoms=True)
        assert n_atoms == 62, f"n_atoms discrepancy in {form_name}: expected 62, got {n_atoms}"
