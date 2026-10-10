"""Regenerating legacy group-reference tables from explicitly supplied sources.

This is maintenance tooling, not a public chemical-state or molecular-system API.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import pickle
import platform
import re
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

_PEPTIDE_TYPES = {
    "peptide linking",
    "l-peptide linking",
    "d-peptide linking",
    "l-peptide nh3 amino terminus",
    "d-peptide nh3 amino terminus",
    "l-peptide cooh carboxy terminus",
    "d-peptide cooh carboxy terminus",
}
_RTP_SECTIONS = {
    "atoms",
    "bonds",
    "angles",
    "dihedrals",
    "impropers",
    "exclusions",
    "cmap",
    "bondedtypes",
}


def _sha256(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _input_record(path, role):
    return {"role": role, "filename": Path(path).name, "sha256": _sha256(path)}


def _group_name(value):
    if not isinstance(value, str) or not re.fullmatch(
        r"[A-Z0-9][A-Za-z0-9_+.-]*", value
    ):
        raise ValueError(
            f"Unsupported group name for the reference-file layout: {value!r}"
        )
    return value


def _value(category, attribute, code):
    if category is None or not category.hasAttribute(attribute):
        raise ValueError(f"CCD component {code}: missing {attribute}.")
    return category.getValue(attribute, 0)


def _topology(atoms, bonds, code):
    if (
        not isinstance(atoms, list)
        or not atoms
        or any(
            not isinstance(atom, str) or not atom or atom in {".", "?"}
            for atom in atoms
        )
        or len(set(atoms)) != len(atoms)
    ):
        raise ValueError(
            f"Group {code}: atom names must be nonempty, known and unique."
        )
    if not isinstance(bonds, list) or any(
        not isinstance(pair, list)
        or len(pair) != 2
        or any(atom not in atoms for atom in pair)
        or pair[0] == pair[1]
        for pair in bonds
    ):
        raise ValueError(f"Group {code}: each bond must join two declared atoms.")
    return {"atoms": list(atoms), "bonds": [list(pair) for pair in bonds]}


def _ccd_topologies(container, code):
    atoms = container.getObj("chem_comp_atom")
    if atoms is None or not atoms.getRowCount() or not atoms.hasAttribute("atom_id"):
        raise ValueError(f"CCD component {code}: missing atom inventory.")
    names, aliases = [], []
    for row in range(atoms.getRowCount()):
        if not atoms.hasAttribute("comp_id") or atoms.getValue("comp_id", row) != code:
            raise ValueError(f"CCD component {code}: inconsistent atom comp_id.")
        name = atoms.getValue("atom_id", row)
        alias = (
            atoms.getValue("alt_atom_id", row)
            if atoms.hasAttribute("alt_atom_id")
            else name
        )
        names.append(name)
        aliases.append(name if alias in {".", "?", None, ""} else alias)
    pairs = []
    bonds = container.getObj("chem_comp_bond")
    if bonds is not None:
        for attribute in ("comp_id", "atom_id_1", "atom_id_2"):
            if not bonds.hasAttribute(attribute):
                raise ValueError(f"CCD component {code}: missing bond {attribute}.")
        for row in range(bonds.getRowCount()):
            if bonds.getValue("comp_id", row) != code:
                raise ValueError(f"CCD component {code}: inconsistent bond comp_id.")
            pairs.append(
                [bonds.getValue("atom_id_1", row), bonds.getValue("atom_id_2", row)]
            )
    canonical = _topology(names, pairs, code)
    alias_map = dict(zip(names, aliases))
    alternate = _topology(
        aliases, [[alias_map[a], alias_map[b]] for a, b in pairs], code
    )
    return [canonical, alternate]


def _ion_record(name, code, topologies, three_letter_code=None):
    indexed = []
    for topology in topologies:
        positions = {atom: index for index, atom in enumerate(topology["atoms"])}
        indexed.append(
            sorted(
                {
                    tuple(sorted((positions[a], positions[b])))
                    for a, b in topology["bonds"]
                }
            )
        )
    if any(pairs != indexed[0] for pairs in indexed[1:]):
        raise ValueError(
            f"Ion {code}: variants require different indexed connectivity."
        )
    return {
        "name": name,
        "three_letter_code": three_letter_code or code,
        "atom_name": [topology["atoms"] for topology in topologies],
        "bonds": [list(pair) for pair in indexed[0]],
    }


def _selected(kind, code, name, comp_type, amino_acid_names):
    if code == "UNL":
        return False
    normalized = comp_type.strip().casefold()
    if kind == "amino_acids":
        return code in amino_acid_names and normalized in _PEPTIDE_TYPES
    if kind == "saccharides":
        return "saccharide" in normalized
    nonpolymer = normalized in {"non-polymer", "other"}
    ion = name.strip().casefold().endswith(" ion")
    return nonpolymer and (ion if kind == "ions" else not ion)


def _read_ccd(path, kind, amino_acid_names):
    from mmcif.io import IoAdapter

    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    with TemporaryDirectory(prefix="molsysmt-ccd-parser-") as directory:
        containers = IoAdapter(
            raiseExceptions=True, readEncodingErrors="strict"
        ).readFile(
            str(path),
            selectList=["chem_comp", "chem_comp_atom", "chem_comp_bond"],
            outDirPath=directory,
            logFilePath=str(Path(directory) / "parser.log"),
        )
    if not containers:
        raise ValueError("The CCD input contains no data blocks.")
    output, seen = {}, set()
    for container in containers:
        for category_name in ("chem_comp", "chem_comp_atom", "chem_comp_bond"):
            parsed = container.getObj(category_name)
            if parsed is not None and any(
                len(row) != len(parsed.getAttributeList())
                for row in parsed.getRowList()
            ):
                raise ValueError(
                    f"CCD block {container.getName()}: incomplete {category_name} row."
                )
        category = container.getObj("chem_comp")
        if category is None or category.getRowCount() != 1:
            raise ValueError(
                f"CCD block {container.getName()}: expected one chem_comp row."
            )
        code = _group_name(_value(category, "id", container.getName()))
        if code in seen:
            raise ValueError(f"Duplicate CCD component {code}.")
        seen.add(code)
        name = _value(category, "name", code)
        comp_type = _value(category, "type", code)
        if (
            not isinstance(name, str)
            or not isinstance(comp_type, str)
            or name in {".", "?", ""}
            or comp_type in {".", "?", ""}
        ):
            raise ValueError(f"CCD component {code}: name and type must be known.")
        if not _selected(kind, code, name, comp_type, amino_acid_names):
            continue
        topologies = _ccd_topologies(container, code)
        if kind == "ions":
            label = (
                category.getValue("three_letter_code", 0)
                if category.hasAttribute("three_letter_code")
                else code
            )
            output[code] = _ion_record(
                name, code, topologies, code if label in {".", "?", ""} else label
            )
        else:
            output[code] = {"name": name, "topology": topologies}
    return output


def _append_variant(record, variant):
    atoms = set(variant["atoms"])
    bonds = {frozenset(pair) for pair in variant["bonds"]}
    if not any(
        set(current["atoms"]) == atoms
        and {frozenset(pair) for pair in current["bonds"]} == bonds
        for current in record["topology"]
    ):
        record["topology"].append(variant)


def _read_rtp(path):
    output, current, section = {}, None, None
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            content = line.split(";", 1)[0].strip()
            if not content:
                continue
            if content.startswith("[") and content.endswith("]"):
                header = content[1:-1].strip()
                if header.casefold() in _RTP_SECTIONS:
                    section = header.casefold()
                else:
                    current, section = _group_name(header), None
                    if current in output:
                        raise ValueError(f"Duplicate RTP group {current}.")
                    output[current] = {"atoms": [], "bonds": []}
                continue
            fields = content.split()
            if current is not None and section == "atoms":
                if len(fields) < 4:
                    raise ValueError(f"RTP group {current}: incomplete atom row.")
                output[current]["atoms"].append(fields[0])
            elif current is not None and section == "bonds":
                if len(fields) < 2:
                    raise ValueError(f"RTP group {current}: incomplete bond row.")
                if not any(atom.startswith(("-", "+")) for atom in fields[:2]):
                    output[current]["bonds"].append(fields[:2])
    return output


def _supplement(output, path, kind):
    with Path(path).open(encoding="utf-8") as stream:
        extra = json.load(stream)
    if not isinstance(extra, dict):
        raise ValueError("Supplemental JSON must map group names to topology records.")
    for code, record in sorted(extra.items()):
        _group_name(code)
        if (
            not isinstance(record, dict)
            or not isinstance(record.get("topology"), list)
            or not record["topology"]
        ):
            raise ValueError(f"Supplemental group {code}: missing topology variants.")
        if record.get("name") is not None and not isinstance(record["name"], str):
            raise ValueError(f"Supplemental group {code}: invalid name.")
        variants = []
        for item in record["topology"]:
            if not isinstance(item, dict):
                raise ValueError(
                    f"Supplemental group {code}: invalid topology variant."
                )
            variants.append(_topology(item.get("atoms"), item.get("bonds"), code))
        if kind == "ions":
            if code in output:
                existing = output[code]
                variants = [
                    _topology(
                        names,
                        [[names[a], names[b]] for a, b in existing["bonds"]],
                        code,
                    )
                    for names in existing["atom_name"]
                ] + variants
                name, label = existing["name"], existing["three_letter_code"]
            else:
                name, label = record.get("name"), code
            output[code] = _ion_record(name, code, variants, label)
        else:
            target = output.setdefault(
                code, {"name": record.get("name"), "topology": []}
            )
            for variant in variants:
                _append_variant(target, variant)


def _check_output(directory):
    directory = Path(directory)
    if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
        raise FileExistsError(f"Output directory must be empty: {directory}")


def _write_pickle(path, payload):
    with Path(path).open("wb") as stream:
        with gzip.GzipFile(
            filename="", fileobj=stream, mode="wb", mtime=0, compresslevel=9
        ) as compressed:
            pickle.dump(payload, compressed, protocol=4)


def _write_database(output, directory, manifest):
    directory = Path(directory)
    _check_output(directory)
    directory.mkdir(parents=True, exist_ok=True)
    groups = {}
    for code, record in sorted(output.items()):
        groups.setdefault(code[0], {})[code] = record
    payloads = {f"{prefix}.pkl.gz": records for prefix, records in groups.items()}
    payloads["group_names.pkl.gz"] = sorted(output)
    for filename, payload in sorted(payloads.items()):
        _write_pickle(directory / filename, payload)
    manifest["outputs"] = {
        filename: _sha256(directory / filename) for filename in sorted(payloads)
    }
    (directory / "generation_manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )


def _main(kind, argv=None):
    parser = argparse.ArgumentParser(
        description=f"Regenerate {kind} reference tables from a local CCD."
    )
    parser.add_argument(
        "--ccd",
        required=True,
        type=Path,
        help="Local components.cif or components.cif.gz; no download.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="New or empty output directory; existing results are preserved.",
    )
    if kind in {"amino_acids", "ions"}:
        parser.add_argument(
            "--extra",
            type=Path,
            help="Explicit supplemental JSON in the legacy topology schema.",
        )
    if kind == "amino_acids":
        parser.add_argument(
            "--rtp",
            action="append",
            default=[],
            type=Path,
            help="Optional local GROMACS RTP; may be repeated.",
        )
        parser.add_argument(
            "--amino-acid-name",
            action="append",
            help="CCD/RTP allowlist; may be repeated. Defaults to bundled amino-acid group names.",
        )
    args = parser.parse_args(argv)
    _check_output(args.output_dir)
    amino_acid_names = []
    if kind == "amino_acids":
        if args.amino_acid_name is None:
            from molsysmt.element.group.amino_acid import group_names

            amino_acid_names = group_names
        else:
            amino_acid_names = args.amino_acid_name
        if not amino_acid_names:
            raise ValueError("Amino-acid group-name selection is unavailable or empty.")
        amino_acid_names = sorted({_group_name(name) for name in amino_acid_names})
    output = _read_ccd(args.ccd, kind, amino_acid_names)
    inputs = [_input_record(args.ccd, "ccd")]
    for rtp in getattr(args, "rtp", []):
        for code, topology in _read_rtp(rtp).items():
            if code in amino_acid_names:
                variant = _topology(topology["atoms"], topology["bonds"], code)
                _append_variant(
                    output.setdefault(code, {"name": None, "topology": []}), variant
                )
        inputs.append(_input_record(rtp, "gromacs_rtp"))
    if getattr(args, "extra", None) is not None:
        _supplement(output, args.extra, kind)
        inputs.append(_input_record(args.extra, "supplemental_json"))
    from molsysmt import __version__

    manifest = {
        "schema_version": 1,
        "generator": "ccd-group-database@1",
        "group_kind": kind,
        "producer": {
            "molsysmt": __version__,
            "mmcif": version("mmcif"),
            "python": platform.python_version(),
        },
        "inputs": inputs,
        "n_groups": len(output),
        "selection": {"amino_acid_names": amino_acid_names},
    }
    _write_database(output, args.output_dir, manifest)
    print(f"Generated {len(output)} {kind} groups in {args.output_dir}")
    return 0
