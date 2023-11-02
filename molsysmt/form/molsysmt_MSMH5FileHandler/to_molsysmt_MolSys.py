from molsysmt._private.digestion import digest

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.native import MolSys

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

