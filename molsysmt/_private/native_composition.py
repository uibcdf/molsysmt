"""Compose complementary native domains behind the public conversion boundary."""


def compose_partial_molsys(items):
    """Join declared shared axes before selection, without resolving conflicts.

    This bounded route handles partial MolSys objects, including materialized
    H5MSM 0.5 files. The input list declares positional correspondence. Other
    form combinations retain their existing conversion routes.
    """
    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.native import MolSys

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
