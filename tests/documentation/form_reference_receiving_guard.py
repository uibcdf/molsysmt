"""Explicit HTML receiving outside default scientific collection."""

import os
from pathlib import Path

import pytest

from tests.documentation._form_reference_checks import (
    _assert_rendered_native_form_references,
)


@pytest.mark.parametrize(
    "name",
    [
        "MolSys",
        "Topology",
        "Structures",
        "MolSysDict",
        "TopologyDict",
        "StructuresDict",
        "MolecularMechanicsDict",
    ],
)
def test_actual_native_tutorial_delivers_every_intended_reference(name):
    directory = os.environ.get("MOLSYSMT_FORM_REFERENCE_HTML")
    assert directory, "Select the actual received HTML directory explicitly."
    assert Path(directory).is_dir()
    _assert_rendered_native_form_references(directory, name)
