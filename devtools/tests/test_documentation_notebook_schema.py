"""Validate stored documentation notebooks without reader-side schema repairs."""

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
# Discover source notebooks; generated builds and editor checkpoints are excluded.
NOTEBOOKS = tuple(
    sorted(
        path.relative_to(DOCS).as_posix()
        for path in (DOCS / "content").rglob("*.ipynb")
        if ".ipynb_checkpoints" not in path.parts
    )
) + ("index.ipynb",)


def _validator():
    path = ROOT / "devtools/scripts/validate_notebook_schemas.py"
    spec = importlib.util.spec_from_file_location("notebook_schema_gate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("relative_path", NOTEBOOKS)
def test_documentation_notebook_schema(relative_path):
    errors = _validator().validate_notebook(DOCS / relative_path)
    assert errors == [], "\n".join(errors)


def _notebook(minor=5):
    cell = {
        "cell_type": "code",
        "metadata": {},
        "source": ["print(1)"],
        "execution_count": 1,
        "outputs": [{"output_type": "stream", "name": "stdout", "text": ["1\n"]}],
    }
    if minor >= 5:
        cell["id"] = "example-cell"
    return {"nbformat": 4, "nbformat_minor": minor, "metadata": {}, "cells": [cell]}


def _write(path, notebook):
    path.write_text(json.dumps(notebook), encoding="utf-8")
    return path.read_bytes()


def _cli(*paths):
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "devtools/scripts/validate_notebook_schemas.py"),
            *map(str, paths),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )


@pytest.mark.parametrize("minor", [0, 4, 5])
def test_cli_accepts_declared_supported_schema_without_reserializing(tmp_path, minor):
    path = tmp_path / "valid.ipynb"
    before = _write(path, _notebook(minor))
    result = _cli(path)
    assert result.returncode == 0, result.stderr
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "defect",
    [
        "old-id",
        "missing-id",
        "duplicate-id",
        "invalid-id",
        "outputs",
        "missing-count",
        "unknown-version",
        "missing-version",
        "not-an-object",
        "nonfinite-json",
    ],
)
def test_cli_rejects_invalid_stored_input_and_keeps_all_source_bytes(tmp_path, defect):
    notebook = _notebook(4 if defect == "old-id" else 5)
    cell = notebook["cells"][0]
    if defect == "old-id":
        cell["id"] = "forbidden-in-4-4"
    elif defect == "missing-id":
        del cell["id"]
    elif defect == "duplicate-id":
        notebook["cells"].append(dict(cell))
    elif defect == "invalid-id":
        cell["id"] = "not a valid id"
    elif defect == "outputs":
        cell["outputs"] = [{"output_type": "invented", "text": "PRIVATE_CELL_CONTENT"}]
    elif defect == "missing-count":
        del cell["execution_count"]
    elif defect == "unknown-version":
        notebook["nbformat_minor"] = 999
    elif defect == "missing-version":
        del notebook["nbformat_minor"]
    elif defect == "not-an-object":
        notebook = []
    elif defect == "nonfinite-json":
        notebook["metadata"]["value"] = float("nan")
    path = tmp_path / "invalid.ipynb"
    before = _write(path, notebook)
    result = _cli(path)
    assert result.returncode != 0
    assert "Notebook schema validation failed" in result.stderr
    assert "PRIVATE_CELL_CONTENT" not in result.stderr
    assert path.read_bytes() == before


@pytest.mark.parametrize("missing", [False, True])
def test_cli_rejects_empty_or_missing_input_instead_of_passing_vacuously(
    tmp_path, missing
):
    result = _cli(tmp_path / "missing.ipynb" if missing else tmp_path)
    assert result.returncode != 0


def test_directory_validation_deduplicates_and_excludes_generated_sources(tmp_path):
    path = tmp_path / "valid.ipynb"
    _write(path, _notebook())
    for name in ["_build", ".ipynb_checkpoints"]:
        hidden = tmp_path / name
        hidden.mkdir()
        (hidden / "invalid.ipynb").write_text("not JSON")
    result = _cli(tmp_path, path)
    assert result.returncode == 0, result.stderr
    assert "1 stored sources" in result.stdout


def test_validation_refuses_provider_repairs_and_failures(tmp_path, monkeypatch):
    validator = _validator()
    path = tmp_path / "valid.ipynb"
    before = _write(path, _notebook())

    def repair(notebook, **kwargs):
        notebook["metadata"]["silent-repair"] = True
        return iter(())

    monkeypatch.setattr(validator.nbformat.validator, "iter_validate", repair)
    assert "in-memory" in " ".join(validator.validate_notebook(path))

    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_PROVIDER_DETAIL")

    monkeypatch.setattr(validator.nbformat.validator, "iter_validate", broken)
    errors = validator.validate_notebook(path)
    assert errors and "provider failed" in errors[0]
    assert "PRIVATE_PROVIDER_DETAIL" not in " ".join(errors)
    assert path.read_bytes() == before


def test_validation_rejects_a_source_changed_while_the_provider_runs(
    tmp_path, monkeypatch
):
    validator = _validator()
    path = tmp_path / "valid.ipynb"
    _write(path, _notebook())

    def change_source(*args, **kwargs):
        path.write_text("changed by the controlled provider")
        return iter(())

    monkeypatch.setattr(validator.nbformat.validator, "iter_validate", change_source)
    assert "bytes changed" in " ".join(validator.validate_notebook(path))


@pytest.mark.skipif(
    shutil.which("make") is None, reason="The local Makefile route requires make"
)
@pytest.mark.parametrize("valid", [False, True])
def test_documentation_make_checks_schema_before_a_successful_sphinx(tmp_path, valid):
    import shlex

    docs = tmp_path / "docs"
    docs.mkdir()
    shutil.copyfile(DOCS / "Makefile", docs / "Makefile")
    scripts = tmp_path / "devtools/scripts"
    scripts.mkdir(parents=True)
    shutil.copyfile(
        ROOT / "devtools/scripts/validate_notebook_schemas.py",
        scripts / "validate_notebook_schemas.py",
    )
    notebook = _notebook(4)
    if not valid:
        notebook["cells"][0]["id"] = "forbidden-in-4-4"
    before = _write(docs / "index.ipynb", notebook)
    (docs / "content").mkdir()
    marker = tmp_path / "sphinx-ran"
    fake = tmp_path / "successful_sphinx.py"
    fake.write_text(
        "from pathlib import Path\n" + f"Path({str(marker)!r}).write_text('ran')\n"
    )
    # This process always succeeds; only the actual schema preflight rejects input.
    sphinx = f"{shlex.quote(sys.executable)} {shlex.quote(str(fake))}"
    result = subprocess.run(
        [
            "make",
            "-C",
            str(docs),
            "html",
            f"PYTHON={shlex.quote(sys.executable)}",
            f"SPHINXBUILD={sphinx}",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert (result.returncode == 0) is valid, result.stdout + result.stderr
    assert marker.exists() is valid
    assert (docs / "index.ipynb").read_bytes() == before
