"""Validate stored documentation notebooks without reader-side schema repairs."""

import copy
import json
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


@pytest.mark.parametrize("relative_path", NOTEBOOKS)
def test_documentation_notebook_schema(relative_path):
    nbformat = pytest.importorskip("nbformat")
    notebook = json.loads((ROOT / "docs" / relative_path).read_text(encoding="utf-8"))
    original = copy.deepcopy(notebook)

    # Validate the stored JSON directly, without a reader normalizing it first.
    errors = list(nbformat.validator.iter_validate(notebook))
    assert errors == [], "\n".join(str(error) for error in errors)
    assert notebook == original, "Schema validation must not repair the input."

    if notebook["nbformat"] == 4 and notebook["nbformat_minor"] >= 5:
        cell_ids = [cell["id"] for cell in notebook["cells"]]
        assert len(set(cell_ids)) == len(cell_ids), "Cell identifiers must be unique."
