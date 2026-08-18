from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                         skip_digestion=False):
    """
    Converting from file:gro to molsysmt.Topology.

    Parameters
    ----------
    item : file:gro
        Source item in file:gro form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler
    from molsysmt.form.molsysmt_GROFileHandler.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_GROFileHandler_to_molsysmt_Topology

    tmp_item = to_molsysmt_GROFileHandler(item)
    tmp_item = molsysmt_GROFileHandler_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                            structure_indices=structure_indices,
                                                            get_missing_bonds=get_missing_bonds, skip_digestion=True)

    return tmp_item

