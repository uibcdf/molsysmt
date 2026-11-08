"""Keep bounded pose examples executable without changing existing course outputs."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "relative",
    [
        "docs/content/user/tools/structure/get_pairwise_rmsd.ipynb",
        "docs/content/user/tools/structure/get_distance_clusters.ipynb",
        "docs/content/user/cookbook/clustering_poses.ipynb",
        "docs/content/course/Common_Core/16_Structural_Operations.ipynb",
    ],
)
def test_bounded_pose_examples_are_executed_and_keep_scientific_assertions(relative):
    notebook = json.loads((ROOT / relative).read_text())
    cells = [
        cell
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and (
            "Common_Core" not in relative
            or cell.get("id", "").startswith("bounded-pairwise604-")
        )
    ]
    namespace = {}
    assert cells
    for cell in cells:
        assert cell["execution_count"] is not None
        assert not any(output["output_type"] == "error" for output in cell["outputs"])
        exec(compile("".join(cell["source"]), relative, "exec"), namespace)
    # The source examples assert independent analytic values, not only shapes.
    assert any("assert " in "".join(cell["source"]) for cell in cells)
