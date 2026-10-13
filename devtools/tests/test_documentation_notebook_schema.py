"""Validate notebooks affected by the schema mismatch recorded in #144."""

import copy
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = (
    "content/course/Common_Core/08_Extracting_Molecular_Attributes.ipynb",
    "content/course/Common_Core/10_Modifying_Molecular_Attributes.ipynb",
    "content/course/Common_Core/19_Structures_and_Trajectories.ipynb",
    "content/course/Path_Biophysics/39_Physicochemical_Properties.ipynb",
    "content/user/tools/basic/get.ipynb",
    "content/user/tools/basic/set.ipynb",
)


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
