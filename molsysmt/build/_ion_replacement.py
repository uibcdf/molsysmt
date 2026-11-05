"""Count resolution and sparse placement for whole-water ion replacement."""

from copy import deepcopy

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

CALLER = "molsysmt.build.add_ions"
SPECIES = {
    "Na+": ("NA", "NA", "Na", 1),
    "K+": ("K", "K", "K", 1),
    "Li+": ("LI", "LI", "Li", 1),
    "Rb+": ("RB", "RB", "Rb", 1),
    "Cs+": ("CS", "CS", "Cs", 1),
    "Cl-": ("CL", "CL", "Cl", -1),
    "Br-": ("BR", "BR", "Br", -1),
    "F-": ("F", "F", "F", -1),
    "I-": ("I", "I", "I", -1),
}
REFERENCE = dict(
    id="reference:openmm:ba0aa236:water_replacement",
    type="web",
    title="OpenMM Modeller._addIons: random whole-water replacement",
    url=(
        "https://github.com/openmm/openmm/blob/"
        "ba0aa236ac4d07241382869604c4d2ea58c4f3f5/"
        "wrappers/python/openmm/app/modeller.py#L259"
    ),
    roles=["methodological_inspiration"],
)


def fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


def nonnegative_integer(value, name, *, neutralize=False, caller=CALLER):
    if neutralize and isinstance(value, str) and value == "neutralize":
        return value
    if isinstance(value, (int, np.integer)) and not isinstance(value, (bool, np.bool_)):
        if value >= 0:
            return int(value)
    raise ArgumentError(
        name,
        value=value,
        caller=caller,
        message="Supply a nonnegative integer"
        + (" or 'neutralize'." if neutralize else "."),
    )


def scalar_quantity(value, unit, name, *, positive=False):
    try:
        if isinstance(value, str):
            from molsysmt._private.argdigest.argument._quantity_parsing import (
                parse_quantity_string,
            )

            value = parse_quantity_string(name, value, caller=CALLER)
        number = np.asarray(puw.get_value(value, to_unit=unit))
        if number.shape != () or not np.isfinite(number):
            raise ValueError("Expected one finite quantity.")
        number = float(number)
        if number < 0 or positive and number == 0:
            raise ValueError("Quantity must have the required positive sign.")
        return number
    except Exception as error:
        raise ArgumentError(
            name,
            value=value,
            caller=CALLER,
            message=f"Supply one finite {'positive' if positive else 'nonnegative'} quantity in {unit}.",
        ) from error


def charge_total(source, expected, charge_source):
    from molsysmt._private.partial_charges import _charge_value

    if expected is not None:
        value, origin = _charge_value(expected), "caller_declaration"
        formal = source.chemical_states._states[0].atom_attributes.get("formal_charge")
        if (
            formal is not None
            and not formal.isna().any()
            and abs(float(formal.sum()) - value) > 1e-4
        ):
            fail(
                "The declared total conflicts with the complete source formal-charge inventory."
            )
    elif charge_source == "formal_charge":
        values = source.chemical_states._states[0].atom_attributes.get("formal_charge")
        if values is None or values.isna().any():
            fail(
                "Neutralization requires complete formal charges, stored partial charges or an explicit expected_total_charge."
            )
        value, origin = float(values.sum()), "chemical_states.formal_charge"
    elif charge_source == "partial_charge":
        mechanics = source.molecular_mechanics
        values = None if mechanics is None else mechanics.partial_charge
        if values is None:
            fail(
                "Neutralization requested stored partial charges, but no assignment is available."
            )
        # Native MolecularMechanics stores this column numerically in e.
        values = np.asarray(values, dtype=float)
        if values.shape != (source.topology.n_atoms,) or not np.isfinite(values).all():
            fail(
                "Neutralization requires finite partial charges for every source atom."
            )
        value, origin = float(values.sum()), "molecular_mechanics.partial_charge"
    else:
        from molsysmt.physchem import get_charge

        value = float(
            puw.get_value(
                get_charge(source, element="system", definition="physical_pH7"),
                to_unit="elementary_charge",
            )
        )
        origin = "tabulated_physical_pH7_approximation"
    if not np.isfinite(value) or abs(value - np.rint(value)) > 1e-4:
        fail(
            "Monovalent neutralization requires a total charge within 1e-4 e of an integer; do not silently round a fractional declaration."
        )
    return int(np.rint(value)), origin


