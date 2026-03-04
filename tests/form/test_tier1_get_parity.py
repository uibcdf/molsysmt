import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np
import pyunitwizard as puw

# Define the systems from molsysmt/data to be used for parity testing
# We choose a diverse set to exercise different parts of the native topology logic
TEST_SYSTEMS = [
    ('alanine dipeptide', 'alanine_dipeptide.h5msm'),
    ('Barnase-Barstar', 'barnase_barstar.h5msm'),
    ('chicken villin HP35', 'chicken_villin_HP35_solvated.h5msm'),
]

@pytest.fixture(params=TEST_SYSTEMS, ids=[x[0] for x in TEST_SYSTEMS])
def tier1_forms(request):
    """Provides a dictionary of a molecular system in all Tier 1 forms."""
    sys_name, sys_file = request.param
    
    # Resolve the path from the systems catalog
    # Note: Using native h5msm as base to ensure high fidelity
    base_file = systems[sys_name][sys_file]
    
    # We skip forms if the dependency is not available
    forms = {
        'molsysmt.MolSys': msm.convert(base_file, to_form='molsysmt.MolSys', skip_digestion=True),
    }
    
    try:
        forms['openmm.Topology'] = msm.convert(base_file, to_form='openmm.Topology', skip_digestion=True)
    except:
        pass
        
    try:
        forms['mdtraj.Trajectory'] = msm.convert(base_file, to_form='mdtraj.Trajectory', skip_digestion=True)
    except:
        pass

    return forms

def test_get_atom_name_parity(tier1_forms):
    """Verify that atom names are identical across all available Tier 1 forms."""
    results = {}
    for form_name, item in tier1_forms.items():
        results[form_name] = msm.get(item, element='atom', atom_name=True, skip_digestion=True)
    
    native_names = results['molsysmt.MolSys']
    for form_name, names in results.items():
        assert list(names) == list(native_names), f"Atom name discrepancy in {form_name}"

def test_get_n_atoms_parity(tier1_forms):
    """Verify that n_atoms is consistent across forms."""
    results = {}
    for form_name, item in tier1_forms.items():
        results[form_name] = msm.get(item, element='system', n_atoms=True, skip_digestion=True)
    
    native_val = results['molsysmt.MolSys']
    for form_name, val in results.items():
        assert val == native_val, f"n_atoms discrepancy in {form_name}: expected {native_val}, got {val}"

def test_get_n_groups_parity(tier1_forms):
    """Verify that n_groups is consistent across forms."""
    results = {}
    for form_name, item in tier1_forms.items():
        results[form_name] = msm.get(item, element='system', n_groups=True, skip_digestion=True)
    
    native_val = results['molsysmt.MolSys']
    for form_name, val in results.items():
        assert val == native_val, f"n_groups discrepancy in {form_name}: expected {native_val}, got {val}"

def test_get_coordinates_parity(tier1_forms):
    """Verify that coordinates match within tolerance across Tier 1 forms."""
    results = {}
    for form_name, item in tier1_forms.items():
        res = msm.get(item, element='atom', coordinates=True, skip_digestion=True)
        if res is not None:
            results[form_name] = res
    
    native_coords = puw.get_value(results['molsysmt.MolSys'], to_unit='nm')
    
    for form_name, coords in results.items():
        val = puw.get_value(coords, to_unit='nm')
        # OpenMM and MDTraj might have slight float precision differences
        np.testing.assert_allclose(val, native_coords, rtol=1e-5, atol=1e-5,
                                   err_msg=f"Coordinate discrepancy in {form_name}")
