"""Human-facing demo atom counts must agree with the actual shipped inventory."""

import json
import re
from importlib.resources import files

import h5py
import numpy as np
import pytest

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


@pytest.mark.parametrize("filename", ["1l2y.pdb", "1l2y.h5msm"])
def test_trpcage_catalog_structure_counts_match_bundled_sources(filename):
    path = msm.systems["Trp-Cage"][filename]
    if filename.endswith(".pdb"):
        with open(path) as source:
            observed = sum(line.startswith("MODEL ") for line in source)
    else:
        with h5py.File(path, "r") as source:
            observed = source["structures/coordinates"].shape[0]
    assert observed == msm.get(path, n_structures=True) == 38
    description = msm.systems.info["Trp-Cage"]["files"][filename]
    declared = re.findall(r"\b(\d+)[ -](?:models?|structures?|frames?)\b", description)
    assert declared and all(int(value) == observed for value in declared), description


def test_cellulase_catalog_identity_matches_deposited_compound_and_title():
    path = msm.systems["1CEN"]["1cen.pdb"]
    with open(path) as source:
        lines = list(source)
    compound = next(line for line in lines if "MOLECULE:" in line)
    molecule = compound.split("MOLECULE:", 1)[1].split(";", 1)[0].strip()
    title = " ".join(line[10:].strip() for line in lines if line.startswith("TITLE "))
    assert molecule == "CELLULASE CELC" and "CELLOHEXAOSE" in title
    info = msm.systems.info["1CEN"]
    for description in [info["title"], info["summary"]]:
        assert molecule.casefold() in description.casefold(), description
        assert "cellohexaose" in description.casefold(), description


@pytest.mark.parametrize("filename", ["1l17.pdb", "1l17.h5msm"])
def test_1l17_catalog_variant_matches_deposited_sequence_labels(filename):
    path = msm.systems["T4 lysozyme L99A"][filename]
    if filename.endswith(".pdb"):
        with open(path) as source:
            lines = list(source)
        variant = next(line.split() for line in lines if line.startswith("SEQADV"))
        assert variant[2:5] == ["VAL", "A", "3"] and variant[7:9] == ["ILE", "3"]
        groups = {
            line[22:26].strip(): line[17:20].strip()
            for line in lines
            if line.startswith("ATOM  ") and line[21] == "A"
        }
    else:
        with h5py.File(path, "r") as source:
            ids = source["topology/groups/group_id"].asstr()[:]
            names = source["topology/groups/group_name"].asstr()[:]
            groups = dict(zip(ids, names, strict=True))
    # These are deposited group IDs, not zero-based native group indices.
    assert groups["3"] == "VAL" and groups["99"] == "LEU"
    description = msm.systems.info["T4 lysozyme L99A"]["files"][filename]
    assert "I3V" in description and "L99A" not in description, description


def test_villin_catalog_length_matches_deposited_sequence():
    path = msm.systems["chicken villin HP35"]["1vii.pdb"]
    with open(path) as source:
        lines = list(source)
    lengths = {int(line[13:17]) for line in lines if line.startswith("SEQRES")}
    groups = {(line[21], line[22:27]) for line in lines if line.startswith("ATOM  ")}
    assert lengths == {len(groups)} == {36}
    summary = msm.systems.info["chicken villin HP35"]["summary"]
    declared = re.findall(r"\b(\d+)[ -](?:residues?|amino[- ]acids?)\b", summary)
    assert declared and all(int(value) == len(groups) for value in declared), summary


def test_native_villin_snapshot_is_not_advertised_as_the_complete_series():
    filename = "traj_chicken_villin_HP35_solvated.h5msm"
    path = msm.systems["chicken villin HP35"][filename]
    with h5py.File(path, "r") as source:
        observed = source["structures/coordinates"].shape[0]
    assert observed == msm.get(path, n_structures=True) == 1
    description = msm.systems.info["chicken villin HP35"]["files"][filename]
    declared = re.findall(r"\b(\d+)[ -]structures?\b", description)
    assert declared and all(int(value) == observed for value in declared), description


def test_xyznpy_catalog_describes_the_shape_and_coordinate_records():
    filename = "traj_particles_4.xyznpy"
    path = msm.systems["particles 4"][filename]
    with open(path, "rb") as source:
        shape = tuple(np.load(source))
        coordinates = np.load(source)
        assert source.read() == b""
    assert shape == coordinates.shape == (3, 4, 3)
    description = msm.systems.info["particles 4"]["files"][filename]
    declared = re.findall(r"\b(\d+)\s+(?:consecutive\s+)?NPY records\b", description)
    assert declared and all(int(value) == 2 for value in declared), description


def test_large_pdb_catalog_atom_count_matches_records_without_conversion():
    path = msm.systems["4V4Z"]["4v4z_openmm.pdb"]
    with open(path) as source:
        observed = sum(line.startswith(("ATOM  ", "HETATM")) for line in source)
    summary = msm.systems.info["4V4Z"]["summary"]
    declared = re.findall(r"\b(\d[\d,]*) atoms\b", summary)
    assert observed == 149640
    assert declared and all(
        int(value.replace(",", "")) == observed for value in declared
    )


def test_caffeine_catalog_atom_count_matches_sdf_counts():
    filename = "caffeine.sdf"
    path = msm.systems["caffeine"][filename]
    with open(path) as source:
        lines = [next(source) for _ in range(4)]
    observed = int(lines[3][:3])
    description = msm.systems.info["caffeine"]["files"][filename]
    declared = re.findall(r"\b(\d+) atoms\b", description)
    assert observed == msm.get(path, n_atoms=True) == 24
    assert declared and all(int(value) == observed for value in declared)
