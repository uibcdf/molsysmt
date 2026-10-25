"""Execute documented placement workflows with local molecular inputs."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


def test_center_cookbook_places_rigid_atoms():
    source = (
        ROOT / "docs/content/user/cookbook/placing_selected_centers.md"
    ).read_text()
    namespace = {}
    for code in re.findall(r"```python\n(.*?)```", source, re.S):
        exec(compile(code, "placing_selected_centers.md", "exec"), namespace)
    np.testing.assert_allclose(namespace["xyz"][0, :, 0], [2.0, 4.0, 1.0, 3.0])


@pytest.mark.parametrize("domain", ["Alzheimer", "Enzyme"])
def test_geometric_course_executes_with_local_source_substitutions(domain, monkeypatch):
    """Replace only remote input identifiers; run actual public scientific tools."""
    if domain == "Enzyme":
        pytest.importorskip("rdkit")
    pytest.importorskip("matplotlib")
    original_convert = msm.convert

    def local_convert(molecular_system, *args, **kwargs):
        if isinstance(molecular_system, str):
            if molecular_system == "pdb:6EQE":
                molecular_system = msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"]
            elif molecular_system == "pdb:2BEG":
                molecular_system = msm.systems["pentalanine"]["traj_pentalanine.h5msm"]
        return original_convert(molecular_system, *args, **kwargs)

    monkeypatch.setattr(msm, "convert", local_convert)
    path = (
        ROOT / f"docs/content/course/Path_{domain}/46_Geometric_Transformations.ipynb"
    )
    namespace = {}
    for cell in json.loads(path.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    center = namespace["center" if domain == "Alzheimer" else "new_center"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(center, to_unit="nm"), 0.0, atol=1e-12
    )
    if domain == "Alzheimer":
        assert msm.get(namespace["molsys"], n_structures=True) == 1
        assert namespace["fibril_atom_indices"]
        assert namespace["peptide_atom_indices"]
        assert set(namespace["fibril_atom_indices"]).isdisjoint(
            namespace["peptide_atom_indices"]
        )
    import matplotlib.pyplot as plt

    plt.close("all")
