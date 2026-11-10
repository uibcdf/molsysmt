"""Observed categorical assignments retain native source groups and units."""

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_analysis_panel import act, mount
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_system_panel import transport


@pytest.mark.parametrize("mode", ["simplified", "full"])
@pytest.mark.parametrize("units", ["nm", "pm"])
def test_categorical_group_structure_mapping_and_source_lifetime(mode, units):
    with msv.demo["pentalanine"] as seed:
        with msv.new_view(seed.molsys, structure_indices=[0, 8, 2]) as view:
            sent = transport(view)
            panel = mount(view)
            before = snapshot(view)
            atoms = [20, 10, 6, 20]
            groups = list(
                dict.fromkeys(
                    map(
                        int,
                        msm.get(
                            view.molsys,
                            element="atom",
                            selection=atoms,
                            group_index=True,
                        ),
                    )
                )
            )
            with msm.pyunitwizard.context(
                standard_units=[units, "ps", "Da", "K", "e", "radians"]
            ):
                packet = act(
                    view,
                    sent,
                    draft={
                        "source": "indices",
                        "indices": "20,10,6,20",
                        "context": "index",
                        "structure_index": 0,
                    },
                    parameters={
                        "task": "secondary_structure",
                        "secondary_mode": mode,
                        "structures": "indices",
                        "indices": "2,0,2",
                    },
                )
            assert packet["stage"] == "report", packet["message"]
            expected = msm.structure.get_secondary_structure(
                view.molsys,
                selection=groups,
                structure_indices=[2, 0, 2],
                simplified=mode == "simplified",
            )
            np.testing.assert_array_equal(panel._report.values, expected)
            assert packet["report"]["unit"] == ""
            assert packet["report"]["structure_indices"] == [2, 0, 2]
            assert packet["report"]["result_axis"] == "group"
            assert packet["report"]["software"]["mdtraj"]
            assert packet["page"]["rows"] == [
                [f, g, repr(str(expected[i, j]))]
                for i, f in enumerate([2, 0, 2])
                for j, g in enumerate(groups)
            ]
            assert (
                packet["report"]["color_unavailable"]
                and packet["report"]["selected_plot_unavailable"]
            )
            unchanged(view, before)
            assert act(view, sent, "clear")["report"] is None


def test_invalid_vocabulary_is_rejected_before_calculation():
    with msv.demo["pentalanine"] as view:
        sent = transport(view)
        panel = mount(view)
        packet = act(
            view,
            sent,
            parameters={"task": "secondary_structure", "secondary_mode": "invented"},
        )
        assert packet["stage"] == "error" and panel._report is None
