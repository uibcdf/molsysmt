from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
@dep_digest('mdtraj')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
        progress_bar=False, skip_digestion=False):

    from mdtraj.formats import HDF5TrajectoryFile
    from molsysmt.form.mdtraj_Topology.extract import extract as extract_mdtraj_Topology
    from tqdm import tqdm

    opened_here = False
    if isinstance(item, str):
        item = HDF5TrajectoryFile(item, mode='r')
        opened_here = True

    try:
        mdtraj_atom_indices = atom_indices
        if is_all(atom_indices):
            mdtraj_atom_indices = None

        if is_all(atom_indices) and is_all(structure_indices):

            if output_filename is not None:
                from .get_structural_attributes import get_n_structures_from_system
                n_structures = get_n_structures_from_system(item, skip_digestion=True)

                item.seek(0)
                tmp_item = HDF5TrajectoryFile(output_filename, 'w', force_overwrite=False, compression='zlib')

                iterator = tqdm(range(n_structures)) if progress_bar else range(n_structures)

                for ii in iterator:
                    output = item.read(1, atom_indices=mdtraj_atom_indices)
                    tmp_item.write(coordinates=output.coordinates, time=output.time,
                        cell_lengths=output.cell_lengths, cell_angles=output.cell_angles,
                        velocities=output.velocities, kineticEnergy=output.kineticEnergy, 
                        potentialEnergy=output.potentialEnergy,
                        temperature=output.temperature, alchemicalLambda=output.alchemicalLambda)

                tmp_item.topology = item.topology
                tmp_item.close()
                tmp_item = HDF5TrajectoryFile(output_filename, mode='r')
            else:
                tmp_item = item

        else:
            # Filtering requested
            if output_filename is None:
                # If no output file is specified, we must convert to mdtraj.Trajectory (in-memory)
                from .to_mdtraj_Trajectory import to_mdtraj_Trajectory
                tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, 
                                               structure_indices=structure_indices, skip_digestion=True)
            else:
                from .get_structural_attributes import get_n_structures_from_system
                topology = item.topology
                if not is_all(atom_indices):
                    topology = extract_mdtraj_Topology(topology, atom_indices=atom_indices, skip_digestion=True)

                if is_all(structure_indices):
                    n_structures = get_n_structures_from_system(item, skip_digestion=True)
                    structure_indices = range(n_structures)

                item.seek(0)
                tmp_item = HDF5TrajectoryFile(output_filename, 'w', force_overwrite=False, compression='zlib')

                iterator = tqdm(structure_indices) if progress_bar else structure_indices

                for ii in iterator:
                    item.seek(ii)
                    output = item.read(1, atom_indices=mdtraj_atom_indices)
                    tmp_item.write(coordinates=output.coordinates, time=output.time,
                            cell_lengths=output.cell_lengths, cell_angles=output.cell_angles,
                            velocities=output.velocities, kineticEnergy=output.kineticEnergy, 
                            potentialEnergy=output.potentialEnergy,
                            temperature=output.temperature, alchemicalLambda=output.alchemicalLambda)

                tmp_item.topology = topology
                tmp_item.close()
                tmp_item = HDF5TrajectoryFile(output_filename, mode='r')

    except Exception as e:
        if opened_here:
            item.close()
        raise e

    return tmp_item

