from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_AmberRestartFile(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:inpcrd')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    try:
        from mdtraj.formats import AmberRestartFile
    except:
        raise LibraryNotFoundError('MDTraj')

    tmp_item = AmberRestartFile(item)

    return tmp_item

