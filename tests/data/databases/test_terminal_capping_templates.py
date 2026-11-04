"""Protecting terminal-cap template generation after peptide-end relabeling."""

import json

import pytest

from molsysmt.data.databases.residue_templates import (
    make_residue_templates_db as generator,
)


@pytest.mark.parametrize("methyl", ["C", "CH3"])
def test_generator_preserves_cap_heavy_bonds_and_coordinate_units(
    tmp_path, monkeypatch, methyl
):
    inputs = tmp_path / "inputs"
    outputs = tmp_path / "outputs"
    inputs.mkdir()
    outputs.mkdir()
    atom_names = {"ACE": ["CH3", "C", "O"], "NME": ["N", methyl]}
    for group, names in atom_names.items():
        lines = [
            f"ATOM  {index + 1:5d} {name:^4} {group:3} A   1    "
            f"{1.5 * index:8.3f}{0.0:8.3f}{0.0:8.3f}{1.0:6.2f}{0.0:6.2f}          {name[0]:>2}  "
            for index, name in enumerate(names)
        ]
        (inputs / f"{group}.pdb").write_text("\n".join(lines) + "\nEND\n")
    monkeypatch.setattr(generator, "TEMPLATES_DIR", inputs)
    monkeypatch.setattr(generator, "OUTPUT_DIR", outputs)
    generator.main()
    ace = json.loads((outputs / "ACE.json").read_text())
    nme = json.loads((outputs / "NME.json").read_text())
    assert {frozenset(pair) for pair in ace["bonds"]} == {
        frozenset(["C", "CH3"]),
        frozenset(["C", "O"]),
    }
    assert nme["bonds"] == [["N", methyl]]
    assert ace["coords_nm"][1] == pytest.approx([0.15, 0.0, 0.0])
    assert nme["coords_nm"][1] == pytest.approx([0.15, 0.0, 0.0])
