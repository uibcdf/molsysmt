
def from_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molmodmt.native.molmod import MolMod
    #from molmodmt.native.io.card import from_mmtf_mdtraj_Trajectory as to_card
    from molmodmt.native.io.composition import from_mdtraj_Topology as to_composition
    from molmodmt.native.io.trajectory import from_mdtraj_Trajectory as to_trajectory

    tmp_item = MolMod()
    tmp_item.composition = to_composition(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = to_trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.card = None
    tmp_item.topography = None
    return tmp_item




