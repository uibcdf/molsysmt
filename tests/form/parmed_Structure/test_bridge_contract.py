"""Protecting coordinate and topology alignment across ParmEd conversion bridges."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture(autouse=True, params=["nm", "angstrom"])
def unit_policy(request):
    with puw.context(standard_units=[request.param, "fs", "degrees"]):
        yield


def _coordinates():
    return np.arange(36, dtype=float).reshape(3, 4, 3) / 100


def _lengths():
    return np.array([[2, 2.1, 2.2], [3, 3.1, 3.2], [4, 4.1, 4.2]])


def _source(form):
    names = ["O", "C", "N", "S"]
    if form.startswith("mdtraj."):
        md = pytest.importorskip("mdtraj")
        topology = md.Topology()
        chain = topology.add_chain("A")
        for group_index in range(2):
            group = topology.add_residue("LIG", chain, resSeq=7 + group_index)
            for index in range(group_index * 2, group_index * 2 + 2):
                topology.add_atom(
                    names[index],
                    md.element.get_by_symbol(names[index]),
                    group,
                    serial=[17, 3, 45, 90][index],
                )
        atoms = list(topology.atoms)
        for index in range(3):
            topology.add_bond(atoms[index], atoms[index + 1])
        if form == "mdtraj.Topology":
            return topology
        return md.Trajectory(
            _coordinates(),
            topology,
            unitcell_lengths=_lengths(),
            unitcell_angles=np.full((3, 3), 90.0),
        )
    pmd = pytest.importorskip("parmed")
    structure = pmd.Structure()
    for index, (element, mass) in enumerate([(8, 16), (6, 12), (7, 14), (16, 32)]):
        structure.add_atom(
            pmd.Atom(
                name=names[index],
                type=names[index],
                atomic_number=element,
                mass=mass,
                number=[17, 3, 45, 90][index],
                charge=[-0.4, 0.1, 0.1, 0.2][index],
            ),
            "LIG",
            7 + index // 2,
            chain="A",
        )
    for index in range(3):
        structure.bonds.append(
            pmd.Bond(structure.atoms[index], structure.atoms[index + 1])
        )
    structure.coordinates = _coordinates() * 10
    structure.box = np.column_stack((_lengths() * 10, np.full((3, 3), 90.0)))
    return structure


def _convert(source, target, route, atom_indices="all", structure_indices="all"):
    if route == "public":
        kwargs = {"selection": atom_indices}
        if msm.get_form(source) != "mdtraj.Topology":
            kwargs["structure_indices"] = structure_indices
        return msm.convert(source, to_form=target, **kwargs)
    from molsysmt.form import _dict_modules, load_converter

    module = _dict_modules[msm.get_form(source)]
    converter = load_converter(module, module._convert_to[target])
    kwargs = {"atom_indices": atom_indices}
    if msm.get_form(source) != "mdtraj.Topology":
        kwargs["structure_indices"] = structure_indices
    return converter(source, **kwargs)


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("source_form", ["mdtraj.Topology", "mdtraj.Trajectory"])
@pytest.mark.parametrize("selected", [False, True])
def test_mdtraj_to_parmed_keeps_topology_and_selected_geometry(
    route, source_form, selected
):
    pytest.importorskip("parmed")
    pytest.importorskip("openmm")
    source = _source(source_form)
    atoms = [1, 2, 3] if selected else [0, 1, 2, 3]
    structures = [2, 0] if selected else [0, 1, 2]

    output = _convert(
        source,
        "parmed.Structure",
        route,
        atom_indices=[3, 1, 2] if selected else "all",
        structure_indices=structures,
    )

    assert msm.get_form(output) == "parmed.Structure"
    assert [atom.name for atom in output.atoms] == [
        ["O", "C", "N", "S"][index] for index in atoms
    ]
    assert [group.number for group in output.residues] == [7, 8]
    assert len(output.bonds) == len(atoms) - 1
    if source_form == "mdtraj.Trajectory":
        np.testing.assert_allclose(
            output.get_coordinates("all"),
            _coordinates()[structures][:, atoms] * 10,
            rtol=1e-6,
            atol=1e-6,
        )
        np.testing.assert_allclose(
            output.get_box("all")[:, :3], _lengths()[structures] * 10
        )
        # The general PBC tool rounds angles to six decimal places in radians.
        np.testing.assert_allclose(output.get_box("all")[:, 3:], 90, atol=3e-5)
        np.testing.assert_allclose(source.xyz, _coordinates(), rtol=1e-6)
    else:
        assert output.coordinates is None
    assert source.n_atoms == 4


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("selected", [False, True])
def test_parmed_to_modeller_uses_first_selected_structure_with_its_box(route, selected):
    pytest.importorskip("openmm")
    source = _source("parmed.Structure")
    structure_index = 2 if selected else 0
    atoms = [1, 2, 3] if selected else [0, 1, 2, 3]
    output = _convert(
        source,
        "openmm.Modeller",
        route,
        atom_indices=[3, 1, 2] if selected else "all",
        structure_indices=[2, 0] if selected else "all",
    )

    assert [atom.name for atom in output.topology.atoms()] == [
        ["O", "C", "N", "S"][index] for index in atoms
    ]
    assert len(list(output.topology.bonds())) == len(atoms) - 1
    np.testing.assert_allclose(
        puw.get_value(output.positions, to_unit="nm"),
        _coordinates()[structure_index, atoms],
    )
    np.testing.assert_allclose(
        puw.get_value(output.topology.getPeriodicBoxVectors(), to_unit="nm"),
        np.diag(_lengths()[structure_index]),
    )
    np.testing.assert_allclose(source.get_coordinates("all"), _coordinates() * 10)
    np.testing.assert_allclose(source.get_box("all")[:, :3], _lengths() * 10)


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("box_mode", ["per_structure", "shared", "none"])
@pytest.mark.parametrize(
    "target",
    ["parmed.Structure", "mdtraj.Trajectory", "molsysmt.MolSys", "molsysmt.Structures"],
)
def test_parmed_selected_geometry_and_mechanics_stay_aligned(route, target, box_mode):
    if target == "mdtraj.Trajectory":
        pytest.importorskip("mdtraj")
        pytest.importorskip("openmm")
    source = _source("parmed.Structure")
    if box_mode == "shared":
        source.box = source.get_box("all")[:1]
    elif box_mode == "none":
        source.box = None
    original_boxes = source.get_box("all")
    if original_boxes is not None:
        original_boxes = original_boxes.copy()
    atoms = [3, 1, 2] if target == "molsysmt.Structures" else [1, 2, 3]
    structures = [2, 0]
    output = _convert(
        source, target, route, atom_indices=[3, 1, 2], structure_indices=structures
    )

    assert msm.get_form(output) == target
    if target == "parmed.Structure":
        coordinates = output.get_coordinates("all") / 10
        boxes = output.get_box("all")
        lengths = None if boxes is None else boxes[:, :3] / 10
        assert [atom.name for atom in output.atoms] == ["C", "N", "S"]
        np.testing.assert_allclose(
            [atom.charge for atom in output.atoms], [0.1, 0.1, 0.2]
        )
    elif target == "mdtraj.Trajectory":
        coordinates = output.xyz
        lengths = output.unitcell_lengths
        assert [atom.name for atom in output.topology.atoms] == ["C", "N", "S"]
    else:
        structural = output.structures if target == "molsysmt.MolSys" else output
        coordinates = puw.get_value(structural.coordinates, to_unit="nm")
        lengths = (
            None
            if structural.box is None
            else puw.get_value(structural.box, to_unit="nm")[:, [0, 1, 2], [0, 1, 2]]
        )
        if target == "molsysmt.MolSys":
            assert output.topology.atoms["atom_id"].tolist() == ["3", "45", "90"]
            np.testing.assert_allclose(
                np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
                [0.1, 0.1, 0.2],
            )
    assert coordinates.shape == (2, 3, 3)
    np.testing.assert_allclose(
        coordinates, _coordinates()[structures][:, atoms], atol=1e-7
    )
    if box_mode == "none":
        assert lengths is None
    else:
        expected = (
            _lengths()[structures]
            if box_mode == "per_structure"
            else _lengths()[[0, 0]]
        )
        np.testing.assert_allclose(lengths, expected, atol=1e-6)
    np.testing.assert_allclose(source.get_coordinates("all"), _coordinates() * 10)
    if original_boxes is None:
        assert source.get_box("all") is None
    else:
        np.testing.assert_array_equal(source.get_box("all"), original_boxes)
    assert len(source.atoms) == 4


@pytest.mark.parametrize("route", ["direct", "public"])
def test_parmed_cell_without_coordinates_remains_queryable(route):
    source = _source("parmed.Structure")
    source.coordinates = None
    source.box = source.get_box("all")[:1]
    if route == "public":
        box = msm.get(source, box=True)
    else:
        from molsysmt.form.parmed_Structure import get_box_from_system

        box = get_box_from_system(source)

    assert box.shape == (1, 3, 3)
    np.testing.assert_allclose(
        puw.get_value(box, to_unit="nm"), np.diag(_lengths()[0])[None]
    )
    assert source.coordinates is None
