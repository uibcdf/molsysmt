"""Retaining the legacy ECI wrapper pending primary-reference review under #475."""

import json
from pathlib import Path

import numpy as np

import molsysmt as msm

LEGACY_ATOL = json.loads(
    (
        Path(__file__).parents[1] / "scientific_truth/evidence/tolerances.json"
    ).read_text()
)["float64_kernel_atol"]["atol"]


def _values(quantity, unit):
    return msm.pyunitwizard.get_value(quantity, to_unit=unit)


def test_collantes_legacy_values_and_sums_remain_unchanged():
    """Protect legacy output without certifying primary values, dimensions or sums."""

    builder = msm.MolSysBuilder()
    for group_name in ("ARG", "ASP", "ALA"):
        atom = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([atom], group_name=group_name)
    system = builder.build()

    observed_groups = msm.physchem.get_charge(
        system, element="group", definition="collantes"
    )
    observed_system = msm.physchem.get_charge(
        system, element="system", definition="collantes"
    )
    expected = np.array([1.69, 1.25, 0.05])

    np.testing.assert_allclose(
        _values(observed_groups, "elementary_charge"),
        expected,
        rtol=0.0,
        atol=LEGACY_ATOL,
    )
    np.testing.assert_allclose(
        _values(observed_system, "elementary_charge"),
        expected.sum(),
        rtol=0.0,
        atol=LEGACY_ATOL,
    )
