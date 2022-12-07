from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from copy import copy

class StructuresIterator():

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.start = start
        self.interval = interval
        self.stop = stop
        self.chunk = chunk

        self.position = 0

        if self.stop is None:
            from .get import get_n_structures_from_system
            self.stop = get_n_structures_from_system(molecular_system)

        self.step=0

    def __iter__(self):
        return self

    def __next__(self):
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


