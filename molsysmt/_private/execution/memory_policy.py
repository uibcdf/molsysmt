"""
Pre-flight memory footprint estimation and eager/heavy decision policy.
"""
from __future__ import annotations

import shutil
import tempfile


_SAFETY_MARGIN = 1.20   # 20% overhead
_FLOAT64_BYTES = 8
_COORDS_DIMS = 3


def estimate_footprint(n_atoms: int, n_structures: int, dtype_bytes: int = _FLOAT64_BYTES) -> int:
    """
    Estimate the memory footprint for loading a trajectory eagerly.

    Returns bytes (with 20% safety margin).
    """
    raw = n_atoms * n_structures * _COORDS_DIMS * dtype_bytes
    return int(raw * _SAFETY_MARGIN)


def decide_mode(footprint_bytes: int, heavy_mode: str = 'auto') -> str:
    """
    Return 'eager' or 'heavy' based on footprint and config.

    Parameters
    ----------
    footprint_bytes : int
        Estimated memory requirement in bytes.
    heavy_mode : str
        'auto' | 'force' | 'off'

    Returns
    -------
    str : 'eager' or 'heavy'
    """
    import molsysmt.configure as config

    if heavy_mode == 'force':
        return 'heavy'
    if heavy_mode == 'off':
        return 'eager'
    # auto
    if footprint_bytes <= config.max_ram_usage:
        return 'eager'
    return 'heavy'


def check_disk_budget(predicted_output_bytes: int, safety: float = 0.10) -> None:
    """
    Raise HeavyOutputFailureError if predicted output exceeds available disk space.

    Parameters
    ----------
    predicted_output_bytes : int
        Estimated size of the output in bytes.
    safety : float
        Fraction of disk to keep free (default 10%).
    """
    from molsysmt._private.smonitor import HeavyOutputFailureError

    free = shutil.disk_usage(tempfile.gettempdir()).free
    available = int(free * (1.0 - safety))
    if predicted_output_bytes > available:
        raise HeavyOutputFailureError(
            reason="Predicted output exceeds available disk space",
            predicted_bytes=predicted_output_bytes,
            available_bytes=available,
        )


def optimize_chunk_size(
    n_atoms: int,
    n_structures_selected: int,
    advisory_chunk_size: int,
    max_ram_usage: int,
    chunk_memory_fraction: float = 0.10,
) -> int:
    """
    Optimize the chunk size dynamically based on the estimated footprint.

    If the system has ample memory compared to the frame size, we scale up
    the chunk size to minimize I/O overhead and Python loop steps.
    """
    if chunk_memory_fraction is None or chunk_memory_fraction <= 0.0:
        return advisory_chunk_size

    footprint_per_frame = estimate_footprint(n_atoms, 1)
    if footprint_per_frame <= 0:
        return advisory_chunk_size

    # Budget for a single chunk: a fraction of the maximum RAM budget
    chunk_budget = int(max_ram_usage * chunk_memory_fraction)

    # Calculate the optimal chunk size based on the memory budget
    optimal_chunk_size = chunk_budget // footprint_per_frame

    # We should at least use the advisory chunk_size requested by the user/config,
    # but we can scale it up if optimal_chunk_size is larger.
    new_chunk_size = max(advisory_chunk_size, optimal_chunk_size)

    # Cap at the total number of structures selected to avoid oversized chunks
    new_chunk_size = min(new_chunk_size, n_structures_selected)

    # Ensure chunk_size is at least 1
    new_chunk_size = max(1, new_chunk_size)

    return int(new_chunk_size)

