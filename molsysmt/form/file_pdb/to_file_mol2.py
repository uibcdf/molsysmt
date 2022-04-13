from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'pdbfixer.PDBFixer')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_parmed_Structure
    from ..parmed_Structure import to_file_mol2 as parmed_structure_to_file_mol2

    tmp_item = to_parmed_Structure(item, check=False)
    tmp_item = parmed_Structure_to_file_mol2(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

