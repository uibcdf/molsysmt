from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices
import numpy as np
from molsysmt import puw

def to_file_trjpk(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'XYZ')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    import pickle as pickle

    # lengths with nm values and times in ps

    if atom_indices is 'all':
        if item['coordinates'] is not None:
            n_atoms = item['coordinates'].shape[1]
        else:
            n_atoms = 0
    else:
        n_atoms = atom_indices.shape[0]

    if structure_indices is 'all':
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
            if structure_indices is not 'all':
                coordinates = coordinates[structure_indices,:,:]
            elif atom_indices is not 'all':
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
            if structure_indices is not 'all':
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
            if structure_indices is not 'all':
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
            if structure_indices is not 'all':
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


