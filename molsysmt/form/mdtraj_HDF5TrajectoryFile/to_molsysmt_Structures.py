from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.HDF5TrajectoryFile to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Structures
    from . import (
        get_box_from_system,
        get_coordinates_from_atom,
        get_kinetic_energy_from_system,
        get_potential_energy_from_system,
        get_temperature_from_system,
        get_time_from_system,
        get_velocities_from_atom,
    )

    tmp_item = Structures()

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    time = get_time_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    velocities = get_velocities_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    temperature = get_temperature_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    potential_energy = get_potential_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    kinetic_energy = get_kinetic_energy_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )

    tmp_item.append(
        time=time,
        box=box,
        coordinates=coordinates,
        velocities=velocities,
        temperature=temperature,
        potential_energy=potential_energy,
        kinetic_energy=kinetic_energy,
        skip_digestion=True,
    )

    return tmp_item
