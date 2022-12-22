from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    try:
        from pytraj import load
    except:
        raise LibraryNotFoundError('pytraj')

    from ..pytraj_Trajectory import extract as extract_pytraj_Trajectory

    tmp_item = load(item)
    tmp_item = extract_pytraj_Trajectory(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)

    return tmp_item

