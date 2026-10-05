"""Executing the README's native preparation without optional repair engines."""

import ast
import builtins
import re
from pathlib import Path

import pytest


@pytest.fixture
def without_optional_engines(monkeypatch):
    original_import = builtins.__import__

    def guarded_import(name, *args, **kwargs):
        if name.split(".")[0] in {"openmm", "pdbfixer"}:
            raise AssertionError(f"Native preparation imported {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", guarded_import)


def test_readme_native_preparation_without_openmm_or_pdbfixer(without_optional_engines):

    readme = Path(__file__).resolve().parents[2] / "README.md"
    code = re.search(r"```python\n(.*?)```", readme.read_text(), re.DOTALL)[1]
    tree = ast.parse(code)
    # The final, explicitly optional OpenMM handoff is outside the native claim.
    assert isinstance(tree.body[-1], ast.Assign)
    assert tree.body[-1].targets[0].id == "sim"
    tree.body.pop()
    namespace = {}
    exec(compile(tree, str(readme), "exec"), namespace)
    msm = namespace["msm"]
    molsys = namespace["molsys"]
    assert msm.get(molsys, n_structures=True) == 1
    assert msm.get(molsys, n_atoms=True) > 596
    assert msm.get(molsys, box=True) is not None


@pytest.mark.parametrize("water_model,n_sites", [("TIP3P", 3), ("SPC/E", 3), ("SPC", 3), ("TIP4P-EW", 4)])
def test_native_water_models_without_optional_engines(without_optional_engines, water_model, n_sites):
    import molsysmt as msm

    solute = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    solvated = msm.build.solvate(
        solute, water_model=water_model, clearance="0.5 nm", engine="MolSysMT"
    )
    n_waters = msm.get(solvated, n_waters=True)
    assert n_waters > 0
    water_atoms = msm.select(solvated, selection='group_type=="water"')
    assert len(water_atoms) == n_sites * n_waters
    n_bonds = msm.get(solvated, n_bonds=True)
    assert n_bonds == msm.get(solute, n_bonds=True) + 2 * n_waters
