def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    if output_filename is None:
        raise ValueError('A value different from None is required for the argument "output_filename"')

    from molsysmt.tools.molsysmt_MolSys import extract
    from molsysmt import puw
    import pickle

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=True, check=False)

    # lengths with nm values and times in ps

    if tmp_item.trajectory.coordinates is not None:
        value = puw.get_value(tmp_item.trajectory.coordinates, to_unit='nm')
        tmp_item.trajectory.coordinates = value

    if tmp_item.trajectory.box is not None:
        value = puw.get_value(tmp_item.trajectory.box, to_unit='nm')
        tmp_item.trajectory.box = value

    if tmp_item.trajectory.time is not None:
        value = puw.get_value(tmp_item.trajectory.time, to_unit='ps')
        tmp_item.trajectory.time = value

    fff = open(output_filename,'wb')
    pickle.dump(tmp_item, fff)
    fff.close()

    tmp_item = output_filename

    return tmp_item

