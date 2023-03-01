from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_Topology(item, atom_indices='all'):

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    tmp_item = to_openmm_GromacsGroFile(item)
    tmp_item = openmm_GromacsGroFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

