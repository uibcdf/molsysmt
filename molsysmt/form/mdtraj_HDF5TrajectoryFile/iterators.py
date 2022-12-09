from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from copy import copy

class StructuresIterator():

    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1,
            structure_indices=None, **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.position = 0

        if self.stop is None:
            from .get import get_n_structures_from_system
            self.stop = get_n_structures_from_system(molecular_system)

        self.step=0

    def __iter__(self):
        print('entra iter')
        return self

    def __next__(self):
        print('entra next')
        if self.position <= self.stop:
            output = copy(self.step)
            self.position += 1
            return output
        else:
            raise StopIteration

class TopologyIterator():

    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteration


