from molsysmt._private_tools.exceptions import *

def from_mdanalysis_Universe (item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_mdanalysis_Universe as mdanalysis_Universe_to_molsysmt_Topology
    from molsysmt.native.io.trajectory import from_mdanalysis_Universe as mdanalysis_Universe_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = mdanalysis_Universe_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.trajectory, _ = mdanalysis_Universe_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdanalysis_Universe (item, molecular_system=None, atom_indices='all', structure_indices='all'):

    raise NotImplementedError()

