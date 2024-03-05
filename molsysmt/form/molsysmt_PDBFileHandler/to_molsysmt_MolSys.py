from molsysmt._private.digestion import digest

@digest(form='molsysmt.PDBFileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.native import MolSys

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                                 skip_digestion=True)

    return tmp_item

