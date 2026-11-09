"""Keep clustering decisions independent of output-unit standardization."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.argdigest.argument.cutoff_distance import digest_cutoff_distance
from molsysmt.native import MolecularMechanics

puw = msm.pyunitwizard
POLICIES = [("nm", "ps"), ("pm", "fs"), ("angstrom", "ps")]
METHODS = ["complete_linkage", "single_linkage"]
CALLER = "molsysmt.structure.get_distance_clusters.get_distance_clusters"


def chain():
    return puw.quantity([[0.0, 1.0, 2.0], [1.0, 0.0, 1.0], [2.0, 1.0, 0.0]], "nm")


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("policy", POLICIES)
@pytest.mark.parametrize("as_string", [False, True])
@pytest.mark.parametrize("boundary", ["below", "equal", "above"])
def test_exact_and_adjacent_cutoffs_ignore_output_policy(
    method, policy, as_string, boundary
):
    value = {
        "below": np.nextafter(1.0, 0.0),
        "equal": 1.0,
        "above": np.nextafter(1.0, np.inf),
    }[boundary]
    cutoff = f"{float(value)!r} nm" if as_string else puw.quantity(float(value), "nm")
    matrix = chain()
    before = puw.get_value(matrix).copy()
    caller_policy = deepcopy(puw.configure.report())
    with puw.context(standard_units=list(policy)):
        active = deepcopy(puw.configure.report())
        result = msm.structure.get_distance_clusters(matrix, cutoff, method=method)
        expected = (
            [0, 1, 2]
            if boundary == "below"
            else ([0, 0, 1] if method == "complete_linkage" else [0, 0, 0])
        )
        assert result["cluster_indices"].tolist() == expected
        assert result["inequality"] == "<="
        # Presentation still follows the caller, without entering the comparison.
        assert puw.get_unit(result["cutoff_distance"]) == puw.unit(policy[0])
        assert puw.get_unit(result["cluster_diameters"]) == puw.unit(policy[0])
        assert puw.configure.report() == active
    assert puw.configure.report() == caller_policy
    np.testing.assert_array_equal(puw.get_value(matrix), before)
    if not as_string:
        assert float(puw.get_value(cutoff)) == float(value)
        assert puw.get_unit(cutoff) == puw.unit("nm")


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("matrix_unit", ["nm", "pm", "angstrom"])
@pytest.mark.parametrize("cutoff_unit", ["nm", "pm", "angstrom"])
@pytest.mark.parametrize("as_string", [False, True])
def test_explicit_input_units_keep_their_decision_across_output_policies(
    method, matrix_unit, cutoff_unit, as_string
):
    # These quantities are fixed before entering any output policy. Different
    # caller conversion histories may yield different canonical float64 values;
    # the invariant here is that presentation cannot alter each supplied input.
    matrix = puw.convert(chain(), to_unit=matrix_unit)
    cutoff = puw.convert(puw.quantity(1.0, "nm"), to_unit=cutoff_unit)
    if as_string:
        cutoff = f"{float(puw.get_value(cutoff))!r} {cutoff_unit}"
    before = puw.get_value(matrix).copy()
    results = []
    for policy in POLICIES:
        with puw.context(standard_units=list(policy)):
            results.append(
                msm.structure.get_distance_clusters(matrix, cutoff, method=method)
            )
    for result in results[1:]:
        np.testing.assert_array_equal(
            result["cluster_indices"], results[0]["cluster_indices"]
        )
        np.testing.assert_array_equal(
            result["representative_indices"], results[0]["representative_indices"]
        )
        assert result["matrix_sha256"] == results[0]["matrix_sha256"]
    np.testing.assert_array_equal(puw.get_value(matrix), before)


def test_cutoff_validation_preserves_clustering_values_but_other_consumers_still_standardize():
    cutoff = puw.quantity(1.0, "nm")
    mechanics = MolecularMechanics()
    with puw.context(standard_units=["pm", "fs"]):
        compared = digest_cutoff_distance(cutoff, caller=CALLER)
        assert float(puw.get_value(compared)) == 1.0
        assert puw.get_unit(compared) == puw.unit("nm")
        msm.set(mechanics, cutoff_distance=cutoff)
        assert puw.get_unit(mechanics.cutoff_distance) == puw.unit("pm")
        assert puw.get_value(mechanics.cutoff_distance) == pytest.approx(1000.0)
    assert digest_cutoff_distance(True, caller="molsysmt.basic.get.get") is True
