"""Execute SDF/PDBQT routes with explicit chemistry and format-specific evidence.

Literal witnesses are shared with the independent format contract suites. Native
source preparation uses the existing reader, so it is not a writer-fidelity oracle.
"""

import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    declared_edges,
    planned_edges,
    read_plan,
)
from tests.conversion_truth.test_declared_native_edges import (
    DOCKING_FORMS,
    _execute_direct,
)
from tests.form.file_pdbqt.test_native_contract import LIGAND, RIGID
from tests.form.file_sdf.test_native_contract import V2000, V3000

PAYLOADS = {
    "V2000": V2000,
    "V3000": V3000,
    "legacy": V2000.replace(" V2000", ""),
    "valence": V3000.replace("80 Na 4 0 0 0 CHG=1", "80 Na 4 0 0 0 CHG=1 VAL=-1"),
    "rigid": RIGID,
    "ligand": LIGAND,
}
SDF_VARIANTS = ("V2000", "V3000", "legacy", "valence")

EDGES = sorted(
    (s, t)
    for s, t in planned_edges(declared_edges(), read_plan())
    if {s, t} & DOCKING_FORMS
)
CASES = [
    (source, target, variant)
    for source, target in EDGES
    for variant in (
        SDF_VARIANTS if "file:sdf" in {source, target} else ("rigid", "ligand")
    )
]


def _source(source, variant, directory):
    directory.mkdir()
    is_sdf = variant in SDF_VARIANTS
    payload = PAYLOADS[variant]
    path = directory / ("source.sdf" if is_sdf else "source.pdbqt")
    path.write_text(payload)
    tree = None
    if source == "molsysmt.MolSys":
        if is_sdf:
            item = msm.convert(path, to_form="molsysmt.MolSys")
        else:
            item = msm.convert(
                path, to_form="molsysmt.MolSys", discard_torsion_tree=True
            )
            if variant == "ligand":
                from molsysmt.form.file_pdbqt import get_torsion_tree

                tree = get_torsion_tree(path)
    elif source == "molsysmt.PDBQTFileHandler":
        from molsysmt.native import PDBQTFileHandler

        item = PDBQTFileHandler(path)
    elif source == "string:pdbqt_text":
        item = "pdbqt_text:" + payload
    else:
        item = str(path)
    return item, tree


def _assert_literal_values(result, target, variant):
    is_sdf = variant in SDF_VARIANTS
    if target in DOCKING_FORMS:
        result = msm.convert(
            result,
            to_form="molsysmt.MolSys",
            **({} if is_sdf else {"discard_torsion_tree": True}),
        )
        target = "molsysmt.MolSys"
    topology = result.topology if target == "molsysmt.MolSys" else result
    if target in {"molsysmt.Topology", "molsysmt.MolSys"}:
        assert topology.n_atoms == (5 if is_sdf else 4)
        assert topology.atoms.atom_type.tolist() == (
            ["C", "O", "O", "Na", "H"] if is_sdf else ["C", "C", "O", "H"]
        )
        if is_sdf:
            assert msm.get(topology, formal_charge=True) == [0, 0, -1, 1, 0]
            assert topology.atoms.isotope.iloc[0] == 13
            assert topology.atoms.isotope.iloc[4] == 2
            np.testing.assert_array_equal(
                msm.get(topology, element="bond", bonded_atom_pairs=True),
                [[0, 1], [0, 2], [0, 4]],
            )
            np.testing.assert_array_equal(
                msm.get(topology, element="bond", bond_order=True), [2, 1, 1]
            )
            if variant == "valence":
                assert msm.get(topology, selection=[3], n_explicit_hydrogens=True) == [
                    0
                ]
                assert msm.get(
                    topology, selection=[3], allows_implicit_hydrogens=True
                ) == [False]
        else:
            assert topology.atoms.atom_id.tolist() == ["17", "3", "45", "90"]
            assert topology.n_bonds == (1 if variant == "ligand" else 0)
            assert msm.get(topology, formal_charge=True) is None
            assert not msm.has_attribute(topology, "formal_charge")
    if target in {"molsysmt.Structures", "molsysmt.MolSys"}:
        structures = result.structures if target == "molsysmt.MolSys" else result
        expected = (
            [[0, 0, 0], [0.12, 0, 0], [-0.12, 0, 0], [0.4, 0, 0], [0, 0.1, 0]]
            if is_sdf
            else [[0.1, 0.2, 0.3], [0.2, 0.3, 0.4], [0.3, 0.4, 0.5], [0.4, 0.5, 0.6]]
        )
        actual = msm.pyunitwizard.get_value(structures.coordinates, to_unit="nm")
        assert actual.shape == (1, len(expected), 3)
        np.testing.assert_allclose(actual[0], expected, atol=1e-7, rtol=0)
    if not is_sdf and target in {"molsysmt.MolecularMechanics", "molsysmt.MolSys"}:
        mechanics = (
            result.molecular_mechanics if target == "molsysmt.MolSys" else result
        )
        assert mechanics.atom_ff_type.tolist() == ["C", "A", "OA", "HD"]
        np.testing.assert_allclose(
            mechanics.partial_charge.astype(float), [0.125, -0.1, -0.25, 0.225]
        )


