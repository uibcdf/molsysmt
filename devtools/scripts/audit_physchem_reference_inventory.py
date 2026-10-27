"""Inventorying literal group tables against a supplied AAindex1 snapshot.

Research aid for #485, not a release gate or scientific-unit certification.
This script uses the standard library and never downloads or imports providers.
"""

import argparse
import ast
import hashlib
import json
import math
import subprocess
from pathlib import Path

GROUP_CODES = dict(
    zip(
        "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
        "ARNDCQEGHILKMFPSTWYV",
    )
)


def parse_aaindex1(text):
    """Read paired amino-acid headers without assuming dictionary order."""
    records = []
    seen = set()
    for block in text.split("//"):
        lines = block.strip().splitlines()
        if not lines:
            continue
        fields = {}
        key = None
        for line in lines:
            if line and not line[0].isspace():
                key = line[0]
                fields[key] = line[2:].strip()
            elif line.strip() and key is not None:
                fields[key] += " " + line.strip()
        accession = fields.get("H")
        tokens = fields.get("I", "").split()
        if not accession or accession in seen or len(tokens) != 30:
            raise ValueError(f"Invalid or duplicate AAindex1 record: {accession!r}")
        pairs = [label.split("/") for label in tokens[:10]]
        if any(len(pair) != 2 for pair in pairs):
            raise ValueError(f"Invalid AAindex1 paired header: {accession}")
        order = [pair[0] for pair in pairs] + [pair[1] for pair in pairs]
        if len(set(order)) != 20 or set(order) != set(GROUP_CODES.values()):
            raise ValueError(f"Invalid AAindex1 amino-acid axis: {accession}")
        values = {
            aa: None if number == "NA" else float(number)
            for aa, number in zip(order, tokens[10:])
        }
        records.append({"accession": accession, "values": values})
        seen.add(accession)
    if not records:
        raise ValueError("No AAindex1 records found")
    return records


def matching_accessions(table, records):
    """Compare twenty values with absolute tolerance 1e-9 and no rescaling."""
    return [
        record["accession"]
        for record in records
        if all(
            record["values"][aa] is not None
            and math.isclose(
                table[group], record["values"][aa], rel_tol=0, abs_tol=1e-9
            )
            for group, aa in GROUP_CODES.items()
        )
    ]


def inventory(root, snapshot):
    """Inspect direct exports and literal dictionaries without importing MolSysMT."""
    records = parse_aaindex1(snapshot.read_text())
    tables = []
    hashes = {}
    paths = sorted((root / "molsysmt/physchem/groups").glob("*.py"))
    initializer = root / "molsysmt/physchem/__init__.py"
    for path in [initializer, *paths]:
        hashes[str(path.relative_to(root))] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    for path in paths:
        for node in ast.parse(path.read_text()).body:
            if not isinstance(node, ast.Assign):
                continue
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            if not isinstance(value, dict) or not set(GROUP_CODES) <= value.keys():
                continue
            numeric = all(
                isinstance(value[group], (int, float))
                and not isinstance(value[group], bool)
                for group in GROUP_CODES
            )
            for target in node.targets:
                if isinstance(target, ast.Name):
                    tables.append(
                        {
                            "path": str(path.relative_to(root)),
                            "table": target.id,
                            "keys": len(value),
                            "twenty_standard_values_numeric": numeric,
                            "aaindex1_twenty_value_matches": (
                                matching_accessions(value, records) if numeric else []
                            ),
                        }
                    )
    exports = [
        alias.asname or alias.name
        for node in ast.parse(initializer.read_text()).body
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    ]
    return {
        "schema_version": 1,
        "issue": "uibcdf/molsysmt#485",
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        "method": "Static literal-table inventory; twenty-value comparison, atol=1e-9, no rescaling.",
        "aaindex1": {
            "url": "https://www.genome.jp/ftp/db/community/aaindex/aaindex1",
            "sha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
            "records": len(records),
        },
        "source_sha256": hashes,
        "direct_public_physchem_exports": exports,
        "group_tables": tables,
        "limits": [
            "Numeric agreement does not verify units, source identity, licenses or additivity.",
            "No match can reflect normalization, rounding, updates or coverage; it is not a defect diagnosis.",
            "A literal table is not proof of a public delivery route or scientific validation.",
            "No benchmarks, client acceptance, original-paper review or new API are claimed.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aaindex1", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = inventory(Path(__file__).resolve().parents[2], args.aaindex1)
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
