from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

