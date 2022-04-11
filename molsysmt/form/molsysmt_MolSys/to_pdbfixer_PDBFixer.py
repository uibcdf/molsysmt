from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

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

