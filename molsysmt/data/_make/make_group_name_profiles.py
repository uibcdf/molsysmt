"""Generate bounded naming profiles from the reviewed offline source receipt."""

import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVIEW = ROOT / "devtools/data/name_scheme_profile_review_549_20261104.json"
OUTPUT = ROOT / "molsysmt/data/databases/naming_schemes/group_name_profiles.json"


def generate(review_path=REVIEW):
    """Reuse the code authority and verify every admitted CCD projection."""
    raw = review_path.read_bytes()
    review = json.loads(raw)
    tree = ast.parse((ROOT / "molsysmt/element/group/amino_acid/codes.py").read_text())
    alphabet = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "aa3_to_aa1"
            for target in node.targets
        )
    )
    states = {
        "GLH": "GLU",
        "HID": "HIS",
        "HIE": "HIS",
        "HIP": "HIS",
        "ASH": "ASP",
        "CYM": "CYS",
        "CYX": "CYS",
        "LYN": "LYS",
    }
    standard = {
        name: name
        for name in alphabet
        if name not in {"SEC", "PYL", "ASX", "GLX", "XAA", "XLE"}
    }
    ccd = {}
    for row in review["records"]:
        if "chem_comp" not in row:
            continue
        component = row["chem_comp"]
        name = row["code"]
        if component["id"] != name:
            raise ValueError("CCD record identity disagrees with the requested code.")
        peptide = "peptide" in component["type"].lower()
        parents = component.get("mon_nstd_parent_comp_id") or []
        if not isinstance(parents, list) or len(parents) > 1:
            raise ValueError(
                "A bounded naming entry needs at most one declared parent."
            )
        parent = (
            parents[0] if parents else name if peptide and name in alphabet else None
        )
        if peptide and (
            parent not in alphabet
            or alphabet[parent] != component.get("one_letter_code")
        ):
            raise ValueError("CCD parent and reported one-letter code disagree.")
        ccd[name] = {
            "parent": parent,
            "group_type": "amino acid"
            if peptide
            else "water"
            if name == "HOH"
            else "small molecule",
            "source_name": component["name"],
            "source_type": component["type"],
            "source_url": row["url"],
            "source_sha256": row["sha256"],
        }
    return {
        "schema": "molsysmt.group_name_profiles@1",
        "version": 1,
        "review_sha256": hashlib.sha256(raw).hexdigest(),
        "sequence": {
            "version": 1,
            "source_url": "https://www.ddbj.nig.ac.jp/ddbj/code-e.html",
            "alphabet": "aa3_to_aa1",
        },
        "amber": {
            "version": 1,
            "source": review["amber_source"],
            "parents": standard | states,
        },
        "ccd": {"version": 1, "snapshot_date": review["date"], "entries": ccd},
        "legacy": {
            "version": 1,
            "source": review["mdtraj_source"],
            "parent_mapping": "molsysmt.element.group.amino_acid.group_types.name_to_type",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(generate(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if OUTPUT.read_text() != rendered:
            raise SystemExit("The bundled group naming profiles are stale.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(rendered)


if __name__ == "__main__":
    main()
