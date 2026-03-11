from molsysmt._private.arg_digestion import arg_digest


@arg_digest(form='molsysmt.TopologyDict')
def to_molsysmt_Topology(item, skip_digestion=False):
    """Converting TopologyDict to Topology."""

    from molsysmt import MolSysBuilder

    builder = MolSysBuilder()
    data = item.to_dict(copy=True)

    for atom in data.get('atoms', []) or []:
        builder.add_atom(
            atom_id=atom.get('atom_id', None),
            atom_name=atom.get('atom_name', None),
            atom_type=atom.get('atom_type', None),
        )

    for group in data.get('groups', []) or []:
        builder.add_group(
            atom_indices=group.get('atom_indices', []),
            group_id=group.get('group_id', None),
            group_name=group.get('group_name', None),
            group_type=group.get('group_type', None),
        )

    for bond in data.get('bonds', []) or []:
        builder.add_bond(
            atom_index_1=bond['atom_index_1'],
            atom_index_2=bond['atom_index_2'],
            bond_order=bond.get('bond_order', None),
            bond_type=bond.get('bond_type', None),
        )

    for chain in data.get('chains', []) or []:
        builder.add_chain(
            group_indices=chain.get('group_indices', []),
            chain_id=chain.get('chain_id', None),
            chain_name=chain.get('chain_name', None),
            chain_type=chain.get('chain_type', None),
        )

    for molecule in data.get('molecules', []) or []:
        builder.add_molecule(
            group_indices=molecule.get('group_indices', []),
            molecule_id=molecule.get('molecule_id', None),
            molecule_name=molecule.get('molecule_name', None),
            molecule_type=molecule.get('molecule_type', None),
        )

    for entity in data.get('entities', []) or []:
        builder.add_entity(
            molecule_indices=entity.get('molecule_indices', []),
            entity_id=entity.get('entity_id', None),
            entity_name=entity.get('entity_name', None),
            entity_type=entity.get('entity_type', None),
        )

    return builder.build(skip_digestion=True).topology
