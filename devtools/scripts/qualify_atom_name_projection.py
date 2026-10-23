"""Qualify label projection against the immutable DockingMT 181L archive.

This replays labels/IDs/group membership only, not chemistry, geometry or docking.
"""

import argparse
import gzip
import hashlib
import json
import time
from pathlib import Path

import numpy as np

import molsysmt as msm
from molsysmt.native import MolSys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--archive", required=True, type=Path, help="Archived 181L audit JSON gzip file."
)
archive = parser.parse_args().archive
expected = "5b9bd57c4f72d63ec9283c971056d71e34f3360a365338f2bee1e3dbe6105cf0"
if hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
    raise SystemExit("The archive does not match the declared 181L producer SHA-256.")
data = json.loads(gzip.decompress(archive.read_bytes()))
audit = data["audit"]
topology = audit["expanded_receptor_snapshot"]["topology"]
atoms = topology["atoms"]
groups = topology["groups"]
source = MolSys(n_atoms=len(atoms), n_groups=len(groups))
source.topology.atoms["atom_name"] = [atom["atom_name"] for atom in atoms]
source.topology.atoms["atom_id"] = [atom["atom_id"] for atom in atoms]
for index, group in enumerate(groups):
    source.topology.atoms.loc[group["atom_indices"], "group_index"] = index
# Use the consumer's declared inverse label map, not heuristic name matching.
for rename in audit["decisions"]["generated_H_name_map"]:
    index = rename["atom_index"]
    assert source.topology.atoms.loc[index, "atom_id"] == rename["atom_id"]
    assert source.topology.atoms.loc[index, "atom_name"] in (
        rename["original_name"],
        rename["name"],
    )
    source.topology.atoms.loc[index, "atom_name"] = rename["original_name"]
before = source.topology.atoms.copy(deep=True)
start = time.perf_counter()
result = msm.build.project_atom_names(
    source, target_form="file:pdbqt", return_report=True
)
elapsed = time.perf_counter() - start
report = result["report"]
output = result["molecular_system"]
assert source.topology.atoms.equals(before)
assert report["source_atom_ids"].tolist() == report["output_atom_ids"].tolist()
assert output.topology.atoms.atom_name.tolist() == report["output_atom_names"].tolist()
assert output.topology.atoms.atom_id.tolist() == before.atom_id.tolist()
assert len(report["renamed_atom_indices"]) == len(
    audit["decisions"]["generated_H_name_map"]
)
assert all(
    0 < len(name) <= 4 and name.isascii() and not any(c.isspace() for c in name)
    for name in report["output_atom_names"]
)
for group in range(len(groups)):
    indices = source.topology.atoms.index[
        source.topology.atoms.group_index == group
    ].to_numpy()
    changed = np.intersect1d(indices, report["renamed_atom_indices"])
    for index in changed:
        assert (
            np.sum(
                report["output_atom_names"][indices]
                == report["output_atom_names"][index]
            )
            == 1
        )
mapped = msm.basic.compose_atom_maps([report])
assert mapped["source_atom_names"].tolist() == before.atom_name.tolist()
summary = {
    "archive_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
    "reference": "uibcdf/dockingmt#33",
    "archive_url": "https://github.com/uibcdf/dockingmt/blob/365668e30f5f519adf4abc5c5e5e387d50af00a1/devguide/validation/data/181l_receptor/audit_2026-10-06.json.gz",
    "atoms": len(atoms),
    "groups": len(groups),
    "renamed": len(report["renamed_atom_indices"]),
    "seconds": round(elapsed, 4),
    "scope": "Label-only reconstruction from archived source names, IDs, group memberships and declared inverse rename map. No chemical preparation, charge assignment, geometry or docking calculation repeated. Not consumer adoption or installed qualification.",
    "all_output_names_fit": True,
    "new_names_group_unique": True,
    "ids_and_source_preserved": True,
}
print(json.dumps(summary, indent=2))