def resolve_counts(n_cations, n_anions, charge, n_waters, concentration):
    if n_cations == "neutralize" and n_anions == "neutralize":
        positive, negative = max(-charge, 0), max(charge, 0)
    elif n_cations == "neutralize":
        positive, negative = n_anions - charge, n_anions
    elif n_anions == "neutralize":
        positive, negative = n_cations, charge + n_cations
    else:
        positive, negative = n_cations, n_anions
    if positive < 0 or negative < 0:
        fail(
            "The explicit count and the sign of the neutralizing species cannot neutralize this total charge."
        )
    available = n_waters - positive - negative
    if available < 0:
        fail(
            "The requested base ion population exceeds the number of replaceable waters."
        )
    # OpenMM's water-count proxy, with round-half-up and base replacements excluded.
    pairs = int(np.floor(available * concentration / 55.4 + 0.5))
    positive, negative = positive + pairs, negative + pairs
    if positive + negative > n_waters:
        fail("The requested salt population exceeds the number of replaceable waters.")
    return positive, negative, pairs


def water_candidates(source):
    """Identify complete declared water molecules, including extra sites."""
    from molsysmt.basic import get

    topology = source.topology
    try:
        membership = np.asarray(
            get(source, element="atom", molecule_index=True), dtype=np.int64
        )
    except (TypeError, ValueError) as error:
        raise StructuralInconsistencyError(
            reason="Ion replacement requires declared molecule membership for every atom.",
            caller=CALLER,
        ) from error
    if np.any(membership < 0) or np.any(membership >= topology.n_molecules):
        fail("Ion replacement requires declared molecule membership for every atom.")
    types = topology.molecules["molecule_type"].fillna("").to_numpy()
    water_molecules = np.flatnonzero(np.asarray(types == "water", dtype=bool))
    water_atoms = np.isin(membership, water_molecules)
    oxygens = np.flatnonzero(
        water_atoms
        & np.asarray(topology.atoms["atom_type"].fillna("") == "O", dtype=bool)
    )
    if len(oxygens) != len(water_molecules) or len(
        np.unique(membership[oxygens])
    ) != len(water_molecules):
        fail(
            "Every declared water molecule must contain exactly one oxygen replacement site."
        )
    state = source.chemical_states._states[0]
    if len(state.bonds):
        first = state.bonds["atom1_index"].to_numpy(dtype=np.int64)
        second = state.bonds["atom2_index"].to_numpy(dtype=np.int64)
        if np.any(
            (water_atoms[first] | water_atoms[second])
            & (membership[first] != membership[second])
        ):
            fail(
                "A declared water is covalently bonded to another molecule; resolve its chemical identity before ion replacement."
            )
    formal = state.atom_attributes.get("formal_charge")
    assignments = []
    if formal is not None:
        assignments.append(formal.to_numpy(dtype=float, na_value=np.nan))
    mechanics = source.molecular_mechanics
    if mechanics is not None and mechanics.partial_charge is not None:
        assignments.append(np.asarray(mechanics.partial_charge, dtype=float))
    for values in assignments:
        if values.shape != (topology.n_atoms,):
            fail("Stored charge assignments must align with the source atom axis.")
        known = np.isfinite(values)
        missing = np.bincount(
            membership[water_atoms & ~known], minlength=topology.n_molecules
        )
        totals = np.bincount(
            membership[water_atoms & known],
            weights=values[water_atoms & known],
            minlength=topology.n_molecules,
        )
        if np.any(
            (missing[water_molecules] == 0) & (np.abs(totals[water_molecules]) > 1e-4)
        ):
            fail(
                "Ion replacement assumes neutral waters, but a complete stored assignment declares a charged water molecule."
            )
    return oxygens, membership, water_atoms


def place(
    source, oxygens, water_atoms, count, solute_distance, ion_distance, rng, attempts
):
    """Use shared Rust cell lists; never construct a dense water-pair matrix."""
    from molsysmt.structure import get_neighbors

    eligible = np.ones(len(oxygens), dtype=bool)
    nonwater = np.flatnonzero(~water_atoms)
    if len(nonwater):
        offsets, _, _ = get_neighbors(
            source,
            selection=oxygens,
            selection_2=nonwater,
            threshold=puw.quantity(solute_distance, "nm"),
            pbc=True,
            output_type="csr",
        )
        eligible &= np.diff(offsets) == 0
    # Existing ions need the ion-specific clearance as well as solute clearance.
    if ion_distance > solute_distance:
        from molsysmt.basic import select

        ions = select(source, selection='molecule_type == "ion"')
        if len(ions):
            offsets, _, _ = get_neighbors(
                source,
                selection=oxygens,
                selection_2=ions,
                threshold=puw.quantity(ion_distance, "nm"),
                pbc=True,
                output_type="csr",
            )
            eligible &= np.diff(offsets) == 0
    candidates = np.flatnonzero(eligible)
    if len(candidates) < count:
        fail(
            f"Only {len(candidates)} waters satisfy the source clearance, but {count} ions were requested."
        )
    offsets, neighbors, _ = get_neighbors(
        source,
        selection=oxygens,
        threshold=puw.quantity(ion_distance, "nm"),
        pbc=True,
        output_type="csr",
    )
    for attempt in range(1, attempts + 1):
        blocked = ~eligible.copy()
        chosen = []
        for index in rng.permutation(candidates):
            if blocked[index]:
                continue
            chosen.append(index)
            if len(chosen) == count:
                return np.asarray(chosen, dtype=np.int64), attempt
            blocked[index] = True
            blocked[neighbors[offsets[index] : offsets[index + 1]]] = True
    fail(
        f"Could not place {count} ions with the specified periodic distances after {attempts} bounded random greedy attempts. Reduce the counts or clearances, enlarge the box, or choose another seed."
    )


