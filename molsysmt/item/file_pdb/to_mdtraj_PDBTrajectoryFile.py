from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_mdtraj_PDBTrajectoryFile(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from mdtraj.formats.pdb import PDBTrajectoryFile
    from ..mdtraj_PDBTrajectoryFile import extract as extract_mdtraj_PDBTrajectoryFile

    tmp_item = PDBTrajectoryFile(item)
    tmp_item = extract_mdtraj_PDBTrajectoryFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, check=False)

    return tmp_item

