"""Export the actual peptide lesson's model through the public viewer API.

Run from the repository root in the qualified documentation environment:
python docs/generate_static_views/course_alzheimer_peptide.py
"""

import argparse
import json
import os
from pathlib import Path

SCIENCE_CELLS = (
    "peptide759-imports",
    "peptide759-uncapped",
    "peptide759-capped",
    "peptide759-helical",
    "peptide759-angles",
)
DOCS = Path(__file__).resolve().parents[1]
LESSON = DOCS / "content/course/Path_Alzheimer/24_Peptide_Synthesis.ipynb"
DEFAULT_OUTPUT = DOCS / "_static/views/course_alzheimer_peptide_helix.html"


def main(output_filename=None):
    """Generate this scene without duplicating the lesson's scientific recipe."""
    if os.environ.get("MSM_VIEWS_FROM_HTML_FILES", "").lower() == "true":
        raise RuntimeError("Run scene generation outside notebook pre-execution.")
    cells = {c.get("id"): c for c in json.loads(LESSON.read_text())["cells"]}
    namespace = {"__name__": "__peptide_lesson_generation__"}
    for key in SCIENCE_CELLS:
        cell = cells[key]
        if cell["cell_type"] != "code":
            raise ValueError(f"Expected an executable scientific cell: {key}")
        exec(compile("".join(cell["source"]), str(LESSON), "exec"), namespace)
    output = Path(output_filename) if output_filename is not None else DEFAULT_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    with namespace["msm"].view(namespace["helical_peptide"]) as view:
        view.whole.set_representation("ball-and-stick")
        view.export.html(
            str(output),
            title="KLVFF with declared initial backbone torsions",
            shared_runtime=str(output.parent.parent),
            background="transparent",
        )
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, help="Override this scene's HTML output."
    )
    arguments = parser.parse_args()
    print(main(arguments.output))
