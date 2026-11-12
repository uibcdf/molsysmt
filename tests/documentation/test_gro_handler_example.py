"""Check actual GRO documentation workflows and advertised operation availability."""

import hashlib
import importlib
import io
import json
import re
from contextlib import closing
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    NotImplementedIteratorError,
    NotImplementedMethodError,
    NotWithThisFormError,
)
from molsysmt.native import GROFileHandler

ROOT = Path(__file__).resolve().parents[2]
PAGE = (
    ROOT
    / "docs/content/user/foundations/native_world/file_handlers/molsysmt_GROFileHandler.md"
)
TUTORIAL = (
    ROOT / "docs/content/user/tools/form/class/molsysmt/molsysmt_GROFileHandler.ipynb"
)
GRO_TEXT = (
    "Local water\n"
    "    3\n"
    "    7HOH      O   17   0.100   0.200   0.300\n"
    "    7HOH     H1    3   0.195   0.200   0.300\n"
    "    7HOH     H2   45   0.076   0.292   0.300\n"
    "   2.00000   3.00000   4.00000\n"
)


@pytest.mark.parametrize(
    "operation", ["extract", "add", "merge", "append_structures", "iterators", "set"]
)
def test_tutorial_operation_limits_match_actual_adapter(operation):
    tutorial = json.loads(TUTORIAL.read_text())
    operations = "".join(tutorial["cells"][3]["source"])
    marker = f"molsysmt_GROFileHandler.{operation}"
    rows = [
        line
        for line in operations.splitlines()
        if line.startswith("|") and marker in line
    ]
    assert len(rows) == 1
    description = rows[0].split("|")[2].strip()
    adapter = importlib.import_module("molsysmt.form.molsysmt_GROFileHandler")
    with closing(GROFileHandler(io.StringIO(GRO_TEXT))) as handler:
        before = handler.file.getvalue()
        if operation == "extract":
            with closing(msm.extract(handler)) as copied:
                assert copied is not handler and copied.file is not handler.file
            with pytest.raises(NotImplementedMethodError):
                msm.extract(handler, selection=[0])
            assert description.startswith("Whole-handler only:"), description
        elif operation == "iterators":
            for iterator_type in [adapter.StructuresIterator, adapter.TopologyIterator]:
                with pytest.raises(NotImplementedIteratorError):
                    next(iter(iterator_type(handler)))
            assert description.startswith("Unavailable:"), description
        elif operation == "set":
            with pytest.raises(NotWithThisFormError):
                msm.set(handler, coordinates=handler.entry.coordinates)
            assert description.startswith("Unavailable:"), description
        else:
            with pytest.raises(NotImplementedMethodError):
                if operation == "add":
                    adapter.add(handler, handler)
                elif operation == "merge":
                    adapter.merge([handler, handler])
                else:
                    adapter.append_structures(
                        handler, coordinates=handler.entry.coordinates
                    )
            assert description.startswith("Unavailable:"), description
        assert not handler.file.closed and handler.file.getvalue() == before


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_bundled_gro_example_keeps_copy_units_and_deposited_coordinates(
    length_unit, time_unit
):
    blocks = re.findall(r"```python\n(.*?)\n```", PAGE.read_text(), re.S)
    assert len(blocks) == 1
    path = Path(msm.systems["nglview"]["md_1u19.gro"])
    original = path.read_bytes()
    lines = original.decode().splitlines()
    expected = np.array(
        [
            [float(line[start : start + 8]) for start in (20, 28, 36)]
            for line in lines[2:4]
        ]
    )
    namespace = {}
    puw = msm.pyunitwizard
    try:
        with puw.context(
            standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
        ):
            exec(compile(blocks[0], str(PAGE), "exec"), namespace)
            handler, copied = namespace["handler"], namespace["copied"]
            coordinates = namespace["coordinates"]
            assert handler.file.closed and copied.file.closed
            assert (
                isinstance(handler.file, io.StringIO)
                and copied.file is not handler.file
            )
            assert handler.entry is not copied.entry
            assert (
                handler.entry.n_atoms == copied.entry.n_atoms == int(lines[1]) == 5547
            )
            assert puw.get_unit(handler.entry.coordinates) == puw.unit("nm")
            assert coordinates.shape == (1, 2, 3)
            assert puw.get_unit(coordinates) == puw.unit(length_unit)
            np.testing.assert_allclose(
                puw.get_value(coordinates, to_unit="nm")[0],
                expected,
                rtol=1e-12,
                atol=1e-12,
            )
            assert not np.shares_memory(
                puw.get_value(handler.entry.coordinates),
                puw.get_value(copied.entry.coordinates),
            )
    finally:
        for name in ["handler", "copied"]:
            if name in namespace:
                namespace[name].close()
    assert (
        hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(original).digest()
    )
