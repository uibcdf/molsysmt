"""Generating synthetic SDF compatibility fixtures with an optional RDKit writer.

Run from the repository root:
    python devtools/scripts/generate_sdf_reference_corpus.py

RDKit is used only to generate this committed fixture snapshot. Native parser
tests use the JSON records without importing it. These molecules are synthetic,
achiral inputs; no external ligand dataset or RDKit source is redistributed.
Counts and net charges below are independently specified chemical expectations.
The snapshot also records the reference producer and atom/bond assignments.
"""

import json
from pathlib import Path

# name, SMILES, atom count with explicit H, bond count, total formal charge
CASES = (
    ("ethanol", "CCO", 9, 8, 0),
    ("benzene", "c1ccccc1", 12, 12, 0),
    ("pyridine", "c1ccncc1", 11, 11, 0),
    ("imidazole", "c1ncc[nH]1", 9, 9, 0),
    ("indole", "c1ccc2[nH]ccc2c1", 16, 17, 0),
    ("nitrobenzene", "O=[N+]([O-])c1ccccc1", 14, 14, 0),
    ("acetate", "CC(=O)[O-]", 7, 6, -1),
    ("tetramethylammonium", "C[N+](C)(C)C", 17, 16, 1),
    ("glycine_zwitterion", "[NH3+]CC(=O)[O-]", 10, 9, 0),
    ("phosphate", "O=P([O-])([O-])[O-]", 5, 4, -3),
    ("sulfate", "O=S(=O)([O-])[O-]", 5, 4, -2),
    ("labelled_ethanol", "[13CH3]C([2H])([2H])O", 9, 8, 0),
    ("acetaminophen", "CC(=O)Nc1ccc(O)cc1", 20, 20, 0),
    ("dimethyl_sulfoxide", "CS(C)=O", 10, 9, 0),
    ("azide", "[N-]=[N+]=[N-]", 3, 2, -1),
    ("acetonitrile", "CC#N", 6, 5, 0),
    ("fluorocyclohexane", "FC1CCCCC1", 18, 18, 0),
)
UNSUPPORTED_CASES = (
    ("methyl_radical_valence", "[CH3]"),
    ("atomic_oxygen_valence", "[O]"),
    ("copper_ammine_valence", "[NH3]->[Cu+2]<-[NH3]"),
)
OUTPUT = (
    Path(__file__).resolve().parents[2]
    / "tests/form/file_sdf/data/reference_corpus.json"
)


def main():
    from rdkit import Chem, rdBase
    from rdkit.Chem import rdDepictor

    records = []
    for name, smiles, n_atoms, n_bonds, total_charge in CASES:
        original = Chem.AddHs(Chem.MolFromSmiles(smiles))
        if (
            original.GetNumAtoms() != n_atoms
            or original.GetNumBonds() != n_bonds
            or Chem.GetFormalCharge(original) != total_charge
        ):
            raise ValueError(
                f"Reference writer disagrees with explicit expectations for {name}."
            )
        rdDepictor.Compute2DCoords(original)
        for aromatic_encoding in ("aromatic", "kekule"):
            if aromatic_encoding == "aromatic" and not any(
                b.GetIsAromatic() for b in original.GetBonds()
            ):
                continue
            molecule = Chem.Mol(original)
            molecule.SetProp("_Name", name)
            if aromatic_encoding == "kekule":
                Chem.Kekulize(molecule, clearAromaticFlags=True)
            for version in ("V2000", "V3000"):
                block = Chem.MolToMolBlock(
                    molecule,
                    includeStereo=False,
                    kekulize=False,
                    forceV3000=version == "V3000",
                )
                atoms = list(molecule.GetAtoms())
                records.append(
                    {
                        "name": name,
                        "smiles": smiles,
                        "version": version,
                        "aromatic_encoding": aromatic_encoding,
                        "n_atoms": n_atoms,
                        "n_bonds": n_bonds,
                        "total_charge": total_charge,
                        "symbols": [atom.GetSymbol() for atom in atoms],
                        "formal_charges": [atom.GetFormalCharge() for atom in atoms],
                        "isotopes": [atom.GetIsotope() for atom in atoms],
                        "radicals": [atom.GetNumRadicalElectrons() for atom in atoms],
                        "bonds": sorted(
                            [
                                [
                                    *sorted(
                                        (bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())
                                    ),
                                    4
                                    if bond.GetIsAromatic()
                                    else int(bond.GetBondTypeAsDouble()),
                                ]
                                for bond in molecule.GetBonds()
                            ]
                        ),
                        "sdf": block + "$$$$\n",
                    }
                )
    unsupported = []
    for name, smiles in UNSUPPORTED_CASES:
        molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
        rdDepictor.Compute2DCoords(molecule)
        molecule.SetProp("_Name", name)
        block = Chem.MolToMolBlock(molecule, includeStereo=False, forceV3000=True)
        if "VAL=" not in block:
            raise ValueError(
                f"{name} no longer reproduces the valence-override boundary."
            )
        unsupported.append({"name": name, "smiles": smiles, "sdf": block + "$$$$\n"})
    payload = {
        "schema": "molsysmt.sdf_reference_corpus@1",
        "producer": {"software": "RDKit", "version": rdBase.rdkitVersion},
        "generation": "generate_sdf_reference_corpus.py; explicit H; 2D; stereo disabled",
        "records": records,
        "unsupported_valence_records": unsupported,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(records)} supported and {len(unsupported)} unsupported reference records."
    )


if __name__ == "__main__":
    main()
