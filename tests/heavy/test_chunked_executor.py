"""
Tests for ChunkedExecutor — parity between eager and heavy paths.
Uses the pentalanine h5msm fixture (5000 frames, 62 atoms, with coordinates and time).
"""
import pytest
import numpy as np
import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import ChunkedExecutor, Reducer, estimate_footprint, decide_mode

from .conftest import N_ATOMS, N_STRUCTURES


class CoordinatesCollector(Reducer):
    """Collects all coordinates across chunks."""

    def initialize(self, metadata):
        self.all_coords = []

    def consume(self, chunk):
        self.all_coords.append(chunk['coordinates'].copy())

    def finalize(self):
        return np.concatenate(self.all_coords, axis=0)


@pytest.mark.heavy
def test_chunked_executor_heavy_force_parity(pentalanine_h5msm):
    """ChunkedExecutor in heavy mode must produce same coordinates as msm.get."""
    molsys = msm.convert(pentalanine_h5msm, to_form='molsysmt.H5MSMFileHandler')

    # Reference: eager get of all coordinates
    ref_coords = puw.get_value(
        msm.get(molsys, element='atom', selection='all', coordinates=True)
    )
    assert ref_coords.shape == (N_STRUCTURES, N_ATOMS, 3)

    # Heavy result via ChunkedExecutor with small chunk_size (odd to test boundary)
    reducer = CoordinatesCollector()
    executor = ChunkedExecutor(
        molecular_system=molsys,
        form='molsysmt.H5MSMFileHandler',
        operation='test_collect_coordinates',
        reducer=reducer,
        chunk_size=7,
        heavy_mode='force',
        attributes=['coordinates'],
    )
    result = executor.execute()

    assert result.shape == (N_STRUCTURES, N_ATOMS, 3)
    np.testing.assert_allclose(result, ref_coords, atol=1e-5)


@pytest.mark.heavy
def test_chunked_executor_decision_auto_small():
    """Auto mode on a small trajectory should select eager path."""
    fp = estimate_footprint(N_ATOMS, N_STRUCTURES)
    mode = decide_mode(fp, heavy_mode='auto')
    assert mode == 'eager'


@pytest.mark.heavy
def test_chunked_executor_decision_force():
    """force mode always selects heavy regardless of footprint."""
    fp = estimate_footprint(N_ATOMS, N_STRUCTURES)
    mode = decide_mode(fp, heavy_mode='force')
    assert mode == 'heavy'
