from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_structure_indices

def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', check=True):

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

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from molsysmt.tools.string_pdb_text import extract as extract_string_pdb_text

    tmp_item = extract_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure=indices, check=False)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = PDBFile(tmp_item)

    return tmp_item

