from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSysBuilder


def _materialize_derived_components(builder):
    from molsysmt.native._topology_infer import (
        infer_component_indices_from_topology,
    )

    topology = builder.topology
    component_indices = infer_component_indices_from_topology(topology)
    topology._set_component_indices(component_indices)
    n_components = (
        int(max(component_indices)) + 1
        if len(component_indices) > 0
        else 0
    )
    topology.reset_components(n_components=n_components)
    topology.rebuild_components(
        redefine_indices=False,
        redefine_ids=True,
        redefine_types=True,
        redefine_names=True,
    )


def build_molsys_builder_from_molsys_dict(item):
    """Replaying a MolSysDict payload into a declared MolSysBuilder state."""

    data = item.to_dict(copy=True)
    topology = data.get("topology", {}) or {}
    structures = data.get("structures", {}) or {}

    builder = MolSysBuilder(skip_digestion=True)

    atoms = topology.get("atoms", []) or []
    for atom in atoms:
        builder.add_atom(
            atom_id=atom.get("atom_id", None),
            atom_name=atom.get("atom_name", None),
            atom_type=atom.get("atom_type", None),
            skip_digestion=True,
        )

    for group in topology.get("groups", []) or []:
        builder.add_group(
            group.get("atom_indices", []),
            group_id=group.get("group_id", None),
            group_name=group.get("group_name", None),
            group_type=group.get("group_type", None),
            skip_digestion=True,
        )

    for bond in topology.get("bonds", []) or []:
        builder.add_bond(
            bond["atom_index_1"],
            bond["atom_index_2"],
            bond_order=bond.get("bond_order", None),
            bond_type=bond.get("bond_type", None),
            skip_digestion=True,
        )

    for chain in topology.get("chains", []) or []:
        builder.add_chain(
            chain.get("group_indices", []),
            chain_id=chain.get("chain_id", None),
            chain_name=chain.get("chain_name", None),
            chain_type=chain.get("chain_type", None),
            skip_digestion=True,
        )

    for molecule in topology.get("molecules", []) or []:
        builder.add_molecule(
            molecule.get("group_indices", []),
            molecule_id=molecule.get("molecule_id", None),
            molecule_name=molecule.get("molecule_name", None),
            molecule_type=molecule.get("molecule_type", None),
            skip_digestion=True,
        )

    for entity in topology.get("entities", []) or []:
        builder.add_entity(
            entity.get("molecule_indices", []),
            entity_id=entity.get("entity_id", None),
            entity_name=entity.get("entity_name", None),
            entity_type=entity.get("entity_type", None),
            skip_digestion=True,
        )

    if any(atom.get("isotope", None) is not None for atom in atoms):
        builder.topology.atoms["isotope"] = [
            atom.get("isotope", None) for atom in atoms
        ]

    if structures.get("coordinates", None) is not None:
        builder.set_coordinates(puw.quantity(structures["coordinates"], "nm"), skip_digestion=True)
    if structures.get("box", None) is not None:
        builder.set_box(puw.quantity(structures["box"], "nm"), skip_digestion=True)
    if structures.get("time", None) is not None:
        builder.set_time(puw.quantity(structures["time"], "ps"), skip_digestion=True)
    if structures.get("structure_id", None) is not None:
        builder.set_structure_id(structures["structure_id"], skip_digestion=True)

    _materialize_derived_components(builder)

    return builder
