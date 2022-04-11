from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'file:inpcrd')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if output_filename is None:
        raise ValueError('A value different from None is required for the argument "output_filename"')

    from . import extract
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

