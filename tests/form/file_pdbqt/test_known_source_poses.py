"""Checking pose identity and coordinate truth independently of pose inference."""

import copy
import json

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol, unchanged


def rigid_tree(source, order):
    return {
        "schema_version": "molsysmt.pdbqt-torsion-tree@1",
        "atom_ids": source.topology.atoms.atom_id.to_numpy(),
        "fragment_atom_indices": np.asarray(order, dtype=np.int64),
        "fragment_offsets": np.asarray([0, len(order)], dtype=np.int64),
        "branch_atom_pairs": np.empty((0, 2), dtype=np.int64),
        "branch_fragment_pairs": np.empty((0, 2), dtype=np.int64),
        "root_fragment_index": 0,
        "torsdof": 0,
    }


def ensemble(text):
    """Place three independently specified displacements in literal fixed fields."""
    bodies = []
    for label, offset in ((9, 0), (2, 10), (51, -5)):
        lines = [f"MODEL {label}", f"REMARK VINA RESULT: {-label}.0 0.0 0.0"]
        for line in text.removeprefix("pdbqt_text:").splitlines():
            if line.startswith(("ATOM  ", "HETATM")):
                xyz = [float(line[start : start + 8]) for start in (30, 38, 46)]
                line = (
                    line[:30]
                    + "".join(f"{value + offset:8.3f}" for value in xyz)
                    + line[54:]
                )
            lines.append(line)
        bodies.append("\n".join([*lines, "ENDMDL"]))
    return "pdbqt_text:" + "\n".join(bodies) + "\n"


@pytest.fixture
def pose_case():
    source = declared_methanol()
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(source, [1, 0, 5, 4, 3, 2]),
        return_atom_map=True,
    )
    return source, text, mapping


