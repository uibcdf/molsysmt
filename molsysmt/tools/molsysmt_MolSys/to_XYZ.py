def to_XYZ(item, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys

    if not is_molsysmt_MolSys(item):
        raise ValueError

    from molsysmt import get

    tmp_item = get(item, target='atom', selection=atom_indices, frame_indices=frame_indices,
                coordinates=True)

    return tmp_item

