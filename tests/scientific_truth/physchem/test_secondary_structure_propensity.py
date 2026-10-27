"""Verifying the bounded reference-table claim against the audited original."""

import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "category,table",
    [
        ("alpha_helix", "alpha_helix_levitt"),
        ("beta_sheet", "beta_sheet_levitt"),
        ("reverse_turn", "beta_turn_levitt"),
    ],
)
def test_levitt_detailed_primary_tables_match_all_standard_groups(category, table):
    # Independent visual transcription of P_ij, Tables III–V (not summary II).
    # Original DOI 10.1021/bi00613a026; immutable source PDF hash is in receipt.
    receipt = json.loads(
        (
            Path(__file__).parents[3]
            / "devtools/data/secondary_structure_propensity_review_20261026.json"
        ).read_text()
    )["levitt_primary"]
    builder = msm.MolSysBuilder()
    for name in receipt["amino_acid_order"]:
        index = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([index], group_name=name)
    result = msm.physchem.get_secondary_structure_propensity(builder.build(), category)
    assert result.shape == (20,)
    np.testing.assert_allclose(
        result, receipt["independent_visual_transcription"][table], atol=1e-14, rtol=0
    )
