"""Checking declared index lineage independently of atom matching or coordinates."""

import copy
import json
import pickle

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
from tests.form.file_pdbqt.test_known_source_poses import ensemble, rigid_tree


def mapping(n_source, inverse, **kwargs):
    forward = np.full(n_source, -1, dtype=np.int64)
    inverse = np.asarray(inverse, dtype=np.int64)
    present = inverse >= 0
    forward[inverse[present]] = np.flatnonzero(present)
    return dict(
        schema="molsysmt.atom_map@1",
        n_source_atoms=n_source,
        n_output_atoms=len(inverse),
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=inverse,
        **kwargs,
    )


def test_generation_reordering_omission_and_no_negative_index_lookup():
    first = mapping(3, [2, 0, -1, 1])
    second = mapping(4, [2, 1, 0])
    snapshot = pickle.dumps([first, second])
    result = msm.basic.compose_atom_maps([first, second])
    np.testing.assert_array_equal(result["output_to_source_atom_indices"], [-1, 0, 2])
    np.testing.assert_array_equal(result["source_to_output_atom_indices"], [1, -1, 2])
    np.testing.assert_array_equal(result["generated_output_atom_indices"], [0])
    assert result["source_atom_status"].tolist() == ["retained", "omitted", "retained"]
    assert pickle.dumps([first, second]) == snapshot
    result["stages"][0]["source_to_output_atom_indices"][0] = 99
    assert first["source_to_output_atom_indices"][0] == 1


@pytest.mark.parametrize("omit_parent", [False, True])
def test_typed_hydrogen_projection_export_and_pose_axes(omit_parent):
    source = declared_methanol()
    projected = msm.build.merge_nonpolar_hydrogens(
        source, typing_scheme="autodock4", return_report=True
    )
    reduced = projected["molecular_system"]
    selection = [1, 2] if omit_parent else [0, 1, 2]
    chosen = reduced.extract(atom_indices=selection, structure_indices=[0])
    text, exported = msm.convert(
        reduced,
        to_form="string:pdbqt_text",
        selection=selection,
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(chosen, np.arange(len(selection))[::-1]),
        return_atom_map=True,
    )
    read = msm.form.string_pdbqt_text.read_poses(
        ensemble(text),
        reduced,
        exported,
        missing_atoms="omit" if omit_parent else "error",
        return_report=True,
    )
    reports = [projected["report"], exported, read["report"]]
    result = msm.basic.compose_atom_maps(reports)
    if omit_parent:
        assert result["output_to_source_atom_indices"].tolist() == [1, 5]
        assert result["source_to_output_atom_indices"].tolist() == [
            -1,
            0,
            -1,
            -1,
            -1,
            1,
        ]
        assert result["source_to_representative_atom_indices"].tolist() == [
            -1,
            0,
            -1,
            -1,
            -1,
            1,
        ]
        assert result["source_atom_status"].tolist() == [
            "omitted",
            "retained",
            "omitted",
            "omitted",
            "omitted",
            "retained",
        ]
    else:
        assert result["output_to_source_atom_indices"].tolist() == [0, 1, 5]
        assert result["source_to_output_atom_indices"].tolist() == [0, 1, -1, -1, -1, 2]
        assert result["source_to_representative_atom_indices"].tolist() == [
            0,
            1,
            0,
            0,
            0,
            2,
        ]
        assert result["source_atom_status"].tolist() == [
            "retained",
            "retained",
            "merged",
            "merged",
            "merged",
            "retained",
        ]
    np.testing.assert_allclose(result["stages"][0]["charge_transfers"], [0.1, 0.2, 0.3])
    assert result["stages"][0]["charge_unit"] == "elementary_charge"
    assert result["stages"][0]["software"] == projected["report"]["software"]
    assert result["stages"][2]["input_axis"] == "pdbqt_written_atoms"
    assert result["stages"][2]["n_source_atoms"] == len(selection)
    assert (
        result["stages"][0]["selected_total_charge"]
        == projected["report"]["selected_total_charge"]
    )
    assert (
        result["stages"][1]["first_root_source_atom_index"]
        == exported["first_root_source_atom_index"]
    )
    np.testing.assert_array_equal(
        result["stages"][1]["ordered_root_source_atom_indices"],
        exported["ordered_root_source_atom_indices"],
    )
    np.testing.assert_array_equal(
        result["stages"][1]["torsion_tree"]["atom_ids"],
        exported["torsion_tree"]["atom_ids"],
    )
    assert (
        result["stages"][1]["charge_rounding_error_bound"]
        == exported["charge_rounding_error_bound"]
    )
    assert result["generated_output_atom_indices"].size == 0
    assert result["output_atom_ids"].tolist() == (
        ["3", "11"] if omit_parent else ["17", "3", "11"]
    )
    # Incremental composition preserves exactly the same flattened stage lineage.
    partial = msm.basic.compose_atom_maps(reports[:2])
    restored = msm.basic.compose_atom_maps(
        [json.loads(json.dumps(partial, default=lambda v: v.tolist())), reports[2]]
    )
    assert len(restored["stages"]) == 3
    for field in (
        "source_to_output_atom_indices",
        "source_to_representative_atom_indices",
        "output_to_source_atom_indices",
    ):
        np.testing.assert_array_equal(restored[field], result[field])


