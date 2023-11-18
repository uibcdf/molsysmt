from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_molsysmt_StructuresOld as openmm_GromacsGroFile_to_molsysmt_StructuresOld

    tmp_item = to_openmm_GromacsGroFile(item)
    tmp_item = openmm_GromacsGroFile_to_molsysmt_StructuresOld(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

