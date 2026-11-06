"""Deriving a bounded H-name reference from pinned OpenMM PDB name data."""

import argparse
import json
from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree

SOURCE_COMMIT = "ba0aa236ac4d07241382869604c4d2ea58c4f3f5"
SOURCE_SHA256 = "740c56071d092940ce386074447ce88ed2b07c77d0065f2bd0d1087e9ef76969"
GROUPS = "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split()


def derive(source):
    """Extract only H-name alternatives; never copy group-name replacements."""
    raw = Path(source).read_bytes()
    if sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError("The PDB-name reference differs from the reviewed source.")
    root = ElementTree.fromstring(raw)

    def names(node):
        output = {}
        for atom in node:
            canonical = atom.attrib["name"]
            if canonical.startswith("H"):
                for key, value in atom.attrib.items():
                    if key.startswith("alt") and value != canonical:
                        if value in output and output[value] != canonical:
                            raise ValueError(
                                "Conflicting aliases in one reference scope."
                            )
                        output[value] = canonical
        return dict(sorted(output.items()))

    common = names(next(node for node in root if node.attrib["name"] == "Protein"))
    groups = {
        name: names(next(node for node in root if node.attrib["name"] == name))
        for name in GROUPS
    }
    return dict(
        schema="molsysmt.pdb_hydrogen_aliases@1",
        rule_version=1,
        source=dict(
            title="OpenMM PDB atom-name reference: canonical protein hydrogen aliases",
            commit=SOURCE_COMMIT,
            sha256=SOURCE_SHA256,
            url=f"https://github.com/openmm/openmm/blob/{SOURCE_COMMIT}/wrappers/python/openmm/app/data/pdbNames.xml",
            license="MIT",
            license_file="OPENMM_LICENSE.txt",
        ),
        common=common,
        groups=groups,
        scope="Twenty canonical amino-acid group labels only. No group-name substitutions, heavy-atom aliases, coordinate placement, protonation or stereochemical H identity.",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("pdb_names") / "pdbNames.xml",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parents[1]
        / "databases/amino_acids/pdb_hydrogen_aliases.json",
    )
    args = parser.parse_args()
    args.output.write_text(
        json.dumps(derive(args.source), indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
