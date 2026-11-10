"""Sharing the observed-backbone endpoint rule without inventory ordering."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError

CALLER = "molsysmt.chemical_states.get_peptide_termini"


def fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


class _AmbiguousBackbone(Exception):
    pass


def ambiguous(reason):
    raise _AmbiguousBackbone(reason)


def context(source, chemical_state, frames):
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert
    from molsysmt.chemical_states._chemical_graph import validate_chemical_frames
    from molsysmt.native import MolSys

    frames = validate_chemical_frames(source, frames, CALLER)
    if modular_h5msm_dimensions(source) is not None:
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        native, chemical_state = _read_calculation_chemistry(
            source,
            chemical_state=chemical_state,
            structure_indices=frames,
            include_structures=False,
        )
    else:
        native = (
            source
            if isinstance(source, MolSys)
            else convert(
                source,
                to_form="molsysmt.MolSys",
                get_missing_bonds=False,
            )
        )
        if chemical_state == "structure":
            chemical_state = native._resolve_structure_chemical_state_index(frames)
    if native.topology is None or native.chemical_states is None:
        fail(
            "Peptide termini require stable topology and stored chemical connectivity."
        )
    states = native.chemical_states
    index = states._resolve_index(
        None if chemical_state in (None, "reference") else chemical_state
    )
    return native, index


def recognize(source, selection, syntax, chemical_state, frames, on_ambiguous):
    from molsysmt import __version__
    from molsysmt._private.amino_acid_templates import family
    from molsysmt.basic import select
    from molsysmt.chemical_states import get_bondgraph
    from molsysmt.element.group.amino_acid import group_names
    from molsysmt.element.group.terminal_capping import (
        is_c_terminal_capping,
        is_n_terminal_capping,
    )

    atoms = np.unique(
        select(
            source,
            selection=selection,
            syntax=syntax,
            chemical_state=chemical_state,
            structure_indices=frames,
        )
    ).astype(np.int64)
    native, state_index = context(source, chemical_state, frames)
    topology = native.topology
    state = native.chemical_states._states[state_index]
    groups = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    chains = topology.atoms["chain_index"].to_numpy(dtype=np.int64, na_value=-1)
    atom_names = [None if pd.isna(v) else str(v) for v in topology.atoms["atom_name"]]
    elements = [None if pd.isna(v) else str(v) for v in topology.atoms["atom_type"]]
    selected = set(groups[atoms]) - {-1}
    names = topology.groups["group_name"].tolist()
    schemes = topology.group_naming_schemes
    grouped = topology.atoms.groupby("group_index", sort=False).indices
    aa_candidates = {i for i, name in enumerate(names) if name in group_names}
    selected_aa = selected & aa_candidates
    chain_groups = {}
    for g in aa_candidates:
        values = np.unique(chains[grouped.get(g, [])])
        if len(values) != 1 or not 0 <= int(values[0]) < topology.n_chains:
            if g in selected_aa:
                fail(
                    "Peptide termini require one known chain_index per selected amino-acid group."
                )
            continue
        chain_groups.setdefault(int(values[0]), []).append(g)
    selected_chains = {
        chain
        for chain, population in chain_groups.items()
        if selected_aa.intersection(population)
    }
    graph = get_bondgraph(native, chemical_state=state_index)
    relationships = state.bonds.get(
        "bond_type", pd.Series(pd.NA, index=state.bonds.index, dtype="string")
    )
    dative = relationships.eq("dative").fillna(False)
    graph.remove_edges_from(
        state.bonds.loc[dative, ["atom1_index", "atom2_index"]].to_numpy(dtype=int)
    )
    rows = []
    for chain in sorted(selected_chains):
        population = chain_groups[chain]
        try:
            endpoints = {}
            for g in population:
                if family(names[g], schemes[g], caller=CALLER) is None:
                    ambiguous(
                        "A selected chain contains an unsupported amino-acid naming context."
                    )
                mapping = {}
                for name, element in [("N", "N"), ("CA", "C"), ("C", "C")]:
                    found = [
                        int(atom) for atom in grouped[g] if atom_names[atom] == name
                    ]
                    if len(found) != 1 or elements[found[0]] != element:
                        ambiguous(
                            "Peptide terminal recognition requires unique stored N-CA-C backbone atoms."
                        )
                    mapping[name] = found[0]
                if not graph.has_edge(
                    mapping["N"], mapping["CA"]
                ) or not graph.has_edge(mapping["CA"], mapping["C"]):
                    ambiguous(
                        "Peptide terminal recognition requires stored N-CA-C backbone bonds."
                    )
                endpoints[g] = mapping
            incoming = {g: set() for g in population}
            outgoing = {g: set() for g in population}
            n_caps, c_caps = set(), set()
            for g, mapping in endpoints.items():
                for role, incoming_role in [("N", True), ("C", False)]:
                    for neighbor in graph.neighbors(mapping[role]):
                        other = int(groups[neighbor])
                        if other < 0:
                            ambiguous(
                                "A backbone attachment has unknown group membership."
                            )
                        wanted = "C" if incoming_role else "N"
                        if other == g:
                            if neighbor == mapping[wanted]:
                                (incoming if incoming_role else outgoing)[g].add(g)
                            continue
                        if (
                            atom_names[neighbor] != wanted
                            or elements[neighbor] != wanted
                        ):
                            ambiguous(
                                "An unsupported inter-group backbone attachment cannot establish a free peptide end."
                            )
                        if other in endpoints and endpoints[other][wanted] == neighbor:
                            (incoming if incoming_role else outgoing)[g].add(other)
                        elif (
                            is_n_terminal_capping(names[other])
                            if incoming_role
                            else is_c_terminal_capping(names[other])
                        ):
                            caps = n_caps if incoming_role else c_caps
                            if g in caps:
                                ambiguous(
                                    "Multiple stored cap attachments make a peptide end ambiguous."
                                )
                            caps.add(g)
                        else:
                            ambiguous(
                                "A stored peptide backbone attachment crosses chains or has an unsupported cap."
                            )
            if any(
                len(incoming[g]) + int(g in n_caps) > 1
                or len(outgoing[g]) + int(g in c_caps) > 1
                for g in population
            ):
                ambiguous("Branched named peptide backbones have ambiguous termini.")
            starts = [g for g in population if not incoming[g]]
            ends = [g for g in population if not outgoing[g]]
            cyclic = not starts and not ends
            if not cyclic and (len(starts) != 1 or len(ends) != 1):
                ambiguous(
                    "Disconnected named peptide backbones in one chain cannot establish termini."
                )
            start = min(population) if cyclic else starts[0]
            ordered, seen, current = [], set(), start
            while current not in seen:
                seen.add(current)
                ordered.append(current)
                if not outgoing[current]:
                    break
                current = next(iter(outgoing[current]))
            if seen != set(population):
                ambiguous(
                    "Disconnected named peptide paths or cycles cannot establish chain termini."
                )
            rows.append(
                dict(
                    chain_index=chain,
                    status="assessed",
                    reason=None,
                    group_indices=np.asarray(ordered, dtype=np.int64),
                    cyclic=cyclic,
                    n_terminal_group_index=None if cyclic else starts[0],
                    c_terminal_group_index=None if cyclic else ends[0],
                    n_capped=False if cyclic else starts[0] in n_caps,
                    c_capped=False if cyclic else ends[0] in c_caps,
                )
            )
        except _AmbiguousBackbone as error:
            if on_ambiguous == "raise":
                fail(str(error))
            rows.append(
                dict(
                    chain_index=chain,
                    status="unassessed",
                    reason=str(error),
                    group_indices=np.asarray(sorted(population), dtype=np.int64),
                    cyclic=None,
                    n_terminal_group_index=None,
                    c_terminal_group_index=None,
                    n_capped=None,
                    c_capped=None,
                )
            )
    result = {}
    for end in ("n", "c"):
        for capped in (False, True):
            key = (
                f"{end}_capped_group_indices"
                if capped
                else f"{end}_terminal_group_indices"
            )
            result[key] = np.asarray(
                sorted(
                    row[f"{end}_terminal_group_index"]
                    for row in rows
                    if row["status"] == "assessed"
                    and not row["cyclic"]
                    and row[f"{end}_capped"] == capped
                    and row[f"{end}_terminal_group_index"] in selected
                ),
                dtype=np.int64,
            )
    result.update(
        chains=rows,
        unassessed_chain_indices=np.asarray(
            [row["chain_index"] for row in rows if row["status"] == "unassessed"],
            dtype=np.int64,
        ),
        selection_atom_indices=atoms,
        chemical_state_index=state_index,
        method="stored_backbone_connectivity",
        evidence=dict(
            connectivity_completeness=state.connectivity_completeness,
            untyped_stored_bonds=int(relationships.isna().sum()),
            chemical_state_provenance_index=state.provenance_index,
        ),
        software={"molsysmt": __version__},
    )
    return result


def warn_unassessed(report):
    """Expose partial legacy results instead of silently treating gaps as ends."""
    import warnings

    from molsysmt._private.smonitor import UnassessedPeptideBackboneWarning

    for row in report["chains"]:
        if row["status"] == "unassessed":
            warnings.warn(
                UnassessedPeptideBackboneWarning(
                    chain_index=row["chain_index"], reason=row["reason"]
                ),
                stacklevel=3,
            )
