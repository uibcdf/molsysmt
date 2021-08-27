import pickle

def from_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_MolSys_to_molsysmt_MolSys
    from molsysmt import puw

    fff = open(item,'rb')
    tmp_item = pickle.load(fff)
    fff.close()

    # lengths with nm values and time in ps

    if tmp_item.trajectory.coordinates is not None:
        value = tmp_item.trajectory.coordinates
        quantity = puw.quantity(value, 'nm')
        tmp_item.trajectory.coordinates = puw.standardize(quantity)

    if tmp_item.trajectory.box is not None:
        value = tmp_item.trajectory.box
        quantity = puw.quantity(value, 'nm')
        tmp_item.trajectory.box = puw.standardize(quantity)

    if tmp_item.trajectory.time is not None:
        value = tmp_item.trajectory.time
        quantity = puw.quantity(value, 'ps')
        tmp_item.trajectory.time = puw.standardize(quantity)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_molsysmt_MolSys(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices,
            frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system


def to_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_MolSys_to_molsysmt_MolSys
    from molsysmt import puw

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices,
            frame_indices=frame_indices, copy_if_all=False)

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

    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

