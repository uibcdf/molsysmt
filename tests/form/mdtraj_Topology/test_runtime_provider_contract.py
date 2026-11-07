"""Ground the optional MDTraj floor in atom export and metadata-preserving copies."""

import tomllib
from pathlib import Path

import pandas as pd
import pytest
from packaging.requirements import Requirement

import molsysmt as msm
from molsysmt.native import MolSys


def test_optional_requirement_admits_the_qualified_metadata_api_floor():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        r
        for r in map(Requirement, project["optional-dependencies"]["soft"])
        if r.name.lower() == "mdtraj"
    )
    assert requirement.specifier.contains("1.11.0")
    for version in ("1.10.2", "1.10.3"):
        assert not requirement.specifier.contains(version), (
            "MDTraj 1.10.3 accepts formal_charge, but 1.11.0 is needed to retain "
            "charges and chain labels through Topology copies."
        )
    assert all(
        Requirement(raw).name.lower() != "mdtraj" for raw in project["dependencies"]
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
    topology.groups["group_id"] = ["9"]
    topology.atoms["group_index"] = [0, 0, 0]
    topology.reset_chains(n_chains=1)
    topology.chains["chain_id"] = ["Q"]
    topology.atoms["chain_index"] = [0, 0, 0]
    system.chemical_states.add_bonds([[1, 2], [0, 1]])
    msm.set(system, formal_charge=[1, None, -1])
    msm.set(system, element="bond", bond_order=[1, 2])
    return system


@pytest.mark.parametrize("inventory_only", [False, True])
@pytest.mark.parametrize("selection", ["all", [2, 0], []])
def test_native_export_uses_the_charge_api_and_retains_source(
    source, inventory_only, selection
):
    pytest.importorskip("mdtraj")
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.chemical_states.get_bonds().copy(deep=True)
    before_charges = source.get(formal_charge=True)
    item = source.topology if inventory_only else source
    result = msm.convert(item, to_form="mdtraj.Topology", selection=selection)
    indices = [0, 1, 2] if selection == "all" else sorted(selection)
    assert result.n_atoms == len(indices)
    assert [a.name for a in result.atoms] == [["N0", "C1", "O2"][i] for i in indices]
    assert [a.serial for a in result.atoms] == [str(11 * (i + 1)) for i in indices]
    charges = [None, None, None] if inventory_only else [1, None, -1]
    assert [a.formal_charge for a in result.atoms] == [charges[i] for i in indices]
    expected_bonds = 2 if not inventory_only and selection == "all" else 0
    assert result.n_bonds == expected_bonds
    if indices:
        assert result.residue(0).name == "LIG"
        assert result.residue(0).resSeq == "9"
        assert result.chain(0).chain_id == "Q"
    if expected_bonds:
        assert [(a.index, b.index) for a, b in result.bonds] == [(0, 1), (1, 2)]
        assert [b.order for b in result.bonds] == [1, 2]
        recovered = msm.convert(result, to_form="molsysmt.MolSys")
        assert recovered.get(formal_charge=True) == [1, None, -1]
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before_bonds)
    assert source.get(formal_charge=True) == before_charges


@pytest.mark.parametrize("route", ["copy", "extract_all"])
def test_topology_copies_keep_chain_labels_and_known_unknown_charges(source, route):
    pytest.importorskip("mdtraj")
    target = msm.convert(source, to_form="mdtraj.Topology")
    copied = msm.copy(target) if route == "copy" else msm.extract(target)
    assert copied is not target
    assert copied.chain(0).chain_id == "Q"
    assert [a.formal_charge for a in copied.atoms] == [1, None, -1]
    assert [a.serial for a in copied.atoms] == ["11", "22", "33"]
    assert copied.residue(0).resSeq == "9"
    assert [(a.index, b.index) for a, b in copied.bonds] == [(0, 1), (1, 2)]
    assert [b.order for b in copied.bonds] == [1, 2]
    copied.atom(0).name = "changed"
    assert target.atom(0).name == "N0"
    assert source.topology.atoms["atom_name"].tolist() == ["N0", "C1", "O2"]
