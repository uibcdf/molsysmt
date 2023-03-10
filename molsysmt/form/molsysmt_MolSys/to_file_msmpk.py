from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
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

    fff = bz2.BZ2File(output_filename, 'wb')
    pickle.dump(tmp_item, fff)
    fff.close()

    tmp_item = output_filename

    return tmp_item

