from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.StructuresDict')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.structures import Structures
    from . import (
        get_alternate_location_from_atom,
        get_b_factor_from_atom,
        get_box_from_system,
        get_coordinates_from_atom,
        get_kinetic_energy_from_system,
        get_occupancy_from_atom,
        get_potential_energy_from_system,
        get_structure_id_from_system,
        get_temperature_from_system,
        get_time_from_system,
        get_velocities_from_atom,
    )

    tmp_item = Structures()

    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    time = get_time_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    velocities = get_velocities_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    b_factor = get_b_factor_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    occupancy = get_occupancy_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    alternate_location = get_alternate_location_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    temperature = get_temperature_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    potential_energy = get_potential_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    kinetic_energy = get_kinetic_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    tmp_item.append(
        structure_id=structure_id,
        time=time,
        coordinates=coordinates,
        velocities=velocities,
        box=box,
        b_factor=b_factor,
        occupancy=occupancy,
        alternate_location=alternate_location,
        temperature=temperature,
        potential_energy=potential_energy,
        kinetic_energy=kinetic_energy,
        skip_digestion=True,
    )

    return tmp_item
