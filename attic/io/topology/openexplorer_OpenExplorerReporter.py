def from_openexplorer_OpenExplorerReporter(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_molsysmt_Topology import extract
    tmp_item = extract(item.topology, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

