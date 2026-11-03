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
EXPLICIT_EDGES = {tuple(edge) for edge in PLAN.get("explicit_edges", [])}
# Disk/handler routes have explicit resource and schema fixtures in their own module.
H5MSM_FORMS = {"file:h5msm", "molsysmt.H5MSMFileHandler"}
PDB_FORMS = {"file:pdb", "string:pdb_text", "molsysmt.PDBFileHandler"}
GRO_FORMS = {
    "file:gro",
    "molsysmt.GROFileHandler",
    "openmm.GromacsGroFile",
    "mdtraj.GroTrajectoryFile",
}
TRAJECTORY_FORMS = {
    "file:dcd",
    "file:xtc",
    "mdtraj.DCDTrajectoryFile",
    "mdtraj.XTCTrajectoryFile",
}
DOCKING_FORMS = {
    "file:sdf",
    "file:pdbqt",
    "string:pdbqt_text",
    "molsysmt.PDBQTFileHandler",
}
EDGES = sorted(
    (source, target)
    for source, target in planned_edges(declared_edges(), PLAN)
    if (source, target) not in EXPLICIT_EDGES
    and not (
        {source, target}
        & (H5MSM_FORMS | PDB_FORMS | DOCKING_FORMS | GRO_FORMS | TRAJECTORY_FORMS)
    )
)


def _source(form):
    if form == "parmed.Structure":
        pmd = pytest.importorskip("parmed")
        structure = pmd.Structure()
        for name, number, element, mass, charge in (
            ("O", 17, 8, 15.999, -0.834),
            ("H1", 3, 1, 1.008, 0.417),
            ("H2", 45, 1, 1.008, 0.417),
        ):
            structure.add_atom(
                pmd.Atom(
                    name=name,
                    number=number,
                    type="O" if element == 8 else "H",
                    atomic_number=element,
                    mass=mass,
                    charge=charge,
                ),
                "HOH",
                7,
                chain="A",
            )
        for index in (1, 2):
            structure.bonds.append(pmd.Bond(structure.atoms[0], structure.atoms[index]))
        structure.coordinates = _water_coordinates() * 10
        structure.box = np.array(
            [[20, 21, 22, 90, 90, 90], [30, 31, 32, 90, 90, 90]], dtype=float
        )
        return structure
    if form in {
        "MDAnalysis.Universe",
        "MDAnalysis.AtomGroup",
        "MDAnalysis.Topology",
    }:
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
        if form == "MDAnalysis.AtomGroup":
            # Parent indices differ from local positions; omit one parent atom.
            return universe.atoms[[2, 0]]
        if form == "MDAnalysis.Topology":
            return universe._topology.copy()
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
        elif form == "parmed.Structure":
            pytest.importorskip("parmed")
    if "parmed.Structure" in {source, target} and (
        source.startswith("mdtraj.")
        or target.startswith("mdtraj.")
        or source in {"molsysmt.Topology", "molsysmt.MolSys"}
    ):
        # These routes delegate topology conversion through OpenMM.
        pytest.importorskip("openmm")
    arguments = _edge_arguments(source, target)
    assert msm.get_form(_source(source)) == source
    direct = _execute_direct(source, target, _source(source), **arguments)
    result = msm.convert(
        _source(source), to_form=target, **_edge_arguments(source, target)
    )
    assert msm.get_form(result) == target
    if target == "molsysmt.MolSys":
        for output in (direct, result):
            if source in {"MDAnalysis.Topology", "mdtraj.Topology"}:
                assert output.topology.atoms.atom_name.tolist() == ["O", "H1", "H2"]
                assert output.topology.atoms.atom_type.tolist() == ["O", "H", "H"]
                assert output.chemical_states.get_bonds()[
                    ["atom1_index", "atom2_index"]
                ].values.tolist() == [[0, 1], [0, 2]]
            elif source == "molsysmt.TopologyDict":
                assert output.topology.atoms.atom_id.tolist() == ["0", "1", "2", "3"]
                assert output.topology.atoms.atom_name.tolist() == ["N", "CA", "O", "H"]
                assert output.chemical_states is None


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
    from tests.conversion_truth.test_declared_gro_edges import EDGES as gro_edges
    from tests.conversion_truth.test_declared_h5msm_edges import EDGES as disk_edges
    from tests.conversion_truth.test_declared_pdb_edges import EDGES as pdb_edges
    from tests.conversion_truth.test_declared_trajectory_edges import (
        EDGES as trajectory_edges,
    )

    partitions = [
        set(EDGES),
        EXPLICIT_EDGES,
        set(disk_edges),
        set(pdb_edges),
        set(docking_edges),
        set(gro_edges),
        set(trajectory_edges),
    ]
    assert set.union(*partitions) == planned_edges(declared_edges(), PLAN)
    assert sum(map(len, partitions)) == len(set.union(*partitions))


