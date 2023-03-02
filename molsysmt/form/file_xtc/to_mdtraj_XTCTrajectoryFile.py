from molsysmt._private.digestion import digest

@digest(form='file:xtc')
def to_mdtraj_XTCTrajectoryFile(item, atom_indices='all', structure_indices='all'):

    from mdtraj.formats import XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile import extract as extract_mdtraj_XTCTrajectoryFile

    tmp_item = XTCTrajectoryFile(item)
    tmp_item = extract_mdtraj_XTCTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False)

    return tmp_item

def _to_mdtraj_XTCTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_XTCTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)

