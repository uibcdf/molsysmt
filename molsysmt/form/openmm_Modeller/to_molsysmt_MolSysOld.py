from molsysmt._private.digestion import *

@digest(form='openmm.Modeller')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys_old import MolSysOld
    from . import to_molsysmt_TopologyOld
    from . import to_molsysmt_StructuresOld

    tmp_item = MolSysOld()
    tmp_item.topology = to_molsysmt_TopologyOld(item, atom_indices=atom_indices)
    tmp_item.structures  = to_molsysmt_StructuresOld(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

