"""Protected structure-aligned numeric blocks with local replacement.

Units belong to the owning Structures field; this storage receives canonical
raw float64 values. Its internal byte budget is not a public tuning contract.
"""

import numpy as np

from molsysmt._private.variables import is_all

_BLOCK_BYTES = 1024 * 1024


def _freeze(array):
    return np.frombuffer(array.tobytes(), dtype=np.float64).reshape(array.shape)


def _axis(indices, size):
    if is_all(indices):
        return None
    values = np.asarray(indices)
    if values.size == 0:
        values = np.asarray(indices, dtype=np.int64)
    if values.ndim == 0:
        values = values.reshape(1)
    if values.ndim != 1 or values.dtype.kind not in "iu":
        raise ValueError("Selections must contain one-dimensional integer indices")
    if np.any(values < 0) or np.any(values >= size):
        raise IndexError("Selection contains an out-of-range index")
    return values.astype(np.int64, copy=False)


class _StructureArray:
    """Own independently reclaimable blocks of (structures, items, xyz)."""

    def __init__(self, values, *, block_bytes=None):
        values = np.asarray(values, dtype=np.float64)
        if values.ndim != 3 or values.shape[-1] != 3:
            raise ValueError(
                "Expected numeric storage with shape (structures, items, 3)"
            )
        self.shape = values.shape
        budget = _BLOCK_BYTES if block_bytes is None else block_bytes
        self._block_size = max(1, budget // max(1, values.shape[1] * 3 * 8))
        self._blocks = tuple(
            _freeze(values[start : start + self._block_size])
            for start in range(0, values.shape[0], self._block_size)
        )

    @classmethod
    def _from_reader(cls, shape, read_rows):
        """Capture canonical numeric row chunks without an intermediate full array."""
        if len(shape) != 3 or shape[-1] != 3 or any(size < 0 for size in shape):
            raise ValueError("Expected nonnegative (structures, items, 3) axes")
        result = object.__new__(cls)
        result.shape = tuple(shape)
        result._block_size = max(1, _BLOCK_BYTES // max(1, shape[1] * 3 * 8))
        blocks = []
        for start in range(0, shape[0], result._block_size):
            stop = min(start + result._block_size, shape[0])
            values = np.asarray(read_rows(start, stop), dtype=np.float64)
            if values.shape != (stop - start, *shape[1:]):
                raise ValueError("A numeric reader returned inconsistent row axes")
            blocks.append(_freeze(values))
        result._blocks = tuple(blocks)
        return result

    def _row_blocks(self, maximum):
        """Yield protected contiguous row views bounded by storage and caller limits."""
        for index, block in enumerate(self._blocks):
            for offset in range(0, len(block), maximum):
                rows = block[offset : offset + maximum].view()
                yield index * self._block_size + offset, rows

    @property
    def ndim(self):
        return 3

    @property
    def dtype(self):
        return np.dtype(np.float64)

    def __len__(self):
        return self.shape[0]

    def _fork(self, *, deep=False):
        result = object.__new__(type(self))
        result.shape = self.shape
        result._block_size = self._block_size
        result._blocks = tuple(
            _freeze(block) if deep else block.view() for block in self._blocks
        )
        return result

    def __deepcopy__(self, memo):
        if id(self) not in memo:
            memo[id(self)] = self._fork(deep=True)
        return memo[id(self)]

    def __getstate__(self):
        return self.shape, self._block_size, self._blocks

    def __setstate__(self, state):
        self.shape, self._block_size, blocks = state
        self._blocks = tuple(_freeze(block) for block in blocks)

    def _dense(self, *, owned=False):
        if not self._blocks:
            result = np.empty(self.shape, dtype=np.float64)
        elif len(self._blocks) == 1:
            return self._blocks[0].copy() if owned else self._blocks[0].view()
        else:
            result = np.concatenate(self._blocks, axis=0)
        if not owned:
            result.flags.writeable = False
        return result

    def __array__(self, dtype=None, copy=None):
        if copy is False and (
            len(self._blocks) > 1 or dtype is not None and np.dtype(dtype) != self.dtype
        ):
            raise ValueError("A contiguous array requires materializing these blocks")
        result = self._dense(owned=copy is True)
        return result if dtype is None else np.asarray(result, dtype=dtype)

    def __getitem__(self, key):
        # Arbitrary NumPy indexing is an explicit dense boundary. Native hot
        # queries call _select instead, so they never assemble the trajectory.
        return self._dense()[key]

    def _select(self, structure_indices="all", atom_indices="all"):
        structures = _axis(structure_indices, self.shape[0])
        atoms = _axis(atom_indices, self.shape[1])
        if structures is None and atoms is None:
            return self._dense(owned=True)
        if structures is None:
            structures = np.arange(self.shape[0], dtype=np.int64)
        atom_count = self.shape[1] if atoms is None else len(atoms)
        shape = (len(structures), atom_count, 3)
        if not structures.size or not atom_count:
            return np.empty(shape, dtype=np.float64)
        block_ids = structures // self._block_size

        def selected(block_id, rows):
            local = structures[rows] % self._block_size
            block = self._blocks[block_id]
            if atoms is None:
                return block[local]
            return block[local[:, None], atoms[None, :]]

        if np.all(block_ids == block_ids[0]):
            return selected(int(block_ids[0]), slice(None))
        output = np.empty(shape, dtype=np.float64)
        order = np.argsort(block_ids, kind="stable")
        cuts = np.r_[0, np.flatnonzero(np.diff(block_ids[order])) + 1, len(order)]
        for first, last in zip(cuts[:-1], cuts[1:]):
            rows = order[first:last]
            output[rows] = selected(int(block_ids[rows[0]]), rows)
        return output

    def _replace(self, values, structure_indices="all", atom_indices="all"):
        structures = _axis(structure_indices, self.shape[0])
        atoms = _axis(atom_indices, self.shape[1])
        if structures is None:
            structures = np.arange(self.shape[0], dtype=np.int64)
        atom_count = self.shape[1] if atoms is None else len(atoms)
        if not structures.size or not atom_count:
            return self
        values = np.asarray(values, dtype=np.float64)
        if values.shape != (len(structures), atom_count, 3):
            raise ValueError(
                "Replacement shape must match the selected structure and atom axes"
            )
        # Deduplicate by last assignment explicitly; NumPy's advanced-index
        # duplicate write order must not determine scientific values.
        structures, last = np.unique(structures[::-1], return_index=True)
        values = values[len(values) - 1 - last]
        if atoms is not None:
            atom_size = len(atoms)
            atoms, last = np.unique(atoms[::-1], return_index=True)
            values = values[:, atom_size - 1 - last]
        block_ids = structures // self._block_size
        cuts = np.r_[0, np.flatnonzero(np.diff(block_ids)) + 1, len(structures)]
        blocks = list(self._blocks)
        for first, last in zip(cuts[:-1], cuts[1:]):
            block_id = int(block_ids[first])
            local = structures[first:last] % self._block_size
            scratch = blocks[block_id].copy()
            if atoms is None:
                scratch[local] = values[first:last]
            else:
                scratch[local[:, None], atoms[None, :]] = values[first:last]
            blocks[block_id] = _freeze(scratch)
            del scratch
        result = object.__new__(type(self))
        result.shape = self.shape
        result._block_size = self._block_size
        result._blocks = tuple(blocks)
        return result
