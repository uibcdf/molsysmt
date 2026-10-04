"""Curating native residue fragments from a pinned Meeko data snapshot.

RDKit is used only during offline curation. Port-associated implicit hydrogens
represent missing external bonds and are not retained as residue H counts.
The runtime assembler consumes the resulting plain chemical graph records.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

SOURCE_SHA256 = "535dc75a2cc5db579a3114090c9ab1273892c556cb7cc1a850ce2c4cd57c7cde"
SOURCE_COMMIT = "1eac18bd6d1111f35f9f1abaa8af502c2668d054"
ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "peptide_templates/meeko_residue_chem_templates.json.gz"
OUTPUT = ROOT.parent / "databases/peptide_templates/residue_fragments.json"
VARIANTS = (
    "ALA",
    "ARG",
    "ASN",
    "ASP",
    "ASH",
    "CYS",
    "CYX",
    "CYX-",
    "GLN",
    "GLU",
    "GLH",
    "GLY",
    "HID",
    "HIE",
    "HIP",
    "ILE",
    "LEU",
    "LYS",
    "LYN",
    "MET",
    "PHE",
    "PRO",
    "SER",
    "THR",
    "TRP",
    "TYR",
    "VAL",
)
PORTS = {"N-term": "peptide_N", "C-term": "peptide_C", "dissulfide": "disulfide_S"}


def curate():
    """Extract explicit heavy graphs, H inventories and declared link ports."""
    from rdkit import Chem, rdBase

    raw = gzip.decompress(SOURCE.read_bytes())
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("The pinned Meeko source snapshot changed.")
    source = json.loads(raw)["residue_templates"]
    params = Chem.SmilesParserParams()
    params.removeHs = False
    records = {}
    for name in VARIANTS:
        entry = source[name]
        mol = Chem.MolFromSmiles(entry["smiles"], params)
        names = entry["atom_name"]
        if (
            mol is None
            or len(names) != mol.GetNumAtoms()
            or len(set(names)) != len(names)
        ):
            raise ValueError(f"Invalid explicit atom inventory: {name}")
        ports = {
            int(index): PORTS[label] for index, label in entry["link_labels"].items()
        }
        virtual = {
            atom.GetIdx(): atom.GetTotalNumHs()
            for atom in mol.GetAtoms()
            if atom.GetTotalNumHs()
        }
        if set(virtual) != set(ports) or any(count != 1 for count in virtual.values()):
            raise ValueError(f"Unaccounted virtual hydrogens/ports: {name}")
        if {"peptide_N", "peptide_C"} - set(ports.values()):
            raise ValueError(f"Missing peptide ports: {name}")
        atoms = []
        for atom in mol.GetAtoms():
            if atom.GetAtomicNum() == 1:
                if len(atom.GetNeighbors()) != 1:
                    raise ValueError(f"Invalid indexed hydrogen: {name}")
                continue
            atoms.append(
                dict(
                    name=names[atom.GetIdx()],
                    element=atom.GetSymbol(),
                    formal_charge=atom.GetFormalCharge(),
                    is_aromatic=atom.GetIsAromatic(),
                    hydrogen_count=sum(
                        neighbor.GetAtomicNum() == 1 for neighbor in atom.GetNeighbors()
                    ),
                )
            )
        bonds = []
        for bond in mol.GetBonds():
            a, b = bond.GetBeginAtom(), bond.GetEndAtom()
            if a.GetAtomicNum() == 1 or b.GetAtomicNum() == 1:
                continue
            aromatic = bond.GetIsAromatic()
            bonds.append(
                dict(
                    atom_names=[names[a.GetIdx()], names[b.GetIdx()]],
                    bond_order=None if aromatic else int(bond.GetBondTypeAsDouble()),
                    fractional_bond_order=1.5 if aromatic else None,
                    is_aromatic=aromatic,
                    is_conjugated=bond.GetIsConjugated(),
                )
            )
        # CYM is an explicit public state name, not automatic CYS alias resolution.
        public_name = "CYM" if name == "CYX-" else name
        records[public_name] = dict(
            upstream_variant=name,
            atoms=atoms,
            bonds=bonds,
            ports={role: names[index] for index, role in ports.items()},
        )
    return dict(
        schema="molsysmt.peptide_fragments@1",
        version="1",
        units={"formal_charge": "elementary_charge"},
        source=dict(
            title="Meeko residue chemical template data",
            commit=SOURCE_COMMIT,
            url=f"https://github.com/forlilab/Meeko/blob/{SOURCE_COMMIT}/meeko/data/residue_chem_templates.json",
            sha256=SOURCE_SHA256,
            license="LGPL-2.1",
        ),
        curation=dict(
            script="molsysmt/data/_make/make_peptide_chemical_templates.py",
            rdkit_version=rdBase.rdkitVersion,
            hydrogen_policy="stored_counts",
            stereochemistry="unspecified",
            rule_version=1,
        ),
        residues=records,
    )


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(curate(), indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
