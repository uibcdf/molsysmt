from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to molsysmt.Topology.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_PDBFileHandler_to_molsysmt_Topology

    handler = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_Topology(handler, atom_indices=atom_indices, skip_digestion=True)
    handler.close()

    return tmp_item
