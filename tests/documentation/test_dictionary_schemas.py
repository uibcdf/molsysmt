"""Checking documented dictionary keys/types against real serialized payloads."""

import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures

PAGES = (
    Path(__file__).resolve().parents[2]
    / "docs/content/user/foundations/native_world/classes"
)


def _text(name):
    return (PAGES / f"molsysmt_{name}.md").read_text()


def _rows(text, heading):
    marker = f"## {heading}\n"
    assert marker in text, f"The guide must explain its {heading.lower()}."
    section = text.split(marker, 1)[1].split("\n## ", 1)[0]
    result = {}
    for line in section.splitlines():
        columns = [column.strip() for column in line.strip("|").split("|")]
        key = re.fullmatch(r'`"?(\w+)"?`', columns[0].strip("* "))
        if line.startswith("|") and key:
            result[key.group(1)] = columns[1:]
    assert result, "The published schema must describe actual fields."
    return result


def _example(name):
    text = _text(name)
    blocks = re.findall(r"```python\n(.*?)\n```", text, flags=re.DOTALL)
    assert blocks, "The schema guide must contain a runnable example."
    namespace = {}
    for block in blocks:
        exec(compile(block, f"molsysmt_{name}.md", "exec"), namespace)
    return namespace


@pytest.mark.parametrize("name", ["TopologyDict", "MolSysDict", "StructuresDict"])
def test_schema_examples_reconstruct_documented_values(name):
    namespace = _example(name)
    rebuilt = namespace["rebuilt"]
    assert msm.get(rebuilt, n_atoms=True) == 2
    if name == "StructuresDict":
        assert type(namespace["structures_dict"]) is dict
        assert msm.get(rebuilt, n_structures=True) == 2
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(rebuilt.coordinates, to_unit="angstrom"),
            np.arange(12).reshape(2, 2, 3),
        )
    else:
        assert msm.get(rebuilt, element="atom", atom_id=True) == ["10", "20"]
        assert msm.get(rebuilt, n_bonds=True) == 1
        if name == "MolSysDict":
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(
                    rebuilt.structures.coordinates, to_unit="nm"
                ),
                [[[0, 0, 0], [0.12, 0, 0]]],
            )
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(rebuilt.structures.time, to_unit="ps"), [2]
            )


@pytest.mark.parametrize("name", ["TopologyDict", "MolSysDict"])
def test_documented_record_keys_match_emitted_schema(name):
    data = _example(name)["data"]
    rows = _rows(_text(name), "Declarative Schema")
    assert set(rows) == set(data)
    if name == "MolSysDict":
        assert set(_rows(_text(name), "Structural Payload")) == set(data["structures"])
        topology = data["topology"]
        rows = _rows(_text("TopologyDict"), "Declarative Schema")
    else:
        topology = data
    collections = {"atoms", "groups", "bonds", "chains", "molecules", "entities"}
    assert set(topology) - {"format", "kind", "version", "metadata"} == collections
    for collection in collections:
        assert topology[collection], f"The example must exercise {collection} records."
        documented_keys = set(re.findall(r"`(\w+)`", rows[collection][1]))
        for record in topology[collection]:
            assert set(record) == documented_keys, collection


def test_structures_dictionary_table_matches_real_payload_types():
    puw = msm.pyunitwizard
    molsys = Structures(
        coordinates=puw.quantity(np.zeros((2, 2, 3)), "nm"),
        velocities=puw.quantity(np.ones((2, 2, 3)), "nm/ps"),
        box=puw.quantity(np.tile(np.eye(3), (2, 1, 1)), "nm"),
        time=puw.quantity([0.0, 1.0], "ps"),
        structure_id=[0, 1],
        b_factor=puw.quantity(np.ones((2, 2)), "nm**2"),
        occupancy=np.ones((2, 2)),
    )
    molsys.temperature = puw.quantity([300.0, 301.0], "K")
    molsys.potential_energy = puw.quantity([-1.0, -2.0], "kJ/mol")
    molsys.kinetic_energy = puw.quantity([0.1, 0.2], "kJ/mol")
    molsys.alternate_location = [{0: {"location_id": ["A"]}}, {}]
    data = msm.convert(molsys, to_form="molsysmt.StructuresDict")
    rows = _rows(_text("StructuresDict"), "Declarative Schema")
    assert set(data) == set(rows)
    for key, value in data.items():
        declared_type = rows[key][0]
        if declared_type == "quantity":
            assert puw.is_quantity(value), key
        elif declared_type == "array":
            assert isinstance(value, np.ndarray), key
        else:
            assert declared_type == "sequence of dictionaries"
            assert len(value) == 2 and all(isinstance(sites, dict) for sites in value)
