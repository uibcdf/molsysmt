from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='mdtraj.HDF5TrajectoryFile')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
        progress_bar=False, digest=True):

    from .get import get_n_structures_from_system
    from ..mdtraj_Topology import extract as extract_mdtraj_Topology
    from mdtraj.formats import HDF5TrajectoryFile
    from tqdm import tqdm

    mdtraj_atom_indices = atom_indices
    if is_all(atom_indices):
        mdtraj_atom_indices = None

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=None):

            n_structures = get_n_structures_from_system(item, digest=False)

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
 
        else:

            tmp_item = item
    else:

        topology = item.topology

        if not is_all(atom_indices):
            topology = extract_mdtraj_Topology(topology, atom_indices=atom_indices, digest=False)

        if is_all(structure_indices):

            n_structures = get_n_structures_from_system(item, digest=False)
            structure_indices = range(n_structures)

        item.seek(0)

        tmp_item = HDF5TrajectoryFile(output_filename, 'w', force_overwrite=False, compression='zlib')

        if progress_bar:
            iterator = tqdm(structure_indices)
        else:
            iterator = structure_indices

        for ii in iterator:
            item.seek(ii)
            output = item.read(1, atom_indices=mdtraj_atom_indices)
            tmp_item.write(coordinates=output.coordinates, time=output.time,
                    cell_lengths=output.cell_lengths, cell_angles=output.cell_angles,
                    velocities=output.velocities, kineticEnergy=output.kineticEnergy, potentialEnergy=output.potentialEnergy,
                    temperature=output.temperature, alchemicalLambda=output.alchemicalLambda)

        tmp_item.topology = topology
 
    return tmp_item

