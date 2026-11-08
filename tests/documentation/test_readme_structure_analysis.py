"""Executing the README's bundled input and public structure-analysis example."""

import re
from pathlib import Path

import numpy as np

import molsysmt as msm


def test_readme_structure_analysis_uses_the_public_chemical_graph_namespace():
    page = Path(__file__).resolve().parents[2] / "README.md"
    blocks = re.findall(r"```python\n(.*?)```", page.read_text(), re.S)
    load = next(block for block in blocks if "['Trp-Cage']" in block)
    analysis = next(block for block in blocks if "quartets =" in block)
    namespace = {}
    for block in (load, analysis):
        exec(compile(block, str(page), "exec"), namespace)
    assert [namespace[key] for key in ("n_atoms", "n_groups", "n_chains")] == [
        304,
        20,
        1,
    ]
    quartets = np.asarray(namespace["quartets"])
    assert quartets.ndim == 2 and quartets.shape[1] == 4 and len(quartets) > 0
    angles = msm.pyunitwizard.get_value(namespace["phi"], to_unit="radian")
    assert angles.shape[-1] == len(quartets)
    assert np.isfinite(angles).all()
    assert msm.pyunitwizard.are_compatible(namespace["rmsd"], "nm")
    assert msm.pyunitwizard.are_compatible(namespace["rg"], "nm")
