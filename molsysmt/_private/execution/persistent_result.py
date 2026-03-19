"""
Disk-backed result handle for heavy trajectory outputs that exceed RAM.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np


class PersistentResultHandle:
    """
    A disk-backed array-like result for heavy-mode analysis outputs.

    Backed by a NumPy memmap on a temporary file.
    Temporary by default: call cleanup() or use as a context manager.

    Parameters
    ----------
    shape : tuple
        Shape of the result array.
    dtype : dtype-like
        NumPy dtype (default float64).
    """

    def __init__(self, shape: tuple, dtype=np.float64):
        self.shape = shape
        self.dtype = np.dtype(dtype)

        self._temp = tempfile.NamedTemporaryFile(suffix='.npy', delete=False)
        self._path = Path(self._temp.name)
        self._temp.close()

        self._array = np.memmap(self._path, dtype=self.dtype, mode='w+', shape=self.shape)

    # --- array-like interface ---

    def __getitem__(self, key):
        return self._array[key]

    def __setitem__(self, key, value):
        self._array[key] = value

    def __len__(self):
        return self.shape[0]

    @property
    def path(self) -> Path:
        return self._path

    def to_memory(self) -> np.ndarray:
        """Copy the full result into RAM as a regular numpy array."""
        return np.array(self._array)

    def flush(self):
        """Flush memmap writes to disk."""
        self._array.flush()

    # --- lifecycle ---

    def cleanup(self):
        """Delete the backing temporary file."""
        del self._array
        self._path.unlink(missing_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()

    def __repr__(self):
        return f"PersistentResultHandle(shape={self.shape}, dtype={self.dtype}, path={self._path})"
