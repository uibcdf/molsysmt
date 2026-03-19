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

    Backed by a NumPy memmap file. By default a temporary file is created
    automatically and deleted on cleanup(). Pass *path* to use a specific
    file instead (the file is NOT deleted on cleanup in that case, giving
    the caller full control over its lifecycle).

    Parameters
    ----------
    shape : tuple
        Shape of the result array.
    dtype : dtype-like
        NumPy dtype (default float64).
    path : str or Path or None
        If None (default), a temporary file is created automatically.
        If provided, the memmap is written to that path. Parent directories
        are created if they do not exist. The file is not deleted on cleanup().
    """

    def __init__(self, shape: tuple, dtype=np.float64, path=None):
        self.shape = shape
        self.dtype = np.dtype(dtype)
        self._owns_file = path is None  # only delete on cleanup if we created it

        if path is None:
            tmp = tempfile.NamedTemporaryFile(suffix='.npy', delete=False)
            self._path = Path(tmp.name)
            tmp.close()
        else:
            self._path = Path(path)
            self._path.parent.mkdir(parents=True, exist_ok=True)

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
        """
        Release the memmap and, if MolSysMT created the backing file (i.e.
        no *path* was passed to __init__), delete it from disk.
        User-specified files are left intact.
        """
        del self._array
        if self._owns_file:
            self._path.unlink(missing_ok=True)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()

    def __repr__(self):
        return f"PersistentResultHandle(shape={self.shape}, dtype={self.dtype}, path={self._path})"
