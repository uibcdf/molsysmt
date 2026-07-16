from depdigest import dep_digest
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np


def _load_quantity(value, unit):
    if value is None:
        return None
    return puw.quantity(value, unit)


@dep_digest('yaml')
@arg_digest(form='file:structures_yaml')
def to_molsysmt_StructuresDict(item, skip_digestion=False):
    """Reading a YAML structures file into StructuresDict."""

    import yaml

    with open(item, 'r', encoding='utf-8') as file_handle:
        data = yaml.safe_load(file_handle)

    payload = data.get('structures', {})
    output = {}

    if payload.get('structure_id', None) is not None:
        output['structure_id'] = payload['structure_id']
    if payload.get('alternate_location', None) is not None:
        output['alternate_location'] = payload['alternate_location']

    for key, unit in [('time', 'ps'), ('box', 'nm'), ('coordinates', 'nm'), ('velocities', 'nm/ps'), ('b_factor', 'nm**2')]:
        if payload.get(key, None) is not None:
            output[key] = _load_quantity(payload[key], unit)

    if payload.get('occupancy', None) is not None:
        output['occupancy'] = np.asarray(payload['occupancy'])

    return output
