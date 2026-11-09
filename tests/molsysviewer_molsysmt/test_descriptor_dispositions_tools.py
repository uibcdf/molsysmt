"""Receive the bounded Collantes dispositions without certifying their science."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize("pending", [False, True])
@pytest.mark.parametrize(
    "policy", [["nm", "ps", "elementary_charge"], ["pm", "fs", "coulomb"]]
)
def test_provisional_isa_and_eci_preserve_explicit_limits_units_and_read_ownership(
    pending, policy
):
    puw = msm.pyunitwizard
    with msv.demo["pentalanine"] as view:
        tools = view.addons.molsysmt
        if pending:
            tools.structure.translate(
                translation="[1, 0, 0] angstrom", in_place=True, update_view=False
            )
        before = puw.get_value(
            msm.get(view.molsys, coordinates=True), to_unit="nm"
        ).copy()
        status = tools.get_sync_status()
        messages = list(view.widget.initial_messages)
        area_help = inspect.getdoc(tools.physchem.get_surface_area).lower()
        charge_help = inspect.getdoc(tools.physchem.get_charge).lower()
        assert "provisional" in area_help and "473" in area_help
        assert "not a conformational sasa measurement" in area_help
        assert "electronic charge index" in charge_help and "475" in charge_help
        assert (
            "unverified" in charge_help
            and "without physical certification" in charge_help
        )
        with puw.context(standard_units=policy):
            kwargs = {"element": "group", "selection": "group_name=='ALA'"}
            area = tools.physchem.get_surface_area(**kwargs, definition="collantes")
            eci = tools.physchem.get_charge(**kwargs, definition="collantes")
            physical_reference = tools.physchem.get_charge(
                **kwargs, definition="physical_pH7"
            )
            # Compatibility/control values, not verification of the primary table,
            # original ISA units or a physical interpretation of ECI/additivity.
            np.testing.assert_allclose(
                puw.get_value(area, to_unit="angstrom**2"),
                np.full(5, 62.9),
                rtol=4 * np.finfo(float).eps,
                atol=0,
            )
            np.testing.assert_allclose(
                puw.get_value(area, to_unit="nm**2"),
                np.full(5, 0.629),
                rtol=4 * np.finfo(float).eps,
                atol=0,
            )
            np.testing.assert_allclose(
                puw.get_value(eci, to_unit="elementary_charge"),
                np.full(5, 0.05),
                rtol=4 * np.finfo(float).eps,
                atol=0,
            )
            np.testing.assert_array_equal(
                puw.get_value(physical_reference, to_unit="elementary_charge"),
                np.zeros(5),
            )
        assert tools.get_sync_status() == status
        assert view.widget.initial_messages == messages
        np.testing.assert_array_equal(
            puw.get_value(msm.get(view.molsys, coordinates=True), to_unit="nm"), before
        )
