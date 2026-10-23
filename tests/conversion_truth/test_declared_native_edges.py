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
# Disk/handler routes have explicit resource and schema fixtures in their own module.
H5MSM_FORMS = {"file:h5msm", "molsysmt.H5MSMFileHandler"}
PDB_FORMS = {"file:pdb", "string:pdb_text", "molsysmt.PDBFileHandler"}
DOCKING_FORMS = {"file:sdf", "file:pdbqt", "string:pdbqt_text"}
EDGES = sorted(
    (source, target)
    for source, target in planned_edges(declared_edges(), PLAN)
    if not ({source, target} & (H5MSM_FORMS | PDB_FORMS | DOCKING_FORMS))
)


def _source(form):
    if form == "MDAnalysis.Universe":
        mda = pytest.importorskip("MDAnalysis")
        universe = mda.Universe.empty(
            3, n_residues=1, atom_resindex=[0, 0, 0], trajectory=True
        )
        for name, values in {
            "names": ["O", "H1", "H2"],
            "types": ["O", "H", "H"],
            "elements": ["O", "H", "H"],
            "ids": [17, 3, 45],
            "resnames": ["HOH"],
            "resids": [7],
            "segids": ["W"],
            "chainIDs": ["A"] * 3,
            "masses": [15.999, 1.008, 1.008],
            "charges": [-0.834, 0.417, 0.417],
            "bonds": [(0, 1), (0, 2)],
            "altLocs": [""] * 3,
            "icodes": [""],
            "occupancies": [1.0] * 3,
            "tempfactors": [0.0] * 3,
            "record_types": ["ATOM"] * 3,
            "formalcharges": [0] * 3,
        }.items():
            universe.add_TopologyAttr(name, values)
        # MDAnalysis's native boundary uses angstroms and box angles in degrees.
        universe.load_new(
            _water_coordinates() * 10,
            order="fac",
            dimensions=np.array([[20, 20, 20, 90, 90, 90]] * 2),
        )
        return universe
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
        elif form.startswith("MDAnalysis."):
            pytest.importorskip("MDAnalysis")
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


def test_execution_modules_cover_the_selected_graph_once():
    from tests.conversion_truth.test_declared_docking_edges import (
        EDGES as docking_edges,
    )
    from tests.conversion_truth.test_declared_h5msm_edges import EDGES as disk_edges
    from tests.conversion_truth.test_declared_pdb_edges import EDGES as pdb_edges

    partitions = [set(EDGES), set(disk_edges), set(pdb_edges), set(docking_edges)]
    assert set.union(*partitions) == planned_edges(declared_edges(), PLAN)
    assert sum(map(len, partitions)) == len(set.union(*partitions))
