"""Materializing a declared hydrogen inventory on a detached fixed-state ligand."""

from copy import deepcopy

import numpy as np
import pandas as pd
from depdigest import dep_digest

from molsysmt._private.smonitor import (
    NotCompatibleConversionError,
    StructuralInconsistencyError,
)

_SUPPORTED_ELEMENTS = {"H", "C", "N", "O", "F", "P", "S", "Cl", "Br", "I"}
_CALLER = "molsysmt.build.add_missing_hydrogens"


def _fail(reason):
    raise StructuralInconsistencyError(reason=reason, caller=_CALLER)


def _validate_pose(source, pairs):
    """Require finite coordinates and already compact periodic covalent bonds."""
    from molsysmt import pyunitwizard as puw

    positions = np.asarray(puw.get_value(source.structures.coordinates, to_unit="nm"))
    if (
        positions.shape != (1, source.get_n_atoms(), 3)
        or not np.isfinite(positions).all()
    ):
        _fail("Fixed-state hydrogen addition needs one finite coordinate frame.")
    displacement = positions[0, pairs[:, 1]] - positions[0, pairs[:, 0]]
    if np.any(np.linalg.norm(displacement, axis=1) <= 1e-10):
        _fail("Existing bonded atoms have coincident coordinates.")
    if source.structures.box is not None:
        from molsysmt._private.pbc_reconstruction import _minimum_image_vector
        from molsysmt._private.pbc_validation import validate_box_array

        box = validate_box_array(
            puw.get_value(source.structures.box, to_unit="nm"), 1, caller=_CALLER
        )[0]
        inverse = np.linalg.inv(box)
        if any(
            not np.allclose(
                vector, _minimum_image_vector(vector, box, inverse), rtol=0, atol=1e-10
            )
            for vector in displacement
        ):
            _fail(
                "The ligand is split across periodic images; reconstruct compact coordinates explicitly with molsysmt.pbc before adding H."
            )
    return positions


def _stereo_labels(molecule, *, coordinates=False):
    from rdkit import Chem

    from molsysmt._private.stereochemistry import assign_cip, native_labels

    view = Chem.Mol(molecule)
    if coordinates:
        Chem.AssignStereochemistryFrom3D(
            view, confId=view.GetConformer().GetId(), replaceExistingTags=True
        )
    assign_cip(view)
    atoms, bonds = native_labels(view)
    return atoms, [label for label, _ in bonds]


def _check_declared_stereo(molecule, state):
    """Check supported absolute assignments against the supplied source pose."""
    atoms, bonds = _stereo_labels(molecule, coordinates=True)
    declared_atoms = state.atom_attributes.get("stereochemistry")
    if declared_atoms is not None:
        for i, label in enumerate(declared_atoms):
            if pd.isna(label) or label in {"unspecified", "none"}:
                continue
            if label not in {"R", "S", "r", "s"} or atoms[i] != label:
                _fail(
                    f"Atom {i}: declared stereochemistry does not match the fixed 3D pose."
                )
    declared_bonds = state.bonds.get("stereochemistry")
    if declared_bonds is not None:
        for i, label in enumerate(declared_bonds):
            if pd.isna(label) or label in {"unspecified", "none"}:
                continue
            if label not in {"E", "Z"} or bonds[i] != label:
                _fail(
                    f"Bond {i}: unsupported or conflicting declared double-bond stereochemistry; supply absolute E/Z labels."
                )
    return atoms, bonds


