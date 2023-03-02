from molsysmt._private.digestion import digest

@digest(form='file:xtc')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_XTCTrajectoryFile
    from ..mdtraj_XTCTrajectoryFile import to_molsysmt_Structures as mdtraj_XTCTrajectoryFile_to_molsysmt_Structures

    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
    tmp_item = mdtraj_XTCTrajectoryFile_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

