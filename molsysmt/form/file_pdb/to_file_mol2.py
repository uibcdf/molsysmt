from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import to_parmed_Structure
    from ..parmed_Structure import to_file_mol2 as parmed_structure_to_file_mol2

    tmp_item = to_parmed_Structure(item)
    tmp_item = parmed_Structure_to_file_mol2(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename)

    return tmp_item

def _to_file_mol2(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    return to_file_mol2(item, atom_indices=atom_indices,
                        structure_indices=structure_indices, output_filename=output_filename)

