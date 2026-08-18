from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):
    """
    Creating a copy of an item of form mdtraj.HDF5TrajectoryFile.

    Parameters
    ----------
    item : mdtraj.HDF5TrajectoryFile
        Source item in mdtraj.HDF5TrajectoryFile form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    progress_bar : object
        Argument progress_bar.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.HDF5TrajectoryFile
        Resulting object in mdtraj.HDF5TrajectoryFile form.

    .. versionadded:: 1.0.0
    """

    from .get_structural_attributes import get_n_structures_from_system
    from ..mdtraj_Topology.extract import extract as extract_mdtraj_Topology
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