def test_real_fixed_state_hydrogens_keep_absent_original_indices():
    pytest.importorskip("rdkit.Chem")
    from tests.build.add_missing_hydrogens.test_fixed_state import hydrogenate, prepared

    source = prepared("CO", [[0, 0, 0], [1.4, 0, 0]])
    source.topology.atoms["atom_id"] = ["17", "3"]
    added = hydrogenate(source)
    typed = msm.build.assign_autodock_atom_types(
        added["molecular_system"], typing_scheme="autodock4"
    )
    typed = msm.build.assign_partial_charges(typed, method="gasteiger_marsili")
    projected = msm.build.merge_nonpolar_hydrogens(
        typed, typing_scheme="autodock4", return_report=True
    )
    reduced = projected["molecular_system"]
    text, exported = msm.convert(
        reduced,
        to_form="string:pdbqt_text",
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(reduced, [1, 0, 2]),
        return_atom_map=True,
    )
    poses = msm.form.string_pdbqt_text.read_poses(
        ensemble(text), reduced, exported, return_report=True
    )
    reports = [added["report"], projected["report"], exported, poses["report"]]
    result = msm.basic.compose_atom_maps(reports)
    assert result["n_source_atoms"] == 2 and result["n_output_atoms"] == 3
    assert result["source_to_output_atom_indices"].tolist() == [0, 1]
    assert result["output_to_source_atom_indices"].tolist() == [0, 1, -1]
    assert result["generated_output_atom_indices"].tolist() == [2]
    assert result["stages"][0]["parent_atom_pairs"].tolist() == [
        [0, 2],
        [0, 3],
        [0, 4],
        [1, 5],
    ]
    assert result["stages"][0]["origin_schema"] == "molsysmt.hydrogen_addition@1"
    assert result["stages"][0]["software"]["rdkit"]
    assert result["stages"][0]["attribution"] == added["report"]["attribution"]
    assert result["stages"][1]["merged_source_atom_pairs"].tolist() == [
        [2, 0],
        [3, 0],
        [4, 0],
    ]


def test_native_terminal_creation_and_empty_addition_reports():
    from tests.build.add_terminal_atoms.test_add_terminal_atoms import system

    source = system()
    result = msm.build.add_terminal_atoms(
        source,
        [{"parent_atom_index": 1, "atom_type": "H", "atom_id": "40"}],
        msm.pyunitwizard.quantity([[[0.14, 0, 0.1]], [[0.14, 0, 1.1]]], "nm"),
    )
    mapped = msm.basic.compose_atom_maps([result["report"]])
    assert mapped["output_to_source_atom_indices"].tolist() == [0, 1, -1]
    assert mapped["stages"][0]["generated_atom_ids"] == ["40"]
    empty = msm.build.add_terminal_atoms(
        source, [], msm.pyunitwizard.quantity(np.empty((2, 0, 3)), "nm")
    )
    restored = msm.basic.compose_atom_maps([empty["report"]])
    assert restored["output_to_source_atom_indices"].tolist() == [0, 1]


