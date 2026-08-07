from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
@dep_digest('pytraj')
def to_pytraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from pytraj import load

    from ..pytraj_Trajectory.extract import extract as extract_pytraj_Trajectory

    tmp_item = load(item)
    tmp_item = extract_pytraj_Trajectory(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item

