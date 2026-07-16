from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw


def _to_builtin(value):
    if hasattr(value, 'tolist'):
        value = value.tolist()
    if isinstance(value, dict):
        return {key: _to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_builtin(item) for item in value]
    return value


def _serialize_quantity(value, unit):
    if value is None:
        return None
    return puw.get_value(value, to_unit=unit).tolist()


@dep_digest('yaml')
@arg_digest(form='molsysmt.StructuresDict')
def to_file_structures_yaml(item, output_filename, skip_digestion=False):
    """Writing StructuresDict to a YAML structures file."""

    import yaml

    structures = {}

    for key in ['structure_id', 'alternate_location']:
        value = item.get(key, None)
        if value is not None:
            structures[key] = _to_builtin(value)

    for key, unit in [('time', 'ps'), ('box', 'nm'), ('coordinates', 'nm'), ('velocities', 'nm/ps'), ('b_factor', 'nm**2')]:
        value = item.get(key, None)
        if value is not None:
            structures[key] = _serialize_quantity(value, unit)

    occupancy = item.get('occupancy', None)
    if occupancy is not None:
        structures['occupancy'] = _to_builtin(occupancy)

    data = {
        'format': 'molsysmt',
        'kind': 'structures',
        'version': '0.1',
        'metadata': {},
        'structures': structures,
    }

    with open(output_filename, 'w', encoding='utf-8') as file_handle:
        yaml.safe_dump(data, file_handle, sort_keys=False)

    return output_filename
