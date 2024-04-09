from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_molsysmt_Topology(item, atom_indices='all', get_missing_bonds=True, skip_digestion=False):

    from . import to_molsysmt_PDBFileHandler
    from ..molsysmt_PDBFileHandler import to_molsysmt_Topology as molsysmt_PDBFileHandler_to_molsysmt_Topology

    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_PDBFileHandler_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                            get_missing_bonds=get_missing_bonds,
                                                            skip_digestion=True)

    return tmp_item

