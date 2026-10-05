"""Changing only the order encoding of explicitly marked aromatic relationships."""

from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.chemical_template import _context, _value
from molsysmt._private.smonitor import StructuralInconsistencyError


def normalize(molecular_system, chemical_state, caller):
    from molsysmt import __version__, _ackredit
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt.basic import convert, get_form
    from molsysmt.native import ChemicalStates, MolSys, Topology

    context = _context(molecular_system, chemical_state, "chemical_state", caller)
    state = context["state"]

    def fail(reason):
        raise StructuralInconsistencyError(reason=reason, caller=caller)

    if state is None:
        fail("Aromatic order normalization requires an unambiguous chemical state.")
    bonds = state.bonds
    flags = bonds.get("is_aromatic", pd.Series(pd.NA, index=bonds.index))
    indices = bonds.index[flags.eq(True).fillna(False)].to_numpy(dtype=np.int64)
    orders, fractions, pairs, changed = [], [], [], []
    for index in indices:
        ends = [_value(bonds, field, index) for field in ("atom1_index", "atom2_index")]
        if (
            any(
                not isinstance(end, int)
                or isinstance(end, bool)
                or not 0 <= end < context["n_atoms"]
                for end in ends
            )
            or ends[0] == ends[1]
        ):
            fail(f"Aromatic bond {index} has invalid atom indices.")
        if _value(bonds, "bond_type", index) != "covalent":
            fail(f"Aromatic bond {index} requires a covalent relationship.")
        if any(
            _value(state.atom_attributes, "is_aromatic", end) is False for end in ends
        ):
            fail(f"Aromatic bond {index} contradicts a declared nonaromatic atom.")
        if any(
            _value(bonds, field, index) is not None
            for field in ("stereochemistry", "stereo_atom1_index", "stereo_atom2_index")
        ):
            fail(f"Aromatic bond {index} has unsupported stereo declarations.")
        order, fraction = (
            _value(bonds, "bond_order", index),
            _value(bonds, "fractional_bond_order", index),
        )
        if order not in {None, 1, 2} or fraction not in {None, 1.5}:
            fail(f"Aromatic bond {index} has an incompatible order encoding.")
        pairs.append(ends)
        orders.append(np.nan if order is None else order)
        fractions.append(np.nan if fraction is None else fraction)
        if order is not None or fraction != 1.5:
            changed.append(index)
    if len({tuple(sorted(pair)) for pair in pairs}) != len(pairs):
        fail("Aromatic bonds must have unique atom pairs.")

    if isinstance(molecular_system, MolSys):
        result = molecular_system.copy()
    elif isinstance(molecular_system, Topology):
        topology = molecular_system.copy()
        result = MolSys._from_partial_domains(
            topology=topology, chemical_states=topology._chemical_states_domain
        )
    elif isinstance(context["source"], ChemicalStates):
        result = MolSys._from_partial_domains(chemical_states=context["source"].copy())
    else:
        result = convert(molecular_system, to_form="molsysmt.MolSys").copy()
    state_index = context["chemical_state_index"]
    invalidated = sorted(result.interactions) if changed else []
    if changed:
        states = result.chemical_states.copy()
        target = states._states[state_index].bonds
        # Native nullable columns retain unknown integer orders without zero sentinels.
        if "fractional_bond_order" not in target:
            target["fractional_bond_order"] = pd.Series(
                pd.NA, index=target.index, dtype="Float64"
            )
        if "bond_order" in target:
            target.loc[indices, "bond_order"] = pd.NA
        target.loc[indices, "fractional_bond_order"] = 1.5
        result.chemical_states = states
    items = [
        dict(
            id=f"software:molsysmt:{__version__}",
            type="software",
            **deepcopy(SOFTWARE["molsysmt"]),
            version=__version__,
            roles=["executed_software"],
        )
    ]
    report = dict(
        schema="molsysmt.aromatic_bond_normalization@1",
        status="normalized" if changed else "unchanged",
        method="declared_aromatic_fractional_order",
        rule_version=1,
        source_forms=get_form(molecular_system),
        chemical_state_index=state_index,
        bond_indices=indices.copy(),
        bonded_atom_pairs=np.asarray(pairs, dtype=np.int64).reshape(-1, 2),
        original_bond_orders=np.asarray(orders, dtype=np.float64),
        original_fractional_bond_orders=np.asarray(fractions, dtype=np.float64),
        changed_bond_indices=np.asarray(changed, dtype=np.int64),
        unassessed_bond_indices=bonds.index[flags.isna()].to_numpy(dtype=np.int64),
        invalidated_analysis_names=invalidated,
        connectivity_completeness=state.connectivity_completeness,
        software={"molsysmt": __version__},
        unassessed_checks=[
            "aromaticity_perception",
            "valence",
            "resonance_normalization",
            "environmental_protonation",
        ],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    from molsysmt._private.preparation_history import append_report

    append_report(result.chemical_states._states[state_index], report, state_index)
    return dict(molecular_system=result, report=report)
