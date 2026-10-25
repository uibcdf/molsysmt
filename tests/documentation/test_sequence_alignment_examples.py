"""Execute alignment examples with real scientific tools and local source inputs."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


def test_sequence_component_cookbook_executes_its_rigid_pose_checks():
    path = ROOT / "docs/content/user/cookbook/aligning_components_by_sequence.md"
    namespace = {}
    for code in re.findall(r"```python\n(.*?)```", path.read_text(), re.S):
        exec(compile(code, str(path), "exec"), namespace)
    assert np.allclose(
        msm.pyunitwizard.get_value(namespace["rmsd"], to_unit="nm"), 0.0, atol=1e-11
    )


@pytest.mark.parametrize("domain", ["Alzheimer", "Enzyme", "Antiviral", "Biophysics"])
def test_comparison_course_keeps_aligned_system_and_measures_actual_rmsd(
    domain, monkeypatch
):
    pytest.importorskip("matplotlib")
    original = msm.convert

    def local_convert(source, *args, **kwargs):
        # Replace remote identity only; preserve all scientific arguments.
        if isinstance(source, str) and source in {"pdb:6EQE", "pdb:6LU7", "pdb:1K4C"}:
            if source == "pdb:6LU7":
                # A separate peptide supplies CA atoms, as the real N3 ligand does.
                protein = original(msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"])
                peptide = original(
                    msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
                    structure_indices=[0],
                )
                source = msm.merge([protein, peptide])
            else:
                source = msm.systems["T4 lysozyme L99A"]["181l.bcif.gz"]
        return original(source, *args, **kwargs)

    monkeypatch.setattr(msm, "convert", local_convert)
    path = ROOT / f"docs/content/course/Path_{domain}/34_Comparison_Superposition.ipynb"
    namespace = {}
    for cell in json.loads(path.read_text())["cells"]:
        if cell["cell_type"] == "code":
            exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
    assert msm.get_form(namespace["aligned_molsys"]) == "molsysmt.MolSys"
    before = msm.pyunitwizard.get_value(namespace["rmsd_raw"], to_unit="nm")
    after = msm.pyunitwizard.get_value(namespace["rmsd_opt"], to_unit="nm")
    assert np.all(np.isfinite(after))
    assert np.all(after <= before + 1e-10)
    if domain in {"Antiviral", "Biophysics"}:
        np.testing.assert_allclose(after, 0.0, atol=1e-10)
    import matplotlib.pyplot as plt

    plt.close("all")