@pytest.mark.parametrize(
    "source,target,variant", CASES, ids=[f"{s}->{t}:{v}" for s, t, v in CASES]
)
def test_declared_docking_edge_executes_directly_and_publicly(
    source, target, variant, tmp_path
):
    for route in ("direct", "public"):
        item, tree = _source(source, variant, tmp_path / route)
        result = None
        try:
            assert msm.get_form(item) == source
            kwargs = {}
            if target.startswith("file:"):
                extension = target.split(":")[1]
                kwargs["output_filename"] = str(
                    tmp_path / f"{route}-result.{extension}"
                )
            if source == "molsysmt.MolSys":
                if target == "file:sdf":
                    kwargs["ctfile_version"] = (
                        "V3000" if variant in {"V3000", "valence"} else "V2000"
                    )
                else:
                    kwargs.update(typing_scheme="autodock4", torsion_tree=tree)
            elif target == "molsysmt.MolSys" and variant == "ligand":
                kwargs["discard_torsion_tree"] = True
            result = (
                _execute_direct(source, target, item, **kwargs)
                if route == "direct"
                else msm.convert(item, to_form=target, **kwargs)
            )
            assert msm.get_form(result) == target
            if target.startswith("file:"):
                assert Path(result).is_file()
                assert Path(result).stat().st_size > 0
                if source != "molsysmt.MolSys":
                    payload = PAYLOADS[variant]
                    assert Path(result).read_bytes() == payload.encode()
            _assert_literal_values(result, target, variant)
        finally:
            if (
                target == "molsysmt.PDBQTFileHandler"
                and result is not None
                and result is not item
            ):
                result.close()
            if source == "molsysmt.PDBQTFileHandler":
                item.close()


def test_docking_routes_do_not_attempt_optional_engine_imports():
    script = r"""
import importlib.abc
import importlib.machinery
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from tests.conversion_truth.test_declared_docking_edges import (
    CASES, test_declared_docking_edge_executes_directly_and_publicly,
)

engines = {"rdkit", "MDAnalysis", "mdtraj", "openmm", "vina"}
assert not engines.intersection(name.split(".")[0] for name in sys.modules)
attempted = []
class BlockLoader(importlib.abc.Loader):
    def create_module(self, spec):
        attempted.append(spec.name)
        raise ImportError("optional engine deliberately blocked: " + spec.name)
    def exec_module(self, module):
        raise AssertionError("blocked loader must never execute")
class BlockEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in engines:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            if spec is not None:
                spec.loader = BlockLoader()
            return spec
sys.meta_path.insert(0, BlockEngines())

for source, target, variant in CASES:
    with TemporaryDirectory() as directory:
        test_declared_docking_edge_executes_directly_and_publicly(
            source, target, variant, Path(directory),
        )
assert not attempted, attempted
assert not engines.intersection(name.split(".")[0] for name in sys.modules)
print(len(CASES))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == str(len(CASES))