@dep_digest("rdkit")
def add(source_input, chemical_state, structure_indices, attribute_policy):
    from rdkit import Chem, rdBase

    from molsysmt import __version__, _ackredit
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt._private.stereochemistry import REFERENCE
    from molsysmt.basic import convert
    from molsysmt.build import add_terminal_atoms
    from molsysmt.native import MolSys
    from molsysmt.physchem import get_chemical_readiness, get_hydrogen_inventory
    from molsysmt.topology import get_covalent_blocks

    source = (
        source_input
        if isinstance(source_input, MolSys)
        else convert(source_input, to_form="molsysmt.MolSys")
    )
    if (
        source.topology is None
        or source.chemical_states is None
        or source.structures is None
    ):
        _fail(
            "Fixed-state hydrogen addition requires topology, chemical assignments and coordinates."
        )
    if (
        source.chemical_states.n_chemical_states != 1
        or source.structures.n_structures != 1
    ):
        _fail(
            "Extract exactly one chemical state and one structure before fixed-state hydrogen addition."
        )
    if source.structures.coordinates is None or not source.get_n_atoms():
        _fail(
            "Fixed-state hydrogen addition requires a nonempty ligand with coordinates."
        )
    inventory = get_hydrogen_inventory(
        source, chemical_state=chemical_state, structure_indices=structure_indices
    )
    if inventory["status"] != "available":
        _fail(
            "The declared hydrogen inventory is unresolved or conflicting: "
            + ", ".join(item["reason_code"] for item in inventory["issues"])
        )
    readiness = get_chemical_readiness(
        source, chemical_state=chemical_state, structure_indices=structure_indices
    )
    for name in (
        "atom_type",
        "formal_charge",
        "atom_is_aromatic",
        "n_unpaired_electrons",
        "n_implicit_hydrogens",
        "n_explicit_hydrogens",
        "allows_implicit_hydrogens",
    ):
        if readiness["fields"][name]["status"] != "present":
            _fail(
                f"Fixed-state hydrogen addition requires explicit supported {name} on every atom."
            )
    state_index = inventory["chemical_state_index"]
    state = source.chemical_states._states[state_index]
    symbols = source.topology.atoms["atom_type"].tolist()
    unsupported = [
        i for i, symbol in enumerate(symbols) if symbol not in _SUPPORTED_ELEMENTS
    ]
    if unsupported:
        _fail(
            f"Unsupported elements at atom indices {unsupported}; this slice supports closed-shell organic ligands, not metals or query atoms."
        )
    if np.any(state.atom_attributes["n_unpaired_electrons"].to_numpy(dtype=int)):
        _fail("Radical states are outside the fixed-state hydrogen addition contract.")
    bonds = state.bonds
    if len(bonds):
        if "is_aromatic" not in bonds or bonds["is_aromatic"].isna().any():
            _fail(
                "Every covalent bond requires explicit supported order and aromaticity."
            )
        orders = bonds.get("bond_order", pd.Series(pd.NA, index=bonds.index))
        known_orders = orders.isin([1, 2, 3]) | bonds["is_aromatic"].eq(True)
        if not known_orders.all():
            _fail(
                "Every covalent bond requires explicit supported order and aromaticity."
            )
    pairs = inventory_pairs = readiness["bonded_atom_pairs"]
    if len(np.unique(get_covalent_blocks(source, output_type="numpy.ndarray"))) != 1:
        _fail("Fixed-state hydrogen addition requires one connected isolated ligand.")
    original_positions = _validate_pose(source, inventory_pairs)
    n_atoms = source.get_n_atoms()
    # Temporary unique IDs make the adapter's original atom order verifiable even
    # when user IDs repeat across residues. They never enter the returned system.
    view = source.copy()
    view.topology.atoms["atom_id"] = pd.array(
        [f"_H_input_{i}" for i in range(n_atoms)], dtype="string"
    )
    try:
        molecule = convert(view, to_form="rdkit.Mol")
    except (ValueError, RuntimeError, NotCompatibleConversionError) as error:
        _fail(
            f"The selected chemistry cannot be represented by the hydrogen engine: {error}"
        )
    if molecule.GetNumAtoms() != n_atoms or molecule.GetNumBonds() != len(pairs):
        _fail("The engine conversion changed source atom or bond counts.")
    if molecule.GetNumConformers() != 1:
        _fail("The engine needs exactly one source conformer.")
    molecule.GetConformer().Set3D(True)
    if not np.array_equal(
        molecule.GetConformer().GetPositions(),
        puw.get_value(source.structures.coordinates, to_unit="angstrom")[0],
    ):
        _fail("The engine conversion changed the source pose or coordinate units.")
    fields = state.atom_attributes
    for i, atom in enumerate(molecule.GetAtoms()):
        isotope = source.topology.atoms.iloc[i].get("isotope", pd.NA)
        expected_isotope = 0 if pd.isna(isotope) else int(isotope)
        if (
            not atom.HasProp("_MolSysMTAtomID")
            or atom.GetProp("_MolSysMTAtomID") != f"_H_input_{i}"
            or atom.GetSymbol() != symbols[i]
            or atom.GetIsotope() != expected_isotope
            or atom.GetFormalCharge() != int(fields["formal_charge"].iloc[i])
            or atom.GetIsAromatic() != bool(fields["is_aromatic"].iloc[i])
            or atom.GetNumRadicalElectrons()
            != int(fields["n_unpaired_electrons"].iloc[i])
            or atom.GetNumImplicitHs() != int(fields["n_implicit_hydrogens"].iloc[i])
            or atom.GetNumExplicitHs() != int(fields["n_explicit_hydrogens"].iloc[i])
            or atom.GetNoImplicit() == bool(fields["allows_implicit_hydrogens"].iloc[i])
        ):
            _fail(
                f"Atom {i}: engine sanitation reinterpreted the declared chemical state or H inventory."
            )
        if atom.HasQuery() or atom.HasProp("_isotopicHs"):
            _fail(
                f"Atom {i}: query chemistry or virtual isotopic additions are unsupported."
            )
    for i, ((left, right), row) in enumerate(zip(pairs, bonds.to_dict("records"))):
        bond = molecule.GetBondBetweenAtoms(int(left), int(right))
        aromatic = bool(row["is_aromatic"])
        if (
            bond is None
            or bond.HasQuery()
            or bond.GetIsAromatic() != aromatic
            or (not aromatic and bond.GetBondTypeAsDouble() != int(row["bond_order"]))
        ):
            _fail(
                f"Bond {i}: engine sanitation reinterpreted the declared covalent graph."
            )
    stereo_before = _check_declared_stereo(molecule, state)
    try:
        generated = Chem.AddHs(molecule, addCoords=True)
    except (ValueError, RuntimeError) as error:
        _fail(f"Local hydrogen coordinate placement failed: {error}")
    n_new = generated.GetNumAtoms() - n_atoms
    if n_new != int(inventory["missing_hydrogen_counts"].sum()):
        _fail("The engine added a different number of H than the declared inventory.")
    if generated.GetNumBonds() != len(bonds) + n_new:
        _fail("Hydrogen placement changed existing connectivity or added extra bonds.")
    for original in molecule.GetAtoms():
        retained = generated.GetAtomWithIdx(original.GetIdx())
        if (
            retained.GetSymbol(),
            retained.GetIsotope(),
            retained.GetFormalCharge(),
            retained.GetNumRadicalElectrons(),
            retained.GetIsAromatic(),
        ) != (
            original.GetSymbol(),
            original.GetIsotope(),
            original.GetFormalCharge(),
            original.GetNumRadicalElectrons(),
            original.GetIsAromatic(),
        ):
            _fail(
                f"Atom {original.GetIdx()}: hydrogen placement changed its chemical identity."
            )
    for original in molecule.GetBonds():
        retained = generated.GetBondBetweenAtoms(
            original.GetBeginAtomIdx(), original.GetEndAtomIdx()
        )
        if retained is None or retained.GetBondType() != original.GetBondType():
            _fail("Hydrogen placement changed an existing covalent relationship.")
    expected_old = molecule.GetConformer().GetPositions()
    positions = generated.GetConformer().GetPositions()
    if (
        not np.array_equal(positions[:n_atoms], expected_old)
        or not np.isfinite(positions).all()
    ):
        _fail("The engine moved an existing atom or generated nonfinite coordinates.")
    parents, records = [], []
    for i in range(n_atoms, generated.GetNumAtoms()):
        atom = generated.GetAtomWithIdx(i)
        neighbors = list(atom.GetNeighbors())
        if (
            atom.GetSymbol() != "H"
            or atom.GetIsotope()
            or atom.GetFormalCharge()
            or atom.GetDegree() != 1
            or neighbors[0].GetIdx() >= n_atoms
        ):
            _fail("The engine produced an unsupported added atom or parent mapping.")
        parent = neighbors[0].GetIdx()
        distance = np.linalg.norm(positions[i] - positions[parent])
        if not 0.5 <= distance <= 1.6:
            _fail(
                f"New H {i}: degenerate local geometry or unsupported parent-H distance."
            )
        parents.append(parent)
        records.append(
            dict(
                parent_atom_index=parent,
                atom_type="H",
                atom_name=f"H{i + 1}",
                chemical_attributes=dict(
                    formal_charge=0,
                    is_aromatic=False,
                    n_unpaired_electrons=0,
                    n_implicit_hydrogens=0,
                    n_explicit_hydrogens=0,
                    allows_implicit_hydrogens=False,
                    stereochemistry="unspecified",
                ),
            )
        )
    if not np.array_equal(
        np.bincount(parents, minlength=n_atoms), inventory["missing_hydrogen_counts"]
    ):
        _fail(
            "Generated parent-H assignments disagree with the declared per-atom inventory."
        )
    stereo_after = _stereo_labels(generated, coordinates=True)
    if any(
        a is not None and stereo_after[0][i] != a
        for i, a in enumerate(stereo_before[0])
    ):
        _fail(
            "Hydrogen placement changed the stereochemistry implied by existing coordinates."
        )
    if stereo_before[1] != stereo_after[1][: len(bonds)]:
        _fail("Hydrogen placement changed existing double-bond stereochemistry.")
    assembled = add_terminal_atoms(
        source,
        records,
        puw.quantity(positions[None, n_atoms:], "angstrom"),
        attribute_policy=attribute_policy,
    )
    output = assembled["molecular_system"]
    if n_new:
        attrs = output.chemical_states._states[state_index].atom_attributes
        attrs.loc[: n_atoms - 1, ["n_implicit_hydrogens", "n_explicit_hydrogens"]] = 0
        output.chemical_states._states[state_index]._normalize_atom_attribute_columns()
    if not np.array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm")[:, :n_atoms],
        original_positions,
    ):
        _fail("Native reconstruction failed to preserve original coordinates.")
    software = {"molsysmt": __version__, "rdkit": rdBase.rdkitVersion}
    items = [dict(REFERENCE, roles=["scientific_criterion"])]
    items.extend(
        dict(
            id=f"software:{name}:{version}",
            type="software",
            **deepcopy(SOFTWARE.get(name, dict(title=name))),
            version=version,
            roles=["executed_software"],
        )
        for name, version in software.items()
    )
    report = dict(
        schema="molsysmt.hydrogen_addition@1",
        status="added" if n_new else "unchanged",
        mode="fixed_chemical_state",
        method="local_hydrogen_placement",
        engine="RDKit",
        parameters=dict(addCoords=True, pH=None, optimize=False),
        chemical_state_index=state_index,
        chemical_state_id=state.state_id,
        structure_index=inventory["structure_index"],
        inventory=inventory,
        chemical_readiness=readiness,
        n_added_hydrogens=n_new,
        atom_correspondence=assembled["report"]["atom_correspondence"],
        parent_hydrogen_pairs=assembled["report"]["parent_atom_pairs"],
        generated_atom_ids=assembled["report"].get("generated_atom_ids", []),
        original_coordinates_preserved=True,
        coordinate_unit="nm",
        coordinate_evidence="generated_local_geometry",
        geometry_reference="https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.AddHs",
        limitations=[
            "No receptor/environment optimization or energy minimization.",
            "OH/NH orientations can require separate environmental refinement.",
            "No pH, protomer, tautomer or heavy-atom conformer selection.",
        ],
        input_provenance=dict(chemical_state_provenance_index=state.provenance_index),
        dropped_attributes=assembled["report"]["dropped_attributes"],
        invalidated_interactions=assembled["report"]["invalidated_interactions"],
        software=software,
        references=[dict(REFERENCE)],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=_CALLER, items=items
        ),
    )
    with _ackredit.scope(_CALLER) as provider:
        _ackredit.credit(provider, items, _CALLER)
    return dict(molecular_system=output, report=deepcopy(report))
