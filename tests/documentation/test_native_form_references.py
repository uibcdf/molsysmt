"""Require complete source references, not merely existing Python objects."""

import importlib
import json
import re

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures
from tests.documentation._form_reference_checks import (
    PAGES,
    ROOT,
    _assert_native_form_reference_contract,
)

DICTIONARY_FORMS = [
    "MolSysDict",
    "TopologyDict",
    "StructuresDict",
    "MolecularMechanicsDict",
]


@pytest.mark.parametrize(
    "name", ["MolSys", "Topology", "Structures", *DICTIONARY_FORMS]
)
def test_native_tutorial_references_cover_all_registered_routes(name):
    _assert_native_form_reference_contract(name)


@pytest.mark.parametrize("name", DICTIONARY_FORMS)
def test_dictionary_tutorial_attribute_declarations_match_the_live_adapter(name):
    notebook = json.loads((ROOT / PAGES / f"molsysmt_{name}.ipynb").read_text())
    source = "".join(notebook["cells"][2]["source"])
    rows = "\n".join(line for line in source.splitlines() if line.startswith("|"))
    attributes = importlib.import_module(f"molsysmt.form.molsysmt_{name}").attributes
    declared = {attribute for attribute, flag in attributes.items() if flag}
    assert set(re.findall(r"`([^`]+)`", rows)) == declared
    assert re.findall(r"\*\*(\d+) (?:declared )?attributes\*\*", source) == [
        str(len(declared))
    ]


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_structural_molsys_route_keeps_indices_units_and_missing_domains(
    length_unit, time_unit
):
    puw = msm.pyunitwizard
    original = np.arange(18, dtype=float).reshape(2, 3, 3)
    with puw.context(
        standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
    ):
        structures = Structures(
            coordinates=puw.quantity(original, "nm"),
            time=puw.quantity([2, 5], "ps"),
        )
        molsys = msm.convert(
            structures,
            selection=[2, 0],
            structure_indices=[1, 0],
            to_form="molsysmt.MolSys",
        )
        assert molsys.topology is None and molsys.chemical_states is None
        coordinates = molsys.get(element="atom", coordinates=True)
        assert coordinates.shape == (2, 2, 3)
        assert puw.get_unit(coordinates) == puw.unit(length_unit)
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="nm"), original[[1, 0]][:, [2, 0]]
        )
        time = molsys.get(time=True)
        assert puw.get_unit(time) == puw.unit(time_unit)
        np.testing.assert_allclose(puw.get_value(time, to_unit="ps"), [5, 2])
        molsys.structures.set_coordinates(value=puw.quantity(np.zeros((2, 2, 3)), "nm"))
        np.testing.assert_array_equal(
            puw.get_value(structures.get_coordinates(), to_unit="nm"), original
        )
