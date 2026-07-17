"""Tests for the explicit form support-tier registry."""

import ast
from pathlib import Path

import pytest

from molsysmt._private.form_tier import FORM_TIERS, check_form_tier, get_form_tier
from molsysmt._private.smonitor import InternalAlgorithmError


def _discovered_form_names():
    form_root = Path(__file__).resolve().parents[2] / "molsysmt" / "form"
    names = set()
    for init_file in form_root.glob("*/__init__.py"):
        tree = ast.parse(init_file.read_text())
        for node in tree.body:
            if not isinstance(node, ast.Assign):
                continue
            if any(isinstance(target, ast.Name) and target.id == "form_name" for target in node.targets):
                if isinstance(node.value, ast.Constant):
                    names.add(node.value.value)
                break
    return names


def test_form_tier_registry_exactly_matches_discovered_adapters():
    assert set(FORM_TIERS) == _discovered_form_names()
    assert set(FORM_TIERS.values()) <= {1, 2, 3}


def test_form_tier_lookup_never_defaults_unknown_form_to_tier_1():
    assert get_form_tier("unknown.Form") is None
    with pytest.raises(InternalAlgorithmError):
        check_form_tier("unknown.Form")


def test_tier_1_form_is_explicit_and_silent():
    assert get_form_tier("molsysmt.MolSys") == 1
    assert check_form_tier("molsysmt.MolSys") is None


@pytest.mark.parametrize(
    "form_name",
    [
        "file:dcd",
        "file:gro",
        "file:h5",
        "mdtraj.DCDTrajectoryFile",
        "mdtraj.HDF5TrajectoryFile",
        "mdtraj.XTCTrajectoryFile",
        "molsysmt.GROFileHandler",
    ],
)
def test_pre_1_0_trajectory_cohort_is_contractual(form_name):
    assert get_form_tier(form_name) == 1


@pytest.mark.parametrize(
    "form_name",
    [
        "MDAnalysis.AtomGroup",
        "MDAnalysis.Topology",
        "MDAnalysis.Universe",
    ],
)
def test_pre_1_0_mdanalysis_cohort_is_contractual(form_name):
    assert get_form_tier(form_name) == 1


@pytest.mark.parametrize(
    "form_name",
    [
        "file:mol2",
        "file:psf",
        "file:smi",
        "openff.Molecule",
        "openff.Topology",
        "parmed.Structure",
        "rdkit.Mol",
        "string:smiles",
    ],
)
def test_pre_1_0_chemical_interoperability_cohort_is_contractual(form_name):
    assert get_form_tier(form_name) == 1
