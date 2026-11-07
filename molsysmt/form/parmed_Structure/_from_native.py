"""Building ParmEd objects from explicitly supplied native domains."""

import math

import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.atom_types import CHEMICAL_ATOM_TYPES
from molsysmt._private.smonitor import NotCompatibleConversionError

_NONAROMATIC_QUALITATIVE_NAMES = {
    0: "ZERO",
    1: "SINGLE",
    2: "DOUBLE",
    3: "TRIPLE",
    4: "QUADRUPLE",
    5: "QUINTUPLE",
    6: "HEXTUPLE",
    1.5: "ONEANDAHALF",
    2.5: "TWOANDAHALF",
    3.5: "THREEANDAHALF",
    4.5: "FOURANDAHALF",
    5.5: "FIVEANDAHALF",
}


def _known(value):
    return value is not None and not pd.isna(value)


def _serial(value):
    """Accept integer labels only when the target preserves their spelling."""
    try:
        number = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return number if str(number) == str(value) else None


def _numeric_order(bond):
    fractional = getattr(bond, "fractional_bond_order", None)
    order = fractional if _known(fractional) else getattr(bond, "bond_order", None)
    if not _known(order):
        return None
    order = float(order)
    return order if math.isfinite(order) and order >= 0 else None


def box_limitation(box):
    """Check raw row-vector orientation before crystallographic reduction."""
    if box is None:
        return None
    values = np.asarray(puw.get_value(box, to_unit="nm"), dtype=float)
    if values.size == 0:
        return None
    if not np.isfinite(values).all():
        return "ParmEd requires finite periodic box vectors."
    # ParmEd stores lengths/angles, whose inverse has lower-triangular vectors
    # and positive diagonals. Compare raw components at the cell's own scale;
    # the PBC length/angle rounding must not hide a rotation or handedness loss.
    scale = np.max(np.abs(values), axis=(1, 2))
    tolerance = 64 * np.finfo(float).eps * scale
    forbidden = np.abs(values[:, [0, 0, 1], [1, 2, 2]])
    diagonals = np.diagonal(values, axis1=1, axis2=2)
    if np.any(forbidden > tolerance[:, None]) or np.any(diagonals <= 0):
        return (
            "ParmEd lengths/angles cannot preserve rotated, reflected, or singular "
            "box vectors without changing the coordinate convention."
        )
    return None


