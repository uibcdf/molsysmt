"""Exercise the styled default through both public query routes."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures, Topology


@pytest.mark.parametrize("kind", ["molsys", "topology", "structures"])
@pytest.mark.parametrize("native", [False, True])
def test_default_summary_renders_with_the_declared_styler_runtime(kind, native):
    if kind == "molsys":
        source = MolSys(n_atoms=2)
    elif kind == "topology":
        source = Topology(n_atoms=2)
    else:
        source = Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
        )
    result = source.info() if native else msm.info(source)
    assert result.data["n_atoms"].tolist() == [2]
    html = result.to_html()
    assert "<table" in html and 'class="dataframe"' in html
