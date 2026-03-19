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
    import molsysmt.config as config

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
