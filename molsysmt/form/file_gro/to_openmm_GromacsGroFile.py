from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:gro')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

