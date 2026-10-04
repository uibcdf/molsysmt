"""Protecting the preserved Rust experiment without adding a release tag."""

import hashlib
import json
import subprocess

import pytest

from devtools.scripts.validate_development_archives import (
    ARCHIVE_DIRECTORY,
    REPOSITORY_ROOT,
    validate_archive,
)

MANIFEST = ARCHIVE_DIRECTORY / "rust_c1_spike_20261002.json"


def test_rust_spike_archive_restores_exact_objects():
    validate_archive(MANIFEST)


def test_rust_spike_archive_replaces_nonrelease_tag():
    """Fail if the archive is lost or the rejected development tag returns."""
    validate_archive(MANIFEST)
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["commit"] == "87317ba766e8d99e6b5129e25eebb83ffb089c0d"
    assert manifest["tag_object"] == "6456293bb980e32b15b885c5b38a344af4cafd03"
    assert manifest["original_ref"] == "refs/tags/archive/rust-c1-spike-20261002"
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", manifest["original_ref"]],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
    )
    assert result.returncode == 1, (
        "The nonrelease tag still occupies the release namespace"
    )


@pytest.mark.parametrize("defect", ["checksum", "commit", "tag_object"])
def test_corrupted_archive_or_identity_is_rejected(tmp_path, defect):
    manifest = json.loads(MANIFEST.read_text())
    bundle = tmp_path / manifest["bundle"]
    data = (ARCHIVE_DIRECTORY / manifest["bundle"]).read_bytes()
    if defect == "checksum":
        data = data[:-1] + bytes([data[-1] ^ 1])
    else:
        manifest[defect] = "0" * 40
    bundle.write_bytes(data)
    copied = tmp_path / MANIFEST.name
    copied.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="mismatch"):
        validate_archive(copied)


def test_metadata_cannot_replace_the_archive_payload(tmp_path):
    """Even a checksum matching an empty bundle cannot borrow source objects."""
    manifest = json.loads(MANIFEST.read_text())
    # Keep the valid header and replace the pack with an empty, valid Git pack.
    original = (ARCHIVE_DIRECTORY / manifest["bundle"]).read_bytes()
    header = original.split(b"\n\n", 1)[0] + b"\n\n"
    pack = b"PACK" + (2).to_bytes(4, "big") + (0).to_bytes(4, "big")
    data = header + pack + hashlib.sha1(pack).digest()
    (tmp_path / manifest["bundle"]).write_bytes(data)
    manifest["sha256"] = hashlib.sha256(data).hexdigest()
    copied = tmp_path / MANIFEST.name
    copied.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="missing from the restored pack"):
        validate_archive(copied)
