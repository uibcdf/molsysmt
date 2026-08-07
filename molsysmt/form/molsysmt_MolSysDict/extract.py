"""Extracting aligned subsets from the declarative molecular-system schema."""

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.native import MolSysDict, TopologyDict


def _structure_count(structures):
    """Returning the represented frame count without inventing structures."""

    for key in ('structure_id', 'time', 'box', 'coordinates'):
        value = structures.get(key)
        if value is not None:
            return len(value)
    return 0


@arg_digest(form='molsysmt.MolSysDict')
def extract(
    item,
    atom_indices='all',
    structure_indices='all',
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting aligned topology and structure subsets from schema 0.1."""

    if is_all(atom_indices) and is_all(structure_indices):
        return item.copy() if copy_if_all else item

    data = item.to_dict(copy=True)
    source_topology = data.get('topology', {}) or {}
    if is_all(atom_indices):
        selected_atoms = list(range(len(source_topology.get('atoms', []) or [])))
    else:
        selected_atoms = sorted(int(index) for index in atom_indices)

    topology_payload = {
        'format': 'molsysmt',
        'kind': 'topology',
        'version': data.get('version', '0.1'),
        'metadata': data.get('metadata', {}),
        **source_topology,
    }
    from molsysmt.form.molsysmt_TopologyDict.extract import extract as extract_topology

    extracted_topology = extract_topology(
        TopologyDict(data=topology_payload),
        atom_indices=selected_atoms,
        copy_if_all=True,
        skip_digestion=True,
    ).to_dict(copy=False)
    data['topology'] = {
        key: extracted_topology.get(key, [])
        for key in ('atoms', 'groups', 'bonds', 'chains', 'molecules', 'entities')
    }

    structures = data.get('structures', {}) or {}
    if is_all(structure_indices):
        selected_structures = list(range(_structure_count(structures)))
    else:
        selected_structures = [int(index) for index in structure_indices]

    for key in ('structure_id', 'time', 'box'):
        value = structures.get(key)
        if value is not None:
            array = np.asarray(value)
            structures[key] = array[selected_structures].tolist()
    coordinates = structures.get('coordinates')
    if coordinates is not None:
        array = np.asarray(coordinates)
        structures['coordinates'] = array[
            np.ix_(selected_structures, selected_atoms, np.arange(3))
        ].tolist()
    data['structures'] = structures

    return MolSysDict(data=data)
