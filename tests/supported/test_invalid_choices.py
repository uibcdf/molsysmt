"""Check errors for invalid supported-capability filters."""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError


@pytest.mark.parametrize(
    ("call", "argument"),
    [
        (lambda: msm.supported.forms(form_type="unknown"), "form_type"),
        (
            lambda: msm.supported.conversions(from_form_type="unknown"),
            "from_form_type",
        ),
    ],
)
def test_invalid_filter_reports_argument_choice(call, argument):
    """An invalid filter raises the catalog exception for that argument."""
    with pytest.raises(ArgumentChoiceError, match=argument):
        call()
