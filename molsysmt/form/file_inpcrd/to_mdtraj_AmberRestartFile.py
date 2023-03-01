from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_mdtraj_AmberRestartFile(item, atom_indices='all', structure_indices='all'):

    try:
        from mdtraj.formats import AmberRestartFile
    except:
        raise LibraryNotFoundError('MDTraj')

    tmp_item = AmberRestartFile(item)

    return tmp_item

def _to_mdtraj_AmberRestartFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_AmberRestartFile(item, atom_indices=atom_indices, structure_indices=structure_indices)
