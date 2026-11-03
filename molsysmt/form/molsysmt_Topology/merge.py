from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.Topology")
def merge(items, atom_indices="all", keep_ids=True, skip_digestion=False):
    """
    Merging multiple items into a single item of form molsysmt.Topology.


    Parameters
    ----------
    items : object
        Argument items.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    keep_ids : object, default=True
        Argument keep_ids.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Topology

    selections = ["all"] * len(items) if is_all(atom_indices) else atom_indices
    if len(selections) != len(items):
        raise ArgumentError(
            "atom_indices",
            value=atom_indices,
            caller="molsysmt.form.molsysmt_Topology.merge",
        )
    output = Topology(skip_digestion=True)
    for item, selection in zip(items, selections):
        output.add(item, atom_indices=selection, keep_ids=keep_ids, skip_digestion=True)
    return output
