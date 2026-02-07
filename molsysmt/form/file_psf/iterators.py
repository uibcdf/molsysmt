from molsysmt._private.smonitor import NotImplementedIteratorError
from molsysmt._private.arg_digestion import arg_digest

class TopologyIterator():

    @arg_digest(form='file:psf')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, step=1, stop=None, chunk=1,
            output_type='values', skip_digestion=False, **kwargs):

        raise NotImplementedIteratorError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


