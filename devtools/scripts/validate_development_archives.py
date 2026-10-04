#!/usr/bin/env python3
"""Checking that a development archive restores its actual Git objects."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_DIRECTORY = REPOSITORY_ROOT / "devtools/data/development_archives"


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repository), *arguments],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def validate_archive(manifest_path: Path, repository: Path = REPOSITORY_ROOT) -> None:
    """Restore an incremental bundle into temporary storage and verify its identity.

    Main history supplies prerequisite objects through an alternate object directory.
    Every archive-specific object must be in a newly restored local pack, so objects
    already present in the source repository cannot substitute for a missing payload.
    The source repository and its refs are never modified.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported development archive schema")
    bundle = (manifest_path.parent / manifest["bundle"]).resolve()
    if bundle.parent != manifest_path.parent.resolve():
        raise ValueError("The bundle must belong to the manifest directory")
    if hashlib.sha256(bundle.read_bytes()).hexdigest() != manifest["sha256"]:
        raise ValueError("Development archive checksum mismatch")
    prerequisite = manifest["prerequisite"]
    _git(repository, "merge-base", "--is-ancestor", prerequisite, "HEAD")
    objects = Path(_git(repository, "rev-parse", "--git-path", "objects"))
    if not objects.is_absolute():
        objects = repository / objects

    with tempfile.TemporaryDirectory(
        prefix="molsysmt-development-archive-"
    ) as directory:
        restored = Path(directory)
        _git(restored, "init", "--bare", "--quiet")
        (restored / "objects/info/alternates").write_text(
            str(objects.resolve()) + "\n", encoding="utf-8"
        )
        expected_head = f"{manifest['tag_object']} {manifest['original_ref']}"
        if _git(restored, "bundle", "list-heads", str(bundle)) != expected_head:
            raise ValueError(
                "Development archive ref or annotated-tag identity mismatch"
            )
        _git(restored, "bundle", "verify", str(bundle))
        _git(restored, "bundle", "unbundle", str(bundle))
        tag = manifest["tag_object"]
        commit = manifest["commit"]
        local_objects = set()
        for index in (restored / "objects/pack").glob("*.idx"):
            listing = _git(restored, "verify-pack", "-v", str(index))
            local_objects.update(line.split()[0] for line in listing.splitlines())
        if tag not in local_objects:
            raise ValueError(
                "Archive-specific Git objects are missing from the restored pack"
            )
        if _git(restored, "cat-file", "-t", tag) != "tag":
            raise ValueError("Development archive does not preserve an annotated tag")
        if _git(restored, "rev-parse", f"{tag}^{{commit}}") != commit:
            raise ValueError("Development archive commit mismatch")
        if _git(restored, "rev-parse", f"{commit}^@") != prerequisite:
            raise ValueError("Development archive prerequisite mismatch")
        needed = set(
            _git(
                restored,
                "rev-list",
                "--objects",
                "--no-object-names",
                tag,
                f"^{prerequisite}",
            ).splitlines()
        )
        if not needed.issubset(local_objects):
            raise ValueError(
                "Archive-specific Git objects are missing from the restored pack"
            )
        # Read the experiment's new objects; unchanged objects belong to main history.
        for object_name in needed:
            _git(restored, "cat-file", "-e", object_name)


def main() -> int:
    manifests = sorted(ARCHIVE_DIRECTORY.glob("*.json"))
    if not manifests:
        raise ValueError("No development archive manifests found")
    for manifest in manifests:
        validate_archive(manifest)
        print(f"PASS: {manifest.relative_to(REPOSITORY_ROOT)} restores its Git objects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
