from molsysmt._private.smonitor import NotImplementedIteratorError


class StructuresIterator:
    """
    StructuresIterator for file:h5msm.

    Opens the file as an H5MSMFileHandler and delegates to its iterator.
    The file is owned by this iterator and closed in __exit__.
    """

    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1,
                 structure_indices=None, output_type='values', skip_digestion=True, **kwargs):

        from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
        from molsysmt.form.molsysmt_H5MSMFileHandler.iterators import StructuresIterator as _Inner

        self._handler = to_molsysmt_H5MSMFileHandler(molecular_system, skip_digestion=True)
        self._inner = _Inner(
            self._handler,
            atom_indices=atom_indices,
            start=start,
            step=step,
            stop=stop,
            chunk=chunk,
            structure_indices=structure_indices,
            output_type=output_type,
            skip_digestion=True,
            **kwargs,
        )

    def __iter__(self):
        return self

    def __next__(self):
        return self._inner.__next__()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._handler is not None:
            self._handler.close()
            self._handler = None


class TopologyIterator:

    def __init__(self, molecular_system):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError
