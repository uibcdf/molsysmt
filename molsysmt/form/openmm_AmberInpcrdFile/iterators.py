from molsysmt._private.exceptions import NotImplementedIteratorError

class StructuresIterator():

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1, structure_indices=None):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError
