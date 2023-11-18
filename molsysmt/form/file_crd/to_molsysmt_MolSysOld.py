from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys_old import MolSysOld
    from .to_molsysmt_TopologyOld import to_molsysmt_TopologyOld
    from .to_molsysmt_StructuresOld import to_molsysmt_StructuresOld

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.structures = to_molsysmt_StructuresOld(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

