"""Bind the verified installed Conda matrix to its tested package digests."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from devtools.scripts.validate_conda_staging import _require_staging_provenance


def _staged_identity(record, package, subdir, filename_pattern):
    _require_staging_provenance(record, package)
    if record["url"].rsplit("/", 2)[1] != subdir or not re.fullmatch(
        filename_pattern, record["fn"]
    ):
        raise ValueError(f"Unexpected {package} staging artifact for {subdir}")
    return {field: record[field] for field in ("url", "fn", "sha256")}


def verify_installations(
    matrix, directory, *, molsysmt_version, molsysmt_build, viewer_version, viewer_build
):
    """Identify the files common to the cells of an independently verified run."""
    if (
        matrix.get("schema") != "molsyssuite.installed-matrix@1"
        or matrix.get("state") != "verified"
    ):
        raise ValueError("A verified installed-matrix receipt is required")
    attempt = matrix["run_attempt"]
    cells = {
        directory
        / f"conda-staging-{job['platform']}-py{job['python']}-attempt-{attempt}"
        / "installed-pair.json": (job["platform"], job["python"])
        for job in matrix["jobs"]
        if job["kind"] == "installed"
    }
    if not cells or set(directory.glob("*/installed-pair.json")) != cells.keys():
        raise ValueError(
            "The installed-pair artifact receipts do not cover the exact cells"
        )

    molsysmt_pattern = rf"molsysmt-{re.escape(molsysmt_version)}-pyabi3h[0-9a-f]+_{molsysmt_build}\.conda"
    viewer_pattern = rf"molsysviewer-{re.escape(viewer_version)}-py_{viewer_build}\.(?:conda|tar\.bz2)"
    molsysmt_files = {}
    viewer = None
    for path, (platform, python) in sorted(cells.items()):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if (
            receipt.get("schema") != "molsysmt.installed-conda-pair@1"
            or receipt.get("python") != python
            or any(
                receipt.get(field) != matrix[field]
                for field in ("candidate_sha", "run_id", "run_attempt")
            )
        ):
            raise ValueError(
                f"Wrong source, run, attempt or Python in {path.parent.name}"
            )

        packages = receipt["packages"]
        molsysmt = _staged_identity(
            packages["molsysmt"], "molsysmt", platform, molsysmt_pattern
        )
        if molsysmt_files.setdefault(platform, molsysmt) != molsysmt:
            raise ValueError(
                f"Installed MolSysMT artifact identity differs on {platform}"
            )

        installed_viewer = _staged_identity(
            packages["molsysviewer"], "molsysviewer", "noarch", viewer_pattern
        )
        if viewer is not None and viewer != installed_viewer:
            raise ValueError(
                "Installed MolSysViewer artifact identity differs across cells"
            )
        viewer = installed_viewer

    return {"molsysmt": molsysmt_files, "molsysviewer": viewer}


def require_tested_artifact(files, target, filename, sha256):
    """Reject a promotion request for bytes outside the tested matrix."""
    record = files["molsysmt"].get(target)
    if record is None or (record["fn"], record["sha256"]) != (filename, sha256):
        raise ValueError(f"Requested {target} filename and digest were not tested")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--molsysmt-version", required=True)
    parser.add_argument("--molsysmt-build", type=int, required=True)
    parser.add_argument("--viewer-version", required=True)
    parser.add_argument("--viewer-build", type=int, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    try:
        files = verify_installations(
            matrix,
            args.directory,
            molsysmt_version=args.molsysmt_version,
            molsysmt_build=args.molsysmt_build,
            viewer_version=args.viewer_version,
            viewer_build=args.viewer_build,
        )
        require_tested_artifact(files, args.target, args.filename, args.sha256)
    except (RuntimeError, ValueError, KeyError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(files, indent=2))


if __name__ == "__main__":
    main()
