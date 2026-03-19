from molsysmt._private.smonitor import NotImplementedIteratorError
from ..mdtraj_XTCTrajectoryFile.iterators import StructuresIterator as StructuresIterator_XTCTrajectoryFile
from .to_mdtraj_XTCTrajectoryFile import to_mdtraj_XTCTrajectoryFile
from molsysmt._private.arg_digestion import arg_digest


class StructuresIterator(StructuresIterator_XTCTrajectoryFile):

    @arg_digest(form='file:xtc')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1,
            structure_indices=None, output_type='values', skip_digestion=False, **kwargs):

        molecular_system = to_mdtraj_XTCTrajectoryFile(molecular_system)

        super().__init__(molecular_system, atom_indices=atom_indices, start=start, step=step,
                stop=stop, chunk=chunk, structure_indices=structure_indices,
                output_type=output_type, skip_digestion=True, **kwargs)