def build_ions(species, coordinates):
    # Shared with solvation; the general constructor lives behind this operation.
    group, atom, element, charge = SPECIES[species]
    result = _build_ions(group, atom, element, coordinates)
    result.chemical_states._states[0].set_atom_attribute(
        "formal_charge", np.full(len(coordinates), charge, dtype=np.int16)
    )
    result.chemical_states._states[0].connectivity_completeness = "complete"
    return result


def attribute(report):
    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import SOFTWARE

    references = [deepcopy(REFERENCE)] if report["added"]["total"] else []
    items = deepcopy(references)
    for name, version in report["software"].items():
        items.append(
            dict(
                id=f"software:{name}:{version}",
                type="software",
                **deepcopy(SOFTWARE.get(name, dict(title=name))),
                version=version,
                roles=["executed_software"],
            )
        )
    report["references"] = references
    report["attribution"] = dict(
        schema="molsysmt.scientific_attribution@1", target=CALLER, items=items
    )
    with _ackredit.scope(CALLER) as provider:
        _ackredit.credit(provider, items, CALLER, contextual=True)


def _build_ions(ion_name, atom_name, atom_type, positions):
    """Build a MolSys with single-atom ion groups at the given positions.

    Parameters
    ----------
    ion_name : str
        Group/residue name (PDB convention, e.g. 'NA', 'CL').
    atom_name : str
        Atom name (same as group name for monatomic ions).
    atom_type : str
        Element symbol (e.g. 'Na', 'Cl').
    positions : np.ndarray, shape (n_ions, 3)
        Coordinates in nm for each ion.

    Returns
    -------
    molsysmt.MolSys
    """
    import pandas as pd

    from molsysmt.native import MolSys, Structures

    n_ions = positions.shape[0]

    result = MolSys(
        n_atoms=n_ions,
        n_groups=n_ions,
        n_components=n_ions,
        n_molecules=n_ions,
        n_entities=0,
        n_chains=1,
        n_bonds=0,
    )
    new_topo = result.topology
    new_topo.atoms["atom_id"] = pd.array(
        [str(i + 1) for i in range(n_ions)], dtype="string"
    )
    new_topo.atoms["atom_name"] = np.full(n_ions, atom_name, dtype=object)
    new_topo.atoms["atom_type"] = np.full(n_ions, atom_type, dtype=object)
    new_topo.atoms["group_index"] = pd.array(
        np.arange(n_ions, dtype=np.int64), dtype="Int64"
    )
    result.chemical_states._set_component_indices(np.arange(n_ions, dtype=np.int64))
    new_topo.atoms["chain_index"] = pd.array(
        np.zeros(n_ions, dtype=np.int64), dtype="Int64"
    )

    new_topo.groups["group_id"] = pd.array(
        [str(i + 1) for i in range(n_ions)], dtype="string"
    )
    new_topo.groups["group_name"] = np.full(n_ions, ion_name, dtype=object)
    new_topo.groups["group_type"] = np.full(n_ions, "ion", dtype=object)
    new_topo.groups["molecule_index"] = pd.array(
        np.arange(n_ions, dtype=np.int64), dtype="Int64"
    )

    new_topo.chains["chain_id"] = pd.array(["ION"], dtype="string")
    new_topo.chains["chain_name"] = [None]
    new_topo.chains["chain_type"] = [None]

    xyz = positions.reshape(1, n_ions, 3)
    new_struc = Structures(
        coordinates=puw.quantity(xyz, "nm"),
        structure_id=np.array(["1"], dtype=object),
    )

    # Declare stable hierarchy once during construction; later chemistry edits
    # must not be needed to recover solvent/ion molecule labels.
    new_topo.rebuild_molecules(redefine_indices=False)
    new_topo.rebuild_entities()
    result.structures = new_struc
    return result
