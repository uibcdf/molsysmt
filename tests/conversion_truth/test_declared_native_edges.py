"""Execute each registered resident/native-engine edge and its public route.

This is reachability evidence, not a fidelity or scientific accuracy certificate.
Sources are rebuilt for each call so mutation by one adapter cannot mask another.
"""

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    audit_plan,
    declared_edges,
    planned_edges,
    read_plan,
)
from tests.native.test_molsys import build_minimal_molsys

PLAN = read_plan()
EDGES = sorted(planned_edges(declared_edges(), PLAN))


def _source(form):
    if form.startswith("mdtraj."):
        md = pytest.importorskip("mdtraj")
        topology = md.Topology()
        group = topology.add_residue("HOH", topology.add_chain())
        oxygen = topology.add_atom("O", md.element.oxygen, group)
        for name in ("H1", "H2"):
            hydrogen = topology.add_atom(name, md.element.hydrogen, group)
            topology.add_bond(oxygen, hydrogen)
        if form == "mdtraj.Topology":
            return topology
        return md.Trajectory(_water_coordinates(), topology)
    if form.startswith("openmm."):
        pytest.importorskip("openmm")
        from openmm import app, unit

        topology = app.Topology()
        group = topology.addResidue("HOH", topology.addChain("A"), id="1")
        oxygen = topology.addAtom("O", app.element.oxygen, group, id="1")
        for index, name in enumerate(("H1", "H2"), start=2):
            hydrogen = topology.addAtom(
                name, app.element.hydrogen, group, id=str(index)
            )
            topology.addBond(oxygen, hydrogen)
        if form == "openmm.Topology":
            return topology
        return app.Modeller(topology, _water_coordinates()[0] * unit.nanometer)
    system = build_minimal_molsys(n_structures=2)
    if form in {"molsysmt.ChemicalStates", "molsysmt.ChemicalStatesDict"}:
        source = system.chemical_states
    elif form in {"molsysmt.Interactions", "molsysmt.InteractionsDict"}:
        source = msm.Interactions.from_records(
            [
                {
                    "structure_index": 1,
                    "interaction_type": "pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [3]},
                    ],
                }
            ],
            n_atoms=4,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="execution-control",
        )
    elif form in {"molsysmt.MolecularMechanics", "molsysmt.MolecularMechanicsDict"}:
        source = system.molecular_mechanics
        source.partial_charge = [0.1, -0.1, 0.2, -0.2]
    elif form in {"molsysmt.Topology", "molsysmt.TopologyDict"}:
        source = system.topology
    elif form in {"molsysmt.Structures", "molsysmt.StructuresDict"}:
        source = system.structures
    else:
        source = system
    return source if msm.get_form(source) == form else msm.convert(source, to_form=form)


def _water_coordinates():
    # A literal three-atom, two-structure fixture in nanometers.
    first = np.array([[0.0, 0.0, 0.0], [0.095, 0.0, 0.0], [-0.024, 0.092, 0.0]])
    return np.stack([first, first + [0.1, 0.2, 0.3]])


def _edge_arguments(source, target):
    if (source, target) in {
        ("mdtraj.Topology", "mdtraj.Trajectory"),
        ("openmm.Topology", "openmm.Modeller"),
        ("openmm.Topology", "molsysmt.MolSys"),
    }:
        return {
            "coordinates": msm.pyunitwizard.quantity(_water_coordinates()[:1], "nm")
        }
    return {}


def _execute_direct(source, target, item, **kwargs):
    from molsysmt.form import _dict_modules, load_converter

    module = _dict_modules[source]
    converter = load_converter(module, module._convert_to[target])
    result = converter(item, **kwargs)
    assert msm.get_form(result) == target
    return result


@pytest.mark.parametrize(
    "source,target", EDGES, ids=[f"{source}->{target}" for source, target in EDGES]
)
def test_declared_resident_edge_executes_directly_and_publicly(source, target):
    for form in (source, target):
        if form.startswith("mdtraj."):
            pytest.importorskip("mdtraj")
        elif form.startswith("openmm."):
            pytest.importorskip("openmm")
    arguments = _edge_arguments(source, target)
    assert msm.get_form(_source(source)) == source
    _execute_direct(source, target, _source(source), **arguments)
    result = msm.convert(
        _source(source), to_form=target, **_edge_arguments(source, target)
    )
    assert msm.get_form(result) == target


def test_execution_guard_rejects_callable_runtime_failure(monkeypatch):
    from molsysmt.form import _dict_modules

    def broken(item):
        raise TypeError("wrong imported identity converter rejects foreign input")

    monkeypatch.setitem(
        _dict_modules["molsysmt.MolSys"]._convert_to, "molsysmt.Topology", broken
    )
    with pytest.raises(TypeError, match="wrong imported identity"):
        _execute_direct(
            "molsysmt.MolSys", "molsysmt.Topology", _source("molsysmt.MolSys")
        )


def test_execution_guard_rejects_wrong_output_form(monkeypatch):
    from molsysmt.form import _dict_modules

    monkeypatch.setitem(
        _dict_modules["molsysmt.MolSys"]._convert_to,
        "molsysmt.Topology",
        lambda item: item,
    )
    with pytest.raises(AssertionError):
        _execute_direct(
            "molsysmt.MolSys", "molsysmt.Topology", _source("molsysmt.MolSys")
        )


def test_execution_plan_accounts_for_the_entire_declared_graph():
    assert audit_plan(declared_edges(), PLAN)["errors"] == []
