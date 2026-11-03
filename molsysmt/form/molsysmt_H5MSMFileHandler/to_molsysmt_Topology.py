from molsysmt._private.argdigest import arg_digest


def _read_strings(dataset):
    """Reading legacy text or numeric datasets as strings."""

    if dataset.dtype.kind in {"O", "S", "U"}:
        return dataset.asstr()[:]
    return dataset[:].astype(str)


@arg_digest(form="molsysmt.H5MSMFileHandler")
def to_molsysmt_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.H5MSMFileHandler to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """
    from ._read_native import read_native

    return read_native(item, atom_indices=atom_indices, skip_digestion=True).topology
