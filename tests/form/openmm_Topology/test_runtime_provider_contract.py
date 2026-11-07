"""Ground the optional OpenMM floor in native atom export and charge preservation."""

import tomllib
from pathlib import Path

import pandas as pd
import pytest
from packaging.requirements import Requirement

import molsysmt as msm
from molsysmt.native import MolSys


def test_optional_requirement_excludes_the_pre_formal_charge_api():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        r
        for r in map(Requirement, project["optional-dependencies"]["soft"])
        if r.name.lower() == "openmm"
    )
    assert requirement.specifier.contains("8.2.0")
    assert not requirement.specifier.contains("8.1.2"), (
        "Native atom exports pass formalCharge, including None; OpenMM first "
        "accepts this keyword in the stable 8.2.0 API."
    )
    assert not any(
        Requirement(raw).name.lower() == "openmm" for raw in project["dependencies"]
    )


@pytest.fixture
def source():
    system = MolSys(n_atoms=3)
    topology = system.topology
    topology.atoms["atom_name"] = ["N0", "C1", "O2"]
    topology.atoms["atom_type"] = ["N", "C", "O"]
    topology.atoms["atom_id"] = ["11", "22", "33"]
    topology.reset_groups(n_groups=1)
    topology.groups["group_name"] = ["LIG"]
    topology.groups["group_id"] = ["07"]
    topology.atoms["group_index"] = [0, 0, 0]
    topology.reset_chains(n_chains=1)
    topology.chains["chain_id"] = ["Q"]
    topology.atoms["chain_index"] = [0, 0, 0]
    system.chemical_states.add_bonds([[0, 1], [1, 2]])
    msm.set(system, formal_charge=[1, None, -1])
    msm.set(system, element="bond", bond_order=[2, 1])
    return system


@pytest.mark.parametrize("inventory_only", [False, True])
@pytest.mark.parametrize("selection", ["all", [2, 0], []])
def test_native_exports_keep_labels_known_unknown_charges_and_source(
    source, inventory_only, selection
):
    pytest.importorskip("openmm")
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.chemical_states.get_bonds().copy(deep=True)
    item = source.topology if inventory_only else source
    target = msm.convert(item, to_form="openmm.Topology", selection=selection)
    indices = [0, 1, 2] if selection == "all" else sorted(selection)
    atoms = list(target.atoms())
    assert target.getNumAtoms() == len(indices)
    assert [atom.index for atom in atoms] == list(range(len(indices)))
    assert [atom.name for atom in atoms] == [["N0", "C1", "O2"][i] for i in indices]
    assert [atom.id for atom in atoms] == [["11", "22", "33"][i] for i in indices]
    charges = [None, None, None] if inventory_only else [1, None, -1]
    assert [atom.formalCharge for atom in atoms] == [charges[i] for i in indices]
    if indices:
        assert [group.id for group in target.residues()] == ["07"]
        assert [chain.id for chain in target.chains()] == ["Q"]
    bonds = list(target.bonds())
    expected_bonds = (
        [(0, 1, 2), (1, 2, 1)] if not inventory_only and selection == "all" else []
    )
    assert [
        (bond[0].index, bond[1].index, bond.order) for bond in bonds
    ] == expected_bonds
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before_bonds)
    assert source.get(formal_charge=True) == [1, None, -1]


def test_exported_topology_copy_keeps_declared_charges_and_independence(source):
    pytest.importorskip("openmm")
    target = msm.convert(source, to_form="openmm.Topology")
    copied = msm.copy(target)
    assert copied is not target
    assert [atom.formalCharge for atom in copied.atoms()] == [1, None, -1]
    assert [chain.id for chain in copied.chains()] == ["Q"]
    copied_atoms = list(copied.atoms())
    copied_atoms[0].name = "changed"
    assert list(target.atoms())[0].name == "N0"
    recovered = msm.convert(copied, to_form="molsysmt.MolSys")
    assert recovered.get(formal_charge=True) == [1, None, -1]
