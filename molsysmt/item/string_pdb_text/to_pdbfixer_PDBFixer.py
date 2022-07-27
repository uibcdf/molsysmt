from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'string:pdb_text')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = PDBFixer(pdbfile=tmp_item)

    return tmp_item

