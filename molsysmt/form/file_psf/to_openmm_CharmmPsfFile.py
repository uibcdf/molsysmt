from molsysmt._private.digestion import digest

@digest(form='file:psf')
def to_openmm_CharmmPsfFile(item, atom_indices='all'):

    from openmm.app import CharmmPsfFile
    from ..openmm_CharmmPsfFile import extract as extract_openmm_CharmmPsfFile

    tmp_item = CharmmPsfFile(item)
    tmp_item = extract_openmm_CharmmPsfFile(tmp_item, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item

def _to_openmm_CharmmPsfFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_CharmmPsfFile(item, atom_indices=atom_indices)

