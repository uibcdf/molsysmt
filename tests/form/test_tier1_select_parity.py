import pytest
import molsysmt as msm
from molsysmt import systems
import numpy as np

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

@pytest.mark.parametrize("query", [
    "atom_name == 'CA'",
    "group_name == 'ALA'",
    "atom_index in [0, 1, 2, 3, 4]",
    "atom_name == 'CA' and group_name == 'ALA'",
    "group_index == 2",
])
def test_select_parity(pentalanine_tier1_forms, query):
    """Verify that the same query returns identical indices across all Tier 1 forms."""
    
    results = {}
    for form_name, item in pentalanine_tier1_forms.items():
        results[form_name] = msm.select(item, selection=query)
    
    native_indices = list(results['molsysmt.MolSys'])
    
    for form_name, indices in results.items():
        assert list(indices) == native_indices, f"Selection discrepancy in {form_name} for query: {query}"

def test_select_all_parity(pentalanine_tier1_forms):
    """Verify that 'all' selection is consistent."""
    
    results = {}
    for form_name, item in pentalanine_tier1_forms.items():
        results[form_name] = msm.select(item, selection='all')
    
    n_atoms_native = len(results['molsysmt.MolSys'])
    assert n_atoms_native == 62
    
    for form_name, indices in results.items():
        assert len(indices) == 62, f"'all' selection discrepancy in {form_name}"
