from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', structure_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile
    from ..mdtraj_PDBTrajectoryFile import extract as extract_mdtraj_PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)
    tmp_item = extract_mdtraj_PDBTrajectoryFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

