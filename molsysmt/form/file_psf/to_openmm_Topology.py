from molsysmt._private.digestion import digest

@digest(form='file:psf')
def to_openmm_Topology(item, atom_indices='all'):

    from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile
    from ..openmm_CharmmPsfFile import to_openmm_Topology as openmm_CharmmPsfFile_to_openmm_Topology

    tmp_item = to_openmm_CharmmPsfFile(item)
    tmp_item = openmm_CharmmPsfFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

