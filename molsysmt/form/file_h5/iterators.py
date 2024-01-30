from molsysmt._private.exceptions import NotImplementedIteratorError
from ..mdtraj_HDF5TrajectoryFile.iterators import StructuresIterator as StructuresIterator_HDF5TrajectoryFile
from ..mdtraj_HDF5TrajectoryFile.iterators import TopologyIterator as TopologyIterator_HDF5TrajectoryFile
from .to_mdtraj_HDF5TrajectoryFile import to_mdtraj_HDF5TrajectoryFile
from molsysmt._private.digestion import digest

class StructuresIterator(StructuresIterator_HDF5TrajectoryFile):

    @digest(form='file:h5')
    def __init__(self, molecular_system, atom_indices='all', start=0, step=1, stop=None, chunk=1, structure_indices=None,
            output_type='values', skip_digestion=False, **kwargs):

        molecular_system = to_mdtraj_HDF5TrajectoryFile(molecular_system)

        super().__init__(molecular_system, atom_indices=atom_indices, start=start, step=step, stop=stop,
                chunk=chunk, structure_indices=structure_indices, output_type=output_type,
                         skip_digestion=True, **kwargs)

class TopologyIterator(TopologyIterator_HDF5TrajectoryFile):

    @digest(form='file:h5')
    def __init__(self, molecular_system, element='atom', indices='all', start=0, step=1, stop=None, chunk=1,
            output_type='values', skip_digestion=False, **kwargs):

        molecular_system = to_mdtraj_HDF5TrajectoryFile(molecular_system)

        super().__init__(molecular_system, element=element, indices=indices, start=start, step=step, stop=stop,
                chunk=chunk, output_type=output_type, skip_digestion=True, **kwargs)

