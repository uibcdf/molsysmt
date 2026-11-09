"""Execute the public experimental storage examples as one user workflow."""

import re
from pathlib import Path


def test_experimental_storage_guide_examples_execute():
    page = Path(__file__).parents[2] / "docs/content/user/tools/form/file/h5msm_06.md"
    blocks = re.findall(r"^```python\n(.*?)^```", page.read_text(), flags=re.M | re.S)
    assert len(blocks) == 2
    namespace = {"__name__": "h5msm_06_guide"}
    for block in blocks:
        exec(compile(block, str(page), "exec"), namespace)
    assert namespace["mechanics"].forcefield == "request"
    assert namespace["molsys_A"].get(n_atoms=True, n_structures=True) == [2, 1]