@pytest.mark.parametrize("source,target", sorted(EXPLICIT_EDGES))
def test_explicit_producer_edge_executes_with_declared_domains(
    source, target, tmp_path
):
    """Execute resource-dependent additions rather than marking them as debt."""
    if source == "file:fasta":
        item = tmp_path / "source.fasta"
        item.write_text(">first\nAG\n>second\nV\n")
        item = str(item)
    elif source == "file:smi":
        pytest.importorskip("rdkit")
        item = tmp_path / "source.smi"
        item.write_text("CCO ethanol\n")
        item = str(item)
    elif source == "file:topology_yaml":
        pytest.importorskip("yaml")
        item = str(tmp_path / "source.topology.yaml")
        msm.convert(
            build_minimal_molsys().topology,
            to_form="file:topology_yaml",
            output_filename=item,
        )
    elif source == "openmm.AmberPrmtopFile":
        app = pytest.importorskip("openmm.app")
        item = app.AmberPrmtopFile(msm.systems["pentalanine"]["pentalanine.prmtop"])
    elif source == "openmm.CharmmPsfFile":
        app = pytest.importorskip("openmm.app")
        from tests.form.file_psf.test_contract import PSF_TEXT

        path = tmp_path / "source.psf"
        path.write_text(PSF_TEXT)
        item = app.CharmmPsfFile(str(path))
    elif source == "openmm.GromacsTopFile":
        app = pytest.importorskip("openmm.app")
        path = tmp_path / "source.top"
        path.write_text(
            "[ defaults ]\n1 2 yes 0.5 0.8333\n[ atomtypes ]\nC 6 12.011 0 A 0.3 0.1\n[ moleculetype ]\nLIG 3\n[ atoms ]\n1 C 1 LIG C1 1 0 12.011\n2 C 1 LIG C2 1 0 12.011\n[ bonds ]\n1 2 1 0.15 1000\n[ system ]\npair\n[ molecules ]\nLIG 1\n"
        )
        item = app.GromacsTopFile(str(path))
    elif source == "pytraj.Topology":
        pytest.importorskip("pytraj")
        item = msm.convert(build_minimal_molsys(), to_form=source)
    else:
        item = {
            "string:amino_acids_1": "amino_acids_1:AG",
            "string:amino_acids_3": "amino_acids_3:ALAGLY",
            "string:smiles": "smiles:CCO",
        }[source]
        if source == "string:smiles":
            pytest.importorskip("rdkit")
    assert msm.get_form(item) == source
    direct = _execute_direct(source, target, item)
    public = msm.convert(item, to_form=target)
    assert msm.get_form(public) == target
    assert msm.get(direct, n_atoms=True) == msm.get(public, n_atoms=True)
    sequence = source in {"file:fasta", "string:amino_acids_1", "string:amino_acids_3"}
    if sequence:
        assert msm.get(public, n_atoms=True) == 0
        assert msm.get(public, n_groups=True) == (3 if source == "file:fasta" else 2)
    if target == "molsysmt.MolSys":
        assert (public.chemical_states is None) == (
            sequence or source == "file:topology_yaml"
        )
        if public.chemical_states is not None:
            assert public.chemical_states.get(n_bonds=True) > 0
            assert public.chemical_states._inventory_equals(direct.chemical_states)
    else:
        assert not hasattr(public, "bonds")
    # Literal or provider-owned oracles are separate from direct/public parity.
    for output in (direct, public):
        topology = output.topology if target == "molsysmt.MolSys" else output
        if sequence:
            assert topology.groups.group_name.tolist() == (
                ["ALA", "GLY", "VAL"] if source == "file:fasta" else ["ALA", "GLY"]
            )
            assert topology.n_chains == (2 if source == "file:fasta" else 1)
            assert topology.atoms.empty
        elif source in {"file:smi", "string:smiles"}:
            assert topology.atoms.atom_type.tolist() == ["C", "C", "O"]
            assert output.chemical_states.get_bonds()[
                ["atom1_index", "atom2_index"]
            ].values.tolist() == [[0, 1], [1, 2]]
            assert output.chemical_states.get(element="atom", formal_charge=True) == [
                0,
                0,
                0,
            ]
            assert output.chemical_states.get(
                element="atom", n_implicit_hydrogens=True
            ) == [3, 2, 1]
        elif source.startswith("openmm."):
            atoms = list(item.topology.atoms())
            assert topology.atoms.atom_id.tolist() == [str(atom.id) for atom in atoms]
            assert topology.atoms.atom_name.tolist() == [atom.name for atom in atoms]
            assert topology.atoms.atom_type.tolist() == [
                atom.element.symbol for atom in atoms
            ]
            expected_pairs = sorted(
                sorted((a.index, b.index)) for a, b in item.topology.bonds()
            )
            actual_pairs = output.chemical_states.get_bonds()[
                ["atom1_index", "atom2_index"]
            ].values.tolist()
            assert sorted(sorted(pair) for pair in actual_pairs) == expected_pairs
        elif source in {"file:topology_yaml", "pytraj.Topology"}:
            assert topology.atoms.atom_name.tolist() == ["N", "CA", "O", "H"]
            assert topology.groups.group_name.tolist() == ["ALA", "HOH"]
