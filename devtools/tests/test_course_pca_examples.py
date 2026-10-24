"""Execute the actual PCA lesson cells against bundled molecular systems."""

import json
from pathlib import Path

import pytest

COURSE = Path(__file__).resolve().parents[2] / "docs/content/course"


@pytest.mark.parametrize(
    "path", ["Path_Alzheimer", "Path_Enzyme", "Path_Antiviral", "Path_Biophysics"]
)
def test_pca_course_examples_execute_with_real_demo_selections(path):
    notebook = COURSE / path / "35_Principal_Components.ipynb"
    namespace = {}
    for cell in json.loads(notebook.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(notebook), "exec"), namespace)
    # Empty or substituted demonstrations cannot satisfy the lesson's PCA intent.
    assert namespace["eigenvectors"].shape[0] > 0
    assert namespace["eigenvectors"].shape[0] == len(namespace["eigenvalues"])
