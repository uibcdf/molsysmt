
def from_openexplorer_Explorer(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_items.api_openexplorer_Explorer import to_molsyst_Trajectory as openexplorer_Explorer_to_molsysmt_Structures

    tmp_item, tmp_molecular_system = openexplorer_Explorer_to_molsysmt_Structures(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

