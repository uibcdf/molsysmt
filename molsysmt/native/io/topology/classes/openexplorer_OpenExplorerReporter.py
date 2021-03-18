def from_openexplorer_OpenExplorerReporter(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import extract
    tmp_item = extract(item.topology, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

