"""Measuring isolated-process PDB reader routes on unchanged original inputs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from hashlib import sha256
from pathlib import Path


def probe(path, engine):
    import builtins
    import platform
    import resource
    import tempfile
    from time import perf_counter

    import numpy as np

    import molsysmt as msm
    from molsysmt import pyunitwizard as puw

    original_bytes = path.read_bytes()
    if engine == "MolSysMT":
        original_import = builtins.__import__

        def block_openmm(name, *args, **kwargs):
            if name == "openmm" or name.startswith("openmm."):
                raise AssertionError("Explicit native inference imported OpenMM")
            return original_import(name, *args, **kwargs)

        builtins.__import__ = block_openmm
    options = dict(get_missing_bonds=engine != "disabled")
    if engine != "disabled":
        options["bond_inference_engine"] = engine
    timings = []
    for _ in range(2):
        start = perf_counter()
        molsys = msm.convert(path, to_form="molsysmt.MolSys", **options)
        timings.append(perf_counter() - start)
    pairs = molsys.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(
        dtype=np.int64
    )
    axis = {
        field: np.asarray(msm.get(molsys, element="atom", **{field: True})).tolist()
        for field in ("atom_id", "atom_name", "atom_type", "group_index", "chain_index")
    }
    coordinates = puw.get_value(molsys.structures.coordinates, to_unit="nm")
    history = molsys.chemical_states.get_preparation_history()
    row = dict(
        engine=engine,
        n_atoms=molsys.get_n_atoms(),
        n_bonds=len(pairs),
        first_conversion_seconds=timings[0],
        repeated_conversion_seconds=timings[1],
        pairs=pairs.tolist(),
        candidate_pair_sha256=sha256(pairs.astype("<i8").tobytes()).hexdigest(),
        atom_axis_sha256=sha256(
            json.dumps(axis, separators=(",", ":")).encode()
        ).hexdigest(),
        coordinate_sha256=sha256(
            np.asarray(coordinates, dtype="<f8").tobytes()
        ).hexdigest(),
        history_schemas=[record["report"]["schema"] for record in history],
        software=history[-1]["report"]["software"],
    )
    if engine == "MolSysMT":
        report = history[-1]["report"]
        row["n_added_bonds"] = report["n_added_bonds"]
        row["unassessed_checks"] = report["unassessed_checks"]
        with tempfile.TemporaryDirectory(prefix="molsysmt-native-pdb-") as directory:
            target = Path(directory) / "native.h5msm"
            start = perf_counter()
            msm.convert(molsys, to_form=str(target))
            row["h5msm_write_seconds"] = perf_counter() - start
            row["h5msm_bytes"] = target.stat().st_size
            start = perf_counter()
            loaded = msm.convert(str(target), to_form="molsysmt.MolSys")
            row["h5msm_read_seconds"] = perf_counter() - start
            np.testing.assert_array_equal(
                loaded.topology.bonds[["atom1_index", "atom2_index"]].to_numpy(
                    dtype=np.int64
                ),
                pairs,
            )
            assert (
                loaded.chemical_states.get_preparation_history()[-1]["report"][
                    "software"
                ]
                == report["software"]
            )
            np.testing.assert_array_equal(
                puw.get_value(loaded.structures.coordinates, to_unit="nm"), coordinates
            )
            row["h5msm_geometry_graph_and_producer_preserved"] = True
    assert path.read_bytes() == original_bytes
    row["process_peak_rss_bytes"] = (
        resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    )
    row["python"] = platform.python_version()
    row["numpy"] = np.__version__
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdb", nargs="+", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compare-openmm", action="store_true")
    parser.add_argument(
        "--child-engine",
        choices=["disabled", "MolSysMT", "OpenMM"],
        help=argparse.SUPPRESS,
    )
    arguments = parser.parse_args()
    if arguments.child_engine:
        print(json.dumps(probe(arguments.pdb[0], arguments.child_engine)))
        return
    if arguments.output is None:
        parser.error("--output is required for the combined receipt")
    sources = []
    for path in arguments.pdb:
        rows = []
        for engine in [
            "disabled",
            "MolSysMT",
            *(["OpenMM"] if arguments.compare_openmm else []),
        ]:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    str(path.resolve()),
                    "--child-engine",
                    engine,
                ],
                check=True,
                text=True,
                capture_output=True,
                env=os.environ.copy(),
            )
            rows.append(json.loads(completed.stdout))
        assert len({row["atom_axis_sha256"] for row in rows}) == 1
        assert len({row["coordinate_sha256"] for row in rows}) == 1
        inventories = {
            row["engine"]: {tuple(pair) for pair in row.pop("pairs")} for row in rows
        }
        assert inventories["disabled"] <= inventories["MolSysMT"]
        source = dict(
            source=path.name, sha256=sha256(path.read_bytes()).hexdigest(), routes=rows
        )
        if arguments.compare_openmm:
            source["native_only_pairs"] = sorted(
                inventories["MolSysMT"] - inventories["OpenMM"]
            )
            source["openmm_only_pairs"] = sorted(
                inventories["OpenMM"] - inventories["MolSysMT"]
            )
        sources.append(source)
    root = Path(__file__).resolve().parents[2]
    implementation_files = {
        name: sha256((root / name).read_bytes()).hexdigest()
        for name in (
            "molsysmt/_private/covalent_inference.py",
            "molsysmt/_private/pdb_connectivity.py",
            "molsysmt/_private/preparation_history.py",
            "molsysmt/build/infer_covalent_bonds.py",
            "molsysmt/form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py",
            "molsysmt/form/molsysmt_Topology/merge.py",
        )
    }
    payload = dict(
        schema="molsysmt.native_pdb_reader_probe@1",
        source_base_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip(),
        implementation_files=implementation_files,
        platform="Linux",
        measurement_scope="Each engine runs in a fresh process. Conversion timings exclude interpreter/package startup; RSS is the whole-process high-water mark, including native H5MSM verification where applicable. Two conversions per process are observations, not a statistical benchmark.",
        sources=sources,
    )
    arguments.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "sources": [
                    {
                        "source": row["source"],
                        "bonds": {
                            route["engine"]: route["n_bonds"] for route in row["routes"]
                        },
                    }
                    for row in sources
                ]
            }
        )
    )


if __name__ == "__main__":
    main()
