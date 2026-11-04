"""Distinguish code alphabets, chemical dictionaries and force-field labels."""

import copy
import json
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError

ALPHABET = dict(
    zip(
        "ALA ARG ASN ASP CYS GLU GLN GLY HIS ILE LEU LYS MET PHE PRO PYL SER SEC THR TRP TYR VAL ASX GLX XAA XLE".split(),
        "ARNDCEQGHILKMFPOSUTWYVBZXJ",
        strict=True,
    )
)
STATES = {
    "GLH": "E",
    "HID": "H",
    "HIE": "H",
    "HIP": "H",
    "ASH": "D",
    "CYM": "C",
    "CYX": "C",
    "LYN": "K",
}
MODIFIED = {"MSE": "M", "SEP": "S", "TPO": "T", "PTR": "Y"}


def code(name, scheme=None, **kwargs):
    return msm.element.group.get_1_letter_code_from_name(
        name, naming_scheme=scheme, **kwargs
    )


@pytest.mark.parametrize("name,letter", ALPHABET.items())
@pytest.mark.parametrize("scheme", ["sequence", "legacy"])
def test_explicit_alphabets_preserve_all_twenty_six_symbols(name, letter, scheme):
    assert code(name, scheme) == letter


@pytest.mark.parametrize(
    "name,letter",
    [(name, letter) for name, letter in ALPHABET.items() if name not in {"XAA", "XLE"}],
)
def test_reviewed_unambiguous_alphabet_needs_no_source_override(name, letter):
    assert code(name) == letter


@pytest.mark.parametrize("name,letter", STATES.items())
def test_primary_amber_state_projections(name, letter):
    assert code(name, "amber") == letter


@pytest.mark.parametrize("name", [*STATES, "XAA", "XLE"])
def test_context_dependent_names_never_silently_choose_a_profile(name):
    with pytest.raises(ArgumentError) as refusal:
        code(name)
    assert refusal.value.extra["argument"] == "naming_scheme"
    assert "naming" in str(refusal.value)


@pytest.mark.parametrize("name", ["HID", "CYX", "ASH", "XAA", "XLE", "HOH"])
def test_reviewed_non_peptide_ccd_components_have_no_amino_acid_projection(name):
    with pytest.raises(ArgumentError, match="no supported amino-acid") as refusal:
        code(name, "ccd")
    assert refusal.value.extra["argument"] == "name"


@pytest.mark.parametrize("name", ["GLH", "HIE", "CYM"])
def test_unverified_ccd_names_do_not_fall_back_to_amber_or_legacy(name):
    with pytest.raises(ArgumentError, match="bounded 'ccd'"):
        code(name, "ccd")


@pytest.mark.parametrize("name,letter", MODIFIED.items())
@pytest.mark.parametrize("scheme", [None, "ccd", "legacy"])
def test_reviewed_modified_parent_projection_matches_primary_ccd(name, letter, scheme):
    assert code(name, scheme) == letter


@pytest.mark.parametrize(
    "name,letter",
    [("GLH", "Q"), ("ASH", "D"), ("HIP", "H"), ("CYM", "C"), ("LYN", "K")],
)
def test_legacy_remains_explicit_historical_compatibility(name, letter):
    assert code(name, "legacy") == letter


@pytest.mark.parametrize(
    "name,scheme",
    [
        ("GLH", "sequence"),
        ("MSE", "amber"),
        ("SEP", "sequence"),
        ("HID", "legacy"),
        ("CYX", "legacy"),
    ],
)
def test_explicit_profile_never_uses_another_profiles_names(name, scheme):
    with pytest.raises(ArgumentError, match="No fallback"):
        code(name, scheme)


@pytest.mark.parametrize(
    "scheme", ["AMBER", "pdb", "", 1, False, [], np.array(["ccd"])]
)
def test_invalid_schemes_are_catalogued_at_the_public_boundary(scheme):
    with pytest.raises(ArgumentChoiceError) as refusal:
        code("ALA", scheme)
    assert refusal.value.extra["argument"] == "naming_scheme"
    assert refusal.value.extra["caller"].endswith("get_1_letter_code_from_name")


@pytest.mark.parametrize("name", [None, "", 1, False, [], {}, np.array("ALA")])
def test_invalid_scalar_names_are_rejected_before_interpretation(name):
    with pytest.raises(ArgumentError) as refusal:
        code(name, "sequence")
    assert refusal.value.extra["argument"] == "name"


def test_lookup_preserves_the_authoritative_alphabet_and_legacy_mapping():
    from molsysmt.element.group.amino_acid.codes import aa3_to_aa1
    from molsysmt.element.group.amino_acid.group_types import name_to_type

    before = copy.deepcopy((aa3_to_aa1, name_to_type))
    assert code("GLH", "amber") != code("GLH", "legacy")
    assert (aa3_to_aa1, name_to_type) == before


def test_real_attribution_preserves_reused_references_in_enclosing_captures():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("naming workflow"):
        with ackredit.capture("first") as first:
            assert code("GLH", "amber") == "E"
        with ackredit.capture("second") as second:
            assert code("GLH", "amber") == "E"
        first_ids = {item["id"] for item in first.attribution.to_dict()["items"]}
        second_ids = {item["id"] for item in second.attribution.to_dict()["items"]}
        assert first_ids == second_ids
        assert "ddbj-amino-acid-code-alphabet" in first_ids
        assert any(
            identifier.startswith("molsysmt-group-names:amber:")
            for identifier in first_ids
        )
        assert not any("rcsb" in identifier for identifier in first_ids)
    with ackredit.session("refused projection"):
        with pytest.raises(ArgumentError):
            code("XLE", "ccd")
        assert not ackredit.get_used_items()


def test_optional_attribution_absence_and_failure_do_not_change_letters(monkeypatch):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    assert code("HID", "amber") == "H"

    def broken():
        raise RuntimeError("controlled optional-provider failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert code("HID", "amber") == "H"


def test_importing_the_new_public_helper_does_not_import_ackredit():
    script = "from molsysmt.element.group import get_1_letter_code_from_name; import sys; assert 'ackredit' not in sys.modules; assert 'molsysmt._private.name_resolution' not in sys.modules"
    subprocess.run(
        [sys.executable, "-c", script], check=True, capture_output=True, text=True
    )


def test_profile_asset_regenerates_from_reviewed_receipt():
    root = Path(__file__).resolve().parents[3]
    subprocess.run(
        [
            sys.executable,
            str(root / "molsysmt/data/_make/make_group_name_profiles.py"),
            "--check",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    review = json.loads(
        (
            root / "devtools/data/name_scheme_profile_review_549_20261104.json"
        ).read_text()
    )
    assert {row["code"] for row in review["records"] if row.get("status") == 404} == {
        "GLH",
        "HIE",
        "CYM",
    }
