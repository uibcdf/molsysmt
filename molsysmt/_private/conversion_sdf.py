"""Auditing explicit information SDF cannot retain from a selected native system."""

from molsysmt.basic.conversion_report import ConversionIssue


def audit_sdf_write(item, selection, structure_indices, syntax):
    from molsysmt._private.variables import is_all
    from molsysmt.basic.extract import extract

    selected = item
    if not is_all(selection) or not is_all(structure_indices):
        selected = extract(
            item,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
    issues = []

    def dropped(attribute, reason, scope):
        issues.append(ConversionIssue(attribute=attribute, reason=reason, scope=scope))

    topology = selected.topology
    if topology is not None:
        ids = [str(i) for i in range(1, topology.n_atoms + 1)]
        if topology.atoms["atom_id"].tolist() != ids:
            dropped(
                "atom_id",
                "SDF writes one-based sequential serials, not arbitrary native IDs.",
                "identity",
            )
        names = [
            f"{row.atom_type}{i}"
            for i, row in enumerate(topology.atoms.itertuples(), 1)
        ]
        if topology.atoms["atom_name"].tolist() != names:
            dropped(
                "atom_name",
                "SDF atom lines do not preserve native atom names.",
                "identity",
            )
        if topology.n_groups or topology.n_chains:
            dropped(
                "hierarchy",
                "SDF does not encode native residue or chain hierarchy.",
                "topology",
            )
        bonds = topology._get_chemical_state_bonds()
        if {"joins_components", "bond_type"} <= set(bonds.columns):
            defaults = bonds["bond_type"].map({"covalent": True, "dative": False})
            overrides = bonds["joins_components"].notna() & bonds[
                "joins_components"
            ].ne(defaults)
            if overrides.any():
                dropped(
                    "bond_joins_components",
                    "SDF cannot retain native component-joining overrides; covalent bonds join components and dative bonds do not on reading.",
                    "chemical_state",
                )
        if "bond_order" in bonds.columns and "bond_type" in bonds.columns:
            dative_orders = (
                bonds["bond_type"].eq("dative") & bonds["bond_order"].notna()
            )
            if dative_orders.any():
                dropped(
                    "bond_order",
                    "V3000 coordination type 9 retains direction and relationship kind, not a separately assigned numeric order.",
                    "chemical_state",
                )
        bond_ids = [] if bonds.empty else bonds["bond_id"].tolist()
        if bond_ids != [str(i) for i in range(1, len(bonds) + 1)]:
            dropped(
                "bond_id",
                "SDF bond serials are reassigned by output order.",
                "identity",
            )
    mechanics = selected.molecular_mechanics
    if mechanics is not None:
        if (
            mechanics.atoms_ff is not None and mechanics.atoms_ff.notna().any().any()
        ) or any(
            getattr(mechanics, name, None) is not None
            for name in ("forcefield", "water_model", "implicit_solvent")
        ):
            dropped(
                "molecular_mechanics",
                "SDF output does not encode force-field assignments or partial charges.",
                "molecular_mechanics",
            )
    if selected.interactions:
        dropped(
            "interactions",
            "SDF output cannot retain named interaction analyses.",
            "interactions",
        )
    structures = selected.structures
    if structures is not None:
        for name in (
            "box",
            "time",
            "velocities",
            "occupancy",
            "b_factor",
            "alternate_location",
            "temperature",
            "potential_energy",
            "kinetic_energy",
        ):
            value = getattr(structures, name, None)
            if value is not None:
                dropped(name, f"SDF output cannot retain {name}.", "structures")
        if structures.structure_id is not None:
            values = list(structures.structure_id)
            if values != [0]:
                dropped(
                    "structure_id",
                    "The single SDF record receives structure index and ID zero on reading.",
                    "identity",
                )
    # This audit supplements the general chemical capability audit. It is not
    # exhaustive; unsupported stereo still fails in the writer before any write.
    return issues
