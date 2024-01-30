from molsysmt._private.digestion import digest

@digest(form='file:psf')
def to_openmm_CharmmPsfFile(item, atom_indices='all', skip_digestion=False):

    from openmm.app import CharmmPsfFile
    from ..openmm_CharmmPsfFile import extract as extract_openmm_CharmmPsfFile

    tmp_item = CharmmPsfFile(item, skip_digestion=True)
    tmp_item = extract_openmm_CharmmPsfFile(tmp_item, atom_indices=atom_indices, copy_if_all=False,
                                            skip_digestion=True)

    return tmp_item

