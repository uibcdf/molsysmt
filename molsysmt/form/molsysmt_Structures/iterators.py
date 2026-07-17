from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.indices import indices_iterator


_ATOM_STRUCTURAL_ATTRIBUTES = {
    'alternate_location',
    'b_factor',
    'coordinates',
    'occupancy',
    'velocities',
}

class StructuresIterator():

    @arg_digest(form='molsysmt.Structures')
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
                from .get_structural_attributes import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system, skip_digestion=True)
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
                from . import get_structural_attributes as getters

                if argument in _ATOM_STRUCTURAL_ATTRIBUTES:
                    getter = getattr(getters, f'get_{argument}_from_atom')
                    output = getter(
                        self.molecular_system,
                        indices=self.atom_indices,
                        structure_indices=indices,
                        skip_digestion=True,
                    )
                else:
                    getter = getattr(getters, f'get_{argument}_from_system')
                    output = getter(
                        self.molecular_system,
                        structure_indices=indices,
                        skip_digestion=True,
                    )
                self._output_dictionary[argument] = output

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration
