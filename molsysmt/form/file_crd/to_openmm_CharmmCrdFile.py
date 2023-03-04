from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_openmm_CharmmCrdFile(item, atom_indices='all', structure_indices='all'):

    from openmm.app import CharmmCrdFile
    from ..openmm_CharmmCrdFile import extract as extract_openmm_CharmmCrdFile

    tmp_item = CharmmCrdFile(item)
    tmp_item = extract_openmm_CharmmCrdFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

def _to_openmm_CharmmCrdFile(item, atom_indices='all', structure_indices='all'):

    return to_openmm_CharmmCrdFile(item, atom_indices=atom_indices, structure_indices=structure_indices)

