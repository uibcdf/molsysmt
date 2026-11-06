"""Checking reproducibility and bounded meaning of the bundled name reference."""

import json
from hashlib import sha256
from importlib.resources import files

import pytest

from molsysmt.data._make import make_pdb_hydrogen_aliases as generator


def test_exact_primary_bytes_regenerate_the_packaged_subset_offline():
    source = files("molsysmt.data._make").joinpath("pdb_names/pdbNames.xml")
    data = files("molsysmt.data.databases.amino_acids").joinpath(
        "pdb_hydrogen_aliases.json"
    )
    assert sha256(source.read_bytes()).hexdigest() == generator.SOURCE_SHA256
    assert generator.derive(source) == json.loads(data.read_text())


def test_resource_contains_hydrogen_aliases_not_chemical_group_replacements():
    data = json.loads(
        files("molsysmt.data.databases.amino_acids")
        .joinpath("pdb_hydrogen_aliases.json")
        .read_text()
    )
    assert set(data["groups"]) == set(generator.GROUPS)
    assert "HID" not in data["groups"] and "MSE" not in data["groups"]
    assert data["common"]["HN1"] == "H" and data["groups"]["HIS"]["HB1"] == "HB3"
    assert all(
        value.startswith("H")
        for mapping in [data["common"], *data["groups"].values()]
        for value in mapping.values()
    )
    assert "O1" not in data["common"]
    assert (
        files("molsysmt.data.databases.amino_acids")
        .joinpath(data["source"]["license_file"])
        .is_file()
    )


def test_unreviewed_input_bytes_are_rejected_before_parsing(tmp_path):
    source = tmp_path / "changed.xml"
    source.write_text("<Residues/>")
    with pytest.raises(ValueError, match="reviewed source"):
        generator.derive(source)
