"""Integrity tests for the artifacts used by the curated scientific suite."""

from __future__ import annotations

import ast
import hashlib
import re
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[3]
PROVENANCE = Path(__file__).with_name("PROVENANCE.md")
SYSTEMS_MODULE = REPOSITORY / "molsysmt" / "systems.py"
SHA256 = re.compile(r"[0-9a-f]{64}")


def _nested_catalog_key(node: ast.Subscript) -> tuple[str, str] | None:
    if not isinstance(node.value, ast.Subscript):
        return None
    root = node.value.value
    is_catalog = (
        isinstance(root, ast.Name) and root.id == "systems"
    ) or (
        isinstance(root, ast.Attribute) and root.attr == "systems"
    )
    if not is_catalog:
        return None
    try:
        return ast.literal_eval(node.value.slice), ast.literal_eval(node.slice)
    except (ValueError, TypeError):
        return None


def _catalog_paths() -> dict[tuple[str, str], Path]:
    tree = ast.parse(SYSTEMS_MODULE.read_text(encoding="utf-8"))
    paths = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Subscript):
            continue
        key = _nested_catalog_key(target)
        value = node.value
        if key is None or not isinstance(value, ast.Call):
            continue
        if not isinstance(value.func, ast.Name) or value.func.id != "path":
            continue
        package, filename = (ast.literal_eval(argument) for argument in value.args)
        paths[key] = Path(*package.split("."), filename)
    return paths


def _curated_catalog_paths() -> set[Path]:
    sources = [Path(__file__).parents[1] / "conftest.py"]
    sources.extend(
        path for path in Path(__file__).parent.rglob("test_*.py") if path != Path(__file__)
    )
    keys = set()
    for source in sources:
        tree = ast.parse(source.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                key = _nested_catalog_key(node)
                if key is not None:
                    keys.add(key)

    catalog = _catalog_paths()
    missing = keys - catalog.keys()
    assert not missing, f"Curated tests reference unknown catalog entries: {sorted(missing)}"
    return {catalog[key] for key in keys}


def _declared_digests() -> dict[Path, str]:
    declared = {}
    for line in PROVENANCE.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 4:
            continue
        path_match = re.fullmatch(r"`([^`]+)`", cells[1])
        digest_match = re.fullmatch(r"`([0-9a-f]{64})`", cells[3])
        if path_match and digest_match:
            path = Path(path_match.group(1))
            assert path not in declared, f"Duplicate provenance row for {path}"
            declared[path] = digest_match.group(1)
    assert declared, "PROVENANCE.md contains no artifact rows"
    return declared


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def test_curated_artifact_provenance_is_complete_and_matches_files():
    """Hashing every declared artifact and covering every curated catalog input."""

    declared = _declared_digests()
    missing_rows = _curated_catalog_paths() - declared.keys()
    assert not missing_rows, (
        "Curated catalog artifacts missing from PROVENANCE.md: "
        f"{sorted(map(str, missing_rows))}"
    )

    for relative_path, expected_digest in declared.items():
        assert SHA256.fullmatch(expected_digest)
        artifact = REPOSITORY / relative_path
        assert artifact.is_file(), f"Missing curated artifact: {relative_path}"
        assert _sha256(artifact) == expected_digest, (
            f"Curated artifact digest mismatch: {relative_path}"
        )
