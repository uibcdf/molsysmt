from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    try:
        from pdbfixer.pdbfixer import PDBFixer
    except:
        raise LibraryNotFoundError('pdbfixer')

    from . import to_string_pdb_text
    from io import StringIO

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