def export_limitations(
    topology, chemical_states=None, structures=None, molecular_mechanics=None
):
    """Return bounded target limitations without importing ParmEd."""
    issues = []
    for table, column in ((topology.atoms, "atom_id"), (topology.groups, "group_id")):
        if any(_serial(value) is None for value in table[column]):
            issues.append(
                (
                    column,
                    f"ParmEd requires integer {column} labels with canonical spelling.",
                    "topology",
                )
            )
    for value in topology.atoms["atom_type"]:
        if _known(value) and value not in CHEMICAL_ATOM_TYPES:
            issues.append(
                (
                    "atom_type",
                    "ParmEd export requires explicit chemical element symbols; force-field types belong in atom_ff_type.",
                    "topology",
                )
            )
            break
    if topology.atoms["isotope"].notna().any():
        issues.append(
            (
                "isotope",
                "ParmEd export does not encode explicit isotope identities; an average element mass cannot replace them.",
                "topology",
            )
        )
    group_sequence = topology.atoms["group_index"].tolist()
    runs = [
        value
        for index, value in enumerate(group_sequence)
        if index == 0 or value != group_sequence[index - 1]
    ]
    if len(runs) != len(set(runs)):
        issues.append(
            (
                "group_index",
                "ParmEd requires each group's atoms to be contiguous; this export does not reorder coordinates or split groups.",
                "topology",
            )
        )
    if any(
        group["chain_index"].nunique(dropna=False) > 1
        for _, group in topology.atoms.groupby("group_index")
    ):
        issues.append(
            (
                "chain_index",
                "ParmEd assigns one chain label per group and cannot preserve multiple chains within one group.",
                "topology",
            )
        )
    if (
        chemical_states is not None
        and chemical_states.n_chemical_states > 1
        and chemical_states.reference_chemical_state_index is None
    ):
        issues.append(
            (
                "chemical_state_index",
                "ParmEd export requires an unambiguous reference chemical state; no state is chosen implicitly.",
                "chemical_state",
            )
        )
    elif chemical_states is not None and chemical_states.n_chemical_states:
        state = chemical_states._resolve_chemical_state()
        for bond in state.bonds.itertuples(index=False):
            if _numeric_order(bond) is None:
                issues.append(
                    (
                        "bond_order",
                        "ParmEd requires a finite nonnegative numeric order for every exported bond; an unknown order cannot be replaced by one.",
                        "chemical_state",
                    )
                )
                break
            integral = getattr(bond, "bond_order", None)
            fractional = getattr(bond, "fractional_bond_order", None)
            if (
                _known(integral)
                and _known(fractional)
                and float(integral) != float(fractional)
            ):
                issues.append(
                    (
                        "fractional_bond_order",
                        "ParmEd has one numeric order slot and cannot preserve distinct nominal and fractional orders for the same bond.",
                        "chemical_state",
                    )
                )
                break
        for bond in state.bonds.itertuples(index=False):
            kind = getattr(bond, "bond_type", None)
            if not _known(kind) or kind not in {"covalent", "dative"}:
                issues.append(
                    (
                        "bond_type",
                        f"ParmEd export does not map the supplied bond type {kind!r}.",
                        "chemical_state",
                    )
                )
                break
            aromatic = getattr(bond, "is_aromatic", None)
            if _known(kind) and kind == "dative" and _known(aromatic) and aromatic:
                issues.append(
                    (
                        "bond_is_aromatic",
                        "ParmEd has one qualitative bond slot and cannot encode a bond as both dative and aromatic.",
                        "chemical_state",
                    )
                )
                break
            if _known(kind) and kind == "dative" and not _known(aromatic):
                issues.append(
                    (
                        "bond_is_aromatic",
                        "ParmEd's dative qualitative type denotes a nonaromatic bond and cannot retain an unknown aromaticity independently.",
                        "chemical_state",
                    )
                )
                break
            if (
                _known(aromatic)
                and not aromatic
                and _numeric_order(bond) not in _NONAROMATIC_QUALITATIVE_NAMES
            ):
                issues.append(
                    (
                        "bond_is_aromatic",
                        "ParmEd has no nonaromatic qualitative type for the supplied numeric order.",
                        "chemical_state",
                    )
                )
                break
    if molecular_mechanics is not None:
        atoms_ff = molecular_mechanics.atoms_ff
        charges = (
            None
            if atoms_ff is None or "partial_charge" not in atoms_ff
            else atoms_ff["partial_charge"]
        )
        if charges is not None and any(
            not _known(value) or not math.isfinite(float(value)) for value in charges
        ):
            issues.append(
                (
                    "partial_charge",
                    "ParmEd returns zero for an unassigned partial charge; explicitly missing source charges cannot be preserved by that interface.",
                    "molecular_mechanics",
                )
            )
    reason = box_limitation(None if structures is None else structures.box)
    if reason is not None:
        issues.append(("box", reason, "structures"))
    return issues


def reject_limitations(issues, source_form):
    if issues:
        raise NotCompatibleConversionError(
            from_form=source_form,
            to_form="parmed.Structure",
            missing_arguments=tuple(issue[0] for issue in issues),
            caller="molsysmt.form.parmed_Structure",
            message=" ".join(issue[1] for issue in issues),
        )


def state_association_limitations(item):
    states = item.chemical_states
    if states is None or not states.n_chemical_states or item.structures is None:
        return []
    associations = item._get_structure_chemical_state_indices(resolved=False)
    reference = states.reference_chemical_state_index
    if states.n_chemical_states > 1 and any(
        not _known(value) for value in associations
    ):
        return [
            (
                "structure_chemical_state_index",
                "Selected structures have unresolved chemical-state associations; reference chemistry cannot be assigned to them implicitly.",
                "chemical_state",
            )
        ]
    if any(_known(value) and value != reference for value in associations):
        return [
            (
                "structure_chemical_state_index",
                "Selected structures refer to chemistry other than the exported reference state.",
                "chemical_state",
            )
        ]
    return []


def openmm_export_limitations(item):
    """Inspect represented OpenMM fields without importing either provider."""
    issues = []
    for elements, attribute in (
        (item.atoms(), "atom_id"),
        (item.residues(), "group_id"),
    ):
        if any(_serial(value.id) is None for value in elements):
            issues.append(
                (
                    attribute,
                    f"ParmEd requires integer {attribute} labels with canonical spelling.",
                    "topology",
                )
            )
    for bond in item.bonds():
        if bond.order is None or not math.isfinite(float(bond.order)) or bond.order < 0:
            issues.append(
                (
                    "bond_order",
                    "ParmEd requires an explicit finite nonnegative numeric bond order; an unknown order cannot be replaced by one.",
                    "chemical_state",
                )
            )
            break
    if any(
        bond.type is not None
        and str(bond.type) not in {"Single", "Double", "Triple", "Aromatic"}
        for bond in item.bonds()
    ):
        issues.append(
            (
                "bond_type",
                "ParmEd export has no faithful qualitative mapping for the supplied OpenMM bond type.",
                "chemical_state",
            )
        )
    vectors = item.getPeriodicBoxVectors()
    box = (
        None
        if vectors is None
        else puw.quantity([puw.get_value(vectors, to_unit="nm")], "nm")
    )
    reason = box_limitation(box)
    if reason:
        issues.append(("box", reason, "structures"))
    return issues


