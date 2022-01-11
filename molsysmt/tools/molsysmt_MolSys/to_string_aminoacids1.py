def to_string_aminoacids1(item, atom_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys, to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    if not is_molsysmt_MolSys(item):
        raise ValueError

    tmp_item = to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_string_aminoacids1(tmp_item, atom_indices=atom_indices)

    return tmp_item

