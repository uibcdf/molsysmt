def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys

    if not is_molsysmt_MolSys(item):
        raise ValueError

    tmp_item = item.topology.copy()

    return tmp_item
