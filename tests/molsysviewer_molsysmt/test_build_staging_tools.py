"""Receive detached builders and explicit molecule-overlap filtering."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard
NAMES = ("editable", "remove_overlapping_molecules")


def source():
    builder = msm.build.editable()
    for index in range(5):
        builder.add_atom(atom_id=str(index + 10), atom_name=f"C{index}", atom_type="C")
    for atoms in ([0, 1], [2, 3], [4]):
        group = builder.add_group(atoms, group_name="LIG", group_type="small molecule")
        builder.add_molecule(
            [group], molecule_name="ligand", molecule_type="small molecule"
        )
    builder.add_chain([0, 1, 2], chain_id="A")
    builder.add_bond(0, 1)
    builder.add_bond(2, 3)
    xyz = np.array([[0, 0, 0], [0.11, 0, 0], [1, 0, 0], [1.11, 0, 0], [0.25, 0, 0]])
    coordinates = np.stack([xyz, xyz.copy(), xyz.copy()])
    coordinates[1, 4, 0] = 1.25
    coordinates[2, 4, 0] = 1.95
    builder.set_coordinates(puw.quantity(coordinates, "nm"))
    builder.set_box(puw.quantity(np.tile(2 * np.eye(3), (3, 1, 1)), "nm"))
    builder.set_time(puw.quantity([1, 4, 8], "ps"))
    builder.set_structure_id([11, 24, 80])
    result = builder.build()
    result.interactions = {
        "saved": msm.Interactions.from_records(
            [],
            n_atoms=5,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="receiving.staging",
        )
    }
    return result


def parameters(name):
    return (
        {}
        if name == "editable"
        else dict(selection=[1, 3], selection_2=[4], threshold="0.2 nm", pbc=False)
    )


@pytest.fixture(params=NAMES)
def case(request):
    with msv.new_view(source()) as view:
        view.regions.add(selection=[0, 1], tag="keep")
        view.shapes.add_sphere(atom_indices=[4], tag="anchor")
        yield request.param, view


def test_native_signature_help_namespace_and_local_controls(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    expected = list(native.parameters.values())[1:]
    if name == "remove_overlapping_molecules":
        expected.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    assert inspect.signature(method) == native.replace(parameters=expected)
    assert method.digestion_plan is not None
    assert name in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, name)
    doc = inspect.getdoc(method)
    assert "View integration" in doc and "no update_view" in doc
    assert "\nmolecular_system :" not in doc
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in doc
    for key in ("molecular_system", "update_view", "in_place", "prepare"):
        with pytest.raises(UnknownArgumentError):
            method(**parameters(name), **{key: None})
    with pytest.raises(Exception):
        method(**parameters(name), skip_digestion="yes")


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_builder_copies_native_domains_and_leaves_source_analyses_intact(skip, unit):
    with msv.new_view(source()) as view:
        primary = view.molsys
        primary.molecular_mechanics.forcefield = "AMBER14"
        primary.molecular_mechanics.partial_charge = puw.quantity(
            np.arange(5, dtype=float), "elementary_charge"
        )
        primary.chemical_states._append_state(primary.chemical_states._states[0].copy())
        primary._structure_chemical_state_indices = np.array([0, 1, 0], dtype=np.int64)
        before = snapshot(view)
        with puw.context(standard_units=[unit, "ps"]):
            builder = view.addons.molsysmt.build.editable(skip_digestion=skip)
        assert isinstance(builder, msm.MolSysBuilder)
        assert (builder.n_atoms, builder.n_groups, builder.n_molecules) == (5, 3, 3)
        assert builder.chemical_states.n_chemical_states == 2
        assert builder.topology is not primary.topology
        assert builder.chemical_states is not primary.chemical_states
        assert builder.structures is not primary.structures
        output = builder.build()
        assert not output.interactions
        assert output.molecular_mechanics.forcefield is None
        assert output.molecular_mechanics.partial_charge is None
        np.testing.assert_array_equal(
            output._structure_chemical_state_indices, [0, 1, 0]
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            puw.get_value(primary.structures.coordinates, to_unit="nm"),
        )
        assert output.structures.structure_id.tolist() == [11, 24, 80]
        np.testing.assert_array_equal(
            puw.get_value(output.structures.time, to_unit="ps"), [1, 4, 8]
        )
        builder.remove_bonds([0], chemical_state=0)
        builder.set_coordinates(
            puw.quantity(
                puw.get_value(primary.structures.coordinates, to_unit="nm") + 2, "nm"
            )
        )
        edited = builder.build()
        assert edited.chemical_states.get(n_bonds=True, chemical_state=0) == 1
        assert primary.chemical_states.get(n_bonds=True, chemical_state=0) == 2
        np.testing.assert_array_equal(
            puw.get_value(edited.structures.coordinates, to_unit="nm"),
            puw.get_value(primary.structures.coordinates, to_unit="nm") + 2,
        )
        unchanged(view, before)


def test_builder_outlives_replacement_and_close_without_adoption():
    view = msv.new_view(source())
    method = view.addons.molsysmt.build.editable
    original = method()
    with msv.demo["dialanine"] as replacement:
        view.load(replacement.molsys, mode="replace")
    updated = method()
    assert original.n_atoms == 5
    assert updated.n_atoms == view.molsys.get_n_atoms() != 5
    view.close()
    original.remove_bonds([0])
    assert original.build().get_n_atoms() == 5
    assert original.n_bonds == 1
    assert updated.build().get_n_atoms() == updated.n_atoms
    with pytest.raises(RuntimeError, match="closed view"):
        method()


def test_native_builder_growth_rejection_preserves_both_source_and_staging():
    with msv.new_view(source()) as view:
        before = snapshot(view)
        actual = view.addons.molsysmt.build.editable()
        expected = msm.build.editable(view.molsys)
        with pytest.raises(Exception) as error:
            expected.add_atom(atom_name="N", atom_type="N")
        with pytest.raises(type(error.value)) as caught:
            actual.add_atom(atom_name="N", atom_type="N")
        assert str(caught.value) == str(error.value)
        assert actual.n_atoms == 5
        unchanged(view, before)


@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "index,pbc,ids",
    [
        (0, False, ["12", "13", "14"]),
        (1, False, ["10", "11", "14"]),
        (2, True, ["12", "13", "14"]),
    ],
)
def test_overlap_removes_complete_molecule_from_all_structures(index, pbc, ids, unit):
    with msv.new_view(source()) as view:
        before = snapshot(view)
        primary = view.molsys
        args = dict(
            selection=[1, 3],
            selection_2=[4],
            structure_index=index,
            threshold=puw.quantity(2, "angstrom"),
            pbc=pbc,
        )
        with puw.context(standard_units=[unit, "ps"]):
            output = view.addons.molsysmt.build.remove_overlapping_molecules(**args)
        assert output is not primary
        assert output.topology.atoms.atom_id.tolist() == ids
        assert output.topology.n_molecules == 2
        # Only one candidate atom contacts the reference, but both molecule atoms go.
        kept = np.array([int(value) - 10 for value in ids])
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            puw.get_value(primary.structures.coordinates, to_unit="nm")[:, kept],
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.box, to_unit="nm"),
            puw.get_value(primary.structures.box, to_unit="nm"),
        )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.time, to_unit="ps"), [1, 4, 8]
        )
        assert output.structures.structure_id.tolist() == [11, 24, 80]
        assert output.interactions["saved"].evaluated_structure_indices.tolist() == [
            0,
            1,
            2,
        ]
        assert (
            output.interactions["saved"].atom_source_indices.tolist() == kept.tolist()
        )
        same(output, msm.build.remove_overlapping_molecules(primary, **args))
        unchanged(view, before)


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("partial", [False, True])
def test_overlap_syntax_complement_and_local_skip_keep_native_validation(
    syntax, skip, partial
):
    with msv.new_view(source()) as view:
        before = snapshot(view)
        selection = (
            ("atom_index==1 or atom_index==3" if partial else "atom_index<4")
            if syntax == "MolSysMT"
            else ("index 1 or index 3" if partial else "index 0 to 3")
        )
        args = dict(selection=selection, syntax=syntax, threshold="0.2 nm", pbc=False)
        output = view.addons.molsysmt.build.remove_overlapping_molecules(
            **args, skip_digestion=skip
        )
        # Atom complement includes a partially selected molecule's own partners.
        assert output.topology.atoms.atom_id.tolist() == (
            ["14"] if partial else ["12", "13", "14"]
        )
        same(output, msm.build.remove_overlapping_molecules(view.molsys, **args))
        unchanged(view, before)


@pytest.mark.parametrize("no_box", [False, True])
def test_no_overlap_returns_current_primary_and_no_box_uses_native_nonperiodic(no_box):
    molsys = source()
    if no_box:
        molsys.structures.box = None
    with msv.new_view(molsys) as view:
        before = snapshot(view)
        output = view.addons.molsysmt.build.remove_overlapping_molecules(
            selection=[1, 3],
            selection_2=[4],
            threshold="0.2 nm",
            structure_index=2,
            pbc=no_box,
        )
        assert output is view.molsys
        unchanged(view, before)


@pytest.mark.parametrize(
    "problem", [{"structure_index": 99}, {"selection": [99]}, {"threshold": "bad"}]
)
@pytest.mark.parametrize("skip", [False, True])
def test_overlap_native_rejections_are_not_bypassed_by_local_skip(problem, skip):
    with msv.new_view(source()) as view:
        args = parameters("remove_overlapping_molecules") | problem
        before = snapshot(view)
        with pytest.raises(Exception) as error:
            msm.build.remove_overlapping_molecules(view.molsys, **args)
        with pytest.raises(type(error.value)) as caught:
            view.addons.molsysmt.build.remove_overlapping_molecules(
                **args, skip_digestion=skip
            )
        assert str(caught.value) == str(error.value)
        unchanged(view, before)


def test_pending_reader_does_not_synchronize_or_adopt(case):
    name, view = case
    tools = view.addons.molsysmt
    tools.basic.set(coordinates=view.molsys.structures.coordinates, update_view=False)
    before = snapshot(view)
    output = getattr(tools.build, name)(**parameters(name))
    expected = getattr(msm.build, name)(view.molsys, **parameters(name))
    same(
        output.build() if name == "editable" else output,
        expected.build() if name == "editable" else expected,
    )
    assert tools.get_sync_status()["state"] == "pending"
    unchanged(view, before)


def test_cached_tool_resolves_replacement_and_rejects_closed_empty_owners(case):
    name, view = case
    method = getattr(view.addons.molsysmt.build, name)
    replacement = source()
    replacement.structures.coordinates = (
        replacement.structures.coordinates + puw.quantity(2, "nm")
    )
    view.load(replacement, mode="replace")
    before = snapshot(view)
    output = method(**parameters(name))
    expected = getattr(msm.build, name)(view.molsys, **parameters(name))
    same(
        output.build() if name == "editable" else output,
        expected.build() if name == "editable" else expected,
    )
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**parameters(name))
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(**parameters(name))
