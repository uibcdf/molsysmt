import numpy as np


def ensure_nonempty_structure_indices(structure_indices, *, caller):
    """Reject empty frame selections for reductions over structures."""

    from molsysmt._private.smonitor import ArgumentError
    from molsysmt._private.variables import is_all

    if not is_all(structure_indices) and np.asarray(structure_indices).size == 0:
        raise ArgumentError(
            "structure_indices",
            value=structure_indices,
            caller=caller,
            message="At least one structure must be selected for this reduction.",
        )


def complementary_structure_indices(molecular_system, structure_indices):

    from molsysmt.basic import get

    n_structures = get(molecular_system, element='system', n_structures=True)

    structure_indices = np.array(structure_indices)
    structure_indices = structure_indices[structure_indices < n_structures]

    mask = np.ones(n_structures, dtype=bool)
    mask[structure_indices] = False
    return list(np.where(mask)[0])
