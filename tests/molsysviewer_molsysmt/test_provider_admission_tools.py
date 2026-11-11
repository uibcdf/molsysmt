"""Receive native provider additions without adopting or editing their outputs."""

import doctest
import inspect
from copy import deepcopy
from pathlib import Path

import h5py
import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import MolecularMechanics
from tests.chemical_states.test_normalize_indexed_hydrogen_policy import water
from tests.molsysviewer_molsysmt.test_axis_angle_rotation_tools import (
    snapshot,
    unchanged,
)
from tests.molsysviewer_molsysmt.test_chemical_assignment_readers_tools import same

puw = msm.pyunitwizard
PATHS = {
    "structure.get_pairwise_rmsd": True,
    "structure.get_distance_clusters": False,
    "chemical_states.normalize_indexed_hydrogen_policy": True,
    "h5msm.read_axis_sizes": False,
    "h5msm.write": True,
    "h5msm.write_layers": False,
}


def resolve(root, path):
    for name in path.split("."):
        root = getattr(root, name)
    return root


@pytest.mark.parametrize("path", PATHS)
def test_native_examples_in_bound_help(path):
    with msv.new_view() as owner:
        method = resolve(owner.addons.molsysmt, path)
        test = doctest.DocTestParser().get_doctest(
            inspect.getdoc(method), {}, path, path, 0
        )
        assert test.examples
        assert doctest.DocTestRunner().run(test).failed == 0


def test_documented_population_recipe():
    root = Path(__file__).resolve().parents[2]
    content = (root / "docs/content/user/tools/molsysviewer_tools.md").read_text()
    section = content.split("## Comparing an ordered structure population\n", 1)[1]
    code = section.split("```python\n", 1)[1].split("```", 1)[0]
    exec(compile(code, "<documented population recipe>", "exec"), {})


@pytest.fixture
def view():
    source = water()
    # Two translated arbitrary structures test geometry, not water conformation.
    xyz = np.zeros((2, 3, 3))
    xyz[1, :, 0] = 1
    source.structures.coordinates = puw.quantity(xyz, "nm")
    source.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="fixture",
        )
    }
    with msv.new_view(source) as result:
        yield result


def matrix():
    return puw.quantity([[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]], "nm")


@pytest.mark.parametrize("indices", [[], [1]])
def test_typed_empty_and_singleton_members_are_not_replaced_by_visible_structure(
    view, indices
):
    before = snapshot(view)
    result = view.addons.molsysmt.structure.get_pairwise_rmsd(
        selection="all", structure_indices=indices
    )
    assert result["rmsd"].shape == (len(indices), len(indices))
    assert result["pair_indices"].shape == (0, 2)
    assert result["pair_indices"].dtype == np.int64
    assert result["structure_indices"].tolist() == indices
    clusters = view.addons.molsysmt.structure.get_distance_clusters(
        result["rmsd"], "0 nm"
    )
    assert clusters["cluster_offsets"].tolist() == ([0] if not indices else [0, 1])
    unchanged(view, before)


def test_pairwise_numeric_budget_refusal_does_not_change_owner(view, monkeypatch):
    before = snapshot(view)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2)
    with pytest.raises(MemoryBudgetExceededError):
        view.addons.molsysmt.structure.get_pairwise_rmsd(selection="all")
    unchanged(view, before)


