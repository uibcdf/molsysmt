"""Regenerating only buckets affected by an explicit amino-acid supplement revision.

Trusted legacy reference pickles are maintenance inputs. This tool neither loads
arbitrary molecular systems nor infers chemistry. Run the module with --help.
"""

from __future__ import annotations

import argparse
import gzip
import json
import pickle
import platform
from copy import deepcopy
from pathlib import Path

from molsysmt.data._make._chemical_group_database import (
    _check_output,
    _group_name,
    _input_record,
    _sha256,
    _topology,
    _write_pickle,
)


def _read_extra(path):
    with Path(path).open(encoding="utf-8") as stream:
        records = json.load(stream)
    if not isinstance(records, dict):
        raise ValueError("Supplement must map group names to records.")
    for code, record in records.items():
        _group_name(code)
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("topology"), list)
            or not record["topology"]
        ):
            raise ValueError(f"Supplemental group {code}: missing topology variants.")
    return records


def _main(argv=None):
    parser = argparse.ArgumentParser(
        description="Revise existing amino-acid reference variants using explicit before/after supplements."
    )
    parser.add_argument(
        "--source-dir",
        required=True,
        type=Path,
        help="Trusted legacy amino-acid bucket directory; never modified.",
    )
    parser.add_argument(
        "--previous-extra",
        required=True,
        type=Path,
        help="Supplement snapshot matching the variants to replace exactly.",
    )
    parser.add_argument(
        "--extra",
        required=True,
        type=Path,
        help="Reviewed revised supplement, retaining groups and variant positions.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="New or empty output directory for changed buckets and a manifest.",
    )
    args = parser.parse_args(argv)
    _check_output(args.output_dir)
    previous, revised = _read_extra(args.previous_extra), _read_extra(args.extra)
    if previous.keys() != revised.keys():
        raise ValueError("A supplement revision must preserve group membership.")
    changes = {}
    for code in sorted(revised):
        before, after = previous[code], revised[code]
        if {k: v for k, v in before.items() if k != "topology"} != {
            k: v for k, v in after.items() if k != "topology"
        } or len(before["topology"]) != len(after["topology"]):
            raise ValueError(
                f"Group {code}: metadata and variant counts must be preserved."
            )
        for old, new in zip(before["topology"], after["topology"]):
            if not isinstance(new, dict):
                raise ValueError(f"Group {code}: invalid revised topology.")
            _topology(new.get("atoms"), new.get("bonds"), code)
            if old != new:
                changes.setdefault(code, []).append((old, new))
    if not changes:
        raise ValueError("The supplements contain no revisions.")
    inputs = [
        _input_record(args.previous_extra, "previous_supplemental_json"),
        _input_record(args.extra, "revised_supplemental_json"),
    ]
    buckets, changed_positions = {}, {}
    for prefix in sorted({code[0] for code in changes}):
        source = args.source_dir / f"{prefix}.pkl.gz"
        with gzip.open(source, "rb") as stream:
            records = pickle.load(stream)
        if not isinstance(records, dict):
            raise ValueError(f"Invalid reference bucket: {source.name}")
        inputs.append(_input_record(source, "reference_bucket"))
        for code in sorted(changes):
            if code[0] != prefix:
                continue
            variants = records.get(code, {}).get("topology", [])
            replacements = {}
            for old, new in changes[code]:
                positions = [
                    index for index, variant in enumerate(variants) if variant == old
                ]
                if len(positions) != 1 or positions[0] in replacements:
                    raise ValueError(
                        f"Group {code}: expected exactly one original variant per revision."
                    )
                replacements[positions[0]] = new
            for index, variant in replacements.items():
                variants[index] = deepcopy(variant)
            changed_positions[code] = sorted(replacements)
        for code, record in records.items():
            for variant in record["topology"]:
                _topology(variant["atoms"], variant["bonds"], code)
        buckets[f"{prefix}.pkl.gz"] = records
    from molsysmt import __version__

    manifest = {
        "schema_version": 1,
        "generator": "amino-acid-supplement-revision@1",
        "producer": {
            "molsysmt": __version__,
            "python": platform.python_version(),
            "generator_sha256": _sha256(__file__),
            "common_tools_sha256": _sha256(
                Path(__file__).with_name("_chemical_group_database.py")
            ),
        },
        "inputs": inputs,
        "changed_variant_indices": changed_positions,
    }
    _check_output(args.output_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for filename, records in sorted(buckets.items()):
        _write_pickle(args.output_dir / filename, records)
    manifest["outputs"] = {
        filename: _sha256(args.output_dir / filename) for filename in sorted(buckets)
    }
    (args.output_dir / "generation_manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Revised {sum(map(len, changed_positions.values()))} variants in {len(buckets)} buckets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
