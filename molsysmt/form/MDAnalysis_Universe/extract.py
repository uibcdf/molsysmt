from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="MDAnalysis.Universe")
@dep_digest("MDAnalysis")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting an independent MDAnalysis Universe with selected stored data.


    Parameters
    ----------
    item : molecular system
        Source Universe with declared topology and optional structures.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Whether an unrestricted extraction creates an independent Universe.
        If False, the unrestricted operation returns the original object.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    MDAnalysis.Universe
        Selected atoms and structures in their requested order, with stored atom
        labels, formal charges and retained connectivity metadata preserved.

    Raises
    ------
    NotCompatibleConversionError
        If selected times are irregular or structure indices are supplied for
        a Universe without a trajectory.

    Notes
    -----
    Stored bond orders, opaque type labels and guessed flags are copied without
    chemical interpretation. Available coordinates, velocities, forces, cells
    and uniform time axes retain the provider's units. The source arrays and
    current structure are unchanged. A new in-memory reader cannot represent an
    irregular selected time axis; convert to molsysmt.MolSys to retain it.
    Explicit empty atom or structure selections remain unsupported by this
    in-memory subset adapter. Copying a complete topology-only Universe does not
    create structures. Arbitrary application attributes attached to a Universe
    are outside the provider's copy contract.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices) and not copy_if_all:
        return item

    from ._subset import subset_universe

    return subset_universe(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
    )
