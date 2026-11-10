"""Human-facing demo atom counts must agree with the actual shipped inventory."""

import json
import re
from importlib.resources import files

import molsysmt as msm


def test_alanine_catalog_and_manifest_match_public_inventory():
    filename = "alanine_dipeptide.h5msm"
    observed = msm.get(msm.systems["alanine dipeptide"][filename], n_atoms=True)
    manifest = json.loads(
        files("molsysmt.data").joinpath("demo_manifest.json").read_text()
    )
    entry = next(item for item in manifest["artifacts"] if item["file"] == filename)
    assert (
        observed == entry["expected"][manifest["expected_order"].index("atoms")] == 22
    )
    info = msm.systems.info["alanine dipeptide"]
    for description in [info["summary"], info["files"][filename]]:
        declared = re.findall(r"\b(\d+)\s+(?:heavy/hydrogen\s+)?atoms\b", description)
        assert declared and all(int(value) == observed for value in declared), (
            description
        )
