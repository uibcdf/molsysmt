from molsysmt._private.exceptions import NotImplementedIteratorError

class TopologyIterator():

    def __init__(self, molecular_system):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


