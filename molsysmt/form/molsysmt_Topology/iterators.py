from molsysmt._private.exceptions import NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
from molsysmt._private.indices import indices_iterator


class TopologyIterator():

    @digest(form='molsysmt.Topology')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, stop=None, step=1, chunk=1,
            output_type='values', **kwargs):
 
        self.molecular_system = molecular_system
        self.element = element
        self.indices = indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.index = 0

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)
                self._output_dictionary[key] = None

        if self.stop is None:
            if is_all(indices):
                from .get import get_n_atoms_from_system
                self.stop = get_n_atoms_from_system(molecular_system)
            else:
                self.stop = len(indices)

        from molsysmt import get

        self._get_result = get(self.molecular_system, element=self.element, indices=self.indices, output_type='dictionary', **kwargs)

        self._indices_iterator = indices_iterator(start=self.start, stop=self.stop, step=self.step, chunk=self.chunk)


    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            for key in self.arguments:
                self._output_dictionary[key]=self._get_result[key][indices]

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration

