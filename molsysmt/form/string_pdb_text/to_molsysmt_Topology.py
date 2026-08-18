from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):
    """
    Converting from string:pdb_text to molsysmt.Topology.

    Parameters
    ----------
    item : string:pdb_text
        Source item in string:pdb_text form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
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

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_PDBFileHandler_to_molsysmt_Topology

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                            get_missing_bonds=get_missing_bonds,
                                                            skip_digestion=True)

    return tmp_item
