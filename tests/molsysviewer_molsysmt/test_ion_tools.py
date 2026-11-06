"""Receive independent whole-water ion replacement through the native API."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged

puw = msm.pyunitwizard


@pytest.fixture
def view():
    water = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))
    with msv.new_view(water) as owner:
        owner.regions.add(selection=[0, 1, 2], tag="one-water")
        owner.shapes.add_sphere(atom_indices=[0], tag="caller-shape")
        yield owner


def test_signature_discovery_native_help_and_effect_boundary(view):
    call = view.addons.molsysmt.build.add_ions
    native = inspect.signature(msm.build.add_ions)
    assert inspect.signature(call) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert call.digestion_plan is not None
    assert "add_ions" in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, "add_ions")
    assert "independent" in inspect.getdoc(call)
    for name in inspect.signature(call).parameters:
        assert f"{name} :" in inspect.getdoc(call)
    for parameter in ["molecular_system", "selection", "in_place", "update_view"]:
        with pytest.raises(UnknownArgumentError):
            call(**{parameter: None})


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("report", [False, True])
@pytest.mark.parametrize("pending", [False, True])
def test_native_result_maps_counts_and_pending_source_ownership(
    view, skip, report, pending
):
    if pending:
        view.addons.molsysmt.structure.translate(
            translation="[0.01,0,0] nm", in_place=True, update_view=False
        )
    before = snapshot(view)
    parameters = dict(
        n_cations=2,
        n_anions=1,
        random_seed=19,
        min_solute_distance="5 angstrom",
        min_ion_distance="5 angstrom",
        return_report=report,
        skip_digestion=skip,
    )
    expected = msm.build.add_ions(view.molsys, **parameters)
    result = view.addons.molsysmt.build.add_ions(**parameters)
    output = result["molecular_system"] if report else result
    native = expected["molecular_system"] if report else expected
    assert output is not native and output is not view.molsys
    assert msm.get(output, n_ions=True, n_waters=True, n_atoms=True) == [3, 265, 798]
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"),
        puw.get_value(native.structures.coordinates, to_unit="nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(output.structures.box, to_unit="nm"),
        puw.get_value(view.molsys.structures.box, to_unit="nm"),
    )
    if report:
        data = result["report"]
        assert data["added"] == dict(cation=2, anion=1, salt_pairs=0, total=3)
        assert data["random"]["seed"] == "19"
        assert data["parameters"]["min_ion_distance_nm"] == pytest.approx(
            0.5, rel=1e-14
        )
        reverse = data["output_to_source_atom_indices"]
        forward = data["source_to_output_atom_indices"]
        assert reverse.shape == (798,) and forward.shape == (804,)
        assert np.count_nonzero(forward == -1) == 9
        assert np.count_nonzero(reverse == -1) == 3
        retained = reverse[reverse >= 0]
        np.testing.assert_array_equal(forward[retained], np.arange(retained.size))
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm")[
                0, : retained.size
            ],
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
                0, retained
            ],
        )
    unchanged(view, before)


@pytest.mark.parametrize(
    "parameters",
    [
        {"n_cations": -1},
        {"cation": "unknown"},
        {"min_ion_distance": "1 ps"},
        {"random_seed": -1},
        {"max_attempts": 0},
        {"charge_source": "unknown"},
    ],
)
def test_native_errors_and_units_are_not_repaired(view, parameters):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.add_ions(view.molsys, **parameters)
    with pytest.raises(type(native.value)) as observed:
        view.addons.molsysmt.build.add_ions(**parameters)
    assert str(observed.value) == str(native.value)
    unchanged(view, before)


def test_zero_counts_still_return_an_independent_result(view):
    before = snapshot(view)
    result = view.addons.molsysmt.build.add_ions(random_seed=3)
    assert result is not view.molsys
    assert result.get_n_atoms() == view.molsys.get_n_atoms()
    unchanged(view, before)


def test_neutralization_requires_explicit_charge_and_returns_native_evidence(view):
    before = snapshot(view)
    result = view.addons.molsysmt.build.add_ions(
        n_cations="neutralize",
        expected_total_charge=-2,
        random_seed=3,
        return_report=True,
    )
    assert result["report"]["added"]["cation"] == 2
    assert result["report"]["charge"]["total_elementary_charge"] == -2
    assert result["report"]["charge"]["output_total_elementary_charge"] == 0
    unchanged(view, before)


def test_cached_call_rebinds_and_rejects_empty_or_closed_views(view):
    call = view.addons.molsysmt.build.add_ions
    replacement = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))
    view.load(replacement, mode="replace")
    before = snapshot(view)
    result = call(n_cations=1, random_seed=1)
    assert msm.get(result, n_ions=True) == 1
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.add_ions()
