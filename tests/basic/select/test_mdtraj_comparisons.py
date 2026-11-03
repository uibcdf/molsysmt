"""Public external-comparison populations, independent of provider parse trees."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(
    params=[
        "mdtraj.Topology",
        "mdtraj.Trajectory",
        "molsysmt.Topology",
        "molsysmt.MolSys",
    ]
)
def comparison_system(request):
    md = pytest.importorskip("mdtraj")
    topology = md.Topology()
    chain = topology.add_chain(chain_id="A")
    first = topology.add_residue("ALA", chain, resSeq=10)
    second = topology.add_residue("GLY", chain, resSeq=20)
    atoms = [
        topology.add_atom("N", md.element.nitrogen, first, serial=1),
        topology.add_atom("CA", md.element.carbon, first, serial=2),
        topology.add_atom("C", md.element.carbon, second, serial=3),
        topology.add_atom("O", md.element.oxygen, second, serial=4),
    ]
    for left, right in zip(atoms[:-1], atoms[1:]):
        topology.add_bond(left, right)
    if request.param == "mdtraj.Topology":
        return topology
    if request.param == "mdtraj.Trajectory":
        return md.Trajectory(np.zeros((1, 4, 3)), topology)
    source = (
        md.Trajectory(np.zeros((1, 4, 3)), topology)
        if request.param == "molsysmt.MolSys"
        else topology
    )
    system = msm.convert(source, to_form=request.param)
    assert msm.get(system, n_atoms=True) == 4
    assert msm.get(system, n_groups=True) == 2
    assert msm.get(system, n_chains=True) == 1
    assert msm.get(system, n_components=True) == (
        None if request.param == "molsysmt.Topology" else 1
    )
    assert msm.get(system, n_molecules=True) == 1
    assert msm.get(system, n_entities=True) == 1
    return system


@pytest.mark.parametrize(
    "symbol, expected",
    [
        ("<", [0]),
        ("lt", [0]),
        ("<=", [0, 1]),
        ("le", [0, 1]),
        (">", [2, 3]),
        ("gt", [2, 3]),
        (">=", [1, 2, 3]),
        ("ge", [1, 2, 3]),
        ("==", [1]),
        ("eq", [1]),
        ("!=", [0, 2, 3]),
        ("ne", [0, 2, 3]),
    ],
)
def test_public_mdtraj_comparison_populations(comparison_system, symbol, expected):
    assert (
        msm.select(comparison_system, f"index {symbol} 1", syntax="MDTraj") == expected
    )


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("(index >= 1) and (index <= 2)", [1, 2]),
        ("not (index <= 1)", [2, 3]),
        ("(index < 1) or (index >= 3)", [0, 3]),
        ("index >= 4", []),
    ],
)
def test_public_mdtraj_compound_and_empty_populations(
    comparison_system, expression, expected
):
    assert msm.select(comparison_system, expression, syntax="MDTraj") == expected


def test_public_mdtraj_group_projection(comparison_system):
    assert msm.select(
        comparison_system, "index >= 1", element="group", syntax="MDTraj"
    ) == [0, 1]


def test_public_mdtraj_invalid_input_preserves_provider_cause(comparison_system):
    with pytest.raises(msm.ArgumentError) as error:
        msm.select(comparison_system, "index ==== 1", syntax="MDTraj")
    assert isinstance(error.value.__cause__, ValueError)
