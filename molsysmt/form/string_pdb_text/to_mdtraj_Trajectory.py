from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    from . import to_file_pdb    
    from ..file_pdb import to_mdtraj_Trajectory as file_pdb_to_mdtraj_Trajectory  

    tmp_item = to_file_pdb(item)
    tmp_item = file_pdb_to_mdtraj_Trajectory(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)