@pytest.mark.parametrize(
    "path",
    [*PATHS, "build.add_missing_heavy_atoms", "build.add_missing_terminal_cappings"],
)
def test_exact_native_signature_digestion_help_and_namespace(path):
    with msv.new_view() as owner:
        method = resolve(owner.addons.molsysmt, path)
        native = inspect.signature(resolve(msm, path))
        if PATHS.get(path, True):
            native = native.replace(parameters=list(native.parameters.values())[1:])
        assert inspect.signature(method) == native
        assert method.digestion_plan is not None
        assert "View integration" in inspect.getdoc(method)
        assert "update_view" not in native.parameters
        assert not hasattr(owner.addons.molsysmt, path.split(".")[-1])


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm", "angstrom"])
def test_pairwise_analytical_translation_axes_members_and_native_parity(
    view, skip, unit
):
    args = dict(
        selection=[2, 0],
        structure_indices=[1, 0, 1],
        member_keys=["b", "a", "b-again"],
        skip_digestion=skip,
    )
    before = snapshot(view)
    source_xyz = puw.get_value(view.molsys.structures.coordinates).copy()
    with puw.context(standard_units=[unit, "ps"]):
        policy = deepcopy(puw.configure.report())
        result = view.addons.molsysmt.structure.get_pairwise_rmsd(**args)
        same(result, msm.structure.get_pairwise_rmsd(view.molsys, **args))
        assert puw.get_unit(result["rmsd"]) == puw.unit(unit)
        assert puw.configure.report() == policy
    np.testing.assert_allclose(
        puw.get_value(result["rmsd"], to_unit="nm"), [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    )
    assert result["atom_indices"].tolist() == [0, 2]
    assert result["structure_indices"].tolist() == [1, 0, 1]
    assert result["member_keys"] == args["member_keys"]
    assert result["pair_indices"].tolist() == [[1, 0], [2, 0], [2, 1]]
    assert result["alignment"] == result["periodic_imaging"] == "none"
    puw.get_value(result["rmsd"])[0, 1] = 999
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.coordinates), source_xyz
    )
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "method,expected,representatives",
    [
        ("complete_linkage", [0, 0, 1], [0, 2]),
        ("single_linkage", [0, 0, 0], [1]),
    ],
)
def test_explicit_clustering_on_empty_owner_preserves_analytical_linkage(
    skip, method, expected, representatives
):
    distances = matrix()
    original = puw.get_value(distances).copy()
    args = dict(method=method, member_keys=["a", "b", "c"], skip_digestion=skip)
    with msv.new_view() as owner, puw.context(standard_units=["pm", "ps"]):
        before = snapshot(owner)
        cutoff = puw.quantity(1.0, "nm")
        result = owner.addons.molsysmt.structure.get_distance_clusters(
            distances, cutoff, **args
        )
        same(result, msm.structure.get_distance_clusters(distances, cutoff, **args))
        assert result["cluster_indices"].tolist() == expected
        assert result["representative_indices"].tolist() == representatives
        assert puw.get_unit(result["cluster_diameters"]) == puw.unit("pm")
        assert result["member_keys"] == ["a", "b", "c"]
        result["member_indices"][0] = 99
        np.testing.assert_array_equal(puw.get_value(distances), original)
        unchanged(owner, before)


@pytest.mark.parametrize("skip", [False, True])
def test_normalization_detaches_chemistry_report_and_invalidation(view, skip):
    before = snapshot(view)
    source = view.molsys
    original = source.copy()
    result = view.addons.molsysmt.chemical_states.normalize_indexed_hydrogen_policy(
        skip_digestion=skip
    )
    native = msm.chemical_states.normalize_indexed_hydrogen_policy(
        source, skip_digestion=skip
    )
    same(result["report"], native["report"])
    output, report = result["molecular_system"], result["report"]
    assert output is not source
    assert report["changed_atom_indices"].tolist() == [1]
    assert report["atom_correspondence"] == {"indices": "identity", "n_atoms": 3}
    assert report["invalidated_analysis_names"] == ["empty"]
    assert output.interactions["empty"].evaluated_structure_indices.tolist() == []
    assert source.interactions["empty"].evaluated_structure_indices.tolist() == [0, 1]
    assert msm.get(output, element="atom", allows_implicit_hydrogens=True) == [
        True,
        False,
        False,
    ]
    pd.testing.assert_frame_equal(
        output.chemical_states.get_bonds(), source.chemical_states.get_bonds()
    )
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    assert source.chemical_states.get_preparation_history() == ()
    report["changed_atom_indices"][0] = 99
    assert output.chemical_states.get_preparation_history()[0]["report"][
        "changed_atom_indices"
    ].tolist() == [1]
    output.structures.coordinates = puw.quantity(np.full((2, 3, 3), -99), "nm")
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates),
        puw.get_value(original.structures.coordinates),
    )
    assert msm.get(source, element="atom", allows_implicit_hydrogens=True) == [
        True,
        True,
        False,
    ]
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_explicit_h5msm_axes_and_mechanics_layer_on_empty_owner(tmp_path, skip):
    path = tmp_path / "mechanics.h5msm"
    mechanics = MolecularMechanics()
    mechanics.forcefield = "detached request"
    with msv.new_view() as owner:
        before = snapshot(owner)
        files = owner.addons.molsysmt.h5msm
        refused = tmp_path / "refused-05.h5msm"
        with pytest.raises(ValueError, match="0.5"):
            files.write_layers(
                refused,
                molecular_mechanics=mechanics,
                mechanics_n_atoms=7,
                format_version="0.5",
                skip_digestion=skip,
            )
        assert not refused.exists()
        files.write_layers(
            path,
            molecular_mechanics=mechanics,
            mechanics_n_atoms=7,
            format_version="0.6",
            skip_digestion=skip,
        )
        with h5py.File(path) as stored:
            assert str(stored.attrs["version"]) == "0.6"
        sizes = files.read_axis_sizes(path, skip_digestion=skip)
        assert sizes == {("molecular_mechanics", None, "atom"): 7}
        assert sizes == msm.h5msm.read_axis_sizes(path, skip_digestion=skip)
        loaded = files.read_layers(path)["molecular_mechanics"]
        assert loaded is not mechanics
        assert loaded.forcefield == "detached request"
        loaded.forcefield = "changed reader"
        assert mechanics.forcefield == "detached request"
        unchanged(owner, before)


