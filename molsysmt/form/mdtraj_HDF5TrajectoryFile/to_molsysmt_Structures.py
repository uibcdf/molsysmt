from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

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
