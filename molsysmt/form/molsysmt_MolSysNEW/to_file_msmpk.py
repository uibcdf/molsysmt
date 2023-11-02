from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysNEW')
def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import extract
    from molsysmt import pyunitwizard as puw
    import pickle
    import bz2

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=True)

    # lengths with nm values and times in ps

    if tmp_item.structures.coordinates is not None:
        value = puw.get_value(tmp_item.structures.coordinates, to_unit='nm')
        tmp_item.structures.coordinates = value

    if tmp_item.structures.box is not None:
        value = puw.get_value(tmp_item.structures.box, to_unit='nm')
        tmp_item.structures.box = value

    if tmp_item.structures.time is not None:
        value = puw.get_value(tmp_item.structures.time, to_unit='ps')
        tmp_item.structures.time = value

    if tmp_item.structures.temperature is not None:
        value = puw.get_value(tmp_item.structures.temperature, to_unit='kelvin')
        tmp_item.structures.temperature = value

    if tmp_item.structures.potential_energy is not None:
        value = puw.get_value(tmp_item.structures.potential_energy, to_unit='kJ/mol')
        tmp_item.structures.potential_energy = value

    if tmp_item.structures.kinetic_energy is not None:
        value = puw.get_value(tmp_item.structures.kinetic_energy, to_unit='kJ/mol')
        tmp_item.structures.kinetic_energy = value

    fff = bz2.BZ2File(output_filename, 'wb')
    pickle.dump(tmp_item, fff)
    fff.close()

    tmp_item = output_filename

    return tmp_item

