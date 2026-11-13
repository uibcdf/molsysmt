"""Reject false retirement and mixed-kernel evidence in the fixed workload."""

import json

import pytest

from tests.molsysviewer_molsysmt.jupyter_receiving_guard import (
    _assert_prolonged_memory_result,
)


@pytest.fixture
def memory_receipt(tmp_path):
    records = []
    native = []
    modules = {
        "molsysmt": {"origin": str(tmp_path / "molsysmt/__init__.py")},
        "molsysviewer": {"origin": str(tmp_path / "molsysviewer/__init__.py")},
        "molsysmt._rust": {"loaded": True},
        "molsysviewer_molsysmt": {"loaded": True},
    }
    for cycle in (1, 2):
        rows = []
        for label, witness, atoms, size in (
            ("witness", True, 3983, 47796),
            (f"cycle-{cycle}-created", False, 62, 3720000),
            (f"cycle-{cycle}-recovered", False, 62, 3720000),
        ):
            rows.append(
                {
                    "label": label,
                    "witness": witness,
                    "atoms": atoms,
                    "targets": dict.fromkeys(
                        ("controller", "structure", "model", "x", "y", "z"), witness
                    ),
                    "buffers": [{"bytes": size, "alive": witness}],
                }
            )
        records.append(
            {
                "cycle": cycle,
                "controls": {"started_hidden": True, "next_focused": True},
                "activity": {"distinct_frames": 2, "seconds": 10.1},
                "retirement_memory": {
                    "cdp_collections": 2,
                    "after_collection": {
                        "subjects": {"witness_data_unchanged": True, "rows": rows}
                    },
                },
            }
        )
        native.append(
            {
                "cycle": cycle,
                "kernel_identity": "one-kernel",
                "kernel_pid": 101,
                "kernel_birth": 12.3,
                "open_views": 1,
                "interaction_occurrences": 8,
            }
        )
        (tmp_path / f"kernel-molecular-imports-after-cycle-{cycle}.json").write_text(
            json.dumps({"modules": modules})
        )
    (tmp_path / "kernel-molecular-imports.json").write_text(
        json.dumps({"modules": modules})
    )
    return tmp_path, {
        "cycles": 2,
        "active_seconds_per_cycle": 10,
        "records": records,
        "native": native,
    }


def _receive(output, result):
    (output / "full-result.json").write_text(json.dumps(result))
    _assert_prolonged_memory_result(
        output, cycles=2, active_seconds=10, source=output, viewer=output
    )


def test_independent_witness_and_retired_subject_receipt_passes(memory_receipt):
    _receive(*memory_receipt)


@pytest.mark.parametrize(
    "fault",
    [
        "witness_lost",
        "retired_controller_held",
        "retired_buffer_held",
        "wrong_buffer_size",
        "missing_target",
        "mixed_kernel",
        "incomplete_cycles",
        "no_scientific_occurrences",
    ],
)
def test_false_or_incomplete_retirement_evidence_is_rejected(memory_receipt, fault):
    output, result = memory_receipt
    rows = result["records"][0]["retirement_memory"]["after_collection"]["subjects"][
        "rows"
    ]
    if fault == "witness_lost":
        rows[0]["targets"]["controller"] = False
    elif fault == "retired_controller_held":
        rows[1]["targets"]["controller"] = True
    elif fault == "retired_buffer_held":
        rows[2]["buffers"][0]["alive"] = True
    elif fault == "wrong_buffer_size":
        rows[1]["buffers"][0]["bytes"] = 0
    elif fault == "missing_target":
        del rows[1]["targets"]["x"]
    elif fault == "mixed_kernel":
        result["native"][1]["kernel_birth"] = 99.0
    elif fault == "incomplete_cycles":
        result["records"].pop()
    else:
        result["native"][0]["interaction_occurrences"] = 0
    with pytest.raises(AssertionError):
        _receive(output, result)
