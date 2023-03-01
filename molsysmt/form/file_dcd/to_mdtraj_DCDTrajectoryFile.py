from molsysmt._private.digestion import digest

@digest(form='file:dcd')
def to_mdtraj_DCDTrajectoryFile(item, atom_indices='all', structure_indices='all'):

    from mdtraj.formats import DCDTrajectoryFile
    from ..mdtraj_DCDTrajectoryFile import extract as extract_mdtraj_DCDTrajectoryFile

    tmp_item = DCDTrajectoryFile(item)
    tmp_item = extract_mdtraj_DCDTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False)

    return tmp_item

def _to_mdtraj_DCDTrajectoryFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_DCDTrajectoryFile(item, atom_indices=atom_indices, structure_indices=structure_indices)