@pytest.mark.parametrize("as_file", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_public_pose_read_preserves_known_graph_and_true_coordinates(
    pose_case, tmp_path, as_file, unit
):
    source, text, mapping = pose_case
    before = source.copy()
    item = ensemble(text)
    if as_file:
        item = tmp_path / "poses.pdbqt"
        item.write_text(ensemble(text).removeprefix("pdbqt_text:"))
    old = list(msm.pyunitwizard.configure.get_standard_units())
    try:
        msm.pyunitwizard.configure.set_standard_units(
            [unit, "ps", "Da", "K", "mole", "e"]
        )
        result = msm.form.read_pdbqt_poses(item, source, mapping, return_report=True)
    finally:
        msm.pyunitwizard.configure.set_standard_units(old)
    out, report = result["molecular_system"], result["report"]
    assert out.get_n_atoms() == 6 and out.structures.n_structures == 3
    assert out.structures.structure_id.tolist() == ["9", "2", "51"]
    xyz = msm.pyunitwizard.get_value(out.structures.coordinates, to_unit="nm")
    expected = np.arange(18).reshape(6, 3) / 10
    np.testing.assert_allclose(
        xyz, expected[None] + np.array([0, 1, -0.5])[:, None, None]
    )
    pd.testing.assert_frame_equal(
        out.topology.atoms, source.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        out.chemical_states._states[0].bonds,
        source.chemical_states._states[0].bonds,
        check_frame_type=False,
    )
    assert out.chemical_states._states[0].connectivity_completeness == "complete"
    assert out.structures.box is None and out.structures.time is None
    assert out.molecular_mechanics.partial_charge is None
    assert not out.interactions
    assert report["schema"] == "molsysmt.pdbqt_pose_read@1"
    np.testing.assert_array_equal(
        report["pdbqt_to_output_atom_indices"], [1, 0, 5, 4, 3, 2]
    )
    np.testing.assert_array_equal(report["output_to_source_atom_indices"], np.arange(6))
    assert report["source_coordinates_reused"] is False
    assert "VINA RESULT" in report["remarks"][0][0]
    np.testing.assert_allclose(
        report["partial_charge"], [-0.4, -0.5, 0.1, 0.2, 0.3, 0.3]
    )
    unchanged(source, before)
    report["export_map"]["output_to_source_atom_indices"][0] = 99
    assert mapping["output_to_source_atom_indices"][0] == 1


def test_nonconsecutive_pose_indices_order_repeats_empty_and_unwrapped(pose_case):
    source, text, mapping = pose_case
    result = msm.form.read_pdbqt_poses(
        ensemble(text), source, mapping, structure_indices=[2, 0, 2], return_report=True
    )
    np.testing.assert_array_equal(
        result["report"]["input_structure_indices"], [2, 0, 2]
    )
    assert result["molecular_system"].structures.structure_id.tolist() == [
        "51",
        "9",
        "51",
    ]
    empty = msm.form.read_pdbqt_poses(
        ensemble(text), source, mapping, structure_indices=[]
    )
    assert empty.structures.coordinates.shape == (0, 6, 3)
    single = msm.form.read_pdbqt_poses(text, source, mapping, return_report=True)
    assert single["report"]["model_ids"].tolist() == [None]
    assert single["molecular_system"].structures.n_structures == 1


@pytest.mark.parametrize("indices", [[-1], [3], [True], [1.2], [[0]], "9"])
def test_pose_structure_selection_rejects_labels_and_invalid_indices(
    pose_case, indices
):
    source, text, mapping = pose_case
    with pytest.raises(ArgumentError):
        msm.form.read_pdbqt_poses(
            ensemble(text), source, mapping, structure_indices=indices
        )


def test_missing_source_hydrogens_require_explicit_subsystem(pose_case):
    source, _, _ = pose_case
    selected = source.extract(atom_indices=[0, 1, 5], structure_indices=[0])
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        selection=[0, 1, 5],
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(selected, [1, 0, 2]),
        return_atom_map=True,
    )
    with pytest.raises(FormatError, match="omitted source atoms"):
        msm.form.read_pdbqt_poses(ensemble(text), source, mapping)
    result = msm.form.read_pdbqt_poses(
        ensemble(text), source, mapping, missing_atoms="omit", return_report=True
    )
    output, report = result["molecular_system"], result["report"]
    assert output.structures.coordinates.shape == (3, 3, 3)
    np.testing.assert_array_equal(report["omitted_source_atom_indices"], [2, 3, 4])
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"], [0, 1, -1, -1, -1, 2]
    )
    assert output.topology.atoms.atom_id.tolist() == ["17", "3", "11"]
    np.testing.assert_array_equal(
        output.chemical_states._states[0].atom_attributes.n_explicit_hydrogens,
        [0, 0, 0],
    )
    # Original absent H positions do not enter the retained coordinate axis.
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm")[1],
        np.arange(18).reshape(6, 3)[[0, 1, 5]] / 10 + 1,
    )


def test_projected_known_source_and_json_map(pose_case):
    original, _, _ = pose_case
    source = msm.build.merge_nonpolar_hydrogens(original, typing_scheme="autodock4")
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(source, [1, 0, 2]),
        return_atom_map=True,
    )
    mapping = json.loads(json.dumps(mapping, default=lambda value: value.tolist()))
    result = msm.form.read_pdbqt_poses(
        ensemble(text), source.topology, mapping, return_report=True
    )
    assert result["molecular_system"].get_n_atoms() == 3
    assert result["report"]["omitted_source_atom_indices"].size == 0
    assert result["molecular_system"].chemical_states._states[
        0
    ].atom_attributes.n_explicit_hydrogens.tolist() == [3, 0, 0]


