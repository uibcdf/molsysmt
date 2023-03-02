from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_pytraj_Topology as molsysmt_MolSys_to_pytraj_Topology

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices)
    tmp_item = molsysmt_MolSys_to_pytraj_Topology(tmp_item)

    return tmp_item

def _to_pytraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_pytraj_Topology(item, atom_indices=atom_indices)


