from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError

@digest(form='file:pdb')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    try:
        from mdtraj import load_pdb
    except:
        raise LibraryNotFoundError('mdtraj')

    from ..mdtraj_Trajectory import extract as extract_mdtraj_Trajectory

    tmp_item = load_pdb(item)
    tmp_item = extract_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

def _to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)
