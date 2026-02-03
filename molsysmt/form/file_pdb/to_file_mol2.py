from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:pdb')
def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_parmed_Structure
    from ..parmed_Structure import to_file_mol2 as parmed_structure_to_file_mol2

    tmp_item = to_parmed_Structure(item, skip_digestion=True)
    tmp_item = parmed_Structure_to_file_mol2(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, skip_digestion=True)

    return tmp_item

