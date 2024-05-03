from molsysmt._private.digestion import *

@digest(form='molsysmt.MolSys')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_string_pdb_text

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    with open(output_filename, "w") as fff:
        fff.write(tmp_item)

    return output_filename

