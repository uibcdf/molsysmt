"""Receive CPU SASA without replacing native science or publishing scene edits.

Native non-nm unit correctness and engine-periodic policy remain owning issues
#478/#479. These checks do not qualify GPU execution or an installed artifact.
"""

import inspect
import json
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm

puw = msm.pyunitwizard
CPU = dict(use_gpu=False, n_sphere_points=960, use_cell_list=False)
AREA_ATOL = json.loads(
    (
        Path(__file__).parents[1] / "scientific_truth/evidence/tolerances.json"
    ).read_text()
)["shrake_rupley_sampling_area_atol"]["atol"]


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as original:
        with msv.new_view(original.molsys, structure_indices=[0, 8, 3]) as result:
            result.interactions.attach(
                msm.Interactions.from_records(
                    [],
                    n_atoms=result.molsys.get_n_atoms(),
                    n_structures=3,
                    evaluated_structure_indices=[0, 1, 2],
                    method="receiving.sasa",
                ),
                name="preserve",
                assume_aligned=True,
            )
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


def nm2(value):
    assert puw.is_quantity(value)
    assert puw.get_unit(value).is_compatible_with(puw.unit("nm**2"))
    return puw.get_value(value, to_unit="nm**2")


def test_signature_help_and_integration_controls(view):
    method = view.addons.molsysmt.physchem.get_sasa
    native = inspect.signature(msm.physchem.get_sasa)
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, "get_sasa")
    assert "update_view" not in inspect.signature(method).parameters
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "All primary atoms remain occluders" in doc
    assert "uibcdf/molsysmt#478" in doc and "uibcdf/molsysmt#479" in doc
    for args in [dict(molecular_system=view.molsys), dict(update_view=False)]:
        with pytest.raises(UnknownArgumentError):
            method(**args)
        with pytest.raises(TypeError):
            method(**args, skip_digestion=True)


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("structures", [[2, 0, 2], [1], "all"])
@pytest.mark.parametrize("selection", [[7, 1, 7, 4], [], "atom_name=='CA'"])
def test_selected_atoms_are_output_filter_with_native_axes(
    view, engine, structures, selection
):
    args = dict(CPU, engine=engine, structure_indices=structures)
    full = nm2(msm.physchem.get_sasa(view.molsys, **args))
    indices = msm.select(view.molsys, selection=selection)
    expected = full[:, indices]
    actual = view.addons.molsysmt.physchem.get_sasa(selection=selection, **args)
    assert actual.shape == expected.shape
    np.testing.assert_array_equal(nm2(actual), expected)
    np.testing.assert_array_equal(
        nm2(actual),
        nm2(msm.physchem.get_sasa(view.molsys, selection=selection, **args)),
    )


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize(
    "element", ["group", "component", "molecule", "chain", "entity"]
)
def test_hierarchy_is_sum_of_all_atom_occlusion(view, engine, element):
    args = dict(CPU, engine=engine, structure_indices=[2, 0])
    atoms = nm2(msm.physchem.get_sasa(view.molsys, **args))
    membership = msm.get(view.molsys, element=element, atom_index=True)
    expected = np.column_stack(
        [atoms[:, indices].sum(axis=1) for indices in membership]
    )
    actual = view.addons.molsysmt.physchem.get_sasa(element=element, **args)
    assert actual.shape == expected.shape
    np.testing.assert_allclose(nm2(actual), expected, rtol=1e-7)


@pytest.mark.parametrize("cell_list", [False, True, "auto"])
@pytest.mark.parametrize("box", [False, True])
def test_cpu_cell_list_preserves_requested_structure_results(view, cell_list, box):
    if not box:
        msm.set(view.molsys, box=None)
    args = dict(CPU, structure_indices=[2, 0, 2])
    expected = nm2(msm.physchem.get_sasa(view.molsys, **args))
    args["use_cell_list"] = cell_list
    actual = view.addons.molsysmt.physchem.get_sasa(**args)
    np.testing.assert_allclose(nm2(actual), expected, atol=AREA_ATOL, rtol=0)


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("probe", ["0.14 nm", "1.4 angstroms", "140 pm"])
def test_isolated_real_carbon_has_analytic_area(view, engine, probe):
    carbon = int(msm.select(view.molsys, selection="atom_type=='C'")[0])
    molecular_system = msm.extract(
        view.molsys, selection=[carbon], structure_indices=[0]
    )
    msm.set(molecular_system, box=None)
    with msv.new_view(molecular_system) as isolated:
        actual = isolated.addons.molsysmt.physchem.get_sasa(
            **CPU, engine=engine, probe_radius=probe
        )
        assert actual.shape == (1, 1)
        np.testing.assert_allclose(
            nm2(actual), [[4 * np.pi * (0.17 + 0.14) ** 2]], rtol=1e-6
        )


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
def test_boundary_conditions_have_distinct_explicit_receiving(view, engine):
    carbons = msm.select(view.molsys, selection="atom_type=='C'")[:2]
    molecular_system = msm.extract(
        view.molsys, selection=carbons, structure_indices=[0]
    )
    msm.set(
        molecular_system,
        coordinates=puw.quantity([[[0.1, 0, 0], [1.9, 0, 0]]], "nm"),
        box=puw.quantity([2 * np.eye(3)], "nm"),
    )
    with msv.new_view(molecular_system) as pair:
        actual = nm2(pair.addons.molsysmt.physchem.get_sasa(**CPU, engine=engine))
        # Native MIC distance is 0.2 nm; MDTraj uses 1.8 nm in Cartesian space.
        radius = 0.31
        area = (
            2 * np.pi * radius**2 + np.pi * radius * 0.2
            if engine == "MolSysMT"
            else 4 * np.pi * radius**2
        )
        np.testing.assert_allclose(actual, [[area, area]], atol=AREA_ATOL, rtol=0)
        msm.set(pair.molsys, box=None)
        vacuum = nm2(pair.addons.molsysmt.physchem.get_sasa(**CPU, engine=engine))
        np.testing.assert_allclose(
            vacuum, np.full((1, 2), 4 * np.pi * radius**2), rtol=1e-6
        )


