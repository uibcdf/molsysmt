"""Defining native-backed iterators for MDAnalysis Universe objects."""

from molsysmt._private.arg_digestion import arg_digest
from molsysmt.form.molsysmt_Structures.iterators import (
    StructuresIterator as NativeStructuresIterator,
)
from molsysmt.form.molsysmt_Topology.iterators import (
    TopologyIterator as NativeTopologyIterator,
)


class StructuresIterator(NativeStructuresIterator):
    """Iterating over Universe structures without changing its active frame."""

    @arg_digest(form='MDAnalysis.Universe')
    def __init__(
        self,
        molecular_system,
        atom_indices='all',
        start=0,
        step=1,
        stop=None,
        chunk=1,
        structure_indices=None,
        output_type='values',
        skip_digestion=False,
        **kwargs,
    ):
        from .to_molsysmt_Structures import to_molsysmt_Structures

        requested_structures = (
            'all' if structure_indices is None else structure_indices
        )
        structures = to_molsysmt_Structures(
            molecular_system,
            atom_indices=atom_indices,
            structure_indices=requested_structures,
            skip_digestion=True,
        )
        super().__init__(
            structures,
            atom_indices='all',
            start=start,
            step=step,
            stop=stop,
            chunk=chunk,
            structure_indices=None,
            output_type=output_type,
            skip_digestion=True,
            **kwargs,
        )


class TopologyIterator(NativeTopologyIterator):
    """Iterating over Universe topology through the canonical native seam."""

    @arg_digest(form='MDAnalysis.Universe')
    def __init__(
        self,
        molecular_system,
        element='atom',
        indices='all',
        start=0,
        step=1,
        stop=None,
        chunk=1,
        output_type='values',
        skip_digestion=False,
        **kwargs,
    ):
        from .to_molsysmt_Topology import to_molsysmt_Topology

        topology = to_molsysmt_Topology(
            molecular_system,
            skip_digestion=True,
        )
        super().__init__(
            topology,
            element=element,
            indices=indices,
            start=start,
            step=step,
            stop=stop,
            chunk=chunk,
            output_type=output_type,
            skip_digestion=True,
            **kwargs,
        )
