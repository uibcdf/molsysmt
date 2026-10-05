"""Recording native heavy-template candidate coverage on unchanged PDB inputs."""

from __future__ import annotations

import argparse
import json
import platform
from collections import Counter
from hashlib import sha256
from pathlib import Path

import numpy as np

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdb", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--include-peptide", action="store_true")
    parser.add_argument(
        "--peptide-method",
        choices=["adjacent_backbone_distance", "unique_backbone_distance"],
        default="adjacent_backbone_distance",
    )
    arguments = parser.parse_args()
    rows = []
    for path in arguments.pdb:
        before = path.read_bytes()
        molsys = msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
        coordinates = puw.get_value(
            msm.get(molsys, coordinates=True), to_unit="nm"
        ).copy()
        report = msm.build.get_covalent_bond_candidates(molsys, structure_indices=0)
        peptide = None
        if arguments.include_peptide:
            peptide = msm.build.get_peptide_bond_candidates(
                molsys, structure_indices=0, method=arguments.peptide_method
            )
        np.testing.assert_array_equal(
            puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm"), coordinates
        )
        if path.read_bytes() != before:
            raise AssertionError(f"Source PDB changed during the probe: {path.name}")
        rows.append(
            {
                "source": path.name,
                "sha256": sha256(before).hexdigest(),
                "n_atoms": report["n_atoms"],
                "n_groups": len(report["groups"]),
                "n_candidates": len(report["bonded_atom_pairs"]),
                "n_missing_candidates": int(report["missing_mask"].sum()),
                "group_statuses": dict(
                    Counter(group["status"] for group in report["groups"])
                ),
                "group_reasons": dict(
                    Counter(
                        reason
                        for group in report["groups"]
                        for reason in group["reason_codes"]
                    )
                ),
                "method": report["method"],
                "software": report["software"],
                "coordinates_unchanged": True,
                "candidate_pair_sha256": sha256(
                    report["bonded_atom_pairs"].astype("<i8").tobytes()
                ).hexdigest(),
            }
        )
        if peptide is not None:
            rows[-1]["peptide"] = {
                "method": peptide["method"],
                "software": peptide["software"],
                "n_candidates": len(peptide["bonded_atom_pairs"]),
                "n_missing_candidates": int(peptide["missing_mask"].sum()),
                "link_statuses": dict(
                    Counter(link["status"] for link in peptide["links"])
                ),
                "link_reasons": dict(
                    Counter(
                        reason
                        for link in peptide["links"]
                        for reason in link["reason_codes"]
                    )
                ),
                "effective_max_bond_length_nm": float(
                    puw.get_value(
                        peptide["parameters"]["effective_max_bond_length"], to_unit="nm"
                    )
                ),
                "pbc": peptide["parameters"]["pbc"],
                "candidate_pair_sha256": sha256(
                    peptide["bonded_atom_pairs"].astype("<i8").tobytes()
                ).hexdigest(),
            }
            if "discovery" in peptide:
                rows[-1]["peptide"]["discovery"] = {
                    "status": peptide["discovery"]["status"],
                    "reason_codes": peptide["discovery"]["reason_codes"],
                    "pbc_applied": peptide["discovery"]["pbc_applied"],
                    "n_backbone_endpoints": len(peptide["discovery"]["atom_indices"]),
                    "blocked_chain_indices": peptide["discovery"][
                        "blocked_chain_indices"
                    ].tolist(),
                    "unassessed_group_indices": peptide["discovery"][
                        "unassessed_group_indices"
                    ].tolist(),
                }
    payload = {
        "schema": "molsysmt.covalent_candidate_probe@1",
        "python": platform.python_version(),
        "platform": platform.system(),
        "numpy": np.__version__,
        "sources": rows,
    }
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, separators=(",", ":")))


if __name__ == "__main__":
    main()