@pytest.mark.parametrize("maps", [[], {}, [None], "maps"])
def test_reject_invalid_report_sequence(maps):
    with pytest.raises(ArgumentError):
        msm.basic.compose_atom_maps(maps)


@pytest.mark.parametrize(
    "field,value",
    [
        ("schema", "unknown@1"),
        ("n_source_atoms", True),
        ("n_output_atoms", 2.5),
        ("source_to_output_atom_indices", [0.0, 1.0]),
        ("source_to_output_atom_indices", [True, False]),
        ("source_to_output_atom_indices", [0, -2]),
        ("source_to_output_atom_indices", [0, 0]),
        ("output_to_source_atom_indices", [0, 3]),
        ("source_to_representative_atom_indices", [1, 0]),
        ("source_atom_status", ["omitted", "retained"]),
        ("source_atom_ids", [0, 1]),
        ("merged_source_atom_pairs", [[0]]),
        ("source_to_output_atom_indices", [[0], [1, 2]]),
    ],
)
def test_reject_inconsistent_typed_maps(field, value):
    report = mapping(2, [0, 1])
    report[field] = value
    with pytest.raises(StructuralInconsistencyError):
        msm.basic.compose_atom_maps([report])


def test_adjacent_counts_labels_and_pose_export_binding_are_checked():
    with pytest.raises(StructuralInconsistencyError, match="counts"):
        msm.basic.compose_atom_maps([mapping(2, [1]), mapping(2, [0, 1])])
    with pytest.raises(StructuralInconsistencyError, match="ids"):
        msm.basic.compose_atom_maps(
            [
                mapping(2, [1, 0], output_atom_ids=["b", "a"]),
                mapping(2, [0, 1], source_atom_ids=["a", "b"]),
            ]
        )
    with pytest.raises(StructuralInconsistencyError, match="binding"):
        msm.basic.compose_atom_maps(
            [
                mapping(2, [1, 0], output_payload_sha256="one"),
                mapping(2, [0, 1], input_export_sha256="two"),
            ]
        )


def test_merge_representatives_do_not_create_direct_coordinates_and_remain_typed():
    merged = mapping(3, [0, 2])
    merged.update(
        source_to_representative_atom_indices=[0, 0, 1],
        merged_source_atom_pairs=[[1, 0]],
        charge_transfers=[0.25],
        charge_unit="elementary_charge",
    )
    result = msm.basic.compose_atom_maps([merged, mapping(2, [1, 0])])
    assert result["source_to_output_atom_indices"].tolist() == [1, -1, 0]
    assert result["source_to_representative_atom_indices"].tolist() == [1, 1, 0]
    assert result["output_to_source_atom_indices"].tolist() == [2, 0]
    for field, value in (
        ("charge_unit", "coulomb"),
        ("charge_transfers", [float("nan")]),
        ("merged_source_atom_pairs", [[1, -1]]),
    ):
        bad = copy.deepcopy(merged)
        bad[field] = value
        with pytest.raises(StructuralInconsistencyError):
            msm.basic.compose_atom_maps([bad])


def test_tampered_incremental_history_is_not_silently_accepted():
    result = msm.basic.compose_atom_maps([mapping(3, [1, 0]), mapping(2, [1])])
    result["source_to_output_atom_indices"][0] = -1
    result["output_to_source_atom_indices"][:] = -1
    result["source_to_representative_atom_indices"][:] = -1
    result["source_atom_status"][:] = "omitted"
    with pytest.raises(StructuralInconsistencyError, match="stored stages"):
        msm.basic.compose_atom_maps([result])


