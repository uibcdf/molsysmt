"""Composing supported build reports without duplicating their scientific rules."""

from copy import deepcopy

import numpy as np


def _peptide_record(report):
    """Retain geometry with explicit units and omit the duplicated group audit."""
    from pyunitwizard.record import QuantityRecord

    output = {
        key: deepcopy(value) for key, value in report.items() if key != "group_coverage"
    }
    for name in ("max_bond_length", "effective_max_bond_length"):
        output["parameters"][name] = QuantityRecord.from_quantity(
            output["parameters"][name],
            field=f"covalent_inference.peptide.{name}",
            unit="nm",
        ).to_dict()
    output["distances"] = QuantityRecord.from_quantity(
        output["distances"],
        field="covalent_inference.peptide.distances",
        unit="nm",
    ).to_dict()
    for link in output["links"]:
        if link["distance"] is not None:
            link["distance"] = QuantityRecord.from_quantity(
                link["distance"],
                field="covalent_inference.peptide.link.distance",
                unit="nm",
            ).to_dict()
    return output


def apply(source, selection, structure_indices, chemical_state, return_report, syntax):
    """Apply missing eligible pairs to a copy and retain original report domains."""
    from molsysmt._private.preparation_history import append_report
    from molsysmt._private.smonitor import StructuralInconsistencyError
    from molsysmt.basic import convert, get_form
    from molsysmt.build import get_covalent_bond_candidates, get_peptide_bond_candidates
    from molsysmt.native import MolSys, Topology

    source_forms = get_form(source)
    if isinstance(source, MolSys):
        output = source.copy()
    elif isinstance(source, Topology):
        topology = source.copy()
        output = MolSys._from_partial_domains(
            topology=topology,
            chemical_states=topology._chemical_states_domain,
        )
    else:
        output = convert(source, to_form="molsysmt.MolSys", get_missing_bonds=False)
    heavy = get_covalent_bond_candidates(
        output,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        syntax=syntax,
        skip_digestion=True,
    )
    state_index = heavy["chemical_state_index"]
    if state_index is None:
        raise StructuralInconsistencyError(
            reason="Native covalent inference requires one resolved chemical state.",
            caller="molsysmt.build.infer_covalent_bonds",
        )
    hydrogen = get_covalent_bond_candidates(
        output,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        syntax=syntax,
        method="observed_hydrogen_template_consensus",
        skip_digestion=True,
    )
    peptide = get_peptide_bond_candidates(
        output,
        selection=selection,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        syntax=syntax,
        method="unique_backbone_distance",
        skip_digestion=True,
    )
    candidate_methods = {}
    methods = [evidence["method"] for evidence in (heavy, hydrogen, peptide)]
    for method_index, evidence in enumerate((heavy, hydrogen, peptide)):
        for pair in evidence["bonded_atom_pairs"].tolist():
            # These families are disjoint: heavy/H intra-group or heavy inter-group.
            candidate_methods[tuple(pair)] = method_index
    state = output.chemical_states._states[state_index]
    original = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    stored = {tuple(sorted(pair)) for pair in original.tolist()}
    added = sorted(set(candidate_methods) - stored)
    history_index = len(state._preparation_history)
    invalidated = sorted(output.interactions) if added else []
    if added:
        with output._invalidating_interaction_frames("all"):
            output.topology._append_chemical_state_bonds(
                added,
                types="covalent",
                evidence="inferred",
                state_index=state_index,
                provenance_index=history_index,
            )
            state.connectivity_completeness = "partial"
            with output.topology._using_chemical_state(state_index):
                output.topology.rebuild_components(
                    redefine_ids=False,
                    redefine_types=False,
                    redefine_names=False,
                )
            # Rebuild semantic hierarchy only for the unchanged reference state.
            if output.chemical_states._reference_index == state_index:
                output.topology.rebuild_molecules(force=True)
                output.topology.rebuild_entities(force=True)
    final = {
        tuple(sorted(pair)): index
        for index, pair in enumerate(
            state.bonds[["atom1_index", "atom2_index"]]
            .to_numpy(dtype=np.int64)
            .tolist()
        )
    }
    pairs = sorted(candidate_methods)
    report = dict(
        schema="molsysmt.covalent_inference@1",
        method="supported_group_templates",
        engine="MolSysMT",
        rule_version=1,
        status="added" if added else "unchanged",
        source_forms=source_forms,
        n_atoms=heavy["n_atoms"],
        n_structures=0 if output.structures is None else output.structures.n_structures,
        atom_indices=heavy["atom_indices"].copy(),
        structure_index=heavy["structure_index"],
        chemical_state_index=state_index,
        software=deepcopy(heavy["software"]),
        bonded_atom_pairs=np.asarray(pairs, dtype=np.int64).reshape(-1, 2),
        candidate_methods=methods,
        candidate_method_indices=np.asarray(
            [candidate_methods[pair] for pair in pairs], dtype=np.int8
        ),
        added_bonded_atom_pairs=np.asarray(added, dtype=np.int64).reshape(-1, 2),
        added_bond_indices=np.asarray([final[pair] for pair in added], dtype=np.int64),
        n_added_bonds=len(added),
        preparation_history_index=history_index,
        source_bond_correspondence=np.asarray(
            [
                (index, final[tuple(sorted(pair))])
                for index, pair in enumerate(original.tolist())
            ],
            dtype=np.int64,
        ).reshape(-1, 2),
        heavy_groups=deepcopy(heavy["groups"]),
        hydrogen_groups=[
            {
                key: deepcopy(group[key])
                for key in (
                    "group_index",
                    "status",
                    "reason_codes",
                    "n_candidates",
                    "hydrogen_coverage",
                )
            }
            for group in hydrogen["groups"]
        ],
        peptide=_peptide_record(peptide),
        invalidated_analysis_names=invalidated,
        connectivity_completeness=state.connectivity_completeness,
        unassessed_checks=[
            "bond_orders",
            "valence",
            "protonation",
            "hydrogen_placement",
            "hydrogen_inventory_completeness",
            "polymer_sequence_order",
            "terminal_caps",
            "unsupported_groups",
            "disulfides",
            "metal_coordination",
        ],
    )
    append_report(state, report, state_index)
    return dict(molecular_system=output, report=report) if return_report else output
