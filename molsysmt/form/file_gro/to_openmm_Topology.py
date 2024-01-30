from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    tmp_item = to_openmm_GromacsGroFile(item, skip_digestion=True)
    tmp_item = openmm_GromacsGroFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
