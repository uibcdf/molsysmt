"""Sharing accurate CIP assignment without changing a caller's molecular graph."""

from depdigest import dep_digest

from molsysmt._private.smonitor import StructuralInconsistencyError

REFERENCE = {
    "id": "doi:10.1021/acs.jcim.8b00324",
    "type": "article",
    "title": "Algorithmic Analysis of Cahn-Ingold-Prelog Rules of Stereochemistry: Proposals for Revised Rules and a Guide for Machine Implementation",
    "doi": "10.1021/acs.jcim.8b00324",
    "year": 2018,
}


@dep_digest("rdkit")
def assign_cip(molecule):
    """Assign accurate labels on a private RDKit molecule, clearing stale labels."""
    from rdkit import Chem
    from rdkit.Chem import rdCIPLabeler

    try:
        molecule.UpdatePropertyCache(strict=True)
        Chem.GetSymmSSSR(molecule)
        # Cleaning here would erase explicitly set cis/trans stereo unless
        # directional bond flags also exist. Preserve the declared tags; the
        # accurate labeler computes CIP from the full graph below.
        Chem.AssignStereochemistry(molecule, cleanIt=False, force=True)
        for item in (*molecule.GetAtoms(), *molecule.GetBonds()):
            if item.HasProp("_CIPCode"):
                item.ClearProp("_CIPCode")
        rdCIPLabeler.AssignCIPLabels(molecule)
    except (ValueError, RuntimeError) as error:
        raise StructuralInconsistencyError(
            reason=f"CIP assignment failed: {error}",
            caller="molsysmt.physchem.get_cip_stereochemistry",
        ) from error
    return molecule


def native_labels(molecule):
    """Return native labels and reference atoms in the molecule's atom order."""
    atoms = [
        atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else None
        for atom in molecule.GetAtoms()
    ]
    bonds = []
    for bond in molecule.GetBonds():
        label = bond.GetProp("_CIPCode") if bond.HasProp("_CIPCode") else None
        if label is not None and label not in {"E", "Z"}:
            raise StructuralInconsistencyError(
                reason=f"Unsupported bond CIP descriptor {label!r}.",
                caller="molsysmt.physchem.get_cip_stereochemistry",
            )
        references = list(bond.GetStereoAtoms())
        bonds.append((label, references if label is not None else [-1, -1]))
    if any(value is not None and value not in {"R", "S", "r", "s"} for value in atoms):
        raise StructuralInconsistencyError(
            reason="Only tetrahedral atom CIP descriptors are supported.",
            caller="molsysmt.physchem.get_cip_stereochemistry",
        )
    return atoms, bonds


def apply_atom_labels(molecule, desired):
    """Encode requested absolute labels, verifying against the accurate labeler."""
    from rdkit import Chem

    labels = {
        i: label for i, label in enumerate(desired) if label in {"R", "S", "r", "s"}
    }
    for index in labels:
        molecule.GetAtomWithIdx(index).SetChiralTag(Chem.ChiralType.CHI_TETRAHEDRAL_CW)
    # Dependent pseudoasymmetric centers may change priority after another
    # center is inverted. Converge to verified labels, or reject explicitly.
    for _ in range(len(labels) + 2):
        assign_cip(molecule)
        wrong = [
            i
            for i, label in labels.items()
            if not molecule.GetAtomWithIdx(i).HasProp("_CIPCode")
            or molecule.GetAtomWithIdx(i).GetProp("_CIPCode") != label
        ]
        if not wrong:
            return molecule
        for index in wrong:
            molecule.GetAtomWithIdx(index).InvertChirality()
    raise StructuralInconsistencyError(
        reason="Stored CIP labels cannot be encoded consistently on this graph.",
        caller="molsysmt.physchem.get_cip_stereochemistry",
    )


