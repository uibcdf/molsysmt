from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import pyunitwizard as puw

@digest(form='XYZ')
def to_file_trjpk(item, atom_indices='all', structure_indices='all', output_filename=None):

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

    if 'structure_id' in item:
        if item['structure_id'] is not None:
            structure_id = item['structure_id']
            if not is_all(structure_indices):
                structure_id = structure_id[structure_indices]
        else:
            structure_id = None
    else:
        structure_id = None

    pickle.dump(structure_id, fff)
    del(structure_id)

    fff.close()

    tmp_item = output_filename

    return tmp_item


