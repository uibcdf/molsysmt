"""Shared guards for interaction calculations with projected H5MSM geometry."""

import pytest


@pytest.fixture
def forbid_eager_h5msm_reads(monkeypatch):
    """Reject full coordinate or analysis reads while allowing block delivery."""
    from molsysmt.form import _h5msm05_modular

    def reject(*args, **kwargs):
        pytest.fail(
            "Bounded detection must not materialize coordinates or saved analyses."
        )

    for name in (
        "read_molsys_file",
        "read_independent_structures",
        "read_named_analyses",
    ):
        monkeypatch.setattr(_h5msm05_modular, name, reject)
