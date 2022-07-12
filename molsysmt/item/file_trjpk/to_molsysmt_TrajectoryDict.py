from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
from molsysmt._private.variables import is_all
from molsysmt import puw

def to_molsysmt_TrajectoryDict(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:trjpk')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    import pickle

    tmp_item={}

    fff = open(item, 'rb')
    _ = pickle.load(fff)
    _ = pickle.load(fff)
    coordinates = pickle.load(fff)
    box = pickle.load(fff)
    time = pickle.load(fff)
    step = pickle.load(fff)
    fff.close()

    if coordinates is not None:
        if not is_all(structure_indices):
            coordinates = coordinates[structure_indices, :, :]
        if not is_all(atom_indices):
            coordinates = coordinates[:, atom_indices, :]
        coordinates = puw.quantity(coordinates, unit='nm')

    if box is not None:
        if not is_all(structure_indices):
            box = box[structure_indices, :, :]
        box = puw.quantity(box, unit='nm')

    if time is not None:
        if not is_all(structure_indices):
            time = time[structure_indices]
        time = puw.quantity(time, unit='ps')

    if step is not None:
        if not is_all(structure_indices):
            step = step[structure_indices, :, :]

    tmp_item['coordinates'] = coordinates
    tmp_item['box'] = box
    tmp_item['time'] = time
    tmp_item['step'] = step

    return tmp_item

