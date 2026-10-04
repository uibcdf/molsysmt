"""Applying an auditable bounded AutoDock4 chemical-environment profile."""

import hashlib
import json
from copy import deepcopy

import numpy as np
from depdigest import dep_digest

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

CALLER = "molsysmt.physchem.get_autodock_atom_types"
RULE_VERSION = "chemical_environment@1"
RULES = (
    "element_default",
    "aromatic_carbon",
    "trivalent_nitrogen_adjacent_to_aromatic_atom",
    "trivalent_nitrogen_adjacent_to_sp2_carbon_or_triazene",
    "positive_nitrogen",
    "nonaromatic_two_connected_sulfur",
    "hydrogen_bonded_to_nitrogen_oxygen_fluorine_phosphorus_sulfur",
)
_REFERENCE = dict(
    id="autodock4-atom-type-vocabulary",
    type="webpage",
    title="AutoDock 4.2.6 User Guide: atom types",
    url="https://autodock.scripps.edu/wp-content/uploads/sites/56/2021/10/AutoDock4.2.6_UserGuide.pdf",
    roles=["parameter_scheme"],
)
_COMPARISON = dict(
    id="meeko-ad4-typing-reference",
    type="software",
    title="Meeko chemical-context atom typing",
    version="0.8.0",
    revision="1eac18bd6d1111f35f9f1abaa8af502c2668d054",
    url="https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/atomtyper.py",
    roles=["reference_implementation"],
)


def fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


@dep_digest("rdkit")
def calculate(
    molecular_system, scheme, method, selection, frames, chemical_state, syntax
):
    from rdkit import Chem

    from molsysmt import __version__, _ackredit
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get_form
    from molsysmt.physchem import get_aromaticity, get_hydrogen_inventory
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        detached_chemical_graph_view,
        select_chemical_atoms,
        validate_chemical_frames,
    )

    if scheme != "autodock4":
        raise ArgumentError("typing_scheme", value=scheme, caller=CALLER)
    if method != "chemical_environment":
        raise ArgumentError("method", value=method, caller=CALLER)
    original, original_frames = molecular_system, frames
    if get_form(molecular_system) == "rdkit.Mol":
        if any(atom.HasQuery() for atom in molecular_system.GetAtoms()) or any(
            bond.HasQuery() for bond in molecular_system.GetBonds()
        ):
            fail("AutoDock typing requires a concrete graph, not query atoms or bonds.")
        molecular_system = Chem.Mol(molecular_system)
        original = molecular_system
    source, states, state, index, _, _, frames = chemical_graph_context(
        molecular_system, chemical_state, frames, False, CALLER
    )
    frames = validate_chemical_frames(source, frames, CALLER)
    view = detached_chemical_graph_view(source, states, index, CALLER)
    inventory = get_hydrogen_inventory(view, chemical_state=index)
    if inventory["status"] == "conflict" or np.any(
        inventory["missing_hydrogen_counts"] > 0
    ):
        fail(
            "AutoDock typing requires all hydrogens as indexed atoms; materialize the fixed inventory first."
        )
    aromaticity = get_aromaticity(view, chemical_state=index)
    molecule = convert(view, to_form="rdkit.Mol")
    if molecule.GetNumAtoms() != states.n_atoms:
        fail("AutoDock typing provider changed the atom inventory.")
    if any(
        atom.GetNumImplicitHs() or atom.GetNumExplicitHs()
        for atom in molecule.GetAtoms()
    ):
        fail(
            "AutoDock typing requires indexed hydrogens; provider valence found virtual hydrogens."
        )
    if not np.array_equal(
        aromaticity["atom_is_aromatic"],
        [atom.GetIsAromatic() for atom in molecule.GetAtoms()],
    ):
        fail("Typing and the explicitly requested aromaticity model disagree.")
    labels = np.empty(states.n_atoms, dtype="U2")
    winners = np.zeros(states.n_atoms, dtype=np.int8)
    match_counts = np.ones(states.n_atoms, dtype=np.int8)
    allowed_charges = {
        "H": {0},
        "C": {0},
        "N": {0, 1},
        "O": {0, -1},
        "P": {0, 1},
        "S": {0, -1},
        "F": {0},
        "Cl": {0},
        "Br": {0},
        "I": {0},
    }
    for atom in molecule.GetAtoms():
        i = atom.GetIdx()
        symbol = atom.GetSymbol()
        charge = atom.GetFormalCharge()
        if symbol not in allowed_charges or charge not in allowed_charges[symbol]:
            fail(
                f"AutoDock chemical_environment@1 has no qualified rule for atom {i}: {symbol}, formal charge {charge}."
            )
        neighbors = list(atom.GetNeighbors())
        labels[i] = {"N": "NA", "O": "OA"}.get(symbol, symbol)

        def apply(code, label, atom_index=i):
            labels[atom_index] = label
            winners[atom_index] = code
            match_counts[atom_index] += 1

        if symbol == "C" and atom.GetIsAromatic():
            apply(1, "A")
        if symbol == "N":
            trivalent = atom.GetTotalDegree() == 3 and atom.GetTotalValence() == 3
            if trivalent and any(neighbor.GetIsAromatic() for neighbor in neighbors):
                apply(2, "N")
            if trivalent and any(
                (
                    neighbor.GetAtomicNum() == 6
                    and neighbor.GetTotalDegree() == 3
                    and neighbor.GetTotalValence() == 4
                )
                or (
                    neighbor.GetAtomicNum() == 7
                    and neighbor.GetTotalDegree() == 2
                    and any(
                        bond.GetBondType() == Chem.BondType.DOUBLE
                        for bond in neighbor.GetBonds()
                    )
                )
                for neighbor in neighbors
            ):
                apply(3, "N")
            if charge == 1:
                apply(4, "N")
        if symbol == "S" and not atom.GetIsAromatic() and atom.GetTotalDegree() == 2:
            apply(5, "SA")
        if symbol == "H":
            if len(neighbors) != 1:
                fail(f"Indexed hydrogen {i} requires exactly one covalent parent.")
            if neighbors[0].GetSymbol() in {"N", "O", "F", "P", "S"}:
                apply(6, "HD")
            elif neighbors[0].GetSymbol() != "C":
                fail(
                    f"Hydrogen {i} has an unsupported parent for the bounded polar/nonpolar classification."
                )
    rich = isinstance(selection, str) and not is_all(selection)
    selected = select_chemical_atoms(
        original if rich else source,
        states,
        index,
        selection,
        original_frames if rich else frames,
        syntax,
    )
    references = [deepcopy(_REFERENCE), deepcopy(_COMPARISON)]
    items = deepcopy(aromaticity["attribution"]["items"]) + deepcopy(references)
    with _ackredit.scope(CALLER) as provider:
        _ackredit.credit(provider, items, CALLER)
    report = dict(
        schema="molsysmt.atom_type_assignment@1",
        typing_scheme=scheme,
        method=method,
        rule_version=RULE_VERSION,
        rule_order=RULES,
        rule_indices=winners[selected],
        n_matching_rules=match_counts[selected],
        atom_indices=selected,
        n_atoms=states.n_atoms,
        evaluated_atom_indices=np.arange(states.n_atoms, dtype=np.int64),
        coverage="complete",
        chemical_state_index=index,
        chemical_state_id=state.state_id,
        polar_hydrogen_indices=selected[labels[selected] == "HD"],
        nonpolar_hydrogen_indices=selected[labels[selected] == "H"],
        hydrogen_policy="indexed_atoms_only_no_merging",
        parameters=dict(
            aromaticity_method=aromaticity["method"],
            aromaticity_implementation=aromaticity["implementation"],
        ),
        evidence="declared_graph_with_explicit_aromaticity_perception",
        software={"molsysmt": __version__, "rdkit": aromaticity["software"]["rdkit"]},
        references=references,
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=CALLER, items=items
        ),
    )
    return dict(atom_ff_type=labels[selected], report=report)


