"""Assembling native domains from explicit CTAB data and validating output."""

import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.ctfile import AtomRecord, BondRecord, CTRecord, _fail


def to_native(record, *, discard_properties=False):
    from molsysmt.native import MolSys, Structures, Topology

    if not isinstance(discard_properties, bool):
        _fail("discard_properties must be a boolean.")
    if record.properties and not discard_properties:
        _fail(
            "SD property blocks have no native storage yet; explicitly set "
            "discard_properties=True to discard them, or keep the source SDF."
        )
    topology = Topology(n_atoms=len(record.atoms))
    topology.atoms["atom_id"] = [str(atom.serial) for atom in record.atoms]
    topology.atoms["atom_name"] = [
        f"{atom.element}{atom.serial}" for atom in record.atoms
    ]
    topology.atoms["atom_type"] = [atom.element for atom in record.atoms]
    topology.atoms["isotope"] = pd.array(
        [atom.isotope for atom in record.atoms], dtype="UInt16"
    )
    for name in ("formal_charge", "n_unpaired_electrons"):
        topology._set_chemical_state_atom_attribute(
            name, [getattr(atom, name) for atom in record.atoms]
        )
    mapping = {atom.serial: i for i, atom in enumerate(record.atoms)}
    aromatic_atoms = set()
    for bond in record.bonds:
        if bond.order == 4:
            aromatic_atoms.update((mapping[bond.atom1], mapping[bond.atom2]))
    # A Kekule graph does not declare that its atoms are nonaromatic. Perception
    # belongs to physchem; the reader only records affirmative aromatic evidence.
    topology._set_chemical_state_atom_attribute(
        "is_aromatic",
        [True if i in aromatic_atoms else pd.NA for i in range(len(record.atoms))],
    )
    rows = [
        {
            "atom1_index": mapping[bond.atom1],
            "atom2_index": mapping[bond.atom2],
            "bond_id": str(bond.serial),
            "bond_type": "dative" if bond.order == 9 else "covalent",
            "bond_order": bond.order if bond.order in {1, 2, 3} else pd.NA,
            "fractional_bond_order": 1.5 if bond.order == 4 else pd.NA,
            "is_aromatic": True if bond.order == 4 else pd.NA,
            "donor_atom_index": mapping[bond.atom1] if bond.order == 9 else pd.NA,
            "acceptor_atom_index": mapping[bond.atom2] if bond.order == 9 else pd.NA,
            "evidence": "explicit",
        }
        for bond in record.bonds
    ]
    if rows:
        topology._set_chemical_state_bonds(pd.DataFrame(rows))
    topology._chemical_states[0].connectivity_completeness = "complete"
    topology.rebuild_components()
    topology.rebuild_molecules()
    topology.rebuild_entities()
    if topology.n_molecules == 1 and record.title:
        topology.molecules.loc[0, "molecule_name"] = record.title
    structures = Structures()
    coordinates = np.asarray(
        [atom.coordinates for atom in record.atoms], dtype=float
    ).reshape(1, -1, 3)
    structures.append(
        coordinates=puw.standardize(puw.quantity(coordinates, "angstrom")),
        structure_id=np.asarray([0], dtype=np.int64),
        skip_digestion=True,
    )
    result = MolSys()
    result.topology = topology
    result.structures = structures
    return result


def store_stereochemistry(item, report):
    """Store aligned chemical assignments, without retaining toolkit objects."""
    item.topology._set_chemical_state_atom_attribute(
        "stereochemistry",
        [
            label if label is not None else "unspecified"
            for label in report["atom_stereochemistry"]
        ],
    )
    bonds = item.chemical_states._states[0].bonds.copy()
    for index, label, refs in zip(
        report["bond_indices"],
        report["bond_reference_stereochemistry"],
        report["bond_stereo_atom_indices"],
    ):
        if label is not None:
            bonds.loc[index, "stereochemistry"] = label
            bonds.loc[index, ["stereo_atom1_index", "stereo_atom2_index"]] = refs
    item.topology._set_chemical_state_bonds(bonds)


