from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import puw

def to_file_trjpk(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:

        digest_item(item, 'XYZ')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    import pickle as pickle

    # lengths with nm values and times in ps

    if is_all(atom_indices):
        if item['coordinates'] is not None:
            n_atoms = item['coordinates'].shape[1]
        else:
            n_atoms = 0
    else:
        n_atoms = atom_indices.shape[0]

    if is_all(structure_indices):
        if item['coordinates'] is not None:
            n_structures = item['coordinates'].shape[0]
        elif tmp_item['box'] is not None:
            n_structures = item['box'].shape[0]
        elif tmp_item['time'] is not None:
            n_structures = item['time'].shape[0]
        else:
            n_structures = 0
    else:
        n_structures = structure_indices.shape[0]

    fff = open(output_filename, 'wb')

    pickle.dump(n_atoms, fff)
    pickle.dump(n_structures, fff)

    if 'coordinates' in item:
        if item['coordinates'] is not None:
            coordinates = item['coordinates']
            if not is_all(structure_indices):
                coordinates = coordinates[structure_indices,:,:]
            elif not is_all(atom_indices):
                coordinates = coordinates[:,atom_indices,:]
            coordinates = puw.get_value(coordinates, to_unit='nm')
        else:
            coordinates = None
    else:
        coordinates = None

    pickle.dump(coordinates, fff)
    del(coordinates)

    if 'box' in item:
        if item['box'] is not None:
            box = item['box']
            if not is_all(structure_indices):
                box = box[structure_indices,:,:]
            box = puw.get_value(box, to_unit='nm')
        else:
            box = None
    else:
        box = None

    pickle.dump(box, fff)
    del(box)

    if 'time' in item:
        if item['time'] is not None:
            time = item['time']
            if not is_all(structure_indices):
                time = time[structure_indices]
            time = puw.get_value(time, to_unit='ps')
        else:
            time = None
    else:
        time = None

    pickle.dump(time, fff)
    del(time)

    if 'step' in item:
        if item['step'] is not None:
            step = item['step']
            if not is_all(structure_indices):
                step = step[structure_indices]
        else:
            step = None
    else:
        step = None

    pickle.dump(step, fff)
    del(step)

    fff.close()

    tmp_item = output_filename

    return tmp_item


