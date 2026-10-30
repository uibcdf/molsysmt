"""Borrow independent native domains for read-only cross-domain queries."""


def compose_query_domains(source):
    """Join explicit native domains without copying arrays or rebinding owners.

    This view is private and must never escape as a mutable molecular system.
    Non-native composites retain the ordinary conversion/dispatch route.
    """
    from .chemical_states import ChemicalStates
    from .molsys import MolSys
    from .structures import Structures
    from .topology import Topology

    if not isinstance(source, (list, tuple)):
        return source
    domains = {}
    for item in source:
        kind = next(
            (
                cls
                for cls in (Topology, ChemicalStates, Structures)
                if isinstance(item, cls)
            ),
            None,
        )
        if kind is None or kind in domains:
            return source
        domains[kind] = item
    if ChemicalStates not in domains:
        return source
    topology = domains.get(Topology)
    chemistry = domains[ChemicalStates]
    structures = domains.get(Structures)
    if (topology is not None and topology.n_atoms != chemistry.n_atoms) or (
        structures is not None
        and structures._atom_axis_size() is not None
        and structures.n_atoms != chemistry.n_atoms
    ):
        from molsysmt._private.smonitor import StructuralInconsistencyError

        raise StructuralInconsistencyError(
            reason="Explicit query domains must share the same atom-index axis.",
            caller="molsysmt.get",
        )
    view = object.__new__(MolSys)
    view._topology = topology
    view._chemical_states_domain = chemistry
    view._structures = structures
    view.molecular_mechanics = None
    view._structure_chemical_state_indices = None
    view._interactions = {}
    return view
