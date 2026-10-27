"""Protecting per-result method references from shared declaration mutation."""

import json
from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm

READERS = [
    ("hydrophobic", msm.physchem.get_hydrophobic_sites, "CCC", {}),
    ("halogen", msm.physchem.get_halogen_bond_sites, "CCl.C=O", {}),
    ("metal", msm.physchem.get_metal_coordination_sites, "[Zn+2].O", {}),
    (
        "hbond",
        msm.interactions.hbonds.get_hbond_sites,
        "N.CO",
        {"method": "smarts_donor_acceptor"},
    ),
]


@pytest.mark.parametrize(
    "label,reader,smiles,options", READERS, ids=[row[0] for row in READERS]
)
@pytest.mark.parametrize("selection", ["all", []], ids=["positive", "empty"])
def test_method_references_are_owned_by_each_result(
    monkeypatch, label, reader, smiles, options, selection
):
    from rdkit import Chem

    from molsysmt.physchem import _prolif

    # A private declaration copy keeps this intentionally mutating regression
    # isolated even with the original broken implementation.
    canonical = deepcopy(_prolif.PROLIF_REFERENCE)
    canonical["review"] = {"sources": ["pinned reference"]}
    declaration = deepcopy(canonical)
    monkeypatch.setattr(_prolif, "PROLIF_REFERENCE", declaration)
    source = Chem.MolFromSmiles(smiles)
    earlier = reader(source, selection=selection, **options)
    edited = reader(source, selection=selection, **options)
    expected = deepcopy(earlier)
    edited["method_reference"]["version"] = "user-edited"
    edited["method_reference"]["review"]["sources"].append("user-added")
    later = reader(source, selection=selection, **options)
    other = (
        msm.physchem.get_halogen_bond_sites(Chem.MolFromSmiles("CCl.C=O"))
        if label != "halogen"
        else msm.physchem.get_hydrophobic_sites(Chem.MolFromSmiles("CCC"))
    )

    assert declaration == canonical
    for result in (earlier, later, other):
        assert result["method_reference"] == canonical
        assert result["method_reference"] is not declaration
        assert result["method_reference"] is not edited["method_reference"]
    # Bibliography and numerical results remain independently unchanged.
    assert earlier["attribution"] == expected["attribution"]
    assert later["attribution"] == expected["attribution"]
    assert json.loads(json.dumps(later["method_reference"])) == canonical
    for key, value in expected.items():
        if isinstance(value, np.ndarray):
            np.testing.assert_array_equal(earlier[key], value)
            np.testing.assert_array_equal(later[key], value)
            np.testing.assert_array_equal(edited[key], value)
