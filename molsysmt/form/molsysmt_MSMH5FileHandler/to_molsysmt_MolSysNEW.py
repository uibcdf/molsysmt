from molsysmt._private.digestion import digest

@digest(form='molsysmt.MSMH5FileHandler')
def to_molsysmt_MolSysNEW(item, atom_indices='all', structure_indices='all'):

    from .to_molsysmt_TopologyNEW import to_molsysmt_TopologyNEW
    from .to_molsysmt_StructuresNEW import to_molsysmt_StructuresNEW
    from molsysmt.native import MolSysNEW

    tmp_item = MolSysNEW()
    tmp_item.topology = to_molsysmt_TopologyNEW(item, atom_indices=atom_indices)
    tmp_item.structures = to_molsysmt_StructuresNEW(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

