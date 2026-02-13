#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
import shutil
import sys

import numpy as np

import molsysmt as msm


def _resolve_tleap_binary(explicit_tleap_bin=None, explicit_amberclassic_dir=None):
    """Resolve a local tleap binary path for temporary development comparisons."""

    candidates = []
    if explicit_tleap_bin:
        candidates.append(Path(explicit_tleap_bin))

    env_tleap_bin = os.environ.get("TLEAP_BIN", "")
    if env_tleap_bin:
        candidates.append(Path(env_tleap_bin))

    amberhome = os.environ.get("AMBERHOME", "")
    if amberhome:
        candidates.append(Path(amberhome) / "bin" / "tleap")

    amberclassic_env = os.environ.get("AMBERCLASSIC_DIR", "")
    if amberclassic_env:
        candidates.append(Path(amberclassic_env) / "bin" / "tleap")

    if explicit_amberclassic_dir:
        candidates.append(Path(explicit_amberclassic_dir) / "bin" / "tleap")

    repo_root = Path(__file__).resolve().parents[2]
    candidates.append(repo_root.parent / "AmberClassic" / "bin" / "tleap")

    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return candidate

    return None


def _configure_tleap_for_session(explicit_tleap_bin=None, explicit_amberclassic_dir=None):
    """Provision tleap in PATH for this process only (temporary, non-global)."""

    current = shutil.which("tleap")
    if current is not None:
        return current, False

    resolved = _resolve_tleap_binary(
        explicit_tleap_bin=explicit_tleap_bin,
        explicit_amberclassic_dir=explicit_amberclassic_dir,
    )
    if resolved is None:
        return None, False

    resolved_parent = str(resolved.parent)
    os.environ["PATH"] = resolved_parent + os.pathsep + os.environ.get("PATH", "")
    os.environ["TLEAP_BIN"] = str(resolved)
    return str(resolved), True


def _compute_metrics(molsys):
    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates[0], to_unit="nm")
    bonds = np.array(molsys.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=int))
    atom_types = np.array(molsys.topology.atoms["atom_type"].to_numpy(), dtype=object)

    metrics = {
        "n_atoms": int(len(atom_types)),
        "n_bonds": int(len(bonds)),
        "n_groups": int(molsys.topology.groups.shape[0]),
    }

    if len(bonds) > 0:
        bonded_distances = np.linalg.norm(coordinates[bonds[:, 0], :] - coordinates[bonds[:, 1], :], axis=1)
        metrics["max_bond_nm"] = float(np.max(bonded_distances))
        metrics["min_bond_nm"] = float(np.min(bonded_distances))
    else:
        metrics["max_bond_nm"] = None
        metrics["min_bond_nm"] = None

    heavy_indices = np.where(atom_types != "H")[0]
    bonded_set = {tuple(sorted((int(i), int(j)))) for i, j in bonds.tolist()}

    min_nonbonded_heavy_distance = np.inf
    for idx, atom_index_1 in enumerate(heavy_indices):
        for atom_index_2 in heavy_indices[idx + 1 :]:
            pair = tuple(sorted((int(atom_index_1), int(atom_index_2))))
            if pair in bonded_set:
                continue
            distance = np.linalg.norm(coordinates[atom_index_1, :] - coordinates[atom_index_2, :])
            if distance < min_nonbonded_heavy_distance:
                min_nonbonded_heavy_distance = distance

    if np.isfinite(min_nonbonded_heavy_distance):
        metrics["min_nonbonded_heavy_nm"] = float(min_nonbonded_heavy_distance)
    else:
        metrics["min_nonbonded_heavy_nm"] = None

    return metrics


def _try_build(sequence, engine):
    try:
        molsys = msm.build.build_peptide(sequence, to_form="molsysmt.MolSys", engine=engine)
        return {
            "ok": True,
            "metrics": _compute_metrics(molsys),
            "error_type": None,
            "error_message": None,
        }
    except Exception as exc:
        return {
            "ok": False,
            "metrics": None,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
        }


def _delta(left_value, right_value):
    if left_value is None or right_value is None:
        return None
    return right_value - left_value


