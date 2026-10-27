""" """

# Import package, test suite, and other packages as needed

import numpy as np
import pytest

import molsysmt as msm

# Distance between atoms in space and time


def test_get_surface_area_1():

    molsys = msm.convert(
        msm.systems["T4 lysozyme L99A"]["181l.h5msm"],
        selection='molecule_type=="protein"',
    )

    n_groups = msm.get(molsys, element="system", n_groups=True)
    grantham = msm.physchem.get_surface_area(molsys, definition="collantes")

    assert len(grantham) == n_groups


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "form", ["molsysmt.MolSys", "molsysmt.Topology", "molsysmt.MolSysDict"]
)
@pytest.mark.parametrize("selection", ["all", [0, 0], []])
def test_provisional_isa_quantity_preserves_table_scale_and_standard_units(
    length_unit, form, selection
):
    """Check the adopted convention and conversion, not the unread original paper."""
    builder = msm.MolSysBuilder()
    atom = builder.add_atom(atom_name="CA", atom_type="C")
    builder.add_group([atom], group_name="ALA")
    source = msm.convert(builder.build(), to_form=form)
    count = 1 if selection == "all" else len(selection)
    with msm.pyunitwizard.context(standard_units=[length_unit, "ps", "radians"]):
        result = msm.physchem.get_surface_area(source, selection=selection)
        assert msm.pyunitwizard.is_quantity(result)
        assert result.shape == (count,)
        assert (
            msm.pyunitwizard.get_unit(result) == msm.pyunitwizard.unit(length_unit) ** 2
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
            [62.9] * count,
            atol=1e-12,
            rtol=0,
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result, to_unit="nm**2"),
            [0.629] * count,
            atol=1e-12,
            rtol=0,
        )
