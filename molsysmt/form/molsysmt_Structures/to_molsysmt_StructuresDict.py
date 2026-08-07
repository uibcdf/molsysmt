from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Structures')
def to_molsysmt_StructuresDict(item, atom_indices='all', structure_indices='all', skip_digestion=False):

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

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    time = get_time_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    velocities = get_velocities_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True) if getattr(item, 'velocities', None) is not None else None
    b_factor = get_b_factor_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True) if getattr(item, 'b_factor', None) is not None else None
    occupancy = get_occupancy_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True) if getattr(item, 'occupancy', None) is not None else None
    alternate_location = get_alternate_location_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True) if getattr(item, 'alternate_location', None) is not None else None
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

    tmp_item = {}

    if structure_id is not None:
        tmp_item['structure_id']=structure_id

    if time is not None:
        tmp_item['time']=time

    if coordinates is not None:
        tmp_item['coordinates']=coordinates

    if box is not None:
        tmp_item['box']=box

    if velocities is not None:
        tmp_item['velocities']=velocities

    if b_factor is not None:
        tmp_item['b_factor']=b_factor

    if occupancy is not None:
        tmp_item['occupancy']=occupancy

    if alternate_location is not None:
        tmp_item['alternate_location']=alternate_location

    if temperature is not None:
        tmp_item['temperature'] = temperature

    if potential_energy is not None:
        tmp_item['potential_energy'] = potential_energy

    if kinetic_energy is not None:
        tmp_item['kinetic_energy'] = kinetic_energy

    return tmp_item
