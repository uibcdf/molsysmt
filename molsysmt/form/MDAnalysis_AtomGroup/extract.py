from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="MDAnalysis.AtomGroup")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting an independent MDAnalysis atom group with selected stored data.


    Parameters
    ----------
    item : molecular system
        Source atom group. Atom indices address positions within this group,
        rather than positions in its parent Universe.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Whether an unrestricted extraction creates an independent group.
        If False, the unrestricted operation returns the original object.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.AtomGroup
        Ordered selected atoms backed by an independent Universe containing
        only the selected atoms and requested structures.

    Raises
    ------
    NotCompatibleConversionError
        If selected times are irregular or structure indices are supplied for
        a group whose Universe has no trajectory.

    Notes
    -----
    Retained connectivity preserves stored orders, opaque type labels and
    guessed flags without bond perception. Atom labels and formal charges are
    retained independently. Represented coordinates, velocities, forces, cells
    and uniform time axes preserve their provider units. The original group,
    parent Universe, arrays and current structure remain unchanged. Explicit
    empty atom or structure selections remain unsupported by the in-memory
    subset adapter. Use ``copy`` to retain unselected parent atoms as context.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    indices = item.indices
    if not is_all(atom_indices):
        indices = indices[atom_indices]

    from molsysmt.form.MDAnalysis_Universe._subset import subset_universe

    return subset_universe(
        item.universe,
        atom_indices=indices,
        structure_indices=structure_indices,
    ).atoms
