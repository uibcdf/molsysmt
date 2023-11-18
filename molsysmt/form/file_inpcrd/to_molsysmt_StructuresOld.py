from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_AmberInpcrdFile
    from ..openmm_AmberInpcrdFile import to_molsysmt_StructuresOld as openmm_AmberInpcrdFile_to_molsysmt_StructuresOld

    tmp_item = to_openmm_AmberInpcrdFile(item)
    tmp_item = openmm_AmberInpcrdFile_to_molsysmt_StructuresOld(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

