"""
Parity tests: eager vs heavy path for get_center, get_rmsd, get_distances.

All tests use the bundled pentalanine h5msm trajectory (5000 frames, 62 atoms).
heavy_mode='force' forces chunked execution regardless of footprint.
heavy_mode='off'   forces eager execution.
Max numeric difference between the two paths must be zero (same kernel, same data).
"""
import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw

pytestmark = pytest.mark.heavy

N_FRAMES = 20   # subset used in most tests to keep them fast
N_ATOMS  = 62


@pytest.fixture(scope='module')
def h5msm_path():
    return msm.systems['pentalanine']['traj_pentalanine.h5msm']


@pytest.fixture(scope='module')
def handler(h5msm_path):
    h = msm.convert(h5msm_path, to_form='molsysmt.H5MSMFileHandler')
    yield h
    h.close()


# ---------------------------------------------------------------------------
# get_center
# ---------------------------------------------------------------------------

class TestGetCenterParity:

    def test_file_path_flat_selection(self, h5msm_path):
        from molsysmt.structure import get_center
        indices = list(range(N_FRAMES))
        c_e = get_center(h5msm_path, selection='all', structure_indices=indices, heavy_mode='off')
        c_h = get_center(h5msm_path, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(c_e) - puw.get_value(c_h)))
        assert diff == 0.0, f"center eager vs heavy max_diff={diff}"

    def test_handler_flat_selection(self, handler):
        from molsysmt.structure import get_center
        indices = list(range(N_FRAMES))
        c_e = get_center(handler, selection='all', structure_indices=indices, heavy_mode='off')
        c_h = get_center(handler, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(c_e) - puw.get_value(c_h)))
        assert diff == 0.0, f"center eager vs heavy max_diff={diff}"

    def test_full_trajectory(self, h5msm_path):
        from molsysmt.structure import get_center
        c = get_center(h5msm_path, selection='all', heavy_mode='force')
        assert puw.get_value(c).shape == (5000, 1, 3)

    def test_shape(self, h5msm_path):
        from molsysmt.structure import get_center
        c = get_center(h5msm_path, selection='all',
                       structure_indices=list(range(N_FRAMES)), heavy_mode='force')
        assert puw.get_value(c).shape == (N_FRAMES, 1, 3)


# ---------------------------------------------------------------------------
# get_rmsd
# ---------------------------------------------------------------------------

class TestGetRMSDParity:

    def test_file_path(self, h5msm_path):
        from molsysmt.structure import get_rmsd
        indices = list(range(N_FRAMES))
        r_e = get_rmsd(h5msm_path, selection='all', structure_indices=indices, heavy_mode='off')
        r_h = get_rmsd(h5msm_path, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(r_e) - puw.get_value(r_h)))
        assert diff == 0.0, f"rmsd eager vs heavy max_diff={diff}"

    def test_handler(self, handler):
        from molsysmt.structure import get_rmsd
        indices = list(range(N_FRAMES))
        r_e = get_rmsd(handler, selection='all', structure_indices=indices, heavy_mode='off')
        r_h = get_rmsd(handler, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(r_e) - puw.get_value(r_h)))
        assert diff == 0.0, f"rmsd eager vs heavy max_diff={diff}"

    def test_full_trajectory(self, h5msm_path):
        from molsysmt.structure import get_rmsd
        r = get_rmsd(h5msm_path, selection='all', heavy_mode='force')
        assert puw.get_value(r).shape == (5000,)

    def test_shape(self, h5msm_path):
        from molsysmt.structure import get_rmsd
        r = get_rmsd(h5msm_path, selection='all',
                     structure_indices=list(range(N_FRAMES)), heavy_mode='force')
        assert puw.get_value(r).shape == (N_FRAMES,)

    def test_first_frame_rmsd_is_zero(self, h5msm_path):
        """RMSD of frame 0 vs itself (default reference) must be zero."""
        from molsysmt.structure import get_rmsd
        r = get_rmsd(h5msm_path, selection='all',
                     structure_indices=[0], heavy_mode='force')
        assert puw.get_value(r)[0] == pytest.approx(0.0, abs=1e-10)


# ---------------------------------------------------------------------------
# get_distances
# ---------------------------------------------------------------------------

class TestGetDistancesParity:

    def test_file_path(self, h5msm_path):
        from molsysmt.structure import get_distances
        indices = list(range(5))
        d_e = get_distances(h5msm_path, selection='all', structure_indices=indices, heavy_mode='off')
        d_h = get_distances(h5msm_path, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(d_e) - puw.get_value(d_h)))
        assert diff == 0.0, f"distances eager vs heavy max_diff={diff}"

    def test_handler(self, handler):
        from molsysmt.structure import get_distances
        indices = list(range(5))
        d_e = get_distances(handler, selection='all', structure_indices=indices, heavy_mode='off')
        d_h = get_distances(handler, selection='all', structure_indices=indices, heavy_mode='force')
        diff = np.max(np.abs(puw.get_value(d_e) - puw.get_value(d_h)))
        assert diff == 0.0, f"distances eager vs heavy max_diff={diff}"

    def test_shape(self, h5msm_path):
        from molsysmt.structure import get_distances
        d = get_distances(h5msm_path, selection='all',
                          structure_indices=list(range(5)), heavy_mode='force')
        assert puw.get_value(d).shape == (5, N_ATOMS, N_ATOMS)

    def test_diagonal_is_zero(self, h5msm_path):
        """Self-distances (diagonal) must be zero for all frames."""
        from molsysmt.structure import get_distances
        d = get_distances(h5msm_path, selection='all',
                          structure_indices=[0], heavy_mode='force')
        val = puw.get_value(d)[0]
        assert np.allclose(np.diag(val), 0.0, atol=1e-10)