def _graph_digest(source, report):
    from molsysmt.topology._chemical_graph import chemical_graph_digest

    return chemical_graph_digest(source, report["chemical_state_index"])


def _values_digest(source):
    values = source.molecular_mechanics.atom_ff_type
    payload = json.dumps(
        None if values is None else list(map(str, values)), separators=(",", ":")
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def bind_assignment(source, report):
    bound = deepcopy(report)
    bound.update(
        status="assigned",
        atom_source_indices=np.arange(source.get_n_atoms(), dtype=np.int64),
        chemical_digest=_graph_digest(source, report),
        values_digest=_values_digest(source),
    )
    return bound


def validate_assignment(source, typing_scheme):
    report = getattr(source.molecular_mechanics, "atom_type_assignment", None)
    if report is None:
        return
    if report["typing_scheme"] != typing_scheme:
        fail("Stored atom-type assignment uses a different typing_scheme.")
    if (
        source.topology is None
        or source.chemical_states is None
        or report["chemical_state_index"] >= source.chemical_states.n_chemical_states
        or report.get("status") == "stale"
        or _graph_digest(source, report) != report["chemical_digest"]
        or _values_digest(source) != report["values_digest"]
    ):
        fail(
            "Stored AutoDock types no longer match bound chemistry or values; explicitly recalculate or replace them."
        )
    if source.structures is not None and source.structures.n_structures:
        import pandas as pd

        associated = source._get_structure_chemical_state_indices(resolved=True)
        if np.any(pd.isna(associated)) or np.any(
            np.asarray(associated, dtype=int) != report["chemical_state_index"]
        ):
            fail(
                "Stored AutoDock types do not match the chemical state associated with output structures."
            )


def project_assignment(source, output, indices):
    report = getattr(source.molecular_mechanics, "atom_type_assignment", None)
    if report is None:
        return
    from molsysmt._private.variables import is_all

    if is_all(indices):
        return
    projected = deepcopy(report)
    indices = np.asarray(indices, dtype=np.int64)
    try:
        validate_assignment(source, report["typing_scheme"])
    except StructuralInconsistencyError:
        projected["status"] = "stale"
    else:
        projected.update(
            status="projected",
            chemical_digest=_graph_digest(output, report),
            values_digest=_values_digest(output),
        )
    projected["atom_source_indices"] = report["atom_source_indices"][indices].copy()
    # The original evaluated scope is retained. Per-atom rule evidence and
    # hydrogen indices describe the current projected atom axis.
    projected["rule_indices"] = report["rule_indices"][indices].copy()
    projected["n_matching_rules"] = report["n_matching_rules"][indices].copy()
    labels = np.asarray(output.molecular_mechanics.atom_ff_type, dtype="U2")
    projected["polar_hydrogen_indices"] = np.flatnonzero(labels == "HD")
    projected["nonpolar_hydrogen_indices"] = np.flatnonzero(labels == "H")
    projected["atom_indices"] = np.arange(len(indices), dtype=np.int64)
    output.molecular_mechanics.atom_type_assignment = projected
