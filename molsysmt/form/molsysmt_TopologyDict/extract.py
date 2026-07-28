"""Extracting aligned subsets from the declarative topology schema."""

from copy import deepcopy

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.native import TopologyDict


def _remap_members(values, index_map):
    """Returning retained member indices in their declared order."""

    return [index_map[index] for index in values if index in index_map]


@arg_digest(form='molsysmt.TopologyDict')
def extract(
    item,
    atom_indices='all',
    structure_indices='all',
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting an atom subset while remapping every hierarchy reference."""

    if is_all(atom_indices):
        return item.copy() if copy_if_all else item

    data = item.to_dict(copy=True)
    # Native topology extraction uses canonical source order. Keeping the same
    # rule prevents form-dependent renumbering for an equivalent atom subset.
    selected_atoms = sorted(int(index) for index in atom_indices)
    atom_map = {old: new for new, old in enumerate(selected_atoms)}
    data['atoms'] = [deepcopy(data['atoms'][index]) for index in selected_atoms]

    group_map = {}
    groups = []
    for old_index, group in enumerate(data.get('groups', []) or []):
        members = _remap_members(group.get('atom_indices', []), atom_map)
        if members:
            group_map[old_index] = len(groups)
            new_group = deepcopy(group)
            new_group['atom_indices'] = members
            groups.append(new_group)
    data['groups'] = groups

    bonds = []
    for bond in data.get('bonds', []) or []:
        atom_1 = bond['atom_index_1']
        atom_2 = bond['atom_index_2']
        if atom_1 in atom_map and atom_2 in atom_map:
            new_bond = deepcopy(bond)
            endpoint_1 = atom_map[atom_1]
            endpoint_2 = atom_map[atom_2]
            new_bond['atom_index_1'] = min(endpoint_1, endpoint_2)
            new_bond['atom_index_2'] = max(endpoint_1, endpoint_2)
            bonds.append(new_bond)
    data['bonds'] = bonds

    chains = []
    for chain in data.get('chains', []) or []:
        members = _remap_members(chain.get('group_indices', []), group_map)
        if members:
            new_chain = deepcopy(chain)
            new_chain['group_indices'] = members
            chains.append(new_chain)
    data['chains'] = chains

    molecule_map = {}
    molecules = []
    for old_index, molecule in enumerate(data.get('molecules', []) or []):
        members = _remap_members(molecule.get('group_indices', []), group_map)
        if members:
            molecule_map[old_index] = len(molecules)
            new_molecule = deepcopy(molecule)
            new_molecule['group_indices'] = members
            molecules.append(new_molecule)
    data['molecules'] = molecules

    entities = []
    for entity in data.get('entities', []) or []:
        members = _remap_members(
            entity.get('molecule_indices', []),
            molecule_map,
        )
        if members:
            new_entity = deepcopy(entity)
            new_entity['molecule_indices'] = members
            entities.append(new_entity)
    data['entities'] = entities

    return TopologyDict(data=data)
