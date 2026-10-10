"""Measure bounded site geometry and numeric output in isolated source processes.

Run ``python benchmarks/get_hbond_site_directions.py --output /tmp/site_directions.json``.
End-to-end timings include recognition, units and attribution. Reducer timings
include projected vector geometry, model arithmetic and sparse block packing;
they exclude final concatenation and unit presentation. Peak RSS includes imports,
input coordinates, retained outputs and allocator caches, not just result bytes.
These local source measurements do not qualify installed artifacts.
"""

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
import sys
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CASES = {
    "many_structures": (1, 10000, False),
    "many_sites": (100, 1000, False),
    "periodic": (100, 1000, True),
}


def worker(case):
    import resource

    import numpy as np
    from rdkit import Chem

    import molsysmt as msm
    from molsysmt import pyunitwizard as puw
    from molsysmt.interactions.hbonds._hbond_directions import DirectionReducer
    from molsysmt.native import Structures

    n_sites, n_structures, pbc = CASES[case]
    molecule = Chem.MolFromSmiles(".".join(["CC=O"] * n_sites))
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    one = np.tile([[0.0, 0.1, 0], [0, 0, 0], [0.1, 0, 0]], (n_sites, 1))
    one[:, 0] += np.repeat(np.arange(n_sites) * 0.4, 3)
    cell = np.eye(3) * 100.0
    if pbc:
        one += np.tile([[1, -1, 0], [0, 1, 0], [-1, 0, 0]], (n_sites, 1)) @ cell
    source.structures = Structures(
        coordinates=puw.quantity(np.repeat(one[None], n_structures, axis=0), "nm"),
        box=puw.quantity(np.repeat(cell[None], n_structures, axis=0), "nm")
        if pbc
        else None,
    )
    original_consume = DirectionReducer.consume
    block_seconds = []

    def timed_consume(self, chunk):
        start = perf_counter()
        original_consume(self, chunk)
        block_seconds.append(perf_counter() - start)

    DirectionReducer.consume = timed_consume
    samples = []
    for trial in range(4):
        block_seconds.clear()
        start = perf_counter()
        result = msm.interactions.hbonds.get_hbond_site_directions(
            source, heavy_mode="force", pbc=pbc
        )
        seconds = perf_counter() - start
        assert len(result["directions"]) == n_sites * n_structures * 2
        np.testing.assert_allclose(result["directions"][:, 0], 0.5, atol=1e-12)
        assert np.all(result["status"] == 1)
        samples.append(
            dict(
                seconds=seconds,
                geometry_and_packing_seconds=sum(block_seconds),
                chunks=len(block_seconds),
            )
        )
        if trial < 3:
            del result
    numeric = sum(
        value.nbytes for value in result.values() if isinstance(value, np.ndarray)
    )
    numeric += puw.get_value(result["origins"]).nbytes
    return dict(
        case=case,
        n_atoms=n_sites * 3,
        n_sites=n_sites,
        n_structures=n_structures,
        n_directions=len(result["directions"]),
        pbc=pbc,
        cold=samples[0],
        warm=samples[1:],
        median_warm_seconds=statistics.median(
            value["seconds"] for value in samples[1:]
        ),
        median_warm_geometry_and_packing_seconds=statistics.median(
            value["geometry_and_packing_seconds"] for value in samples[1:]
        ),
        top_level_numeric_bytes=numeric,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        software=result["software"],
        chunk_size=msm.configure.chunk_size,
        numeric_budget=msm.configure.max_ram_usage,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=CASES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.worker:
        print(json.dumps(worker(args.worker)))
        return
    hashes = {
        str(path): hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in (
            Path("molsysmt/interactions/hbonds/get_hbond_site_directions.py"),
            Path("molsysmt/interactions/hbonds/_hbond_directions.py"),
            Path("molsysmt/basic/_index_validation.py"),
            Path("molsysmt/structure/get_vectors.py"),
            Path("molsysmt/structure/_vectors.py"),
            Path("benchmarks/get_hbond_site_directions.py"),
        )
    }
    cases = []
    for case in CASES:
        process = subprocess.run(
            [sys.executable, __file__, "--worker", case],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        cases.append(json.loads(process.stdout))
    report = dict(
        schema="molsysmt.site_directions_benchmark@1",
        python=platform.python_version(),
        platform=platform.platform(),
        source_base=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        source_hashes=hashes,
        evidence="local_source_not_installed_qualification",
        cases=cases,
    )
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(
        json.dumps(
            {
                value["case"]: dict(
                    seconds=value["median_warm_seconds"],
                    bytes=value["top_level_numeric_bytes"],
                )
                for value in cases
            }
        )
    )


if __name__ == "__main__":
    main()
