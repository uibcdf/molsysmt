from .is_molsysmt_MolSys import is_molsysmt_MolSys
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import LibraryNotFound
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    try:
        from pdbfixer.pdbfixer import PDBFixer
    except:
        raise LibraryNotFound('pdbfixer')

    from . import to_string_pdb_text
    from io import StringIO

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