@dep_digest("rdkit")
def molecule_from_sdf(filename):
    """Read a validated single-record graph, retaining explicit hydrogen atoms."""
    from pathlib import Path

    from rdkit import Chem

    from molsysmt._private.ctfile import _fail, read_sdf

    record = read_sdf(filename, allow_stereo=True)
    text = Path(filename).read_text(encoding="utf-8-sig")
    molecule = Chem.MolFromMolBlock(
        text.split("$$$$", 1)[0], sanitize=False, removeHs=False, strictParsing=True
    )
    if molecule is None:
        _fail("RDKit could not interpret the validated SDF stereochemistry.")
    if (
        molecule.GetNumAtoms() != len(record.atoms)
        or [a.GetSymbol() for a in molecule.GetAtoms()]
        != [a.element for a in record.atoms]
        or [a.GetIsotope() or None for a in molecule.GetAtoms()]
        != [a.isotope for a in record.atoms]
        or [a.GetFormalCharge() for a in molecule.GetAtoms()]
        != [a.formal_charge for a in record.atoms]
    ):
        _fail(
            "Stereo interpretation changed the source atom axis, elements, isotopes or charges."
        )
    orders = {
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.TRIPLE,
        4: Chem.BondType.AROMATIC,
        9: Chem.BondType.DATIVE,
    }
    positions = {atom.serial: i for i, atom in enumerate(record.atoms)}
    for serial in record.stereo_atom_serials:
        if (
            molecule.GetAtomWithIdx(positions[serial]).GetChiralTag()
            == Chem.ChiralType.CHI_UNSPECIFIED
        ):
            _fail(
                "The source atom stereo flag has no supported wedge or 3D interpretation; parity-only stereo cannot be discarded."
            )
    if molecule.GetNumBonds() != len(record.bonds):
        _fail("Stereo interpretation changed source connectivity.")
    for entry in record.bonds:
        left, right = positions[entry.atom1], positions[entry.atom2]
        bond = molecule.GetBondBetweenAtoms(left, right)
        if (
            bond is None
            or bond.GetBondType() != orders[entry.order]
            or (entry.order == 9 and bond.GetBeginAtomIdx() != left)
        ):
            _fail(
                "Stereo interpretation changed a source bond or coordination direction."
            )
    return record, molecule


@dep_digest("rdkit")
def write_stereo_sdf(item, record):
    """Encode validated native labels and verify the serialized graph and stereo."""
    import pandas as pd
    from rdkit import Chem

    from molsysmt._private.ctfile import _fail, write_sdf

    molecule = Chem.MolFromMolBlock(
        write_sdf(record).split("$$$$", 1)[0],
        sanitize=False,
        removeHs=False,
        strictParsing=True,
    )
    if molecule is None:
        _fail("The stereo provider could not read the validated native graph.")
    Chem.RemoveStereochemistry(molecule)
    if molecule.GetNumConformers() and all(
        atom.coordinates[2] == 0 for atom in record.atoms
    ):
        molecule.GetConformer().Set3D(False)
    state = item.chemical_states._states[0]
    desired = state.atom_attributes.get("stereochemistry", pd.Series(dtype="string"))
    atom_labels = [value if isinstance(value, str) else None for value in desired]
    apply_atom_labels(molecule, atom_labels)
    stereo_map = {
        "cis": Chem.BondStereo.STEREOCIS,
        "trans": Chem.BondStereo.STEREOTRANS,
        "E": Chem.BondStereo.STEREOE,
        "Z": Chem.BondStereo.STEREOZ,
    }
    for row in state.bonds.itertuples():
        stereo = getattr(row, "stereochemistry", pd.NA)
        if pd.isna(stereo):
            continue
        refs = (
            getattr(row, "stereo_atom1_index", pd.NA),
            getattr(row, "stereo_atom2_index", pd.NA),
        )
        if any(pd.isna(value) for value in refs):
            _fail("Stereo output needs two explicit double-bond reference atoms.")
        bond = molecule.GetBondBetweenAtoms(int(row.atom1_index), int(row.atom2_index))
        if bond.GetBondType() != Chem.BondType.DOUBLE:
            _fail("Only double bonds support cis/trans or E/Z output.")
        left, right = int(refs[0]), int(refs[1])
        if (
            molecule.GetBondBetweenAtoms(left, int(row.atom1_index)) is None
            or molecule.GetBondBetweenAtoms(right, int(row.atom2_index)) is None
        ):
            _fail(
                "Stereo reference atoms must be neighbors of their respective endpoints."
            )
        if bond.GetBeginAtomIdx() != row.atom1_index:
            left, right = right, left
        bond.SetStereoAtoms(left, right)
        bond.SetStereo(stereo_map[stereo])
    assign_cip(molecule)
    Chem.SetDoubleBondNeighborDirections(molecule)
    text = Chem.MolToMolBlock(
        molecule,
        includeStereo=True,
        kekulize=False,
        forceV3000=record.version == "V3000",
    )
    restored = Chem.MolFromMolBlock(
        text, sanitize=False, removeHs=False, strictParsing=True
    )
    if restored is None:
        _fail("Serialized stereo could not be read back.")
    assign_cip(restored)
    if Chem.MolToSmiles(restored, isomericSmiles=True) != Chem.MolToSmiles(
        molecule, isomericSmiles=True
    ):
        _fail(
            "SDF coordinates or encoding cannot preserve the requested stereochemistry."
        )
    return text + "$$$$\n"
