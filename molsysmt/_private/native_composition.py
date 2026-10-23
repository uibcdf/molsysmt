"""Compose complementary native domains behind the public conversion boundary."""


def _compose_standalone_domains(items):
    """Assemble explicit native providers; topology chemistry is a fallback only."""
    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.native import (
        ChemicalStates,
        MolecularMechanics,
        MolSys,
        Structures,
        Topology,
    )

    providers = (
        (Topology, "topology"),
        (ChemicalStates, "chemical_states"),
        (Structures, "structures"),
        (MolecularMechanics, "molecular_mechanics"),
    )
    domains = {}
    try:
        for item in items:
            name = next(name for cls, name in providers if isinstance(item, cls))
            if name in domains:
                raise ValueError(f"Complementary inputs repeat the {name} domain.")
            domains[name] = item
        mechanics = domains.pop("molecular_mechanics", None)
        topology = domains.get("topology")
        if topology is not None:
            # A topology has one owner. An explicit ChemicalStates provider owns
            # chemistry, independent of the topology's compatibility facade.
            domains["topology"] = topology.copy()
            explicit = domains.get("chemical_states")
            domains["chemical_states"] = (
                domains["topology"]._chemical_states_domain
                if explicit is None or explicit is topology._chemical_states_domain
                else explicit.copy()
            )
        result = MolSys._from_partial_domains(**domains)
        if mechanics is not None:
            if mechanics.atoms_ff is not None:
                n_atoms = result._get_n_atoms()
                if n_atoms is None or len(mechanics.atoms_ff) != n_atoms:
                    raise ValueError(
                        "MolecularMechanics atom rows must match the complete declared atom domain."
                    )
            # Conversion/extraction owns independent copying and assignment-map
            # projection. Keep reports intact here; never certify/rebind them.
            result.molecular_mechanics = mechanics
        return result
    except ValueError as error:
        raise StructuralInconsistencyError(
            reason=str(error), caller="molsysmt.convert"
        ) from error


def compose_partial_molsys(items):
    """Join declared shared axes before selection, without resolving conflicts.

    This bounded route handles complementary partial MolSys objects, including
    materialized H5MSM 0.5 files, and standalone native provider lists carrying
    MolecularMechanics or explicit Topology plus ChemicalStates. The input list
    declares positional correspondence. Other combinations retain their routes.
    """
    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.native import (
        ChemicalStates,
        MolecularMechanics,
        MolSys,
        Structures,
        Topology,
    )

    if isinstance(items, (list, tuple)) and len(items) >= 2:
        standalone = (Topology, ChemicalStates, Structures, MolecularMechanics)
        if all(isinstance(item, standalone) for item in items) and (
            any(isinstance(item, MolecularMechanics) for item in items)
            or (
                any(isinstance(item, Topology) for item in items)
                and any(isinstance(item, ChemicalStates) for item in items)
            )
        ):
            return _compose_standalone_domains(items)

    if (
        not isinstance(items, (list, tuple))
        or len(items) < 2
        or not all(isinstance(item, MolSys) for item in items)
        or any(
            all(
                getattr(item, name) is not None
                for name in ("topology", "chemical_states", "structures")
            )
            for item in items
        )
    ):
        return items

    domains, analyses = {}, {}
    state_indices = None
    try:
        for item in items:
            for name in ("topology", "chemical_states", "structures"):
                domain = getattr(item, name)
                if domain is not None:
                    if name in domains:
                        raise ValueError(
                            f"Complementary inputs repeat the {name} domain."
                        )
                    domains[name] = domain
            for name, analysis in item.interactions.items():
                if name in analyses:
                    raise ValueError(
                        f"Complementary inputs repeat interaction analysis {name!r}."
                    )
                analyses[name] = analysis
            if any(
                value is not None
                for value in item.molecular_mechanics.to_dict().values()
            ):
                raise ValueError(
                    "Partial-domain composition cannot transfer molecular mechanics yet."
                )
            if item._structure_chemical_state_indices is not None:
                state_indices = item._structure_chemical_state_indices.copy()
        topology = domains.get("topology")
        # A topology has one MolSys owner; copying preserves both input bindings.
        if topology is not None:
            domains["topology"] = topology.copy()
            chemistry = domains.get("chemical_states")
            if chemistry is not None:
                domains["chemical_states"] = (
                    domains["topology"]._chemical_states_domain
                    if topology._chemical_states_domain is chemistry
                    else chemistry.copy()
                )
        result = MolSys._from_partial_domains(
            **domains, interactions=analyses if state_indices is None else None
        )
        if state_indices is not None:
            result._set_structure_chemical_state_indices(state_indices)
            result.interactions = analyses
        return result
    except ValueError as error:
        raise StructuralInconsistencyError(
            reason=str(error),
            caller="molsysmt.convert",
        ) from error
