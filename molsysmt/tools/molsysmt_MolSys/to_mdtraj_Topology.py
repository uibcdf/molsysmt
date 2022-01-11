def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.exceptions import ItemWithWrongForm
    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    if not is_molsysmt_MolSys(item):
        raise ItemWithWrongForm('molsysmt.MolSys')

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

