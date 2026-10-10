"""Measure fresh-process form validation and conversion without changing policy.

Conversion mode measures the public cold conversion, repeated file conversion
and conversion of an already prepared MolSys separately. Validation mode also
instruments the registry scan; its subsequent conversion is already warmed.
Neither mode measures contact calculation or a complete client workflow.
"""

import argparse
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from statistics import median
from time import perf_counter

ROOT = Path(__file__).resolve().parents[2]


def _source_state(module):
    """Identify an actual checkout independently of distribution metadata."""
    directory = Path(module.__file__).resolve().parent.parent
    if not (directory / ".git").exists():
        return {"kind": "installed", "commit": None, "dirty": None}
    commit = subprocess.check_output(
        ["git", "-C", str(directory), "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "-C", str(directory), "status", "--porcelain"], text=True
    )
    return {"kind": "checkout", "commit": commit, "dirty": bool(dirty)}


def _worker(path, mode):
    """Perform one independently initialized measurement and public parity check."""
    start = perf_counter()
    import molsysmt as msm

    result = {"import_seconds": perf_counter() - start, "worker_pid": os.getpid()}
    before = {name for name in sys.modules if name.startswith("molsysmt.form.")}
    result["initial_form_modules"] = sorted(before)
    if mode == "validation":
        from depdigest import LazyRegistry

        from molsysmt._private.argdigest.argument.to_form import digest_to_form

        scans = []
        original = LazyRegistry._scan_and_load

        def observed(registry):
            start = perf_counter()
            try:
                return original(registry)
            finally:
                scans.append(perf_counter() - start)

        LazyRegistry._scan_and_load = observed
        try:
            start = perf_counter()
            assert digest_to_form("molsysmt.MolSys") == "molsysmt.MolSys"
            result["target_validation_seconds"] = perf_counter() - start
        finally:
            LazyRegistry._scan_and_load = original
        result["scan_seconds"] = scans
        result["validation_added_form_modules"] = len(
            {name for name in sys.modules if name.startswith("molsysmt.form.")} - before
        )

    start = perf_counter()
    molsys = msm.convert(path, to_form="molsysmt.MolSys")
    key = (
        "first_conversion_seconds"
        if mode == "conversion"
        else "conversion_after_validation_seconds"
    )
    result[key] = perf_counter() - start
    result["conversion_added_form_modules"] = len(
        {name for name in sys.modules if name.startswith("molsysmt.form.")} - before
    )
    start = perf_counter()
    repeated = msm.convert(path, to_form="molsysmt.MolSys")
    result["repeated_conversion_seconds"] = perf_counter() - start
    start = perf_counter()
    prepared = msm.convert(molsys, to_form="molsysmt.MolSys")
    result["prepared_conversion_seconds"] = perf_counter() - start

    # Verify outside every timed region. Prepared input presupposes the complete
    # first conversion and warmed provider modules; it is not a cold file route.
    attributes = dict.fromkeys(
        [
            "atom_index",
            "atom_id",
            "atom_name",
            "atom_type",
            "group_index",
            "group_id",
            "group_name",
            "bonded_atom_pairs",
            "bond_order",
            "formal_charge",
            "coordinates",
            "box",
            "time",
        ],
        True,
    )
    for candidate in (repeated, prepared):
        assert msm.compare(molsys, candidate, include_none=True, **attributes), (
            "Measured conversions did not retain the compared molecular attributes."
        )
    result["parity_checked"] = list(attributes)
    result["n_atoms"] = molsys.get_n_atoms()
    native = sys.modules.get("molsysmt._rust")
    result["native_sha256"] = (
        hashlib.sha256(Path(native.__file__).read_bytes()).hexdigest()
        if native is not None
        else None
    )
    result["software"] = {
        name: {
            "distribution_version": importlib.metadata.version(name),
            "source": _source_state(importlib.import_module(name)),
        }
        for name in ["molsysmt", "depdigest", "argdigest", "smonitor", "pyunitwizard"]
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", type=Path, default=ROOT / "molsysmt/data/pdb/181l.pdb"
    )
    parser.add_argument(
        "--mode", choices=["conversion", "validation"], default="conversion"
    )
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--_worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.trials < 1 or not args.input.is_file():
        parser.error("trials must be positive and input must be an existing local file")
    path = args.input.resolve()
    if args._worker:
        print(json.dumps(_worker(str(path), args.mode)))
        return

    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    samples = []
    for _ in range(args.trials):
        run = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--_worker",
                "--input",
                str(path),
                "--mode",
                args.mode,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if run.stderr:
            sys.stderr.write(run.stderr)
        if run.returncode:
            sys.stderr.write(run.stdout)
            raise subprocess.CalledProcessError(
                run.returncode, run.args, output=run.stdout, stderr=run.stderr
            )
        samples.append(json.loads(run.stdout))
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError("Input bytes changed during measurement.")
    timings = {
        name
        for name, value in samples[0].items()
        if name.endswith("_seconds") and isinstance(value, (int, float))
    }
    print(
        json.dumps(
            {
                "schema": "molsysmt.form_registry_startup_benchmark@1",
                "mode": args.mode,
                "python": platform.python_version(),
                "platform": platform.platform(),
                "logical_cpus": os.cpu_count(),
                "input_name": path.name,
                "input_sha256": digest,
                "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "samples": samples,
                "median_seconds": {
                    name: median(s[name] for s in samples) for name in sorted(timings)
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
