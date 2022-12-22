from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all', digest=True):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_pytraj_Topology as molsysmt_MolSys_to_pytraj_Topology

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, digest=False)
    tmp_item = molsysmt_MolSys_to_pytraj_Topology(tmp_item, digest=False)

    return tmp_item

