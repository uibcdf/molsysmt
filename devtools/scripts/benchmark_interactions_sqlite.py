#!/usr/bin/env python3
"""Probe transactional SQLite rows against the interaction record oracle.

The schema carries the supported single-method full-field fixture. It is a
candidate experiment, not a public file format or H5MSM adapter.
"""

from __future__ import annotations

import argparse
import copy
import json
import platform
import sqlite3
import statistics
import tempfile
import time
from collections import Counter
from pathlib import Path

import numpy as np
from benchmark_interactions_contract import (
    METHOD,
    TEMPLATES,
    UNITS,
    _record_atoms,
    _requests,
    _rss,
    _signature,
    expected,
    generate_fixture,
)

KINDS = tuple(template[0] for template in TEMPLATES)
ROLES = ("donor", "hydrogen", "acceptor", "ring", "sulfur", "site")
EVIDENCE = ("observed_geometry", "source_annotation")


def _placeholders(count):
    return ",".join("?" for _ in range(count))


def _relation_payload(record):
    participants = record["participants"]
    role_codes = bytes(ROLES.index(part["role"]) for part in participants)
    offsets = [0]
    atoms = []
    for part in participants:
        atoms.extend(part["atom_indices"])
        offsets.append(len(atoms))
    return (KINDS.index(record["interaction_type"]), role_codes,
            np.asarray(offsets, dtype="<u2").tobytes(),
            np.asarray(atoms, dtype="<i4").tobytes())


