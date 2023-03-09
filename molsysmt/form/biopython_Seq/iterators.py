from molsysmt._private.exceptions import NotImplementedIteratorError

class TopologyIterator():

    @digest(form='biopython.Seq')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, step=1, stop=None, chunk=1,
            output_type='values', **kwargs):
        raise NotImplementedIteratorError

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


