from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='mdtraj.HDF5TrajectoryFile')
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):

    from .get import get_n_structures_from_system
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology
    from mdtraj.formats import HDF5TrajectoryFile
    from tqdm import tqdm

    n_structures = get_n_structures_from_system(item)

    item.seek(0)

    tmp_item = HDF5TrajectoryFile(output_filename, 'w', force_overwrite=False, compression='zlib')

    if progress_bar:
        iterator = tqdm(range(n_structures))
    else:
        iterator = range(n_structures)

    for ii in iterator:
        output = item.read(1, atom_indices=mdtraj_atom_indices)
        tmp_item.write(coordinates=output.coordinates, time=output.time,
            cell_lengths=output.cell_lengths, cell_angles=output.cell_angles,
            velocities=output.velocities, kineticEnergy=output.kineticEnergy, potentialEnergy=output.potentialEnergy,
            temperature=output.temperature, alchemicalLambda=output.alchemicalLambda)

    tmp_item.topology = item.topology
 
    return tmp_item

