import pytest
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
from molsysmt import pyunitwizard as puw

def test_parallel_default_config():
    """Verify that default parallelization configurations are correct."""
    assert msm.configure.parallel_mode == 'auto'
    assert msm.configure.num_threads == -1
    assert msm.configure.parallel_threshold == 500_000
    assert msm.configure.min_payload_per_thread == 250_000

def test_configure_context_manager():
    """Verify that the configure.context manager temporarily overrides settings thread-safely."""
    orig_mode = msm.configure.parallel_mode
    orig_threads = msm.configure.num_threads

    with msm.configure.context(parallel_mode=True, num_threads=4):
        assert msm.configure.parallel_mode is True
        assert msm.configure.num_threads == 4

    assert msm.configure.parallel_mode == orig_mode
    assert msm.configure.num_threads == orig_threads

def test_zero_copy_read_only_views():
    """Verify that native Structures returns read-only zero-copy views for coordinates and box."""
    # Create a small native structures instance
    coors = np.random.rand(10, 5, 3) # n_structures=10, n_atoms=5
    box = np.eye(3).reshape(1, 3, 3).repeat(10, axis=0) # [10, 3, 3]
    
    structs = Structures(
        coordinates=puw.quantity(coors, 'nm'),
        box=puw.quantity(box, 'nm')
    )
    
    # Internal arrays should be float64 numpy arrays and read-only
    assert structs._coordinates is not None
    assert structs._coordinates.flags.writeable is False
    assert structs._box is not None
    assert structs._box.flags.writeable is False
    
    # Coordinates retrieved via getter property should be wrapped in quantity
    coords_q = structs.coordinates
    assert puw.is_quantity(coords_q)
    
    # Underlying array should still be read-only
    underlying = puw.get_value(coords_q)
    assert underlying.flags.writeable is False
    
    # Trying to mutate should raise ValueError
    with pytest.raises(ValueError):
        underlying[0, 0, 0] = 999.0

def test_parallel_execution_modes():
    """Verify that get_center, get_distances, and get_rmsd execute under all modes."""
    # Load pentalanine molecular system
    from molsysmt import systems
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    
    # Test get_center
    c_auto = msm.structure.get_center(molsys, selection='backbone', parallel='auto')
    c_true = msm.structure.get_center(molsys, selection='backbone', parallel=True, num_threads=2)
    c_false = msm.structure.get_center(molsys, selection='backbone', parallel=False)
    
    assert c_auto is not None
    assert c_true is not None
    assert c_false is not None
    
    # Test get_distances
    d_auto = msm.structure.get_distances(molsys, selection='backbone', structure_indices=range(5), parallel='auto')
    d_true = msm.structure.get_distances(molsys, selection='backbone', structure_indices=range(5), parallel=True, num_threads=2)
    d_false = msm.structure.get_distances(molsys, selection='backbone', structure_indices=range(5), parallel=False)
    
    assert d_auto is not None
    assert d_true is not None
    assert d_false is not None
    
    # Test get_rmsd
    r_auto = msm.structure.get_rmsd(molsys, selection='backbone', reference_structure_index=0, parallel='auto')
    r_true = msm.structure.get_rmsd(molsys, selection='backbone', reference_structure_index=0, parallel=True, num_threads=2)
    r_false = msm.structure.get_rmsd(molsys, selection='backbone', reference_structure_index=0, parallel=False)
    
    assert r_auto is not None
    assert r_true is not None
    assert r_false is not None