class SQLiteProbe:
    """Hold one connection and small decoded-relation cache for the probe."""

    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.metadata = {row["key"]: json.loads(row["value"])
                         for row in self.connection.execute(
                             "SELECT key, value FROM metadata"
                         )}
        if self.metadata.get("schema_version") != 1:
            raise ValueError("unsupported SQLite interaction probe schema")
        self.kind_labels = tuple(self.metadata["kind_labels"])
        self.role_labels = tuple(self.metadata["role_labels"])
        self.evidence_labels = tuple(self.metadata["evidence_labels"])
        self.relations = {}
        self.coverage = [row[0] for row in self.connection.execute(
            "SELECT structure_index FROM coverage ORDER BY structure_index"
        )]

    def close(self):
        self.connection.close()

    @classmethod
    def create(cls, path, records, evaluated, n_atoms, n_structures):
        connection = sqlite3.connect(path)
        connection.executescript("""
            PRAGMA journal_mode=DELETE;
            PRAGMA synchronous=FULL;
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE coverage (structure_index INTEGER PRIMARY KEY);
            CREATE TABLE relations (
                relation_id INTEGER PRIMARY KEY,
                kind INTEGER NOT NULL, roles BLOB NOT NULL,
                atom_offsets BLOB NOT NULL, atoms BLOB NOT NULL
            );
            CREATE TABLE occurrences (
                occurrence_id INTEGER PRIMARY KEY,
                structure_index INTEGER NOT NULL,
                relation_id INTEGER NOT NULL,
                evidence INTEGER NOT NULL,
                distance REAL NOT NULL, angle REAL NOT NULL,
                images BLOB NOT NULL, atom_count INTEGER NOT NULL
            );
            CREATE TABLE atom_occurrences (
                atom_index INTEGER NOT NULL,
                occurrence_id INTEGER NOT NULL,
                PRIMARY KEY (atom_index, occurrence_id)
            );
            CREATE INDEX occurrences_by_frame
                ON occurrences (structure_index, occurrence_id);
            CREATE INDEX atom_occurrences_by_occurrence
                ON atom_occurrences (occurrence_id);
        """)
        metadata = {
            "schema_version": 1, "n_atoms": n_atoms,
            "n_structures": n_structures, "method": METHOD,
            "measure_units": UNITS, "parameters": {"seed": 251},
            "source_id": "synthetic_contract", "kind_labels": KINDS,
            "role_labels": ROLES, "evidence_labels": EVIDENCE,
        }
        relation_lookup = {}
        relations = []
        occurrences = []
        atom_occurrences = []
        for occurrence_id, record in enumerate(records):
            key = _relation_payload(record)
            relation_id = relation_lookup.get(key)
            if relation_id is None:
                relation_id = len(relations)
                relation_lookup[key] = relation_id
                relations.append((relation_id, *key))
            involved = sorted(_record_atoms(record))
            images = np.asarray(record["images"], dtype=np.int8).tobytes()
            occurrences.append((
                occurrence_id, record["structure_index"], relation_id,
                EVIDENCE.index(record["evidence"]),
                record["measurements"]["distance"],
                record["measurements"]["angle"], images, len(involved),
            ))
            atom_occurrences.extend((atom, occurrence_id) for atom in involved)
        with connection:
            connection.executemany(
                "INSERT INTO metadata VALUES (?, ?)",
                ((key, json.dumps(value)) for key, value in metadata.items()),
            )
            connection.executemany("INSERT INTO coverage VALUES (?)",
                                   ((frame,) for frame in evaluated))
            connection.executemany("INSERT INTO relations VALUES (?, ?, ?, ?, ?)",
                                   relations)
            connection.executemany(
                "INSERT INTO occurrences VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                occurrences,
            )
            connection.executemany("INSERT INTO atom_occurrences VALUES (?, ?)",
                                   atom_occurrences)
        connection.close()
        return cls(path)

    def _relation(self, relation_id):
        if relation_id not in self.relations:
            row = self.connection.execute(
                "SELECT kind, roles, atom_offsets, atoms FROM relations "
                "WHERE relation_id=?", (relation_id,)
            ).fetchone()
            roles = row["roles"]
            offsets = np.frombuffer(row["atom_offsets"], dtype="<u2")
            atoms = np.frombuffer(row["atoms"], dtype="<i4")
            participants = [
                {"role": self.role_labels[code],
                 "atom_indices": atoms[offsets[index]:offsets[index + 1]].tolist()}
                for index, code in enumerate(roles)
            ]
            self.relations[relation_id] = (self.kind_labels[row["kind"]], participants)
        return self.relations[relation_id]

    def _selected_coverage(self, frames):
        if frames is None:
            return self.coverage
        known = set(self.coverage)
        return [frame for frame in dict.fromkeys(frames) if frame in known]

    def _atom_ids(self, atoms, frames=None, mode="incident"):
        atoms = sorted(set(atoms))
        if not atoms:
            return set()
        sql = (
            "SELECT o.occurrence_id, o.atom_count, COUNT(*) AS hits "
            "FROM atom_occurrences a JOIN occurrences o "
            "ON o.occurrence_id=a.occurrence_id "
            f"WHERE a.atom_index IN ({_placeholders(len(atoms))})"
        )
        parameters = list(atoms)
        if frames is not None:
            if not frames:
                return set()
            sql += f" AND o.structure_index IN ({_placeholders(len(frames))})"
            parameters.extend(frames)
        sql += " GROUP BY o.occurrence_id"
        if mode == "internal":
            sql += " HAVING hits=o.atom_count"
        elif mode == "cross":
            sql += " HAVING hits<o.atom_count"
        return {row[0] for row in self.connection.execute(sql, parameters)}

    def select(self, spec):
        """Select occurrence IDs in requested source-structure order."""
        frames = spec.get("frames")
        coverage = self._selected_coverage(frames)
        if not coverage:
            return coverage, []
        frame_filter = coverage if frames is not None else None
        if "between" in spec:
            a, b = spec["between"]
            selected = self._atom_ids(a, frame_filter) & self._atom_ids(b, frame_filter)
            if spec.get("exclusive", False):
                selected &= self._atom_ids(set(a) | set(b), frame_filter,
                                           mode="internal")
        elif "atoms" in spec:
            selected = self._atom_ids(spec["atoms"], frame_filter,
                                      mode=spec.get("mode", "incident"))
        else:
            if frames is None:
                selected = {row[0] for row in self.connection.execute(
                    "SELECT occurrence_id FROM occurrences"
                )}
            else:
                sql = ("SELECT occurrence_id FROM occurrences WHERE structure_index "
                       f"IN ({_placeholders(len(coverage))})")
                selected = {row[0] for row in self.connection.execute(sql, coverage)}
        if not selected:
            return coverage, []
        sql = ("SELECT occurrence_id, structure_index FROM occurrences "
               f"WHERE occurrence_id IN ({_placeholders(len(selected))})")
        frame_order = {frame: rank for rank, frame in enumerate(coverage)}
        ordered = sorted(self.connection.execute(sql, sorted(selected)),
                         key=lambda row: (frame_order[row["structure_index"]],
                                          row["occurrence_id"]))
        return coverage, [row["occurrence_id"] for row in ordered]

    def materialize(self, selected):
        coverage, ids = selected
        if not ids:
            return coverage, Counter()
        sql = ("SELECT occurrence_id, structure_index, relation_id, evidence, "
               "distance, angle, images FROM occurrences "
               f"WHERE occurrence_id IN ({_placeholders(len(ids))})")
        fetched = {row["occurrence_id"]: row
                   for row in self.connection.execute(sql, ids)}
        output = []
        for occurrence_id in ids:
            row = fetched[occurrence_id]
            kind, participants = self._relation(row["relation_id"])
            images = np.frombuffer(row["images"], dtype=np.int8).reshape(-1, 3)
            output.append(_signature({
                "structure_index": row["structure_index"],
                "interaction_type": kind, "participants": participants,
                "evidence": self.evidence_labels[row["evidence"]],
                "measurements": {"distance": row["distance"],
                                 "angle": row["angle"]},
                "images": images,
            }))
        return coverage, Counter(output)

    def replace_incident(self, frame, atoms, replacements):
        """Transactionally replace affected observations in one covered frame."""
        if frame not in self.coverage:
            raise ValueError("cannot replace an unevaluated structure")
        with self.connection:
            self.connection.execute("BEGIN IMMEDIATE")
            to_remove = self._atom_ids(atoms, [frame])
            if to_remove:
                clause = _placeholders(len(to_remove))
                self.connection.execute(
                    f"DELETE FROM atom_occurrences WHERE occurrence_id IN ({clause})",
                    sorted(to_remove),
                )
                self.connection.execute(
                    f"DELETE FROM occurrences WHERE occurrence_id IN ({clause})",
                    sorted(to_remove),
                )
            for record in replacements:
                if record["structure_index"] != frame:
                    raise ValueError("replacement belongs to another structure")
                key = _relation_payload(record)
                found = self.connection.execute(
                    "SELECT relation_id FROM relations WHERE kind=? AND roles=? "
                    "AND atom_offsets=? AND atoms=?", key
                ).fetchone()
                if found is None:
                    relation_id = self.connection.execute(
                        "INSERT INTO relations (kind, roles, atom_offsets, atoms) "
                        "VALUES (?, ?, ?, ?)", key
                    ).lastrowid
                else:
                    relation_id = found[0]
                involved = sorted(_record_atoms(record))
                images = np.asarray(record["images"], dtype=np.int8).tobytes()
                occurrence_id = self.connection.execute(
                    "INSERT INTO occurrences (structure_index, relation_id, "
                    "evidence, distance, angle, images, atom_count) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (frame, relation_id, EVIDENCE.index(record["evidence"]),
                     record["measurements"]["distance"],
                     record["measurements"]["angle"], images, len(involved)),
                ).lastrowid
                self.connection.executemany(
                    "INSERT INTO atom_occurrences VALUES (?, ?)",
                    ((atom, occurrence_id) for atom in involved),
                )
        self.relations.clear()
        return len(to_remove)