def main():
    parser = argparse.ArgumentParser(
        description="Compare build_peptide outputs between LEaP and MolSysMT engines."
    )
    parser.add_argument(
        "--sequence",
        action="append",
        dest="sequences",
        help="Sequence to test. Can be passed multiple times.",
    )
    parser.add_argument(
        "--sequences-json",
        default=None,
        help="Path to a JSON file with a list of sequences.",
    )
    parser.add_argument(
        "--output-json",
        default=None,
        help="Write full comparison report to this JSON file.",
    )
    parser.add_argument(
        "--tleap-bin",
        default=None,
        help="Explicit tleap binary path for this run only (temporary developer override).",
    )
    parser.add_argument(
        "--amberclassic-dir",
        default=None,
        help="AmberClassic root directory (used to resolve <dir>/bin/tleap for this run only).",
    )
    args = parser.parse_args()

    sequences = []
    if args.sequences:
        sequences.extend(args.sequences)

    if args.sequences_json is not None:
        with open(args.sequences_json, "r", encoding="utf-8") as file_handle:
            loaded = json.load(file_handle)
        if not isinstance(loaded, list) or not all(isinstance(item, str) for item in loaded):
            raise ValueError("--sequences-json must contain a JSON list of strings.")
        sequences.extend(loaded)

    if not sequences:
        sequences = [
            "ACEALAALANME",
            "ACEHISNME",
            "TyrGlyGlyPheMet",
        ]

    resolved_tleap, was_provisioned = _configure_tleap_for_session(
        explicit_tleap_bin=args.tleap_bin,
        explicit_amberclassic_dir=args.amberclassic_dir,
    )
    if resolved_tleap is None:
        print("WARNING: tleap not found in PATH. LEaP comparisons will fail.", file=sys.stderr)
    elif was_provisioned:
        print(
            f"INFO: Using provisional tleap binary for this run: {resolved_tleap}",
            file=sys.stderr,
        )

    report = {"sequences": []}

    for sequence in sequences:
        leap_result = _try_build(sequence, "LEaP")
        molsysmt_result = _try_build(sequence, "MolSysMT")

        entry = {
            "sequence": sequence,
            "LEaP": leap_result,
            "MolSysMT": molsysmt_result,
            "delta": None,
        }

        if leap_result["ok"] and molsysmt_result["ok"]:
            leap_metrics = leap_result["metrics"]
            molsysmt_metrics = molsysmt_result["metrics"]
            entry["delta"] = {
                "n_atoms": _delta(leap_metrics["n_atoms"], molsysmt_metrics["n_atoms"]),
                "n_bonds": _delta(leap_metrics["n_bonds"], molsysmt_metrics["n_bonds"]),
                "n_groups": _delta(leap_metrics["n_groups"], molsysmt_metrics["n_groups"]),
                "max_bond_nm": _delta(leap_metrics["max_bond_nm"], molsysmt_metrics["max_bond_nm"]),
                "min_bond_nm": _delta(leap_metrics["min_bond_nm"], molsysmt_metrics["min_bond_nm"]),
                "min_nonbonded_heavy_nm": _delta(
                    leap_metrics["min_nonbonded_heavy_nm"], molsysmt_metrics["min_nonbonded_heavy_nm"]
                ),
            }

        report["sequences"].append(entry)

    for entry in report["sequences"]:
        sequence = entry["sequence"]
        leap_result = entry["LEaP"]
        molsysmt_result = entry["MolSysMT"]
        print(f"SEQ {sequence}")
        if leap_result["ok"]:
            print(f"  LEaP      OK {leap_result['metrics']}")
        else:
            print(f"  LEaP      ERROR {leap_result['error_type']}: {leap_result['error_message']}")
        if molsysmt_result["ok"]:
            print(f"  MolSysMT  OK {molsysmt_result['metrics']}")
        else:
            print(f"  MolSysMT  ERROR {molsysmt_result['error_type']}: {molsysmt_result['error_message']}")
        if entry["delta"] is not None:
            print(f"  DELTA(MolSysMT-LEaP) {entry['delta']}")
        print("-")

    if args.output_json is not None:
        with open(args.output_json, "w", encoding="utf-8") as file_handle:
            json.dump(report, file_handle, indent=2, sort_keys=True)
        print(f"Report written to {args.output_json}")


if __name__ == "__main__":
    main()
