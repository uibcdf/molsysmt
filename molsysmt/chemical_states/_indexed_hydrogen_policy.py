"""Apply one explicit stored-H permission policy through canonical native tools."""

from copy import deepcopy

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError


def _value(table, field, index):
    value = table.at[index, field] if field in table else None
    if value is None or pd.isna(value):
        return None
    return value.item() if isinstance(value, np.generic) else value


def normalize(molecular_system, chemical_state, caller):
    from molsysmt import __version__, _ackredit
    from molsysmt._private.preparation_history import append_report
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt.basic import convert, get_form
    from molsysmt.basic import set as assign
    from molsysmt.native import MolSys
    from molsysmt.native._query_domains import compose_query_domains
    from molsysmt.physchem import get_hydrogen_inventory

    def fail(reason):
        raise StructuralInconsistencyError(reason=reason, caller=caller)

    source_forms = get_form(molecular_system)
    if isinstance(source_forms, str) and source_forms in {
        "molsysmt.Topology",
        "molsysmt.TopologyDict",
        "molsysmt.ChemicalStates",
        "molsysmt.ChemicalStatesDict",
        "molsysmt.Structures",
        "molsysmt.StructuresDict",
    }:
        fail("Indexed-H policy requires both stable atom elements and chemical states.")
    source = molecular_system
    if not isinstance(source, MolSys):
        native_domains = {
            "molsysmt.Topology",
            "molsysmt.ChemicalStates",
            "molsysmt.ChemicalStatesDict",
            "molsysmt.Structures",
            "molsysmt.MolecularMechanics",
        }
        # Only native-domain composition declares this conversion option.
        options = (
            {"copy_if_all": False}
            if isinstance(source_forms, (list, tuple))
            and set(source_forms) <= native_domains
            else {}
        )
        source = convert(source, to_form="molsysmt.MolSys", **options)
    if source.topology is None or source.chemical_states is None:
        fail(
            "Indexed-H policy requires stable atom elements and a chemical-states domain."
        )
    states = source.chemical_states
    index = states._resolve_index(
        None if chemical_state == "reference" else chemical_state
    )
    state = states._states[index]
    if states.n_atoms == 0 and len(state.bonds):
        fail("An empty atom domain cannot contain stored bond rows.")
    # Borrow metadata only; the view never escapes or receives any mutation.
    view = compose_query_domains([source.topology, states])
    inventory = get_hydrogen_inventory(view, chemical_state=index)
    if inventory["status"] not in {"available", "empty"}:
        reasons = sorted({item["reason_code"] for item in inventory["issues"]})
        fail(
            "Indexed-H policy requires an available stored inventory: "
            + ", ".join(reasons)
        )
    hydrogens = inventory["explicit_hydrogen_atom_indices"].copy()
    pairs = inventory["parent_hydrogen_pairs"].copy()
    if len(pairs):
        pairs = pairs[np.argsort(pairs[:, 1])]
    if not np.array_equal(pairs[:, 1], hydrogens):
        fail("Every indexed H must have exactly one known non-H parent.")

    attributes, bonds = state.atom_attributes, state.bonds
    flags = []
    for hydrogen in hydrogens:
        for field in ("formal_charge", "n_unpaired_electrons"):
            value = _value(attributes, field, hydrogen)
            if not isinstance(value, int) or isinstance(value, bool) or value != 0:
                fail(f"Indexed H {hydrogen} requires known zero {field}.")
        if _value(attributes, "is_aromatic", hydrogen) is not False:
            fail(f"Indexed H {hydrogen} requires known nonaromaticity.")
        if _value(attributes, "stereochemistry", hydrogen) != "unspecified":
            fail(
                f"Indexed H {hydrogen} has unknown or unsupported atom stereochemistry."
            )
        flag = _value(attributes, "allows_implicit_hydrogens", hydrogen)
        if not isinstance(flag, bool):
            fail(f"Indexed H {hydrogen} requires known implicit-H permission.")
        flags.append(flag)
    hydrogen_set = set(hydrogens.tolist())
    for bond_index in bonds.index:
        if not any(
            _value(bonds, field, bond_index) in hydrogen_set
            for field in ("atom1_index", "atom2_index")
        ):
            continue
        order = _value(bonds, "bond_order", bond_index)
        fraction = _value(bonds, "fractional_bond_order", bond_index)
        if (
            (
                order is not None
                and (
                    not isinstance(order, int) or isinstance(order, bool) or order != 1
                )
            )
            or fraction not in {None, 1.0}
            or (order is None and fraction is None)
            or isinstance(fraction, bool)
        ):
            fail(f"Indexed-H bond {bond_index} requires a declared single bond.")
        if _value(bonds, "is_aromatic", bond_index) is not False:
            fail(f"Indexed-H bond {bond_index} requires known nonaromaticity.")
        if any(
            _value(bonds, field, bond_index) not in {None, "unspecified"}
            for field in ("stereochemistry", "stereo_atom1_index", "stereo_atom2_index")
        ):
            fail(f"Indexed-H bond {bond_index} has unsupported bond stereo.")

    flags = np.asarray(flags, dtype=np.bool_)
    changed = hydrogens[flags].copy()
    result = source.copy(deep=False)
    invalidated = sorted(result.interactions) if len(changed) else []
    if len(changed):
        assign(
            result,
            element="atom",
            selection=changed,
            chemical_state=index,
            allows_implicit_hydrogens=False,
        )
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
        schema="molsysmt.indexed_hydrogen_policy@1",
        method="closed_neutral_terminal_hydrogens",
        rule_version=1,
        status="normalized"
        if len(changed)
        else "unchanged"
        if len(hydrogens)
        else "empty",
        source_forms=source_forms,
        chemical_state_index=int(index),
        atom_correspondence=dict(indices="identity", n_atoms=states.n_atoms),
        hydrogen_atom_indices=hydrogens,
        parent_hydrogen_pairs=pairs,
        original_allows_implicit_hydrogens=flags,
        changed_atom_indices=changed,
        invalidated_analysis_names=invalidated,
        software={"molsysmt": __version__},
        unassessed_checks=[
            "valence",
            "protonation",
            "coordinate_quality",
            "general_hydrogen_canonicalization",
        ],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    append_report(result.chemical_states._states[index], report, index)
    return dict(molecular_system=result, report=report)
