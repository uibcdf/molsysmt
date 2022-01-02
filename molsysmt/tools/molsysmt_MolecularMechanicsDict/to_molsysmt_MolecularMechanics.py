def to_molsysmt_MolecularMechanics(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict
    from molsysmt.basic import convert

    if not is_molsysmt_MolecularMechanicsDict(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.MolecularMechanics', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

