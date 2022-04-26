from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:gro')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_openmm_Modeller as openmm_GromacsGroFile_to_openmm_Modeller

    tmp_item = to_openmm_GromacsGroFile(item, check=False)
    tmp_item = openmm_GromacsGroFile_to_openmm_Modeller(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

