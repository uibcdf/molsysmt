from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item)

    return tmp_item

def _to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