@pytest.mark.parametrize(
    "mutation",
    [
        lambda s: s.replace("ENDMDL", "", 1),
        lambda s: s.replace("MODEL 2", "MODEL 9", 1),
        lambda s: s.replace("MODEL 2", "MODEL -2", 1),
        lambda s: s.replace("ENDMDL", "ENDMDL extra", 1),
        lambda s: s.replace("MODEL 9", "ENDMDL\nMODEL 9", 1),
        lambda s: s + "ATOM\n",
        lambda s: s.replace("ENDMDL", "", 3),
        lambda s: s.replace("TORSDOF 0", "TORSDOF 1", 1),
        lambda s: s.replace(" OA", " NA", 1),
        lambda s: s.replace("   0.000", "     nan", 1),
    ],
)
def test_rejects_bad_models_and_unselected_corruption(pose_case, mutation):
    source, text, mapping = pose_case
    with pytest.raises(FormatError):
        msm.form.read_pdbqt_poses(
            mutation(ensemble(text)), source, mapping, structure_indices=[]
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("schema", "molsysmt.atom_projection@1"),
        ("output_to_source_atom_indices", [1, 1, 5, 4, 3, 2]),
        ("output_to_source_atom_indices", [1.0, 0.0, 5.0, 4.0, 3.0, 2.0]),
        ("source_to_output_atom_indices", [0, 1, 2, 3, 4, 5]),
        ("output_atom_ids", ["3", "17", "11", "7", "90", "999"]),
        ("charge_unit", "coulomb"),
        ("written_partial_charge", [0] * 6),
        ("source_chemical_digest", "unknown"),
        ("torsion_tree", None),
    ],
)
def test_rejects_inconsistent_export_map(pose_case, field, value):
    source, text, mapping = pose_case
    mapping = copy.deepcopy(mapping)
    mapping[field] = value
    with pytest.raises(FormatError):
        msm.form.read_pdbqt_poses(text, source, mapping)


def test_rejects_stale_source_chemistry_and_keeps_old_parser_profile(pose_case):
    source, text, mapping = pose_case
    source.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 1
    with pytest.raises(FormatError, match="chemical-state binding"):
        msm.form.read_pdbqt_poses(text, source, mapping)
    with pytest.raises(FormatError, match="MODEL"):
        msm.convert(
            ensemble(text), to_form="molsysmt.MolSys", discard_torsion_tree=True
        )


def test_branched_pose_tree_preserves_covalent_graph(pose_case):
    source, _, _ = pose_case
    tree = rigid_tree(source, [3, 0, 4, 2, 1, 5])
    tree.update(
        fragment_offsets=np.array([0, 4, 6]),
        branch_atom_pairs=np.array([[0, 1]]),
        branch_fragment_pairs=np.array([[0, 1]]),
        torsdof=1,
    )
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=tree,
        return_atom_map=True,
    )
    result = msm.form.read_pdbqt_poses(ensemble(text), source, mapping)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm")[2],
        np.arange(18).reshape(6, 3) / 10 - 0.5,
    )
    assert result.topology.n_bonds == 5
    with pytest.raises(FormatError, match="torsion tree"):
        msm.form.read_pdbqt_poses(
            ensemble(text).replace("TORSDOF 1", "TORSDOF 0", 1), source, mapping
        )


def test_does_not_read_native_source_geometry(pose_case, monkeypatch):
    source, text, mapping = pose_case
    from molsysmt.native._structure_array import _StructureArray

    original = _StructureArray._dense
    source_series = source.structures._coordinates

    def protect_source(self):
        if self is source_series:
            raise AssertionError(
                "Source trajectory must not be materialized for new poses"
            )
        return original(self)

    monkeypatch.setattr(_StructureArray, "_dense", protect_source)
    result = msm.form.read_pdbqt_poses(ensemble(text), source, mapping)
    assert result.structures.coordinates.shape == (3, 6, 3)


def test_user_guide_examples_execute():
    import re
    from pathlib import Path

    guide = (
        Path(__file__).parents[3] / "docs/content/user/tools/form/read_pdbqt_poses.md"
    )
    namespace = {}
    for block in re.findall(r"```python\n(.*?)```", guide.read_text(), flags=re.S):
        exec(compile(block, str(guide), "exec"), namespace)
    assert namespace["report"]["model_ids"].tolist() == ["51", "9", "51"]


def test_new_pose_system_roundtrips_h5msm_05(pose_case, tmp_path):
    source, text, mapping = pose_case
    result = msm.form.read_pdbqt_poses(ensemble(text), source, mapping)
    path = tmp_path / "poses.h5msm"
    msm.convert(result, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    np.testing.assert_array_equal(
        loaded.topology.atoms.atom_id, source.topology.atoms.atom_id
    )
    np.testing.assert_array_equal(loaded.structures.structure_id, ["9", "2", "51"])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
    )
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].bonds,
        result.chemical_states._states[0].bonds,
        check_frame_type=False,
    )


