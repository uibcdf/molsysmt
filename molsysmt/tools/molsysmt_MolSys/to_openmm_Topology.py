def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.exceptions import ItemWithWrongForm
    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.tools.molsysmt_MolSys import get_box_from_system as get_box_from_molsysmt_MolSys
    from molsysmt.tools.openmm_Topology import set_box_to_system as set_box_to_openmm_Topology

    if not is_molsysmt_MolSys(item):
        raise ItemWithWrongForm('molsysmt.MolSys')

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, atom_indices=atom_indices)

    box = get_box_from_molsysmt_MolSys(item, frame_indices=frame_indices)
    set_box_to_openmm_Topology(tmp_item, frame_indices=frame_indices, box=box)

    return tmp_item

