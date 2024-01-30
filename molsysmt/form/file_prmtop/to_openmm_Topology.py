from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):

    from . import to_openmm_AmberPrmtopFile
    from ..openmm_AmberPrmtopFile import to_openmm_Topology as openmm_AmberPrmtopFile_to_openmm_Topology

    tmp_item = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    tmp_item = openmm_AmberPrmtopFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

