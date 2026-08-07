"""Defining native-backed iterators for MDAnalysis Topology objects."""

from molsysmt._private.argdigest import arg_digest
from molsysmt.form.molsysmt_Topology.iterators import (
    TopologyIterator as NativeTopologyIterator,
)


class TopologyIterator(NativeTopologyIterator):
    """Iterating through the canonical native topology seam."""

    @arg_digest(form='MDAnalysis.Topology')
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