def test_empty_axes_have_explicit_shapes_and_linear_numpy_storage():
    result = msm.basic.compose_atom_maps([mapping(0, []), mapping(0, [])])
    assert result["source_to_output_atom_indices"].shape == (0,)
    assert result["output_to_source_atom_indices"].dtype == np.int64
    n = 100_000
    result = msm.basic.compose_atom_maps(
        [mapping(n, np.arange(n)[::-1]), mapping(n, np.arange(n)[::2])]
    )
    assert result["n_output_atoms"] == n // 2
    assert result["source_atom_status"].dtype.kind == "U"
    for stage in result["stages"]:
        for field in (
            "source_to_output_atom_indices",
            "output_to_source_atom_indices",
            "source_to_representative_atom_indices",
        ):
            assert stage[field].ndim == 1 and stage[field].dtype == np.int64
    assert result["source_to_output_atom_indices"].nbytes == n * 8


def test_repeated_merges_follow_representatives_without_resurrecting_positions():
    first = mapping(3, [0, 2], source_to_representative_atom_indices=[0, 0, 1])
    second = mapping(2, [1], source_to_representative_atom_indices=[0, 0])
    with msm.pyunitwizard.context(standard_units=["pm", "coulomb"]):
        result = msm.basic.compose_atom_maps([first, second])
    assert result["source_to_output_atom_indices"].tolist() == [-1, -1, 0]
    assert result["source_to_representative_atom_indices"].tolist() == [0, 0, 0]
    assert result["output_to_source_atom_indices"].tolist() == [2]
    assert result["source_atom_status"].tolist() == ["merged", "merged", "retained"]


def test_an_explicit_rename_requires_its_own_declared_axis_stage():
    before = mapping(2, [0, 1], output_atom_names=["old-C", "old-O"])
    after = mapping(
        2, [1, 0], source_atom_names=["C1", "O1"], output_atom_names=["O1", "C1"]
    )
    with pytest.raises(StructuralInconsistencyError, match="names"):
        msm.basic.compose_atom_maps([before, after])
    rename = mapping(
        2,
        [0, 1],
        source_atom_names=["old-C", "old-O"],
        output_atom_names=["C1", "O1"],
        method="caller_declared_rename",
    )
    result = msm.basic.compose_atom_maps([before, rename, after])
    assert result["output_atom_names"].tolist() == ["O1", "C1"]
    assert result["source_to_output_atom_indices"].tolist() == [1, 0]


@pytest.mark.parametrize(
    "changes",
    [
        {"parent_atom_pairs": [[-1, 2]], "atom_correspondence": [[0, 0], [1, 1]]},
        {
            "parent_atom_pairs": [[0, 2], [1, 2]],
            "atom_correspondence": [[0, 0], [1, 1]],
        },
        {"parent_atom_pairs": [[0, 2]], "atom_correspondence": [[0, 0], [0, 1]]},
        {
            "parent_atom_pairs": [[0, 2]],
            "atom_correspondence": [[0, 0], [1, 1]],
            "generated_atom_ids": [12],
        },
    ],
)
def test_reject_inconsistent_creation_evidence(changes):
    report = dict(
        schema="molsysmt.terminal_attachment@1", source={"n_atoms": 2}, **changes
    )
    with pytest.raises(StructuralInconsistencyError):
        msm.basic.compose_atom_maps([report])


def test_user_guide_workflow_and_json_example_execute():
    import re
    from pathlib import Path

    page = (
        Path(__file__).parents[2] / "docs/content/user/tools/basic/compose_atom_maps.md"
    )
    scope = {}
    for code in re.findall(r"```python\n(.*?)```", page.read_text(), flags=re.S):
        exec(compile(code, str(page), "exec"), scope)
    assert scope["restored"]["output_to_source_atom_indices"].tolist() == [0, 1, -1]


def test_empty_original_source_can_have_declared_generated_outputs():
    result = msm.basic.compose_atom_maps([mapping(0, [-1]), mapping(1, [0])])
    assert result["n_source_atoms"] == 0 and result["n_output_atoms"] == 1
    assert result["output_to_source_atom_indices"].tolist() == [-1]
    assert result["generated_output_atom_indices"].tolist() == [0]


