"""Validate editing requests without changing read-only angle semantics."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError


def angular_values(value, argument, caller):
    if not puw.is_quantity(value) or not puw.are_compatible(value, "radians"):
        raise ArgumentError(
            argument, caller=caller, message="An angular quantity is required."
        )
    values = np.asarray(puw.get_value(value, to_unit="radians"))
    if np.iscomplexobj(values) or values.dtype.kind not in "iuf":
        raise ArgumentError(
            argument, caller=caller, message="Edit angles must be real and finite."
        )
    values = np.asarray(values, dtype=np.float64)
    if values.ndim == 0:
        values = values.reshape(1, 1)
    elif values.ndim == 1:
        values = values[None, :]
    if values.ndim != 2 or not values.size or not np.isfinite(values).all():
        raise ArgumentError(
            argument,
            caller=caller,
            message="Edit angles must be a nonempty finite scalar, vector or matrix.",
        )
    return values


def check_angle_shape(values, n_structures, n_quartets, argument, caller):
    if n_structures < 1 or n_quartets < 1:
        raise ArgumentLengthError(
            argument=argument,
            expected=(n_structures, n_quartets),
            actual=values.shape,
            caller=caller,
            message="A torsion edit needs at least one selected structure and quartet.",
        )
    if values.shape[0] not in (1, n_structures) or values.shape[1] not in (
        1,
        n_quartets,
    ):
        raise ArgumentLengthError(
            argument=argument,
            expected=(n_structures, n_quartets),
            actual=values.shape,
            caller=caller,
            message="Each angular dimension must match its selected axis or have size one.",
        )


def quartet_indices(value, n_atoms, caller):
    quartets = np.asarray(value)
    if quartets.ndim == 1 and quartets.size == 4:
        quartets = quartets.reshape(1, 4)
    if (
        quartets.ndim != 2
        or quartets.shape[1] != 4
        or not len(quartets)
        or quartets.dtype.kind not in "iu"
        or np.any(quartets < 0)
        or np.any(quartets >= n_atoms)
        or np.any(np.diff(np.sort(quartets, axis=1), axis=1) == 0)
    ):
        raise ArgumentError(
            "dihedral_quartets",
            caller=caller,
            message="Provide nonempty quartets of four distinct in-range atom indices.",
        )
    return np.asarray(quartets, dtype=np.int64)


def block_mask(molecular_system, quartets, blocks, n_atoms, structure_indices, caller):
    mask = np.zeros((len(quartets), n_atoms), dtype=np.bool_)
    if blocks is None:
        from molsysmt.chemical_states import get_covalent_blocks

        for index, quartet in enumerate(quartets):
            covalent_blocks = get_covalent_blocks(
                molecular_system,
                remove_bonds=quartet[1:3],
                structure_indices=structure_indices,
            )
            for block in covalent_blocks:
                if quartet[3] in block:
                    mask[index, list(block)] = True
    else:
        if not isinstance(blocks, (list, tuple, np.ndarray)) or not len(blocks):
            raise ArgumentError(
                "blocks",
                caller=caller,
                message="Explicit blocks must be a nonempty collection of atom-index lists.",
            )
        for block in blocks:
            indices = np.asarray(block)
            if (
                indices.ndim != 1
                or not indices.size
                or indices.dtype.kind not in "iu"
                or np.any(indices < 0)
                or np.any(indices >= n_atoms)
            ):
                raise ArgumentError(
                    "blocks",
                    caller=caller,
                    message="Each block must contain in-range integer atom indices.",
                )
            for index, quartet in enumerate(quartets):
                if quartet[3] in indices:
                    mask[index, np.asarray(indices, dtype=np.int64)] = True
    if not np.all(mask[np.arange(len(quartets)), quartets[:, 3]]):
        raise ArgumentError(
            "blocks",
            caller=caller,
            message="Every quartet's fourth atom must belong to a moving block.",
        )
    return mask
