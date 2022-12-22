from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', digest=True):

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item, digest=False)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, digest=False)

    return tmp_item

