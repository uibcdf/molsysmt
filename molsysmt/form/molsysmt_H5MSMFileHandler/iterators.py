from molsysmt._private.smonitor import NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.indices import indices_iterator
from molsysmt import pyunitwizard as puw
import numpy as np


class StructuresIterator():

    @arg_digest(form='molsysmt.H5MSMFileHandler')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type='values', skip_digestion=False, **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for key, val in kwargs.items():
            if val:
                self.arguments.append(key)
                self._output_dictionary[key] = None

        if self.stop is None:
            if structure_indices is None:
                self.stop = molecular_system.file['structures'].attrs['n_structures_written']
            else:
                self.stop = len(structure_indices)

        self._indices_iterator = indices_iterator(indices=structure_indices, start=self.start,
                stop=self.stop, step=self.step, chunk=self.chunk)

        self._length_unit = molecular_system.file.attrs['length_unit']
        self._time_unit = molecular_system.file.attrs['time_unit']

    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            f = self.molecular_system.file['structures']

            for argument in self.arguments:

                if argument == 'coordinates':
                    if is_all(self.atom_indices):
                        coords = f['coordinates'][indices, :, :].astype('float64')
                    else:
                        # h5py only supports 1D fancy indexing per axis.
                        # Load frames first (1D → valid), then slice atoms in numpy.
                        coords = f['coordinates'][np.atleast_1d(np.array(indices)), :, :].astype('float64')
                        coords = coords[:, self.atom_indices, :]
                    self._output_dictionary['coordinates'] = puw.quantity(
                            coords, self._length_unit, standardized=True)

                elif argument == 'box':
                    if f.attrs['constant_box']:
                        box = f['box'][0, :, :].astype('float64')
                        n = len(np.atleast_1d(indices))
                        box = np.repeat(box[np.newaxis, :, :], n, axis=0)
                    else:
                        box = f['box'][indices, :, :].astype('float64')
                    self._output_dictionary['box'] = puw.quantity(
                            box, self._length_unit, standardized=True)

                elif argument == 'time':
                    if f['time'].shape[0] == 0:
                        self._output_dictionary['time'] = None
                    elif f.attrs['constant_time_step']:
                        init_time = f['time'][0]
                        time_step = f.attrs['time_step']
                        self._output_dictionary['time'] = puw.quantity(
                                init_time + time_step * np.atleast_1d(np.array(indices, dtype='float64')),
                                self._time_unit, standardized=True)
                    else:
                        self._output_dictionary['time'] = puw.quantity(
                                f['time'][indices].astype('float64'),
                                self._time_unit, standardized=True)

                elif argument == 'structure_id':
                    if f['id'].shape[0] == 0:
                        # The dataset exists but stores nothing, as with 'time' above:
                        # reading it would index an empty dimension.
                        self._output_dictionary['structure_id'] = None
                    elif f.attrs['constant_id_step']:
                        init_id = f['id'][0]
                        id_step = f.attrs['id_step']
                        self._output_dictionary['structure_id'] = (
                                init_id + id_step * np.atleast_1d(np.array(indices)))
                    else:
                        self._output_dictionary['structure_id'] = f['id'][indices]

            if self._output_type == 'values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type == 'dictionary':
                output = self._output_dictionary

            return output

        else:

            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # The molecular system is owned by the caller — do not close it here.
        pass


class TopologyIterator():

    def __init__(self, molecular_system):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError
