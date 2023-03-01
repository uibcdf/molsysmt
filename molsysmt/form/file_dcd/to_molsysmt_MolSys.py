from molsysmt._private.digestion import digest

@digest(form='file:dcd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
    from ..mdtraj_DCDTrajectoryFile import to_molsysmt_MolSys as mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys

    tmp_item = to_mdtraj_DCDTrajectoryFile(item)
    tmp_item = mdtraj_DCDTrajectoryFile_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)

