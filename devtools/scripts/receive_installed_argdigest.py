#!/usr/bin/env python
"""Verifying public ArgDigest bytes and installed consumer receiving evidence."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import platform
import sys
import sysconfig
import tarfile
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree

try:
    from devtools.scripts.validate_installed_molsysmt import (
        _is_editable,
        find_runtime_dependency_violations,
    )
except ImportError:
    from validate_installed_molsysmt import (
        _is_editable,
        find_runtime_dependency_violations,
    )

FILENAME = "argdigest-0.17.1-py_0.tar.bz2"
SHA256 = "5af09e12b0c3d344337f2a2d90ac8b5fcea5be8a8467694c41e3daac018c3899"
PUBLIC_URL = "https://conda.anaconda.org/uibcdf/noarch/" + FILENAME
MODULES = (
    "molsysmt",
    "argdigest",
    "smonitor",
    "depdigest",
    "pyunitwizard",
    "molsysviewer",
    "numpy",
    "pandas",
    "h5py",
    "mmcif",
    "nglview",
    "jinja2",
)


def verify_public_bytes(archive, *, purelib=None, expected_sha256=SHA256):
    """Rejecting a wrong archive or any altered installed provider source."""
    archive = Path(archive)
    with archive.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    if digest != expected_sha256:
        raise RuntimeError("public ArgDigest archive SHA-256 differs")
    purelib = Path(purelib or sysconfig.get_path("purelib"))
    checked = {}
    with tarfile.open(archive, "r:bz2") as package:
        index = json.load(package.extractfile("info/index.json"))
        if (index["name"], index["version"], index["build"]) != (
            "argdigest",
            "0.17.1",
            "py_0",
        ):
            raise RuntimeError("public ArgDigest archive identity differs")
        for member in package.getmembers():
            path = PurePosixPath(member.name)
            if path.parts[:2] != ("site-packages", "argdigest"):
                continue
            if not member.isfile() or ".." in path.parts:
                raise RuntimeError("unexpected public ArgDigest runtime entry")
            relative = Path(*path.parts[1:])
            expected = package.extractfile(member).read()
            actual = purelib / relative
            if not actual.is_file() or actual.read_bytes() != expected:
                raise RuntimeError(
                    f"installed public ArgDigest bytes differ: {relative}"
                )
            checked[relative.as_posix()] = hashlib.sha256(expected).hexdigest()
    if "argdigest/__init__.py" not in checked:
        raise RuntimeError("public ArgDigest archive has no runtime package")
    actual_files = {
        p.relative_to(purelib).as_posix()
        for p in (purelib / "argdigest").rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    }
    if actual_files != set(checked):
        raise RuntimeError("installed public ArgDigest file inventory differs")
    return checked


def installed_origins(*, modules=MODULES, prefix=None, purelib=None):
    """Rejecting editable distributions and imports outside the actual prefix."""
    prefix = Path(prefix or sys.prefix).resolve()
    purelib = Path(purelib or sysconfig.get_path("purelib"))
    result = {}
    for name in modules:
        distribution = metadata.distribution(name)
        if _is_editable(distribution):
            raise RuntimeError(
                f"editable distribution cannot qualify receiving: {name}"
            )
        module = importlib.import_module(name)
        origin = Path(module.__file__).resolve()
        if not origin.is_relative_to(prefix):
            raise RuntimeError(f"installed {name} resolves outside prefix: {origin}")
        if (
            name == "argdigest"
            and origin != (purelib / "argdigest/__init__.py").resolve()
        ):
            raise RuntimeError(
                "imported ArgDigest differs from the verified installed payload"
            )
        result[name] = {
            "version": distribution.version,
            "origin": str(origin),
            "module_sha256": hashlib.sha256(origin.read_bytes()).hexdigest(),
            "direct_url": json.loads(
                distribution.read_text("direct_url.json") or "null"
            ),
        }
    if result.get("argdigest", {}).get("version") != "0.17.1":
        raise RuntimeError("installed public ArgDigest version differs")
    violations = find_runtime_dependency_violations(["molsysmt", "argdigest"])
    if violations:
        raise RuntimeError("installed dependency violations: " + "; ".join(violations))
    return result


def verify_junit(path):
    """Rejecting empty, skipped or unsuccessful receiving executions."""
    root = ElementTree.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    counts = {
        key: sum(int(s.attrib.get(key, 0)) for s in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    if not counts["tests"] or any(
        counts[key] for key in ("failures", "errors", "skipped")
    ):
        raise RuntimeError(f"receiving execution is incomplete: {counts}")
    cases = list(root.iter("testcase"))
    if len(cases) != counts["tests"]:
        raise RuntimeError("receiving JUnit case inventory differs from counters")
    if any(
        case.find(tag) is not None
        for case in cases
        for tag in ("failure", "error", "skipped")
    ):
        raise RuntimeError("receiving JUnit has an unsuccessful case")
    return {
        **counts,
        "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "cases": [
            f"{c.attrib.get('classname', '')}::{c.attrib['name']}" for c in cases
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--consumer-commit", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--consumer-junit", type=Path)
    parser.add_argument("--scientific-junit", type=Path)
    parser.add_argument("--scientific-nodes", type=Path)
    args = parser.parse_args()
    if len(args.consumer_commit) != 40 or any(
        c not in "0123456789abcdef" for c in args.consumer_commit
    ):
        raise RuntimeError("receiving requires the full consumer commit")
    checked = verify_public_bytes(args.archive)
    origins = installed_origins()
    if bool(args.consumer_junit) != bool(args.scientific_junit):
        raise RuntimeError("both receiving executions are required together")
    executions = {}
    if args.consumer_junit:
        executions = {
            "consumer": verify_junit(args.consumer_junit),
            "scientific": verify_junit(args.scientific_junit),
        }
        cases = executions["consumer"]["cases"]
        for guard in (
            "test_inherited_constructors",
            "test_contract_ownership_receiving",
            "test_smonitor_contracts",
        ):
            if not any(guard in case for case in cases):
                raise RuntimeError(
                    f"installed receiving omitted required guard: {guard}"
                )
        if not args.scientific_nodes:
            raise RuntimeError("the registered scientific selection is required")
        nodes = json.loads(args.scientific_nodes.read_text())
        verify_scientific_coverage(nodes, executions["scientific"]["cases"])
        executions["scientific"]["registered_nodes"] = nodes
    payload = {
        "schema": "molsysmt.installed_argdigest_receiving@1",
        "created_at": datetime.now(UTC).isoformat(),
        "consumer_commit": args.consumer_commit,
        "python": sys.version,
        "platform": platform.platform(),
        "prefix": sys.prefix,
        "public_provider": {"filename": FILENAME, "sha256": SHA256, "url": PUBLIC_URL},
        "verified_provider_runtime_files": checked,
        "installed_origins": origins,
        "executions": executions,
        "verdict": "pass" if executions else "preflight_pass",
        "scope": "Linux installed consumer receiving; not an installed release-pair matrix or publication authorization",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        f"Installed ArgDigest receiving: {payload['verdict']} ({len(checked)} verified runtime files)"
    )
    return 0


def verify_scientific_coverage(nodes, cases):
    """Rejecting a successful subset that omits a registered scientific control."""
    if not nodes or len(nodes) != len(set(nodes)):
        raise RuntimeError("invalid registered scientific selection")
    observed = {case.split("[", 1)[0] for case in cases}
    for node in nodes:
        path, *parts = node.split("::")
        expected = path.removesuffix(".py").replace("/", ".") + "::" + "::".join(parts)
        if expected not in observed:
            raise RuntimeError(
                f"installed receiving omitted scientific control: {node}"
            )


if __name__ == "__main__":
    raise SystemExit(main())
