"""The canonical hydrogen-bond namespace preserves the existing methods."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotImplementedMethodError


def test_hbonds_namespace_preserves_legacy_function_identity(hp35_molsys):
    canonical = msm.interactions.hbonds
    legacy = msm.hbonds

    assert canonical.get_acceptor_atoms is legacy.get_acceptor_atoms
    assert canonical.get_donor_atoms is legacy.get_donor_atoms
    assert canonical.get_buch_hbonds is legacy.get_buch_hbonds
    assert canonical.get_luzard_chandler_hbonds is legacy.get_luzard_chandler_hbonds

    triples, distances = canonical.get_buch_hbonds(hp35_molsys)
    assert triples.shape[0] == 1
    assert triples.shape[2] == 3
    assert distances.shape == (1, len(triples[0]))


@pytest.mark.parametrize(
    "method_name", ["get_buch_hbonds", "get_luzard_chandler_hbonds"]
)
def test_second_system_is_rejected_visibly(hp35_molsys, method_name):
    method = getattr(msm.interactions.hbonds, method_name)
    with pytest.raises(NotImplementedMethodError):
        method(hp35_molsys, molecular_system_2=hp35_molsys)


@pytest.mark.parametrize(
    "method_name", ["get_buch_hbonds", "get_luzard_chandler_hbonds"]
)
def test_empty_selection_has_an_evaluated_structure(hp35_molsys, method_name):
    method = getattr(msm.interactions.hbonds, method_name)
    atoms, *measurements = method(hp35_molsys, selection=[0])
    assert atoms.shape == (1, 0, 3)
    assert all(measurement.shape == (1, 0) for measurement in measurements)


@pytest.mark.parametrize(
    "method_name", ["get_buch_hbonds", "get_luzard_chandler_hbonds"]
)
def test_new_output_options_preserve_legacy_positional_calls(hp35_molsys, method_name):
    method = getattr(msm.interactions.hbonds, method_name)
    common = [hp35_molsys, "all", None, None, "all", None, None, None, None, None]
    if method_name == "get_buch_hbonds":
        arguments = common + ["2.3 angstroms", False, "MolSysMT", False]
    else:
        arguments = common + ["3.5 angstroms", "30 degrees", False, "MolSysMT"]
    actual = method(*arguments)
    expected = method(hp35_molsys, pbc=False)
    np.testing.assert_array_equal(actual[0], expected[0])
    for observed, reference in zip(actual[1:], expected[1:]):
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(observed), msm.pyunitwizard.get_value(reference)
        )
