import pytest
from pathlib import Path
from devtools.scripts.validate_public_api_stability import (
    validate_api_stability,
    compare_signatures,
)


def test_compare_signatures_detects_parameter_inserted_in_middle():
    old_sig = {
        "pos_args": ["a", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a", "b", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Positional parameters altered" in d for d in diffs)


def test_compare_signatures_detects_default_list_to_tuple():
    old_sig = {
        "pos_args": ["forcefield"],
        "pos_defaults": {"forcefield": "['AMBER99SB-ILDN', 'TIP3P']"},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["forcefield"],
        "pos_defaults": {"forcefield": "('AMBER99SB-ILDN', 'TIP3P')"},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Default value changed for 'forcefield'" in d for d in diffs)


def test_compare_signatures_detects_parameter_added_at_end():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a", "b", "c"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Added positional parameter(s)" in d for d in diffs)


def test_compare_signatures_detects_parameter_dropped():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["a"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Dropped positional parameter 'b'" in d for d in diffs)


def test_compare_signatures_detects_order_swap():
    old_sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    new_sig = {
        "pos_args": ["b", "a"],
        "pos_defaults": {},
        "kwonly_args": [],
        "kwonly_defaults": {},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(old_sig, new_sig, "dummy_fn")
    assert any("Positional parameters altered" in d for d in diffs)


def test_compare_signatures_identical_passes():
    sig = {
        "pos_args": ["a", "b"],
        "pos_defaults": {"b": "None"},
        "kwonly_args": ["c"],
        "kwonly_defaults": {"c": "True"},
        "vararg": None,
        "kwarg": None,
    }
    diffs = compare_signatures(sig, sig, "dummy_fn")
    assert diffs == []
