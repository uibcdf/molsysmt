"""Report reference names using per-group source declarations, without repair."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Topology


@pytest.mark.parametrize("container", ["native", "dict", "h5msm"])
def test_reference_report_preserves_mixed_meanings_and_original_indices(
    container, tmp_path
):
    topology = Topology(n_groups=6)
    topology.groups["group_name"] = ["GLH", "GLH", "HID", "HID", "HOH", "ALA"]
    topology.set_group_naming_schemes(["amber", "legacy", "amber", "ccd", None, None])
    before = topology.groups.copy()
    source = topology
    if container == "dict":
        source = msm.convert(topology, to_form="molsysmt.TopologyDict")
    elif container == "h5msm":
        source = msm.convert(topology, to_form=str(tmp_path / "names.h5msm"))
    assert msm.build.get_non_standard_residues(source, selection=[3, 2, 1, 0]) == {
        2: "HIS",
        1: "GLN",
        0: "GLU",
    }
    pd.testing.assert_frame_equal(before, topology.groups, check_frame_type=False)
    assert topology.n_atoms == 0


def test_reference_report_refuses_undeclared_ambiguous_label():
    topology = Topology(n_groups=1)
    topology.groups["group_name"] = ["HID"]
    with pytest.raises(ArgumentError) as error:
        msm.build.get_non_standard_residues(topology)
    assert error.value.extra["argument"] == "naming_scheme"
