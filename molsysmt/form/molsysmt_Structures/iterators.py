from molsysmt._private.exceptions import NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
from molsysmt._private.indices import indices_iterator
import numpy as np

class StructuresIterator():

    @digest(form='molsysmt.Structures')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type = 'values', skip_digestion=False, **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.structure_index = None

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)
                self._output_dictionary[key] = None

        if self.stop is None:
            if structure_indices is None:
                from .get import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system)
            else:
                self.stop = len(structure_indices)

        self._indices_iterator = indices_iterator(indices=structure_indices, start=self.start,
                stop=self.stop, step=self.step, chunk=self.chunk)


    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            for argument in self.arguments:

                if argument == 'coordinates':
                    coordinates = self.molecular_system.coordinates[indices,:,:]
                    if isinstance(indices, int):
                        coordinates = coordinates[np.newaxis,:,:]
                    if not is_all(self.atom_indices):
                        coordinates = coordinates[:, self.atom_indices, :]
                    self._output_dictionary['coordinates'] = coordinates
                    del(coordinates)
                elif argument == 'time':
                    self._output_dictionary['time'] = self.time[indices]
                elif argument == 'id':
                    self._output_dictionary['id'] = indices
                elif argument == 'box':
                    self._output_dictionary['box'] = self.box[indices,:,:]

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration

