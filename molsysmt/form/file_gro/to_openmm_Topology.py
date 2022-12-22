from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_Topology(item, atom_indices='all', digest=True):

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    tmp_item = to_openmm_GromacsGroFile(item, digest=False)
    tmp_item = openmm_GromacsGroFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

