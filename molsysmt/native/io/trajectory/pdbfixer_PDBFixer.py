
def from_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.trajectory import Trajectory
    from molsysmt.api_forms.api_pdbfixer_PDBFixer import get_frame_from_atom

    tmp_item = Trajectory()
    _, _, coordinates, box = get_frame_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item.append_frames(coordinates=coordinates, box=box)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_sytem = None

    return tmp_item, tmp_molecular_system