def from_native(item, version, *, allow_stereo=False):
    """Validate a selected native graph without mutating it or guessing chemistry."""
    if version not in {"V2000", "V3000"}:
        _fail("ctfile_version must be 'V2000' or 'V3000'.")
    if (
        item.topology is None
        or item.structures is None
        or item.structures.n_structures != 1
    ):
        _fail("SDF output requires topology and exactly one selected structure.")
    if item.chemical_states is None or item.chemical_states.n_chemical_states != 1:
        _fail("SDF output requires exactly one explicitly selected chemical state.")
    topology = item.topology
    if topology._chemical_states[0].connectivity_completeness != "complete":
        _fail("SDF output requires a complete, explicitly known graph.")
    if item.structures.coordinates is None:
        _fail("SDF output requires coordinates.")
    coordinates = puw.get_value(item.structures.coordinates, to_unit="angstrom")
    if coordinates.shape != (1, topology.n_atoms, 3):
        _fail("SDF coordinates must align with the topology atom axis.")
    state = topology._chemical_states[0]
    atoms_state = state.atom_attributes
    # Inspect explicit CIP labels before serializing: wedge/parity output cannot
    # be approximated by copying a label into a CTAB integer field.
    stereo = atoms_state.get("stereochemistry", pd.Series(dtype="string")).dropna()
    if not stereo.isin(
        ["unspecified", "R", "S", "r", "s"] if allow_stereo else ["unspecified"]
    ).all():
        _fail(
            "Native atom stereochemistry cannot yet be encoded by the native SDF writer."
        )
    record = CTRecord("", version)
    if topology.n_molecules == 1:
        title = topology.molecules.loc[0, "molecule_name"]
        if pd.notna(title):
            record.title = str(title)
    for i, atom in topology.atoms.iterrows():
        charge = atoms_state.loc[i].get("formal_charge", pd.NA)
        radical = atoms_state.loc[i].get("n_unpaired_electrons", pd.NA)
        if pd.isna(charge) or pd.isna(radical):
            _fail(
                "SDF output needs explicit formal charges and radical counts for every atom."
            )
        if int(radical) not in {0, 1, 2}:
            _fail("SDF output cannot encode this radical count.")
        record.atoms.append(
            AtomRecord(
                i + 1,
                str(atom["atom_type"]),
                tuple(coordinates[0, i]),
                formal_charge=int(charge),
                isotope=None if pd.isna(atom["isotope"]) else int(atom["isotope"]),
                n_unpaired_electrons=int(radical),
            )
        )
    encoded_aromatic_atoms = set()
    for i, bond in topology._get_chemical_state_bonds().iterrows():
        atom1, atom2 = int(bond["atom1_index"]), int(bond["atom2_index"])
        bond_type = bond.get("bond_type", None)
        if pd.notna(bond.get("stereochemistry", pd.NA)) and not (
            allow_stereo and bond["stereochemistry"] in {"cis", "trans", "E", "Z"}
        ):
            _fail(
                "Native bond stereochemistry cannot yet be encoded by the native SDF writer."
            )
        aromatic_flag = bond.get("is_aromatic", pd.NA)
        aromatic = pd.notna(aromatic_flag) and bool(aromatic_flag)
        bond_order = bond.get("bond_order", pd.NA)
        if bond_type == "dative":
            if version != "V3000":
                _fail("Coordination bonds require ctfile_version='V3000'.")
            donor = bond.get("donor_atom_index", pd.NA)
            acceptor = bond.get("acceptor_atom_index", pd.NA)
            if pd.isna(donor) or pd.isna(acceptor):
                _fail(
                    "SDF coordination output requires explicit donor and acceptor indices."
                )
            if {int(donor), int(acceptor)} != {atom1, atom2}:
                _fail(
                    "SDF coordination donor and acceptor must be distinct bond endpoints."
                )
            if (
                aromatic
                or pd.notna(bond.get("fractional_bond_order", pd.NA))
                or (pd.notna(bond_order) and int(bond_order) != 1)
            ):
                _fail(
                    "SDF coordination type 9 cannot encode an additional bond multiplicity."
                )
            # Native tables sort endpoints. The serialized direction follows
            # explicit roles rather than the sorted storage order.
            atom1, atom2 = int(donor), int(acceptor)
            order = 9
        elif bond_type != "covalent":
            _fail(
                "Only covalent and directed dative bonds are supported by the native SDF writer."
            )
        elif aromatic:
            order = 4
            encoded_aromatic_atoms.update(
                (int(bond["atom1_index"]), int(bond["atom2_index"]))
            )
        elif pd.notna(bond_order) and int(bond_order) in {1, 2, 3}:
            if pd.notna(bond.get("fractional_bond_order", pd.NA)):
                _fail("A nonaromatic fractional bond order cannot be encoded in SDF.")
            order = int(bond_order)
        else:
            _fail("SDF output requires a supported explicit bond order.")
        if bond_type == "covalent" and any(
            pd.notna(bond.get(field, pd.NA))
            for field in ("donor_atom_index", "acceptor_atom_index")
        ):
            _fail(
                "SDF covalent bond types cannot retain donor or acceptor assignments."
            )
        record.bonds.append(BondRecord(i + 1, atom1 + 1, atom2 + 1, order))
    for i, value in atoms_state.get("is_aromatic", pd.Series(dtype="boolean")).items():
        if pd.notna(value) and bool(value) != (i in encoded_aromatic_atoms):
            _fail(
                "Native atom aromaticity cannot be retained by the supplied explicit SDF bond types."
            )
    return record
