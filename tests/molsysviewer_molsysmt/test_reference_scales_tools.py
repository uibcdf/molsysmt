"""Receive strict reference scales without assigning physical scene properties."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, UnknownGroupInTableError

puw = msm.pyunitwizard
CASES = [
    ("get_bulkiness", {}, 11.5),
    ("get_secondary_structure_propensity", {"conformation": "alpha_helix"}, 1.29),
    ("get_secondary_structure_propensity", {"conformation": "beta_sheet"}, 0.90),
    ("get_secondary_structure_propensity", {"conformation": "reverse_turn"}, 0.77),
]


@pytest.fixture(params=CASES, ids=["bulkiness", "helix", "sheet", "turn"])
def case(request):
    return request.param


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            result.interactions.attach(
                msm.Interactions.from_records(
                    [],
                    n_atoms=result.molsys.get_n_atoms(),
                    n_structures=3,
                    evaluated_structure_indices=[0, 1, 2],
                    method="receiving.scales",
                ),
                name="preserve",
                assume_aligned=True,
            )
            result.regions.add(selection=[0, 2, 4], tag="source")
            yield result


@pytest.fixture(scope="module")
def protein():
    with msv.demo["181L"] as result:
        yield result


def call(view, case, **kwargs):
    return getattr(view.addons.molsysmt.physchem, case[0])(**(case[1] | kwargs))


def native(view, case, **kwargs):
    return getattr(msm.physchem, case[0])(view.molsys, **(case[1] | kwargs))


def values(result, case):
    if case[0] == "get_bulkiness":
        assert puw.is_quantity(result)
        return puw.get_value(result, to_unit="angstrom**2")
    assert type(result) is np.ndarray and result.dtype == np.float64
    assert not puw.is_quantity(result)
    return result


def test_exact_native_signatures_help_and_no_invented_arguments(view, case):
    method = getattr(view.addons.molsysmt.physchem, case[0])
    signature = inspect.signature(getattr(msm.physchem, case[0]))
    assert inspect.signature(method) == signature.replace(
        parameters=list(signature.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert not hasattr(view.addons.molsysmt, case[0])
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    assert "strict reference lookup per group" in doc
    assert "\nmolecular_system :" not in doc
    for kwargs in [
        dict(molecular_system=view.molsys),
        dict(update_view=False),
        dict(structure_indices=[0]),
        dict(normalize=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            call(view, case, **kwargs)
        with pytest.raises(TypeError):
            call(view, case, **kwargs, skip_digestion=True)


def test_propensity_category_is_required_and_positional_or_keyword(view):
    method = view.addons.molsysmt.physchem.get_secondary_structure_propensity
    assert (
        inspect.signature(method).parameters["conformation"].default
        is inspect.Parameter.empty
    )
    with pytest.raises(TypeError):
        method(selection=[1])
    np.testing.assert_array_equal(method("alpha_helix", selection=[1]), [1.29])
    np.testing.assert_array_equal(
        method(conformation="reverse_turn", selection=[1]), [0.77]
    )


@pytest.mark.parametrize("selection", ["group_name=='ALA'", [5, 1, 5], 1, []])
@pytest.mark.parametrize("skip", [False, True])
def test_known_values_group_axis_order_repeats_and_empty(view, case, selection, skip):
    result = call(view, case, selection=selection, skip_digestion=skip)
    count = (
        5
        if isinstance(selection, str)
        else 1
        if isinstance(selection, int)
        else len(selection)
    )
    observed = values(result, case)
    assert observed.shape == (count,) and observed.dtype.kind == "f"
    np.testing.assert_allclose(observed, [case[2]] * count, rtol=0, atol=1e-12)
    np.testing.assert_array_equal(
        observed,
        values(native(view, case, selection=selection, skip_digestion=skip), case),
    )
    # Three structures do not add a structure axis or repeat a reference value.
    assert msm.get(view.molsys, n_structures=True) == 3 and observed.ndim == 1


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_native_units_and_dimensionless_ratios_remain_distinct(view, case, length_unit):
    with puw.context(standard_units=[length_unit, "ps", "radians"]):
        result = call(view, case, selection=[1, 2])
        if case[0] == "get_bulkiness":
            assert puw.get_unit(result) == puw.unit(length_unit) ** 2
            np.testing.assert_allclose(
                puw.get_value(result, to_unit="nm**2"),
                [0.115, 0.115],
                rtol=0,
                atol=1e-12,
            )
        np.testing.assert_allclose(
            values(result, case), [case[2], case[2]], rtol=0, atol=1e-12
        )


def test_frequency_ratios_are_not_probabilities_and_have_no_coil_remainder(view):
    method = view.addons.molsysmt.physchem.get_secondary_structure_propensity
    ratios = [
        method(category, selection=[1])[0]
        for category in ["alpha_helix", "beta_sheet", "reverse_turn"]
    ]
    np.testing.assert_array_equal(ratios, [1.29, 0.9, 0.77])
    assert ratios[0] > 1 and sum(ratios) != 1
    with pytest.raises(msm.ArgumentError, match="conformation"):
        method("coil", selection=[1])


@pytest.mark.parametrize(
    "syntax,selection", [("MolSysMT", "group_index in [1, 3]"), ("MDTraj", "resid 1 3")]
)
def test_native_and_external_group_populations(view, case, syntax, selection):
    result = call(view, case, selection=selection, syntax=syntax)
    np.testing.assert_allclose(
        values(result, case), [case[2], case[2]], rtol=0, atol=1e-12
    )
    np.testing.assert_array_equal(
        values(result, case), values(native(view, case, selection=[1, 3]), case)
    )


def test_real_protein_mixed_groups_and_nonconsecutive_repeated_indices(protein, case):
    names = protein.molsys.topology.groups["group_name"].to_numpy()
    gly = int(np.flatnonzero(names == "GLY")[0])
    ala = int(np.flatnonzero(names == "ALA")[0])
    pro = int(np.flatnonzero(names == "PRO")[0])
    indices = [gly, ala, pro, gly]
    # Independent checked reference rows; do not use the implementation's tables.
    if case[0] == "get_bulkiness":
        expected = [3.4, 11.5, 17.43, 3.4]
    else:
        expected = {
            "alpha_helix": [0.56, 1.29, 0.52, 0.56],
            "beta_sheet": [0.92, 0.9, 0.64, 0.92],
            "reverse_turn": [1.64, 0.77, 1.91, 1.64],
        }[case[1]["conformation"]]
    np.testing.assert_allclose(
        values(call(protein, case, selection=indices), case),
        expected,
        rtol=0,
        atol=1e-12,
    )


def test_native_default_does_not_silently_filter_terminal_caps(view, case):
    with pytest.raises(UnknownGroupInTableError):
        native(view, case)
    with pytest.raises(UnknownGroupInTableError):
        call(view, case)


@pytest.mark.parametrize("element", ["atom", "system", "chain", "molecule"])
def test_unsupported_levels_reject_before_selection_without_aggregation(
    view, case, element
):
    args = dict(element=element, selection="invalid !!!!!")
    with pytest.raises(ArgumentChoiceError, match="element"):
        native(view, case, **args)
    with pytest.raises(ArgumentChoiceError, match="element"):
        call(view, case, **args)


@pytest.mark.parametrize(
    "args", [dict(definition="guess"), dict(selection=[999]), dict(selection=[-1])]
)
@pytest.mark.parametrize("skip", [False, True])
def test_native_error_types_preserve_scene_and_sync_state(view, case, args, skip):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as expected:
        native(view, case, **args, skip_digestion=skip)
    with pytest.raises(type(expected.value)):
        call(view, case, **args, skip_digestion=skip)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_detached_values_preserve_primary_domains_named_coverage_and_scene(view, case):
    primary = view.molsys
    owners = (
        primary.topology,
        primary.structures,
        primary.chemical_states,
        primary.interactions["preserve"],
    )
    atoms, groups = (
        primary.topology.atoms.copy(deep=True),
        primary.topology.groups.copy(deep=True),
    )
    coordinates = puw.get_value(primary.structures.coordinates).copy()
    coverage = owners[3].to_dict()
    scene, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    result = call(view, case, selection=[1, 2])
    result[:] *= 2
    np.testing.assert_allclose(
        values(call(view, case, selection=[1, 2]), case),
        [case[2], case[2]],
        rtol=0,
        atol=1e-12,
    )
    assert view.molsys is primary
    assert all(
        a is b
        for a, b in zip(
            owners,
            (
                primary.topology,
                primary.structures,
                primary.chemical_states,
                primary.interactions["preserve"],
            ),
        )
    )
    pd.testing.assert_frame_equal(primary.topology.atoms, atoms)
    pd.testing.assert_frame_equal(primary.topology.groups, groups)
    np.testing.assert_array_equal(
        puw.get_value(primary.structures.coordinates), coordinates
    )
    np.testing.assert_equal(owners[3].to_dict(), coverage)
    assert (
        view.export_state() == scene
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_reads_pending_current_primary_without_synchronizing(view, case):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    np.testing.assert_allclose(
        values(call(view, case, selection=[1, 2]), case),
        [case[2]] * 2,
        rtol=0,
        atol=1e-12,
    )
    assert tools.get_sync_status() == status
    with pytest.raises(SystemEditPendingError):
        view.export_state()


def test_cached_facade_uses_replacement_and_keeps_closed_empty_guards(view, case):
    method = getattr(view.addons.molsysmt.physchem, case[0])
    with msv.demo["dialanine"] as other:
        assert other.molsys.topology.groups["group_name"].tolist() == [
            "ACE",
            "ALA",
            "NME",
        ]
        view.load(other.molsys, mode="replace")
    result = method(**case[1], selection="group_name=='ALA'")
    np.testing.assert_allclose(values(result, case), [case[2]], rtol=0, atol=1e-12)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.physchem, case[0])(**case[1], selection=[])
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(**case[1], selection=[])


def test_real_optional_attribution_remains_native_once_per_lookup(view):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("bound scales"):
        with ackredit.scope("consumer.bound_scales"):
            view.addons.molsysmt.physchem.get_bulkiness(selection=[1])
            view.addons.molsysmt.physchem.get_secondary_structure_propensity(
                "alpha_helix", selection=[]
            )
        assert {"zimmerman_1968", "proust_2019", "levitt_1978"} <= set(
            ackredit.get_used_items()
        )
        children = ackredit.current_session().usage_tree["consumer.bound_scales"][
            "children"
        ]
        assert "molsysmt.physchem.get_bulkiness" in children
        assert "molsysmt.physchem.get_secondary_structure_propensity" in children