def _summary(samples):
    values = sorted(samples)
    return {"median_ms": statistics.median(values),
            "p95_ms": values[int(0.95 * (len(values) - 1))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frames", type=int, default=1000)
    parser.add_argument("--atoms", type=int, default=500)
    parser.add_argument("--per-frame", type=int, default=8)
    parser.add_argument("--samples", type=int, default=20)
    parser.add_argument("--distribution", choices=("stable", "churn", "mixed",
                                                    "persistent"), default="mixed")
    args = parser.parse_args()
    if args.frames < 30 or args.atoms < 30 or not 1 <= args.per_frame <= 119 \
            or args.samples < 1:
        parser.error("frames and atoms must be >=30; per-frame 1..119; samples >=1")
    rss_before_records = _rss()
    records, evaluated = generate_fixture(args.frames, args.atoms,
                                          args.per_frame, args.distribution, 251)
    requests = _requests(np.random.default_rng(252), records, args.frames,
                         args.atoms, args.samples)
    requests["nonconsecutive"].append({"frames": [2, 1, 0, 2]})
    requests["frame"].append({"frames": [1]})
    rss_after_records = _rss()
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "interactions.sqlite"
        start = time.perf_counter()
        probe = SQLiteProbe.create(path, records, evaluated, args.atoms, args.frames)
        build_s = time.perf_counter() - start
        if (probe.metadata["method"] != METHOD
                or probe.metadata["measure_units"] != UNITS
                or probe.metadata["source_id"] != "synthetic_contract"):
            raise AssertionError("SQLite analysis metadata changed on reopen")
        rss_after_build = _rss()
        file_bytes = path.stat().st_size
        first_start = time.perf_counter()
        first = probe.materialize(probe.select({"atoms": [0]}))
        first_atom_s = time.perf_counter() - first_start
        if first != expected(records, evaluated, atoms=[0]):
            raise AssertionError("first SQLite atom query differs from oracle")
        timings = {}
        query_only = {}
        checked = 0
        for name, specs in requests.items():
            full_samples = []
            select_samples = []
            for spec in specs:
                actual = probe.materialize(probe.select(spec))
                if actual != expected(records, evaluated, **spec):
                    raise AssertionError(f"SQLite oracle mismatch in {name}: {spec}")
                start = time.perf_counter_ns()
                probe.select(spec)
                select_samples.append((time.perf_counter_ns() - start) / 1_000_000)
                start = time.perf_counter_ns()
                probe.materialize(probe.select(spec))
                full_samples.append((time.perf_counter_ns() - start) / 1_000_000)
                checked += 1
            query_only[name] = _summary(select_samples)
            timings[name] = _summary(full_samples)

        frame = next(record["structure_index"] for record in records
                     if record["structure_index"] in evaluated)
        old = next(record for record in records if record["structure_index"] == frame)
        moved_atom = old["participants"][0]["atom_indices"][0]
        partner = next(atom for atom in range(args.atoms)
                       if atom not in _record_atoms(old) and atom != moved_atom)
        replacement = {
            "structure_index": frame, "interaction_type": "disulfide_candidate",
            "participants": [{"role": "sulfur", "atom_indices": [moved_atom]},
                             {"role": "sulfur", "atom_indices": [partner]}],
            "evidence": "observed_geometry",
            "measurements": {"distance": 0.19, "angle": -1.0},
            "images": [[0, 0, 0], [0, 0, 0]],
        }
        start = time.perf_counter()
        removed_count = probe.replace_incident(frame, [moved_atom], [replacement])
        edit_s = time.perf_counter() - start
        edited = [record for record in records if not (
            record["structure_index"] == frame
            and moved_atom in _record_atoms(record)
        )] + [replacement]
        if probe.materialize(probe.select({"frames": [frame]})) != expected(
            edited, evaluated, frames=[frame]
        ):
            raise AssertionError("SQLite local edit differs from oracle")
        if probe.materialize(probe.select({"atoms": [moved_atom]})) != expected(
            edited, evaluated, atoms=[moved_atom]
        ):
            raise AssertionError("SQLite atom index is stale after edit")
        file_after_edit = path.stat().st_size
        repeated_edit_samples = []
        candidates = [atom for atom in range(args.atoms)
                      if atom not in _record_atoms(old) and atom != moved_atom]
        for iteration in range(20):
            next_record = copy.deepcopy(replacement)
            next_record["participants"][1]["atom_indices"] = [
                candidates[(iteration + 1) % len(candidates)]
            ]
            start = time.perf_counter()
            removed = probe.replace_incident(frame, [moved_atom], [next_record])
            repeated_edit_samples.append((time.perf_counter() - start) * 1000)
            if removed != 1:
                raise AssertionError("repeated edit did not replace exactly one row")
            edited = [record for record in edited if not (
                record["structure_index"] == frame
                and moved_atom in _record_atoms(record)
            )] + [next_record]
            if probe.materialize(probe.select({"frames": [frame]})) != expected(
                edited, evaluated, frames=[frame]
            ):
                raise AssertionError("repeated SQLite edit differs from oracle")
        file_after_repeated_edits = path.stat().st_size
        relation_rows_before_compaction = probe.connection.execute(
            "SELECT COUNT(*) FROM relations"
        ).fetchone()[0]
        start = time.perf_counter()
        with probe.connection:
            probe.connection.execute(
                "DELETE FROM relations WHERE relation_id NOT IN "
                "(SELECT DISTINCT relation_id FROM occurrences)"
            )
        probe.connection.execute("VACUUM")
        compaction_s = time.perf_counter() - start
        file_after_compaction = path.stat().st_size
        relation_rows_after_compaction = probe.connection.execute(
            "SELECT COUNT(*) FROM relations"
        ).fetchone()[0]
        probe.close()
        reopened = SQLiteProbe(path)
        if reopened.metadata != probe.metadata:
            raise AssertionError("SQLite analysis metadata changed after edits")
        if reopened.materialize(reopened.select({"frames": [frame]})) != expected(
            edited, evaluated, frames=[frame]
        ):
            raise AssertionError("SQLite committed edit was not persistent")
        reopened.close()
        print(json.dumps({
            "platform": platform.platform(), "sqlite": sqlite3.sqlite_version,
            "frames": args.frames, "atoms": args.atoms,
            "distribution": args.distribution,
            "evaluated_frames": len(evaluated), "occurrences": len(records),
            "queries_checked": checked, "build_s": build_s,
            "first_atom_query_s": first_atom_s,
            "rss_before_records_bytes": rss_before_records.get("VmRSS"),
            "rss_after_records_bytes": rss_after_records.get("VmRSS"),
            "rss_after_build_bytes": rss_after_build.get("VmRSS"),
            "peak_rss_bytes": _rss().get("VmHWM"),
            "file_bytes": file_bytes, "file_after_edit_bytes": file_after_edit,
            "file_after_repeated_edits_bytes": file_after_repeated_edits,
            "file_after_compaction_bytes": file_after_compaction,
            "query_only_ms": query_only, "complete_query_ms": timings,
            "edited_frame": frame, "removed_occurrences": removed_count,
            "edit_s": edit_s,
            "repeated_edit_ms": _summary(repeated_edit_samples),
            "relation_rows_before_compaction": relation_rows_before_compaction,
            "relation_rows_after_compaction": relation_rows_after_compaction,
            "compaction_s": compaction_s,
        }, indent=2))


if __name__ == "__main__":
    main()