@pytest.mark.parametrize("skip", [False, True])
def test_bound_h5msm_write_preserves_default_and_rejects_lossy_05(view, tmp_path, skip):
    view.molsys.molecular_mechanics.forcefield = "request"
    before = snapshot(view)
    default_path, explicit_path = (
        tmp_path / "default.h5msm",
        tmp_path / "explicit.h5msm",
    )
    files = view.addons.molsysmt.h5msm
    files.write(default_path, skip_digestion=skip)
    with h5py.File(default_path) as stored:
        assert str(stored.attrs["version"]) == "1.0"
    default_loaded = files.read(default_path)
    assert default_loaded.molecular_mechanics.forcefield == "request"
    np.testing.assert_array_equal(
        puw.get_value(default_loaded.structures.coordinates),
        puw.get_value(view.molsys.structures.coordinates),
    )
    refused = tmp_path / "refused-05.h5msm"
    with pytest.raises(ValueError, match="0.5"):
        files.write(refused, skip_digestion=skip, format_version="0.5")
    assert not refused.exists()
    files.write(explicit_path, skip_digestion=skip, format_version="0.6")
    loaded = files.read(explicit_path)
    assert loaded.molecular_mechanics.forcefield == "request"
    np.testing.assert_array_equal(
        puw.get_value(loaded.structures.coordinates),
        puw.get_value(view.molsys.structures.coordinates),
    )
    unchanged(view, before)


def test_pending_primary_readers_follow_native_data_without_scene_sync(view, tmp_path):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([2, 0, 0], "nm"),
        structure_indices=[1],
        in_place=True,
        update_view=False,
    )
    assert tools.get_sync_status()["state"] == "pending"
    before = snapshot(view)
    result = tools.structure.get_pairwise_rmsd(
        selection="all", structure_indices=[1, 0]
    )
    np.testing.assert_allclose(
        puw.get_value(result["rmsd"], to_unit="nm"), [[0, 3], [3, 0]]
    )
    normalized = tools.chemical_states.normalize_indexed_hydrogen_policy()
    np.testing.assert_array_equal(
        puw.get_value(normalized["molecular_system"].structures.coordinates),
        puw.get_value(view.molsys.structures.coordinates),
    )
    path = tmp_path / "pending.h5msm"
    tools.h5msm.write(path)
    assert tools.h5msm.read_axis_sizes(path)[("structures", None, "structure")] == 2
    np.testing.assert_array_equal(
        puw.get_value(tools.h5msm.read(path).structures.coordinates),
        puw.get_value(view.molsys.structures.coordinates),
    )
    unchanged(view, before)


def test_explicit_utilities_do_not_enter_primary_coordinator(
    view, tmp_path, monkeypatch
):
    tools = view.addons.molsysmt
    path = tmp_path / "axes.h5msm"
    msm.h5msm.write_layers(
        path,
        molecular_mechanics=MolecularMechanics(),
        mechanics_n_atoms=7,
        format_version="0.6",
    )
    tools.structure.translate(
        translation="[1, 0, 0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Explicit utilities must not read or synchronize the primary."
        )

    coordinator = view.addons.manager.system_edits
    with monkeypatch.context() as isolated:
        for operation in ("read", "execute", "synchronize"):
            isolated.setattr(coordinator, operation, forbidden)
        tools.structure.get_distance_clusters(matrix(), "1 nm")
        assert (
            tools.h5msm.read_axis_sizes(path)[("molecular_mechanics", None, "atom")]
            == 7
        )
    unchanged(view, before)


