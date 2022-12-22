from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', digest=True):

    from ..molsysmt_MolSys import extract as extract_molsysmt_MolSys
    from molsysmt import pyunitwizard as puw
    import pickle

    fff = open(item,'rb')
    tmp_item = pickle.load(fff)
    fff.close()

    # lengths with nm values and time in ps

    if tmp_item.structures.coordinates is not None:
        value = tmp_item.structures.coordinates
        quantity = puw.quantity(value, 'nm')
        tmp_item.structures.coordinates = puw.standardize(quantity)

    if tmp_item.structures.box is not None:
        value = tmp_item.structures.box
        quantity = puw.quantity(value, 'nm')
        tmp_item.structures.box = puw.standardize(quantity)

    if tmp_item.structures.time is not None:
        value = tmp_item.structures.time
        quantity = puw.quantity(value, 'ps')
        tmp_item.structures.time = puw.standardize(quantity)

    tmp_item = extract_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, digest=False)

    return tmp_item

