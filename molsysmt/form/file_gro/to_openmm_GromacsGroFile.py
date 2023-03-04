from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all'):

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices)

    return tmp_item

def _to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all'):

    return to_openmm_GromacsGroFile(item, atom_indices=atom_indices, structure_indices=structure_indices)

