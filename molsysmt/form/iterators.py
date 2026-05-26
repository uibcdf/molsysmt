from molsysmt._private.smonitor import NotImplementedIteratorError


class BaseStructuresIterator:
    """
    Abstract base class for all molecular structures iterators.

    Subclasses must implement __next__ to yield structure chunks.
    Provides context manager methods (__enter__ and __exit__) out of the box.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close any open file handles or resources."""
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError()


class BaseTopologyIterator:
    """
    Abstract base class for all topology iterators.
    """

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedError()


class StructuresIterator(BaseStructuresIterator):

    def __init__(self, molecular_system, atom_indices='all', start=0, interval=1, stop=None, chunk=1, structure_indices=None):
        pass

    def __next__(self):
        raise NotImplementedIteratorError


class TopologyIterator(BaseTopologyIterator):

    def __init__(self, molecular_system):
        pass

    def __next__(self):
        raise NotImplementedIteratorError



