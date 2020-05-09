def from_prmtop(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt import convert
    tmp_item = convert(item, to_form='openmm.Topology')
    tmp_item = convert(tmp_item, to_form='molsysmt.DataFrame')

    return tmp_item

