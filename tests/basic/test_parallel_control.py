import pytest
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures
from molsysmt import pyunitwizard as puw


def test_parallel_default_config():
    """Verify that automatic native thread selection is the default."""
    assert msm.configure.parallel_mode == "auto"
    assert msm.configure.num_threads == -1
    assert msm.configure.parallel_threshold == 500_000
    assert msm.configure.min_payload_per_thread == 250_000


def test_session_policy_and_function_override_are_composable():
    """Resolve per-call values without mutating the surrounding session."""
    from molsysmt.configure import _get_effective_num_threads
    from molsysmt.configure import with_configure_overrides

    @with_configure_overrides
    def resolve(payload_size, parallel=None, num_threads=None):
        return _get_effective_num_threads(payload_size)

    with msm.configure.context(parallel_mode=True, num_threads=4):
        assert resolve(10) == 4
        assert resolve(10, parallel=False) == 1
        assert resolve(10, parallel=True, num_threads=2) == 2
        assert msm.configure.parallel_mode is True
        assert msm.configure.num_threads == 4


def test_set_parallelization_updates_the_session_policy():
    """Configure both session-level controls through the validated public helper."""
    old_parallel = msm.configure.parallel_mode
    old_num_threads = msm.configure.num_threads
    try:
        policy = msm.configure.set_parallelization(parallel=True, num_threads=3)
        assert policy == {"parallel": True, "num_threads": 3}
        assert msm.configure.parallel_mode is True
        assert msm.configure.get_num_threads() == 3
    finally:
        msm.configure.parallel_mode = old_parallel
        msm.configure.num_threads = old_num_threads


def test_nested_public_calls_inherit_the_outer_function_override():
    """Keep a local policy active through decorated internal public calls."""
    from molsysmt.configure import _get_effective_num_threads
    from molsysmt.configure import with_configure_overrides

    @with_configure_overrides
    def inner(parallel=None, num_threads=None):
        return _get_effective_num_threads(1_000_000)

    @with_configure_overrides
    def outer(parallel=None, num_threads=None):
        return inner()

    with msm.configure.context(parallel_mode=True, num_threads=8):
        assert outer(parallel=True, num_threads=2) == 2
        assert inner() == 8


def test_auto_policy_uses_workload_threshold_and_thread_limit():
    """Scale an automatic call from serial to the configured maximum."""
    from molsysmt.configure import _get_effective_num_threads

    with msm.configure.context(
        parallel_mode="auto",
        num_threads=8,
        parallel_threshold=500,
        min_payload_per_thread=250,
    ):
        assert _get_effective_num_threads(499) == 1
        assert _get_effective_num_threads(500) == 2
        assert _get_effective_num_threads(1_000) == 4
        assert _get_effective_num_threads(10_000) == 8


def test_rayon_pools_are_reusable_at_different_sizes():
    """Use multiple cached Rayon pools in the same Python process."""
    import molsysmt._rust as rust

    assert rust.probe_num_threads(1) == 1
    assert rust.probe_num_threads(2) == 2
    assert rust.probe_num_threads(1) == 1


def test_python_kernel_seam_passes_the_resolved_pool_size(monkeypatch):
    """Pass the effective session or call-local size into a native binding."""
    from molsysmt._private import rust_backend
    from molsysmt.configure import with_configure_overrides

    observed = []

    def fake_get_center(coordinates, weights, num_threads):
        observed.append(num_threads)
        return np.zeros((coordinates.shape[0], 1, 3))

    monkeypatch.setattr(rust_backend._rust, "get_center", fake_get_center)

    @with_configure_overrides
    def run(parallel=None, num_threads=None):
        coordinates = np.zeros((2, 3, 3))
        return rust_backend.get_center(coordinates, np.ones(3))

    with msm.configure.context(parallel_mode=True, num_threads=4):
        run()
        run(parallel=False)
        run(parallel=True, num_threads=2)

    assert observed == [4, 1, 2]


def test_parallel_false_rejects_a_conflicting_local_thread_count():
    """Reject contradictory per-function controls."""
    from molsysmt.configure import _get_effective_num_threads
    from molsysmt.configure import with_configure_overrides

    @with_configure_overrides
    def resolve(parallel=None, num_threads=None):
        return _get_effective_num_threads(1_000_000)

    with pytest.raises(msm.ArgumentConflictError):
        resolve(parallel=False, num_threads=4)

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

def test_native_parallel_kernel_surface():
    """Verify that the public operations backed by native kernels execute."""
    # Load pentalanine molecular system
    from molsysmt import systems
    molsys = msm.convert(systems['pentalanine']['traj_pentalanine.h5'], to_form='molsysmt.MolSys')
    
    center_serial = msm.structure.get_center(
        molsys,
        selection="backbone",
        parallel=False,
    )
    center_parallel = msm.structure.get_center(
        molsys,
        selection="backbone",
        parallel=True,
        num_threads=2,
    )
    assert np.allclose(puw.get_value(center_serial), puw.get_value(center_parallel))
    
    # Test get_distances
    distances = msm.structure.get_distances(
        molsys,
        selection='backbone',
        structure_indices=range(5),
        parallel=True,
        num_threads=2,
    )
    assert distances is not None
    
    # Test get_rmsd
    rmsd = msm.structure.get_rmsd(
        molsys,
        selection='backbone',
        reference_structure_index=0,
        parallel=False,
    )
    assert rmsd is not None

    # Test get_least_rmsd
    least_rmsd = msm.structure.get_least_rmsd(
        molsys,
        selection='backbone',
        reference_structure_index=0,
        parallel=True,
        num_threads=2,
    )
    assert least_rmsd is not None

    # Test get_least_rmsd on GPU (will execute on GPU if CUDA is available, or fallback to CPU safely)
    lr_gpu = msm.structure.get_least_rmsd(molsys, selection='backbone', reference_structure_index=0, use_gpu=True)
    assert lr_gpu is not None


    # Test least_rmsd_fit
    fit = msm.structure.least_rmsd_fit(
        molsys,
        selection='backbone',
        selection_fit='backbone',
        reference_structure_index=0,
        parallel=True,
        num_threads=2,
    )
    assert fit is not None


def test_gpu_mode_configuration():
    """Verify that default, context manager overrides, and resolution of gpu_mode function correctly."""
    # Verify default config values
    assert msm.configure.gpu_mode == 'auto'
    assert msm.configure.use_gpu == 'auto'
    assert msm.configure.gpu_threshold == 3_000_000

    # Test context manager temporary overrides
    with msm.configure.context(gpu_mode=True):
        assert msm.configure.gpu_mode is True
        assert msm.configure.use_gpu is True

    with msm.configure.context(gpu_mode=False):
        assert msm.configure.gpu_mode is False
        assert msm.configure.use_gpu is False

    # Test resolve_use_gpu utility
    from molsysmt._private.gpu import resolve_use_gpu
    
    with msm.configure.context(gpu_mode=False):
        # Even if per-call is auto, if global is False, resolve_use_gpu returns False
        assert resolve_use_gpu('auto', payload_size=5_000_000) is False
        # If per-call is False, it returns False
        assert resolve_use_gpu(False, payload_size=5_000_000) is False