def set_box(target, box):
    """Store independent per-structure cells using the owning PBC tools."""
    if box is None or len(box) == 0:
        return
    from molsysmt.pbc import get_lengths_and_angles_from_box

    lengths, angles = get_lengths_and_angles_from_box(box)
    target.box = np.column_stack(
        (
            puw.get_value(lengths, to_unit="angstrom"),
            puw.get_value(angles, to_unit="degrees"),
        )
    )


def export_native(
    topology, *, chemical_states=None, structures=None, molecular_mechanics=None
):
    """Build a detached provider object without recovering attached domains."""
    reject_limitations(
        export_limitations(topology, chemical_states, structures, molecular_mechanics),
        "molsysmt.MolSys"
        if chemical_states is not None
        or structures is not None
        or molecular_mechanics is not None
        else "molsysmt.Topology",
    )
    import parmed as pmd
    from parmed.periodic_table import AtomicNum, Mass
    from parmed.topologyobjects import QualitativeBondType

    result = pmd.Structure()
    state = (
        None
        if chemical_states is None or not chemical_states.n_chemical_states
        else chemical_states._resolve_chemical_state()
    )
    formal = None if state is None else state.get_atom_attribute("formal_charge")
    aromatic = None if state is None else state.get_atom_attribute("is_aromatic")
    charges = (
        None if molecular_mechanics is None else molecular_mechanics.partial_charge
    )
    ff_types = None if molecular_mechanics is None else molecular_mechanics.atom_ff_type
    groups = []
    group_chains = (
        topology.atoms.groupby("group_index")["chain_index"].first().to_dict()
    )
    for group in topology.groups.itertuples(index=True):
        chain_index = group_chains.get(group.Index)
        chain = (
            ""
            if not _known(chain_index)
            else str(topology.chains.iloc[int(chain_index)].chain_id)
        )
        provider_group = pmd.Residue(
            str(group.group_name),
            _serial(group.group_id),
            chain=chain,
            list=result.residues,
        )
        result.residues.append(provider_group)
        groups.append(provider_group)
    for index, atom in enumerate(topology.atoms.itertuples(index=False)):
        element = atom.atom_type
        provider_atom = pmd.Atom(
            name=atom.atom_name,
            number=_serial(atom.atom_id),
            atomic_number=AtomicNum[element] if _known(element) else 0,
            # Element reference masses are not force-field parameterization.
            mass=Mass[element] if _known(element) else 0,
            type=""
            if ff_types is None or not _known(ff_types[index])
            else str(ff_types[index]),
            charge=None if charges is None else float(charges[index]),
            formal_charge=None
            if formal is None or not _known(formal.iloc[index])
            else int(formal.iloc[index]),
            aromatic=None
            if aromatic is None or not _known(aromatic.iloc[index])
            else bool(aromatic.iloc[index]),
        )
        groups[int(atom.group_index)].add_atom(provider_atom)
        result.atoms.append(provider_atom)
    if state is not None:
        for bond in state.bonds.itertuples(index=False):
            flag = getattr(bond, "is_aromatic", None)
            kind = getattr(bond, "bond_type", None)
            qualitative = None
            if _known(kind) and kind == "dative":
                qualitative = QualitativeBondType.DATIVE
            elif _known(flag) and flag:
                qualitative = QualitativeBondType.AROMATIC
            elif _known(flag) and not flag:
                name = _NONAROMATIC_QUALITATIVE_NAMES.get(_numeric_order(bond))
                qualitative = (
                    None if name is None else getattr(QualitativeBondType, name)
                )
            result.bonds.append(
                pmd.Bond(
                    result.atoms[int(bond.atom1_index)],
                    result.atoms[int(bond.atom2_index)],
                    order=_numeric_order(bond),
                    qualitative_type=qualitative,
                )
            )
    if structures is not None:
        if structures.coordinates is not None:
            result.coordinates = np.array(
                puw.get_value(structures.coordinates, to_unit="angstrom"), copy=True
            )
        set_box(result, structures.box)
    return result
