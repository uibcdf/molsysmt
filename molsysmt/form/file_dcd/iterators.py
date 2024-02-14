from molsysmt._private.exceptions import NotImplementedIteratorError
from ..mdtraj_DCDTrajectoryFile.iterators import StructuresIterator as StructuresIterator_DCDTrajectoryFile
from .to_mdtraj_DCDTrajectoryFile import to_mdtraj_DCDTrajectoryFile
from molsysmt._private.digestion import digest

class StructuresIterator(StructuresIterator_DCDTrajectoryFile):

    @digest(form='file:dcd')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1, structure_indices=None,
            output_type='values', skip_digestion=False, **kwargs):

        molecular_system = to_mdtraj_DCDTrajectoryFile(molecular_system)

        super().__init__(molecular_system, atom_indices=atom_indices, start=start, step=step, stop=stop,
                chunk=chunk, structure_indices=structure_indices, output_type=output_type, skip_digestion=True, **kwargs)

