"""Explicit local GUI guard, separate from the default scientific test lane.

Select this node with pytest in the qualified GUI environment. Set
MOLSYSVIEWER_ROOT and, for the recorded overlay, MOLSYSVIEWER_PROVIDER_ROOT.
Missing browser/Jupyter prerequisites fail; they are not silently skipped.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def test_actual_jupyter_review_and_independent_popups(tmp_path):
    viewer = Path(os.environ["MOLSYSVIEWER_ROOT"]).resolve()
    output = tmp_path / "jupyter"
    command = [
        sys.executable,
        str(Path(__file__).with_name("system_panel_jupyter.py")),
        "--viewer-root",
        str(viewer),
        "--output",
        str(output),
    ]
    if provider := os.environ.get("MOLSYSVIEWER_PROVIDER_ROOT"):
        command.extend(["--provider-root", provider])
    subprocess.run(command, check=True, timeout=300)
    result = json.loads((output / "full-result.json").read_text())
    assert len(result["checks"]) == 6
    assert result["final_atoms"] == 3817
    assert result["managed_edits"] == 2
    assert not (output / "settings.json").exists()
    assert not (output / "config/jupyter_server_config.py").exists()