@pytest.mark.parametrize(
    "path,args",
    [
        ("structure.get_pairwise_rmsd", {"selection": "all", "max_work": 0}),
        (
            "structure.get_pairwise_rmsd",
            {"selection": "all", "member_keys": ["x", "x"]},
        ),
        (
            "chemical_states.normalize_indexed_hydrogen_policy",
            {"chemical_state": "structure"},
        ),
    ],
)
def test_native_request_rejections_preserve_source_and_scene(view, path, args):
    before = snapshot(view)
    source_flags = msm.get(view.molsys, element="atom", allows_implicit_hydrogens=True)
    with pytest.raises((ArgumentError, UnsupportedHeavyOperationError)):
        resolve(view.addons.molsysmt, path)(**args)
    assert (
        msm.get(view.molsys, element="atom", allows_implicit_hydrogens=True)
        == source_flags
    )
    unchanged(view, before)


@pytest.mark.parametrize("failure", ["asymmetric", "unitless", "work", "budget"])
def test_clustering_keeps_native_refusals_on_empty_owner(failure, monkeypatch):
    distances, args = matrix(), {}
    expected = {
        "asymmetric": StructuralInconsistencyError,
        "unitless": ArgumentError,
        "work": UnsupportedHeavyOperationError,
        "budget": MemoryBudgetExceededError,
    }[failure]
    if failure == "asymmetric":
        puw.get_value(distances)[0, 1] = 0.5
    if failure == "unitless":
        distances = puw.get_value(distances)
    if failure == "work":
        args["max_work"] = 1
    with msv.new_view() as owner:
        before = snapshot(owner)
        with monkeypatch.context() as scoped:
            if failure == "budget":
                scoped.setattr(msm.configure, "max_ram_usage", 2)
            with pytest.raises(expected):
                owner.addons.molsysmt.structure.get_distance_clusters(
                    distances, "1 nm", **args
                )
        unchanged(owner, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("path", PATHS)
def test_unknown_controls_are_not_accepted(view, path, skip, tmp_path):
    before = snapshot(view)
    args = {
        "structure.get_distance_clusters": (matrix(), "1 nm"),
        "h5msm.read_axis_sizes": (tmp_path / "unused.h5msm",),
        "h5msm.write": (tmp_path / "unused.h5msm",),
        "h5msm.write_layers": (tmp_path / "unused.h5msm",),
    }.get(path, ())
    with pytest.raises(TypeError if skip else UnknownArgumentError):
        resolve(view.addons.molsysmt, path)(
            *args, update_view=True, skip_digestion=skip
        )
    unchanged(view, before)


def test_cached_readers_follow_replacement_and_retained_results_survive_close(
    view, tmp_path
):
    tools = view.addons.molsysmt
    pairwise = tools.structure.get_pairwise_rmsd
    normalize = tools.chemical_states.normalize_indexed_hydrogen_policy
    result = pairwise(selection="all")
    normalized = normalize()
    replacement = water(flags=(False, False))
    view.load(replacement, mode="replace")
    assert normalize()["report"]["status"] == "unchanged"
    actual = pairwise(selection="all")
    np.testing.assert_allclose(
        puw.get_value(actual["rmsd"], to_unit="nm")[0, 1], 0.9 * np.sqrt(3)
    )
    explicit = tools.structure.get_distance_clusters
    cluster = explicit(matrix(), "1 nm")
    axes = tools.h5msm.read_axis_sizes
    view.close()
    for method, args, kwargs in [
        (pairwise, (), {"selection": "all"}),
        (normalize, (), {}),
        (explicit, (matrix(), "1 nm"), {}),
        (axes, (tmp_path / "absent.h5msm",), {}),
        (tools.h5msm.write, (tmp_path / "closed.h5msm",), {}),
        (tools.h5msm.write_layers, (tmp_path / "closed.h5msm",), {}),
    ]:
        with pytest.raises(RuntimeError, match="closed"):
            method(*args, **kwargs)
    assert puw.get_value(result["rmsd"], to_unit="nm")[0, 1] == 1
    assert normalized["report"]["changed_atom_indices"].tolist() == [1]
    assert cluster["cluster_indices"].tolist() == [0, 0, 1]
