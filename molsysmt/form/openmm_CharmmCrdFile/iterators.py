from molsysmt._private.exceptions import NotImplementedIteratorError
from molsysmt._private.digestion import digest

class StructuresIterator():

    @digest(form='openmm.CharmmCrdFile')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1, structure_indices=None,
            output_type='values', skip_digestion=False):

        raise NotImplementedIteratorError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


class TopologyIterator():

    @digest(form='openmm.CharmmCrdFile')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, step=1, stop=None, chunk=1,
            output_type='values', skip_digestion=False):

        raise NotImplementedIteratorError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


