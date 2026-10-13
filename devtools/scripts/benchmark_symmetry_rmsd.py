"""Measure warm public declared-graph pose RMSD on a reproducible ligand ensemble.

Run from the repository root. Imports, construction, warm-up and correctness
checks are outside timings. This Linux-only receipt records whole-process peak
RSS, not incremental operation memory or cold import time.
"""

import argparse
import hashlib
import json
import platform
import resource
import statistics
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from rdkit import Chem, rdBase

import molsysmt as msm


def measure(function, trials):
    function()
    samples = []
    for _ in range(trials):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return {"samples_seconds": samples, "median_seconds": statistics.median(samples)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--structures", type=int, default=1000)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.structures < 1 or args.trials < 1:
        parser.error("structures and trials must be positive")
    molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1"), to_form="molsysmt.MolSys")
    phase = np.arange(6) * np.pi / 3
    xyz = 0.14 * np.column_stack((np.cos(phase), np.sin(phase), np.zeros(6)))
    coordinates = np.repeat(xyz[None], args.structures, axis=0)
    coordinates[1::2] = xyz[[1, 2, 3, 4, 5, 0]]
    shifts = np.arange(args.structures) * 0.0001
    coordinates[:, :, 2] += shifts[:, None]
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
    mappings = msm.topology.get_atom_correspondences(molsys)
    options = dict(selection="all", reference_molecular_system=molsys, num_threads=1)

    def cached(source, heavy):
        return msm.structure.get_symmetry_corrected_rmsd(
            source, correspondences=mappings, heavy_mode=heavy, **options
        )

    controls = {}
    with tempfile.TemporaryDirectory(prefix="molsysmt-symmetry-benchmark-") as root:
        path = Path(root) / "source.h5msm"
        msm.convert(molsys, to_form="file:h5msm", output_filename=str(path))
        for name, source, heavy in (
            ("native_eager", molsys, "off"),
            ("native_chunked", molsys, "force"),
            ("h5msm_chunked", str(path), "force"),
        ):
            result = cached(source, heavy)
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"),
                shifts,
                atol=1e-14,
            )
            controls[name] = measure(
                lambda source=source, heavy=heavy: cached(source, heavy), args.trials
            )
            controls[name]["execution"] = result["execution"]
        controls["construct_and_native_eager"] = measure(
            lambda: msm.structure.get_symmetry_corrected_rmsd(
                molsys, heavy_mode="off", **options
            ),
            args.trials,
        )
        disk_bytes = path.stat().st_size
        disk_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    source_files = [
        "molsysmt/topology/get_atom_correspondences.py",
        "molsysmt/topology/_atom_correspondences.py",
        "molsysmt/structure/get_symmetry_corrected_rmsd.py",
        "molsysmt/structure/_symmetry_rmsd.py",
        __file__,
    ]
    receipt = dict(
        schema="molsysmt.symmetry_rmsd_benchmark@1",
        observed_at=datetime.now(timezone.utc).isoformat(),
        workload=dict(
            n_atoms=6,
            n_structures=args.structures,
            n_maps=12,
            coordinate_sha256=hashlib.sha256(coordinates.tobytes()).hexdigest(),
        ),
        environment=dict(
            platform=platform.platform(),
            python=platform.python_version(),
            molsysmt=msm.__version__,
            rdkit=rdBase.rdkitVersion,
            numpy=np.__version__,
            num_threads=1,
            chunk_size=msm.configure.chunk_size,
        ),
        source=dict(
            head=subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True
            ).strip(),
            worktree=subprocess.check_output(
                ["git", "status", "--porcelain"], text=True
            ).splitlines(),
            file_sha256={
                str(
                    Path(name).relative_to(Path.cwd())
                    if Path(name).is_absolute()
                    else name
                ): hashlib.sha256(Path(name).read_bytes()).hexdigest()
                for name in source_files
            },
        ),
        cases=controls,
        storage=dict(
            source_h5msm_bytes=disk_bytes,
            source_h5msm_sha256=disk_hash,
            coordinate_numeric_bytes=coordinates.nbytes,
            mapping_numeric_bytes=sum(
                mappings[name].nbytes
                for name in ("atom_correspondences", "context_atom_correspondences")
            ),
            result_axis_numeric_bytes=args.structures * 32,
        ),
        whole_process_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        * 1024,
        limitations="Linux warm source calls; no concurrent pytest in retained measurement. Other host load uncontrolled. Peak RSS includes imports and caller-owned data, not incremental work. One small highly symmetric ligand is not a macromolecular scaling study or installed artifact qualification.",
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(
        json.dumps(
            {name: values["median_seconds"] for name, values in controls.items()}
        )
    )


if __name__ == "__main__":
    main()
