from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_structure_indices

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.tools.string_pdb_text import extract as extract_string_pdb_text
    from molsysmt._private_tools.files_and_directories import temp_filename

    if output_filename is None:
        output_filename = temp_filename(extension='pdb')

    tmp_item = extract_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False, check=False)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    tmp_item = output_filename

    return tmp_item

