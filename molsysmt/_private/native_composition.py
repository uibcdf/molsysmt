"""Compose complementary native domains behind the public conversion boundary."""


def compose_with_coordinate_source(items, forms, structure_indices):
    """Join explicit native chemistry with one coordinate-only foreign provider.

    The caller validates the original structure axis before this step. Consume
    its structure selection here, then apply atom selection to the assembled
    native result. Never discard a foreign inventory or chemical domain merely
    to make it fit this complementary-input route.
    """
    from molsysmt.attribute import (
        is_chemical_state_attribute,
        is_structural_attribute,
        is_topological_attribute,
    )
    from molsysmt.basic import convert
    from molsysmt.form import _dict_modules
    from molsysmt.native import (
        ChemicalStates,
        MolecularMechanics,
        Structures,
        Topology,
    )

    if "molsysmt.ChemicalStatesDict" in forms:
        items = [
            convert(item, to_form="molsysmt.ChemicalStates")
            if form == "molsysmt.ChemicalStatesDict"
            else item
            for item, form in zip(items, forms, strict=True)
        ]
    standalone = (Topology, ChemicalStates, Structures, MolecularMechanics)
    if not any(isinstance(item, ChemicalStates) for item in items):
        return None
    foreign = [
        index for index, item in enumerate(items) if not isinstance(item, standalone)
    ]
    if len(foreign) != 1:
        return None
    index = foreign[0]
    capabilities = _dict_modules[forms[index]].attributes
    if not capabilities.get("coordinates", False):
        return None
    for attribute, supplied in capabilities.items():
        if supplied and (
            is_chemical_state_attribute(attribute, skip_digestion=True)
            or (
                is_topological_attribute(attribute, skip_digestion=True)
                and not is_structural_attribute(attribute, skip_digestion=True)
            )
        ):
            return None
    providers = list(items)
    providers[index] = convert(
        items[index],
        to_form="molsysmt.Structures",
        structure_indices=structure_indices,
    )
    return _compose_standalone_domains(providers)


def _compose_standalone_domains(items):
    """Assemble explicit native providers; no chemical domain is inferred from topology."""
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
        for name in ("topology", "chemical_states"):
            if name in domains:
                domains[name] = domains[name].copy()
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
        for name in ("topology", "chemical_states"):
            if name in domains:
                domains[name] = domains[name].copy()
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
