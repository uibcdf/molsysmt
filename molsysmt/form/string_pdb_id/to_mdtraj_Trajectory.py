from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, digest=False)
    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item, digest=False)

    return tmp_item

