"""Iterating PDBQT structure blocks through the existing form contract."""

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.pdbqt_iterators import PDBQTStructuresIterator


class StructuresIterator(PDBQTStructuresIterator):
    @arg_digest(form="file:pdbqt")
    def __init__(
        self,
        molecular_system,
        atom_indices="all",
        start=0,
        stop=None,
        step=1,
        chunk=1,
        structure_indices=None,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        """Iterating selected PDBQT structures with bounded coordinate blocks.

        Parameters
        ----------
        molecular_system : molecular system
            PDBQT input in this adapter's registered form; parsing validates homogeneous
            model identity.
        atom_indices : int, list, tuple or numpy.ndarray, default='all'
            Source atom positions to retain. Native graph extraction uses the native
            canonical subset order.
        start : int, default=0
            First position in the requested index sequence.
        stop : int or None, default=None
            Exclusive final position in that sequence; None runs to its end.
        step : int, default=1
            Positive stride through the requested index sequence.
        chunk : int, default=1
            Positive number of structures or elements returned per block; the last block may
            be shorter.
        structure_indices : int, list, tuple or numpy.ndarray, default=None
            Source structure positions, independent of MODEL labels. Query/iteration order
            and repetitions are preserved; serialized documents require unique positions.
        output_type : str, default='values'
            Return ordered values or a dictionary keyed by requested attribute names.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated inputs.
        **kwargs : bool
            Attribute switches. Structural iteration supports coordinates, occupancy,
            b_factor, structure_id, structure_index and n_structures.

        Returns
        -------
        None
            Initialize the iterator; coordinate buffers are allocated when a block is requested.

        Notes
        -----
        Coordinates are allocated per requested block; the source text snapshot remains resident. An existing handler is borrowed. Exhaustion, failure, close and context exit release owned handlers only.

        .. versionadded:: 1.0.0
        """
        super().__init__(
            molecular_system,
            atom_indices,
            start,
            stop,
            step,
            chunk,
            structure_indices,
            output_type,
            kwargs,
        )

    @arg_digest()
    def close(self, skip_digestion=False):
        """Closing this iterator without closing a caller-owned handler.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated inputs.

        Returns
        -------
        None
            Release this iterator and any handler it created. A borrowed handler remains open.

        Notes
        -----
        Coordinates are allocated per requested block; the source text snapshot remains resident. An existing handler is borrowed. Exhaustion, failure, close and context exit release owned handlers only.

        .. versionadded:: 1.0.0
        """
        self._close()


class TopologyIterator:
    @arg_digest(form="file:pdbqt")
    def __init__(
        self,
        molecular_system,
        element="atom",
        indices="all",
        start=0,
        stop=None,
        step=1,
        chunk=1,
        output_type="values",
        skip_digestion=False,
        **kwargs,
    ):
        """Delegating declared PDBQT hierarchy iteration to the native topology.

        Parameters
        ----------
        molecular_system : molecular system
            PDBQT input in this adapter's registered form; parsing validates homogeneous
            model identity.
        element : str, default='atom'
            Hierarchical element level for native topology iteration.
        indices : int, list, tuple or numpy.ndarray, default='all'
            Source element positions to query. Structural getters preserve requested atom
            order and repetitions.
        start : int, default=0
            First position in the requested index sequence.
        stop : int or None, default=None
            Exclusive final position in that sequence; None runs to its end.
        step : int, default=1
            Positive stride through the requested index sequence.
        chunk : int, default=1
            Positive number of structures or elements returned per block; the last block may
            be shorter.
        output_type : str, default='values'
            Return ordered values or a dictionary keyed by requested attribute names.
        skip_digestion : bool, default=False
            Whether to skip argument digestion for already validated inputs.
        **kwargs : bool
            Topology attribute switches supported by the native topology iterator, such as
            atom_name=True.

        Returns
        -------
        None
            Initialize an iterator over a detached reference topology.

        Notes
        -----
        Only the atom-scale reference topology is copied. No ensemble coordinate array is materialized. A temporary handler is closed after that copy; a caller-owned handler remains open.

        .. versionadded:: 1.0.0
        """
        import numpy as np

        from molsysmt._private.variables import is_all
        from molsysmt.form.molsysmt_Topology.iterators import (
            TopologyIterator as NativeIterator,
        )
        from molsysmt.native import PDBQTFileHandler

        borrowed = isinstance(molecular_system, PDBQTFileHandler)
        handler = molecular_system if borrowed else PDBQTFileHandler(molecular_system)
        try:
            topology = handler._native().topology.copy()
            if is_all(indices):
                indices = np.arange(
                    getattr(
                        topology,
                        "n_" + ("entities" if element == "entity" else element + "s"),
                    )
                )
            self._iterator = NativeIterator(
                topology,
                element=element,
                indices=indices,
                start=start,
                stop=stop,
                step=step,
                chunk=chunk,
                output_type=output_type,
                **kwargs,
            )
        finally:
            if not borrowed:
                handler.close()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._iterator)
