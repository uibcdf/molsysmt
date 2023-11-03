from molsysmt._private.exceptions import NotImplementedIteratorError
from ..molsysmt_TopologyNEW.iterators import TopologyIterator as TopologyIterator_molsysmt_TopologyNEW
from ..molsysmt_StructuresNEW.iterators import StructuresIterator as StructuresIterator_molsysmt_StructuresNEW
from .to_molsysmt_TopologyNEW import to_molsysmt_TopologyNEW
from .to_molsysmt_StructuresNEW import to_molsysmt_StructuresNEW
from molsysmt._private.digestion import digest

class StructuresIterator(StructuresIterator_molsysmt_StructuresNEW):

    @digest(form='molsysmt.MolSysNEW')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1, structure_indices=None,
            output_type='values', **kwargs):

        molecular_system = to_molsysmt_StructuresNEW(molecular_system)

        super().__init__(molecular_system, atom_indices=atom_indices, start=start, step=step, stop=stop,
                chunk=chunk, structure_indices=structure_indices, output_type=output_type, **kwargs)


class TopologyIterator(TopologyIterator_molsysmt_TopologyNEW):

    @digest(form='molsysmt.MolSysNEW')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, step=1, stop=None, chunk=1,
            output_type='values', **kwargs):

        molecular_system = to_molsysmt_TopologyNEW(molecular_system)

        super().__init__(molecular_system, element=element, indices=indices, start=start, step=step, stop=stop,
                chunk=chunk, output_type=output_type, **kwargs)


