"""Check real pytest collection rather than the spelling of network markers."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MISSING = "tests/build/get_missing_residues/test_get_missing_residues.py"
DISULFIDE = "tests/build/get_disulfide_bonds/test_get_disulfide_bonds.py"


@pytest.mark.parametrize("network", [False, True])
def test_live_build_test_selection(network):
    environment = dict(
        os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTEST_ADDOPTS=""
    )
    # Native collect-only is the selection oracle; fixtures and scientific
    # computations never execute in this child process.
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "--collect-only",
            "-q",
            "-p",
            "no:cacheprovider",
            "-o",
            "addopts=",
            "-m",
            "network" if network else "not network",
            MISSING,
            DISULFIDE,
        ],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    selected = {
        line.strip()
        for line in result.stdout.splitlines()
        if line.startswith("tests/build/") and "::" in line
    }
    names = (
        [
            "returns_dict",
            "keys_are_tuples",
            "values_are_lists_of_strings",
            "pdb_detects_missing",
            "bcif_detects_missing",
            "with_selection",
            "pdbfixer_parity",
        ]
        if network
        else ["villin_complete", "no_seqres_warns", "explicit_sequence"]
    )
    expected = {f"{MISSING}::test_get_missing_residues_{name}" for name in names}
    if network:
        expected.add(f"{DISULFIDE}::test_get_disulfide_bonds")
    assert selected == expected
