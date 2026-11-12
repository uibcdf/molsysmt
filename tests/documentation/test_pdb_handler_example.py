"""Executing the actual resident PDB-handler example against deposited coordinates."""

import hashlib
import io
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

PAGE = (
    Path(__file__).resolve().parents[2]
    / "docs/content/user/foundations/native_world/file_handlers/molsysmt_PDBFileHandler.md"
)


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_bundled_pdb_handler_example_preserves_coordinates_and_closes_buffer(
    length_unit, time_unit
):
    blocks = re.findall(r"```python\n(.*?)\n```", PAGE.read_text(), re.S)
    assert len(blocks) == 1
    source = Path(msm.systems["Trp-Cage"]["1l2y.pdb"])
    original = source.read_bytes()
    first_atom = next(
        line for line in original.decode().splitlines() if line.startswith("ATOM  ")
    )
    deposited = [float(first_atom[start : start + 8]) for start in (30, 38, 46)]
    namespace = {}
    puw = msm.pyunitwizard
    try:
        with puw.context(
            standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
        ):
            exec(compile(blocks[0], str(PAGE), "exec"), namespace)
            handler = namespace["handler"]
            parsed = namespace["parsed"]
            coordinates = namespace["coordinates"]
            assert isinstance(handler.file, io.StringIO) and handler.file.closed
            assert parsed is handler.content
            assert len(parsed.models) == 38
            assert len(parsed.models[0].atoms) == 304
            np.testing.assert_array_equal(
                parsed.models[0].atoms[0].coordinates, deposited
            )
            assert coordinates.shape == (1, 2, 3)
            assert puw.get_unit(coordinates) == puw.unit(length_unit)
            np.testing.assert_allclose(
                puw.get_value(coordinates, to_unit="angstrom")[0, 0],
                deposited,
                rtol=1e-12,
                atol=1e-12,
            )
    finally:
        if "handler" in namespace:
            namespace["handler"].close()
    assert (
        hashlib.sha256(source.read_bytes()).digest()
        == hashlib.sha256(original).digest()
    )
