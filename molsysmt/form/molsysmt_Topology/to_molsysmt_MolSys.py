from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_MolSys(
    item,
    coordinates=None,
    box=None,
    atom_indices="all",
    skip_digestion=False,
):
    """Converting a native topology into a MolSys container.

    Parameters
    ----------
    item : molsysmt.Topology
        Native topology to wrap.
    coordinates : quantity, optional
        Coordinates with shape ``(n_structures, n_atoms, 3)`` and length units.
    box : quantity, optional
        Periodic boxes with shape ``(n_structures, 3, 3)`` and length units.
    atom_indices : array-like or 'all', default 'all'
        Canonical atom indices to retain.
    skip_digestion : bool, default False
        Whether to bypass public argument digestion.

    Returns
    -------
    molsysmt.MolSys
        Container preserving the topology and any explicitly supplied structures.

    Notes
    -----
    Omitting both ``coordinates`` and ``box`` produces a valid topology-only MolSys with
    zero structures.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys, Structures

    from .extract import extract

    output = MolSys(skip_digestion=True)
    output.topology = extract(
        item,
        atom_indices=atom_indices,
        copy_if_all=True,
        skip_digestion=True,
    )

    if coordinates is not None and not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    output.structures = Structures(
        coordinates=coordinates,
        box=box,
        skip_digestion=True,
    )

    return output
