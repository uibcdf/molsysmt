"""Bound Python result packing independently of the native search workspace."""

import sys

import numpy as np

from molsysmt._private.smonitor import MemoryBudgetExceededError

_POINTER_BYTES = np.dtype(object).itemsize
_VIEW_BYTES = sys.getsizeof(np.empty(0, dtype=np.float64))
_PY_INT_BYTES = sys.getsizeof(int(np.iinfo(np.int64).max))
_PAIR_BYTES = sys.getsizeof([0, 0]) + 2 * _PY_INT_BYTES + 2 * _POINTER_BYTES
_INDEX_BYTES = _PY_INT_BYTES + 2 * _POINTER_BYTES
_BLOCK_ENTRIES = 16384


def require_output_budget(predicted, budget, caller):
    """Reject a known representation cost before constructing Python payloads."""
    if predicted > budget:
        raise MemoryBudgetExceededError(
            reason="Estimated Python compatibility output exceeds the numerical budget. "
            "Use smaller structure/atom blocks; eligible get_neighbors CSR output "
            "avoids per-row object arrays and boxed pair lists.",
            predicted_bytes=int(predicted),
            available_bytes=int(budget),
            caller=caller,
        )


def neighbor_object_bytes(n_rows):
    """Allow for two view headers/slots per row and fixed container overhead."""
    return 4096 + int(n_rows) * (2 * _VIEW_BYTES + 2 * _POINTER_BYTES)


def neighbor_object_arrays(offsets, indices, distances, units, shape, budget, caller):
    """Keep CSR payloads alive through row views and the public unit constructor."""
    from molsysmt import pyunitwizard as puw

    require_output_budget(
        neighbor_object_bytes(shape[0] * shape[1])
        + offsets.nbytes
        + indices.nbytes
        + distances.nbytes,
        budget,
        caller,
    )
    neighbors = np.empty(shape, dtype=object)
    values = np.empty(shape, dtype=object)
    for structure in range(shape[0]):
        for atom in range(shape[1]):
            row = structure * shape[1] + atom
            neighbors[structure, atom] = indices[offsets[row] : offsets[row + 1]]
            values[structure, atom] = distances[offsets[row] : offsets[row + 1]]
    return neighbors, puw.quantity(values, units, form=puw.get_form(units))


def _contact_blocks(matrix, *, paired, strict_upper):
    """Yield row-major positions using bounded slabs, including non-C layouts."""
    if paired:
        flat = matrix.reshape(-1) if matrix.flags.c_contiguous else matrix.flat
        for start in range(0, matrix.size, _BLOCK_ENTRIES):
            positions = np.flatnonzero(flat[start : start + _BLOCK_ENTRIES])
            positions += start
            yield positions
        return
    if matrix.shape[1] == 0:
        return
    rows_per_block = max(1, _BLOCK_ENTRIES // matrix.shape[1])
    for first_row in range(0, matrix.shape[0], rows_per_block):
        # Multiple column blocks occur only for a single row, preserving order.
        first_column = first_row + 1 if strict_upper else 0
        for column in range(first_column, matrix.shape[1], _BLOCK_ENTRIES):
            rows, columns = np.nonzero(
                matrix[
                    first_row : first_row + rows_per_block,
                    column : column + _BLOCK_ENTRIES,
                ]
            )
            rows += first_row
            columns += column
            if strict_upper:
                selected = rows < columns
                rows, columns = rows[selected], columns[selected]
            yield rows, columns


def contact_pairs(
    contact_map,
    *,
    paired,
    strict_upper,
    atom_indices,
    atom_indices_2,
    output_indices,
    sorted_pairs,
    budget,
    caller,
):
    """Pack the existing contact-list contract without whole-map temporaries."""
    if paired and output_indices not in {"selection", "atom"}:
        return []
    positional = paired and output_indices == "selection"
    # Includes list overallocation and sorting references. These Python payload
    # estimates do not reserve allocator arenas or bound the process's RSS.
    item_bytes = _INDEX_BYTES if positional else _PAIR_BYTES
    containers = 4096 + len(contact_map) * (sys.getsizeof([]) + 2 * _POINTER_BYTES)
    slab_size = min(_BLOCK_ENTRIES, max((m.size for m in contact_map), default=0))
    scratch = 4096 + 80 * slab_size
    label_bytes = (
        np.dtype(np.int64).itemsize
        * (
            len(atom_indices)
            + (len(atom_indices_2) if atom_indices_2 is not None else 0)
        )
        if output_indices == "atom"
        else 0
    )
    fixed_bytes = contact_map.nbytes + containers + scratch + label_bytes
    require_output_budget(fixed_bytes, budget, caller)
    n_items = 0
    for matrix in contact_map:
        if strict_upper and not paired:
            n_items += sum(
                np.count_nonzero(matrix[row, row + 1 :])
                for row in range(min(matrix.shape))
            )
        else:
            n_items += np.count_nonzero(matrix)
        require_output_budget(fixed_bytes + n_items * item_bytes, budget, caller)

    query = (
        np.asarray(atom_indices, dtype=np.int64) if output_indices == "atom" else None
    )
    target = (
        (
            query
            if atom_indices_2 is None
            else np.asarray(atom_indices_2, dtype=np.int64)
        )
        if query is not None
        else None
    )
    output = []
    for matrix in contact_map:
        entries = []
        for block in _contact_blocks(matrix, paired=paired, strict_upper=strict_upper):
            if positional:
                entries.extend(block.tolist())
                continue
            rows, columns = (block, block) if paired else block
            if query is not None:
                rows, columns = query[rows], target[columns]
            packed = np.empty((len(rows), 2), dtype=np.int64)
            packed[:, 0], packed[:, 1] = rows, columns
            entries.extend(packed.tolist())
        if sorted_pairs:
            entries.sort()
        output.append(entries)
    return output
