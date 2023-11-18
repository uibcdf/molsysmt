from molsysmt._private.digestion import digest

@digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
    from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld
    from molsysmt.native import MolSysOld

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices)
    tmp_item.structures = to_molsysmt_StructuresOld(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

