"""Checking native extensions at declarative transport boundaries."""


def _reject_extensions(source, allowed):
    """Refuse data outside the receiving schema without copying its payload."""
    from ._copy import _slots

    if set(vars(source)) - set(allowed) - {"_molsys_owner_ref"} or _slots(
        source, exclude=("_molsys_owner_ref",), qualified=True
    ):
        raise ValueError(
            f"Unsupported {type(source).__name__} extension payload in declarative export."
        )


def _validate_topology_extensions(topology):
    _reject_extensions(
        topology,
        {
            "atoms",
            "groups",
            "molecules",
            "entities",
            "chains",
            "_atom_molecule_membership",
            "_chain_group_membership",
            "_group_naming_codes",
            "_atoms_dirty",
            "_groups_dirty",
            "_molecules_dirty",
            "_entities_dirty",
            "_chains_dirty",
        },
    )


def _validate_structures_extensions(structures):
    _reject_extensions(
        structures,
        {
            "_coordinates",
            "_box",
            "_time",
            "_time_step",
            "_velocities",
            "_b_factor",
            "_occupancy",
            "_temperature",
            "_potential_energy",
            "_kinetic_energy",
            "constant_box",
            "constant_time_step",
            "constant_id_step",
            "id_step",
            "structure_id",
            "alternate_location",
            "bioassembly",
        },
    )


def _validate_molsys_extensions(molsys):
    _reject_extensions(
        molsys,
        {
            "_topology",
            "_chemical_states_domain",
            "_structures",
            "molecular_mechanics",
            "_structure_chemical_state_indices",
            "_interactions",
        },
    )
    if molsys.chemical_states is not None:
        _validate_chemical_states_extensions(molsys.chemical_states)


def _validate_chemical_states_extensions(states):
    _reject_extensions(states, {"_n_atoms", "_states", "_reference_index"})
    for state in states._states:
        _reject_extensions(
            state,
            {
                "state_id",
                "atom_attributes",
                "component_indices",
                "bonds",
                "components",
                "_connectivity_completeness",
                "_component_completeness",
                "_component_evidence",
                "_provenance_index",
                "_preparation_history",
            },
        )
