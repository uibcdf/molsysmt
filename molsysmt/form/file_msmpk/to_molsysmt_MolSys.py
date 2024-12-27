from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..molsysmt_MolSys import extract as extract_molsysmt_MolSys
    from molsysmt import pyunitwizard as puw
    import pickle
    import bz2

    fff = bz2.BZ2File(item,'rb')
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

    if tmp_item.structures.temperature is not None:
        value = tmp_item.structures.temperature
        quantity = puw.quantity(value, 'kelvin')
        tmp_item.structures.temperature = puw.standardize(quantity)

    if tmp_item.structures.potential_energy is not None:
        value = tmp_item.structures.potential_energy
        quantity = puw.quantity(value, 'kJ/mol')
        tmp_item.structures.potential_energy = puw.standardize(quantity)

    if tmp_item.structures.kinetic_energy is not None:
        value = tmp_item.structures.kinetic_energy
        quantity = puw.quantity(value, 'kJ/mol')
        tmp_item.structures.kinetic_energy = puw.standardize(quantity)

    tmp_item = extract_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

