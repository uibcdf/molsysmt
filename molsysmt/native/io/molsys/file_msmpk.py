
def from_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_MolSys_to_molsysmt_MolSys
    from molsysmt import puw
    import pickle

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


