"""Resolve complete state-specific covalent graphs for general chemical tools."""

import numpy as np

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def chemical_graph_context(
    molecular_system, chemical_state, structure_indices, assume_complete, caller
):
    """Resolve chemistry without selecting or truncating the source covalent graph."""
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get_form
    from molsysmt.native import ChemicalStates, MolSys, Topology

    selection_frames = structure_indices
    forms = get_form(molecular_system)
    if isinstance(forms, (list, tuple)) and any(
        form in ("molsysmt.ChemicalStates", "molsysmt.ChemicalStatesDict")
        for form in forms
    ):
        # General conversion owns axis validation and declared correspondence.
        # The read-only chemistry context may share full native domains.
        molecular_system = convert(
            molecular_system,
            to_form="molsysmt.MolSys",
            copy_if_all=False,
        )
    dimensions = modular_h5msm_dimensions(molecular_system)
    if dimensions is not None:
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        frames = (
            np.arange(dimensions[1], dtype=np.int64)
            if is_all(structure_indices)
            else structure_indices
        )
        if np.any(np.asarray(frames) < 0) or np.any(
            np.asarray(frames) >= dimensions[1]
        ):
            raise ArgumentError(
                "structure_indices", value=structure_indices, caller=caller
            )
        molecular_system, chemical_state = _read_calculation_chemistry(
            molecular_system,
            chemical_state=chemical_state,
            structure_indices=frames,
            require_topology=False,
        )
        selection_frames = "all"
    if chemical_state == "structure":
        if not isinstance(molecular_system, MolSys):
            raise ArgumentError("chemical_state", value=chemical_state, caller=caller)
        chemical_state = molecular_system._resolve_structure_chemical_state_index(
            structure_indices
        )
    if isinstance(molecular_system, MolSys):
        states = molecular_system.chemical_states
    elif isinstance(molecular_system, ChemicalStates):
        states = molecular_system
    elif get_form(molecular_system) == "molsysmt.ChemicalStatesDict":
        molecular_system = convert(molecular_system, to_form="molsysmt.ChemicalStates")
        states = molecular_system
    else:
        topology = (
            molecular_system
            if isinstance(molecular_system, Topology)
            else convert(molecular_system, to_form="molsysmt.Topology")
        )
        states = topology._chemical_states_domain
    if states is None:
        raise StructuralInconsistencyError(
            reason="A chemical-states domain is required.", caller=caller
        )
    state_index = states._resolve_index(
        None if chemical_state == "reference" else chemical_state
    )
    state = states._states[state_index]
    n_atoms = states.n_atoms
    if (
        n_atoms
        and state.connectivity_completeness != "complete"
        and not assume_complete
    ):
        raise StructuralInconsistencyError(
            reason="Chemical graph analysis requires connectivity declared complete.",
            caller=caller,
        )
    bonds = state.bonds
    if len(bonds):
        if not {"bond_type", "atom1_index", "atom2_index"} <= set(bonds.columns):
            raise StructuralInconsistencyError(
                reason="Bond chemistry columns are missing.", caller=caller
            )
        relationships = bonds["bond_type"]
        if (
            relationships.isna().any()
            or not relationships.isin(["covalent", "dative"]).all()
        ):
            raise StructuralInconsistencyError(
                reason="Every bond requires a covalent or dative relationship.",
                caller=caller,
            )
        covalent = bonds.loc[relationships == "covalent"]
        pairs = covalent[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    else:
        covalent, pairs = bonds, np.empty((0, 2), dtype=np.int64)
    if (
        np.any(pairs < 0)
        or np.any(pairs >= n_atoms)
        or np.any(pairs[:, 0] == pairs[:, 1])
        or len(np.unique(np.sort(pairs, axis=1), axis=0)) != len(pairs)
    ):
        raise StructuralInconsistencyError(
            reason="Covalent bonds must be unique pairs of distinct valid atom indices.",
            caller=caller,
        )
    return (
        molecular_system,
        states,
        state,
        state_index,
        covalent,
        pairs,
        selection_frames,
    )


def select_chemical_atoms(
    source, states, state_index, selection, frames, syntax, *, reference_request
):
    """Select on a chemistry view for indices, retaining coordinates for rich syntax."""
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, select
    from molsysmt.native import MolSys, Topology

    if not isinstance(selection, str) or is_all(selection):
        # Avoid restoration hooks on a shallow copy of shared state records.
        view = object.__new__(type(states))
        view.__dict__ = states.__dict__.copy()
        view._reference_index = state_index
        state = "reference"
    else:
        view = (
            source
            if isinstance(source, (MolSys, Topology))
            else convert(source, to_form="molsysmt.MolSys")
        )
        # An explicit integer is not interchangeable with the public reference
        # sentinel when an external selector enforces state-specific limits.
        state = "reference" if reference_request else state_index
    return np.unique(
        select(
            view,
            selection=selection,
            structure_indices=frames,
            chemical_state=state,
            syntax=syntax,
        )
    ).astype(np.int64)


def detached_chemical_graph_view(source, states, state_index, caller):
    """Detach chemistry and its element inventory without structural series."""
    from molsysmt.basic import convert
    from molsysmt.native import MolSys, Topology

    topology = (
        source.topology
        if isinstance(source, MolSys)
        else source
        if isinstance(source, Topology)
        else convert(source, to_form="molsysmt.Topology")
    )
    if topology is None:
        raise StructuralInconsistencyError(
            reason="Chemical perception requires a chemical element inventory.",
            caller=caller,
        )
    # Topology's compatibility copy restores shared state before detaching it.
    # Copy the inventory independently so a read-only analysis never normalizes
    # the caller's bond table or changes its concrete DataFrame type.
    from copy import deepcopy

    inventory = object.__new__(type(topology))
    inventory.__dict__ = deepcopy(
        {
            key: value
            for key, value in topology.__getstate__().items()
            if key != "_chemical_states_domain"
        }
    )
    topology = inventory
    chemistry = states.copy()
    chemistry._reference_index = state_index
    topology._chemical_states_domain = chemistry
    return MolSys._from_partial_domains(topology=topology, chemical_states=chemistry)


def validate_chemical_frames(source, frames, caller):
    """Validate explicit structure indices before structural domains are detached."""
    from molsysmt._private.variables import is_all
    from molsysmt.basic._index_validation import _get_count, validate_structure_indices

    if is_all(frames) or frames is None:
        return frames
    count = _get_count(source, "structure")
    if count is None:
        from molsysmt.basic import convert, get_form

        form = get_form(source)
        # External providers can carry conformers through conversion even when
        # they expose no direct count getter. Native chemistry-only domains do
        # not acquire a fictitious structure axis by conversion.
        if isinstance(form, str) and not form.startswith("molsysmt."):
            source = convert(source, to_form="molsysmt.MolSys")
            count = _get_count(source, "structure")
    if count is None:
        raise ArgumentError(
            "structure_indices",
            value=frames,
            caller=caller,
            message="Explicit structure_indices require a known source structure axis.",
        )
    return validate_structure_indices(
        source, frames, caller, count_getter=lambda _: count
    )


def chemical_graph_digest(source, state_index, include_template_names=False):
    """Bind stored provenance to ordered chemical data, not coordinates or IDs."""
    import hashlib
    import json

    state = source.chemical_states._states[state_index]

    def table(frame):
        return frame.astype(object).where(frame.notna(), None).to_dict(orient="list")

    data = dict(
        elements=source.topology.atoms["atom_type"].tolist(),
        isotope=table(source.topology.atoms[["isotope"]]),
        atoms=table(state.atom_attributes),
        bonds=table(state.bonds.drop(columns=["bond_id"], errors="ignore")),
        completeness=state.connectivity_completeness,
    )
    if include_template_names:
        data["atom_template_inputs"] = table(
            source.topology.atoms[["atom_name", "group_index", "chain_index"]]
        )
        data["residue_names"] = table(source.topology.groups[["group_name"]])
    payload = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda value: (
            value.item() if isinstance(value, np.generic) else str(value)
        ),
    )
    return hashlib.sha256(payload.encode()).hexdigest()
