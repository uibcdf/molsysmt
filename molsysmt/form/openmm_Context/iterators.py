from molsysmt._private.exceptions import NotImplementedIteratorError
from ..molsysmt_Structures.iterators import StructuresIterator as StructuresIterator_molsysmt_Structures
from .to_molsysmt_Structures import to_molsysmt_Structures
from molsysmt._private.digestion import digest

class StructuresIterator(StructuresIterator_molsysmt_Structures):

    @digest(form='openmm.Context')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1, structure_indices=None,
            output_type='values', **kwargs):

        molecular_system = to_molsysmt_Structures(molecular_system)

        super().__init__(molecular_system, atom_indices=atom_indices, start=start, step=step, stop=stop,
                chunk=chunk, structure_indices=structure_indices, output_type=output_type, **kwargs)

class TopologyIterator():

    def __init__(self, molecular_system):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteratorError


