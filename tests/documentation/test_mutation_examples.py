"""Execute each course mutation block against a local molecular system."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "domain,sequence,ids,expected",
    [
        ("Alzheimer", "PheValPro", ["1", "2", "3"], ["ALA", "VAL", "PRO"]),
        ("Antiviral", "AlaHisPro", ["1", "163", "3"], ["ALA", "GLY", "PRO"]),
        ("Biophysics", "ValValPro", ["76", "76", "3"], ["ILE", "ILE", "PRO"]),
        ("Enzyme", "AlaSerPro", ["238", "289", "3"], ["CYS", "CYS", "PRO"]),
    ],
)
def test_course_mutation_block_captures_independent_result(
    domain, sequence, ids, expected
):
    source = msm.build.build_peptide(sequence)
    source.topology.groups["group_id"] = ids
    original = source.copy()
    path = ROOT / f"docs/content/course/Path_{domain}/23_Structural_Repair.ipynb"
    blocks = [
        "".join(cell["source"])
        for cell in json.loads(path.read_text())["cells"]
        if cell["cell_type"] == "code" and "msm.build.mutate" in "".join(cell["source"])
    ]
    assert len(blocks) == 1
    namespace = {"msm": msm, "molsys": source}
    exec(compile(blocks[0], str(path), "exec"), namespace)
    result = namespace["molsys"]
    assert result is not source
    assert result.topology.groups["group_name"].tolist() == expected
    pd.testing.assert_frame_equal(source.topology.groups, original.topology.groups)
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(original.structures.coordinates, to_unit="nm"),
    )