@pytest.mark.parametrize("skip", [False, True])
def test_syntax_skip_execution_options_and_current_pending_primary(view, skip):
    tools = view.addons.molsysmt
    tools.structure.translate(
        selection=[0],
        translation=puw.quantity([1, 0, 0], "nm"),
        in_place=True,
        update_view=False,
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    args = dict(
        CPU,
        selection="name CA",
        syntax="MDTraj",
        structure_indices=[2, 0],
        parallel=False,
        num_threads=1,
        skip_digestion=skip,
    )
    actual = nm2(tools.physchem.get_sasa(**args))
    expected = nm2(msm.physchem.get_sasa(view.molsys, **args))
    np.testing.assert_array_equal(actual, expected)
    indices = msm.select(view.molsys, selection="atom_name=='CA'")
    reference_args = dict(
        CPU, selection=indices, structure_indices=[2, 0], parallel=False, num_threads=1
    )
    np.testing.assert_array_equal(
        actual, nm2(msm.physchem.get_sasa(view.molsys, **reference_args))
    )
    assert tools.get_sync_status() == status
    with pytest.raises(SystemEditPendingError):
        view.export_state()


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
def test_read_preserves_primary_owners_coordinates_box_scene_and_named_analysis(
    view, engine
):
    primary = view.molsys
    owners = (primary.topology, primary.structures, primary.interactions["preserve"])
    xyz, box = msm.get(primary, coordinates=True, box=True)
    xyz, box = puw.get_value(xyz).copy(), puw.get_value(box).copy()
    coverage = owners[2].to_dict()
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    view.addons.molsysmt.physchem.get_sasa(**CPU, engine=engine)
    assert (
        view.molsys is primary
        and primary.topology is owners[0]
        and primary.structures is owners[1]
    )
    assert primary.interactions["preserve"] is owners[2]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(primary, coordinates=True)), xyz
    )
    np.testing.assert_array_equal(puw.get_value(msm.get(primary, box=True)), box)
    for key, value in coverage.items():
        if isinstance(value, np.ndarray):
            np.testing.assert_array_equal(owners[2].to_dict()[key], value)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize(
    "args",
    [
        dict(engine="missing"),
        dict(n_sphere_points=0),
        dict(n_sphere_points=True),
        dict(probe_radius="1 ps"),
        dict(structure_indices=[999]),
    ],
)
def test_native_rejections_preserve_scene_and_sync_state(view, args):
    parameters = dict(CPU, **args)
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        msm.physchem.get_sasa(view.molsys, **parameters)
    with pytest.raises(type(expected.value)):
        view.addons.molsysmt.physchem.get_sasa(**parameters)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_cached_facade_resolves_replacement_empty_and_closed_views(view):
    facade = view.addons.molsysmt.physchem
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
        np.testing.assert_array_equal(
            nm2(facade.get_sasa(**CPU)), nm2(msm.physchem.get_sasa(view.molsys, **CPU))
        )
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.physchem.get_sasa(**CPU)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        facade.get_sasa(**CPU)


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_mdtraj_unit_context_has_independent_analytic_receiving(view, length_unit):
    carbon = int(msm.select(view.molsys, selection="atom_type=='C'")[0])
    molecular_system = msm.extract(
        view.molsys, selection=[carbon], structure_indices=[0]
    )
    msm.set(molecular_system, box=None)
    with msv.new_view(molecular_system) as isolated:
        # Native-engine non-nm results are deliberately not certified here (#478).
        with puw.context(
            standard_units=[
                length_unit,
                "ps",
                "radians",
                "dalton",
                "e",
                "dimensionless",
            ]
        ):
            actual = isolated.addons.molsysmt.physchem.get_sasa(**CPU, engine="MDTraj")
            assert puw.get_unit(actual).is_compatible_with(puw.unit(length_unit) ** 2)
            np.testing.assert_allclose(nm2(actual), [[4 * np.pi * 0.31**2]], rtol=1e-6)
