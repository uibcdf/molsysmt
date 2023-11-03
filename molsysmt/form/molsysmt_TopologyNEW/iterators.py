from molsysmt._private.exceptions import NotImplementedIteratorError
from molsysmt._private.variables import is_all
from molsysmt._private.digestion import digest
from molsysmt._private.indices import indices_iterator


class TopologyIterator():

    @digest(form='molsysmt.TopologyNEW')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, stop=None, step=1, chunk=1,
            output_type='values', **kwargs):

        raise NotImplementedError

    def __iter__(self):

        raise NotImplementedError

    def __next__(self):

        raise NotImplementedError


