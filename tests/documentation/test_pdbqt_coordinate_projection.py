"""Execute the public prepared-format tutorial and the new course example."""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_prepared_projection_tutorial_and_course_examples(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tutorial = ROOT / "docs/content/user/tools/form/project_pdbqt_coordinates.md"
    scope = {}
    for code in re.findall(r"```python\n(.*?)\n```", tutorial.read_text(), re.S):
        exec(compile(code, str(tutorial), "exec"), scope)
    result = scope["projection"]
    assert result["report"]["coordinate_to_source_atom_indices"] == [1, 0]
    assert result["report"]["metadata_disposition"]["discarded_remark_count"] == 1
    assert result["molecular_system"].splitlines()[1][68:76] == "  -0.250"
    course = (
        ROOT / "docs/content/course/Common_Core/10_Modifying_Molecular_Attributes.ipynb"
    )
    cells = json.loads(course.read_text())["cells"]
    code = next(c for c in cells if c.get("id") == "prepared-pdbqt-projection-code")
    scope = {}
    exec(compile("".join(code["source"]), str(course), "exec"), scope)
    result = scope["projection"]
    assert result["report"]["output_to_source_structure_indices"] == [0]
    assert (
        result["molecular_system"].removeprefix("pdbqt_text:").splitlines()[0][68:76]
        == "   0.125"
    )
