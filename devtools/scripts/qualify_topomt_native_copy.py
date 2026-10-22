"""Qualify the source Topography copy route against resident MolSys ownership.

This read-only client probe does not change the TopoMT checkout, qualify an
installed package or execute a topographical scientific calculation.
"""

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import molsysmt as msm
from devtools.scripts.benchmark_native_copy import _fixture
from molsysmt import pyunitwizard as puw


def _source(root, files):
    def git(*args):
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True
        ).strip()

    return {
        "head": git("rev-parse", "HEAD"),
        "worktree_status": git("status", "--porcelain"),
        "ahead_behind_origin_main": git(
            "rev-list", "--left-right", "--count", "HEAD...origin/main"
        ),
        "sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in files
        },
    }


def qualify():
    import topomt
    from topomt import Topography
    from topomt import __version__ as topomt_version

    provider_root = Path(__file__).resolve().parents[2]
    client_root = Path(topomt.__file__).resolve().parents[1]
    if not (client_root / ".git").exists():
        raise RuntimeError("This source probe requires a TopoMT checkout import.")
    provider = _source(
        provider_root,
        [
            "molsysmt/native/_copy.py",
            "molsysmt/native/molsys.py",
            "molsysmt/native/structures.py",
            "molsysmt/native/topology.py",
            "molsysmt/native/chemical_states.py",
            "devtools/scripts/benchmark_native_copy.py",
        ],
    )
    client_files = [
        "topomt/topography/Topography.py",
        "topomt/features/BaseFeature.py",
        "topomt/features/Pocket.py",
        "topomt/features/Channel.py",
    ]
    client = _source(client_root, client_files)
    results = []
    for deep in (False, True):
        source = _fixture(4, 7)
        original = Topography(source, structure_indices="all")
        feature_id = original.add_new_feature("pocket")
        system = original._molsys
        system.client_metadata = {"values": [1], "owner": system}
        before = puw.get_value(system.structures.coordinates, to_unit="nm").copy()
        duplicate = original.copy(deep=deep)
        copied = duplicate._molsys
        assert source.topology._molsys_owner_ref() is source
        assert system.topology._molsys_owner_ref() is system
        assert copied.topology._molsys_owner_ref() is copied
        assert copied.chemical_states is copied.topology._chemical_states_domain
        assert copied.chemical_states._molsys_owner_ref() is copied
        assert copied.structures._molsys_owner_ref() is copied
        assert np.shares_memory(
            system.structures._coordinates._blocks[0],
            copied.structures._coordinates._blocks[0],
        ) == (not deep)
        assert duplicate[feature_id]._topography is duplicate
        assert original[feature_id]._topography is original
        duplicate.add_new_feature("channel")
        assert len(original) == 1 and len(duplicate) == 2
        copied.client_metadata["values"].append(2)
        assert system.client_metadata["values"] == [1]
        assert copied.client_metadata["owner"] is copied
        msm.set(
            copied,
            selection=[0],
            structure_indices=[3],
            coordinates=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
        )
        np.testing.assert_array_equal(
            puw.get_value(system.structures.coordinates, to_unit="nm"), before
        )
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"), before
        )
        np.testing.assert_array_equal(
            puw.get_value(
                copied.structures.get_coordinates(indices=[0], structure_indices=[3]),
                to_unit="nm",
            ),
            [[[1.0, 2.0, 3.0]]],
        )
        np.testing.assert_array_equal(
            system.interactions["pairs"].evaluated_structure_indices, range(6)
        )
        np.testing.assert_array_equal(
            copied.interactions["pairs"].evaluated_structure_indices, [0, 1, 2, 4, 5]
        )
        np.testing.assert_array_equal(
            source.interactions["pairs"].evaluated_structure_indices, range(6)
        )
        np.testing.assert_array_equal(
            copied.interactions["pairs"]
            .query(structure_indices=[0])
            .to_dict()["occurrence_indices"],
            [0, 1],
        )
        results.append(
            {
                "deep": deep,
                "ownership_metadata_registry_geometry_and_coverage": "passed",
            }
        )
    assert _source(client_root, client_files) == client
    return {
        "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "probe_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "source-client registry/native copy route; no installed-package or scientific-engine qualification",
        "molsysmt": {
            "reported_version": msm.__version__,
            "import_path": msm.__file__,
            **provider,
        },
        "topomt": {
            "reported_version": topomt_version,
            "import_path": topomt.__file__,
            **client,
        },
        "version_note": "Reported development version strings may reflect an earlier editable build; source commits, status and hashes identify the tested code.",
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = qualify()
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"TopoMT native-copy source route: 2 passed; wrote {args.output}")


if __name__ == "__main__":
    main()