def test_ready_native_pose_read_loads_no_optional_chemical_engine():
    import subprocess
    import sys

    script = r"""
import importlib.abc
import importlib.machinery
import sys
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
from tests.form.file_pdbqt.test_known_source_poses import rigid_tree, ensemble
import molsysmt as msm
roots = {"rdkit", "meeko", "openmm", "MDAnalysis", "mdtraj", "vina"}
assert not roots.intersection(name.split(".")[0] for name in sys.modules)
attempted = []
class DeniedLoader(importlib.abc.Loader):
    def create_module(self, spec):
        attempted.append(spec.name)
        raise ImportError("unexpected optional engine: " + spec.name)
    def exec_module(self, module):
        raise AssertionError("unexpected engine execution")
class DeniedEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in roots:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            if spec is not None:
                spec.loader = DeniedLoader()
            return spec
sys.meta_path.insert(0, DeniedEngines())
source = declared_methanol()
text, mapping = msm.convert(source, to_form="string:pdbqt_text", structure_indices=[0],
    typing_scheme="autodock4", torsion_tree=rigid_tree(source, [1,0,5,4,3,2]), return_atom_map=True)
result = msm.form.read_pdbqt_poses(ensemble(text), source, mapping, return_report=True)
assert result["molecular_system"].structures.coordinates.shape == (3,6,3)
assert not attempted, attempted
assert not roots.intersection(name.split(".")[0] for name in sys.modules)
"""
    completed = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_real_vina_output_matches_engine_coordinate_axis(vina_reference_corpus):
    """Exercise real engine syntax/rounding; this is not docking accuracy evidence."""
    Chem = pytest.importorskip("rdkit.Chem")
    Vina = pytest.importorskip("vina").Vina
    root, records = vina_reference_corpus
    molecule = Chem.SDMolSupplier(
        str(root / records["1iep"]["files"]["sdf"]["filename"]), removeHs=False
    )[0]
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    source.topology.atoms["atom_id"] = [
        str(index + 1) for index in range(source.get_n_atoms())
    ]
    source = msm.build.assign_autodock_atom_types(source, typing_scheme="autodock4")
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    source = msm.build.merge_nonpolar_hydrogens(source, typing_scheme="autodock4")
    n = source.get_n_atoms()
    text, mapping = msm.convert(
        source,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(source, np.arange(n)[::-1]),
        return_atom_map=True,
    )
    engine = Vina(sf_name="vina", cpu=1, seed=14, verbosity=0)
    engine.set_receptor(
        str(root / records["1iep-receptor"]["files"]["pdbqt"]["filename"])
    )
    engine.set_ligand_from_string(text.removeprefix("pdbqt_text:"))
    center = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="angstrom"
    )[0].mean(axis=0)
    engine.compute_vina_maps(center=center.tolist(), box_size=[18.0, 18.0, 18.0])
    engine.dock(exhaustiveness=1, n_poses=2, min_rmsd=0.1, max_evals=100)
    payload = engine.poses(n_poses=2)
    engine_xyz = engine.poses(n_poses=2, coordinates_only=True)
    assert len(engine_xyz) >= 1
    result = msm.form.read_pdbqt_poses(
        "pdbqt_text:" + payload, source, mapping, return_report=True
    )
    output = result["molecular_system"]
    actual = msm.pyunitwizard.get_value(
        output.structures.coordinates, to_unit="angstrom"
    )
    np.testing.assert_allclose(
        actual[:, mapping["output_to_source_atom_indices"]],
        engine_xyz,
        atol=0.00051,
        rtol=0,
    )
    assert result["report"]["n_input_structures"] == len(engine_xyz)
    assert output.topology.n_bonds == source.topology.n_bonds
    assert output.get_n_atoms() == 40
