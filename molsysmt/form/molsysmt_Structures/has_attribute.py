from molsysmt._private.argdigest import arg_digest


@arg_digest(form='molsysmt.Structures')
def has_attribute(
    molecular_system,
    attribute,
    include_none=False,
    skip_digestion=False,
):
    """Checking instance-aware attribute availability for native structures."""

    from . import attributes

    if not attributes[attribute]:
        return False
    if include_none:
        return True

    if attribute == 'n_atoms':
        return molecular_system.n_atoms > 0
    if attribute == 'n_structures':
        return True
    if attribute == 'structure_index':
        return molecular_system.n_structures > 0
    if attribute in {'box_shape', 'box_angles', 'box_lengths', 'box_volume'}:
        return molecular_system.box is not None
    if attribute == 'n_bioassemblies':
        return molecular_system.bioassembly is not None
    if attribute == 'total_energy':
        return (
            molecular_system.potential_energy is not None
            and molecular_system.kinetic_energy is not None
        )

    storage = {
        'structure_id': 'structure_id',
        'time': 'time',
        'box': 'box',
        'coordinates': 'coordinates',
        'velocities': 'velocities',
        'b_factor': 'b_factor',
        'alternate_location': 'alternate_location',
        'bioassembly': 'bioassembly',
        'temperature': 'temperature',
        'potential_energy': 'potential_energy',
        'kinetic_energy': 'kinetic_energy',
        'occupancy': 'occupancy',
    }
    if attribute in storage:
        return getattr(molecular_system, storage[attribute]) is not None

    return False