def test_ready_maps_load_no_optional_engine_or_ackredit():
    import subprocess
    import sys

    script = r"""
import importlib.abc
import importlib.machinery
import sys
import molsysmt as msm
roots = {'rdkit', 'meeko', 'openmm', 'MDAnalysis', 'mdtraj', 'vina', 'ackredit'}
assert not roots.intersection(name.split('.')[0] for name in sys.modules)
attempted = []
class DeniedLoader(importlib.abc.Loader):
    def create_module(self, spec):
        attempted.append(spec.name)
        raise ImportError('Unexpected optional load: ' + spec.name)
    def exec_module(self, module):
        raise AssertionError('Unexpected optional execution')
class DeniedEngines(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in roots:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            if spec is not None:
                spec.loader = DeniedLoader()
            return spec
sys.meta_path.insert(0, DeniedEngines())
from molsysmt.native import MolSys
source = MolSys(n_atoms=2)
msm.set(source, atom_name=['H1291', 'H0'])
renamed = msm.build.project_atom_names(source, target_form='file:pdbqt', return_report=True)
assert renamed['report']['output_atom_names'].tolist() == ['H1', 'H0']
assert source.topology.atoms.atom_name.tolist() == ['H1291', 'H0']
assert msm.basic.compose_atom_maps([renamed['report']])['source_to_output_atom_indices'].tolist() == [0, 1]
stage = dict(schema='molsysmt.atom_map@1', n_source_atoms=2, n_output_atoms=1,
    source_to_output_atom_indices=[0,-1], output_to_source_atom_indices=[0])
result = msm.basic.compose_atom_maps([stage])
assert result['source_to_output_atom_indices'].tolist() == [0,-1]
assert not attempted, attempted
assert not roots.intersection(name.split('.')[0] for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_oriented_tree_and_rigid_empty_metadata_survive_json():
    source = declared_methanol()
    tree = rigid_tree(source, [3, 0, 4, 2, 1, 5])
    tree.update(
        fragment_offsets=np.array([0, 4, 6]),
        branch_atom_pairs=np.array([[0, 1]]),
        branch_fragment_pairs=np.array([[0, 1]]),
        torsdof=1,
    )
    _, exported = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=tree,
        return_atom_map=True,
    )
    result = msm.basic.compose_atom_maps(
        [json.loads(json.dumps(exported, default=lambda v: v.tolist()))]
    )
    stage = result["stages"][0]
    assert stage["ordered_root_source_atom_indices"].tolist() == [3, 0, 4, 2]
    assert stage["first_root_source_atom_index"] == 3
    assert stage["branch_source_atom_pairs"].tolist() == [[0, 1]]
    assert stage["torsion_tree"]["branch_atom_pairs"].tolist() == [[1, 4]]
    bad = copy.deepcopy(exported)
    bad["branch_source_atom_pairs"] = [[1, 0]]
    with pytest.raises(StructuralInconsistencyError, match="Rooted export"):
        msm.basic.compose_atom_maps([bad])
    _, rigid = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        return_atom_map=True,
    )
    restored = msm.basic.compose_atom_maps(
        [json.loads(json.dumps(rigid, default=lambda v: v.tolist()))]
    )
    assert restored["stages"][0]["torsion_tree"] is None
    assert restored["stages"][0]["branch_source_atom_pairs"].shape == (0, 2)


def test_quantity_records_do_not_strip_additional_units_or_accept_negative_bounds():
    record = mapping(2, [0, 1])
    record["source_to_output_atom_indices"] = msm.pyunitwizard.quantity([0, 1], "nm")
    with pytest.raises(StructuralInconsistencyError, match="additional unit"):
        msm.basic.compose_atom_maps([record])
    for value in (msm.pyunitwizard.quantity(1.0, "coulomb"), True, float("nan")):
        record = mapping(
            2, [0, 1], selected_total_charge=value, charge_unit="elementary_charge"
        )
        with pytest.raises(StructuralInconsistencyError, match="finite scalar"):
            msm.basic.compose_atom_maps([record])
    record = mapping(
        2, [0, 1], charge_rounding_error_bound=-0.1, charge_unit="elementary_charge"
    )
    with pytest.raises(StructuralInconsistencyError, match="nonnegative"):
        msm.basic.compose_atom_maps([record])
