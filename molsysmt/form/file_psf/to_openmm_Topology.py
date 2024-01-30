from molsysmt._private.digestion import digest

@digest(form='file:psf')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile
    from ..openmm_CharmmPsfFile import to_openmm_Topology as openmm_CharmmPsfFile_to_openmm_Topology

    tmp_item = to_openmm_CharmmPsfFile(item, skip_digestion=True)
    tmp_item = openmm_CharmmPsfFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

