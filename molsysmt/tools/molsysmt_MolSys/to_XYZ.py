def to_XYZ(item, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import get_coordinates_from_atom

    if not is_molsysmt_MolSys(item):
        raise ValueError

    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

