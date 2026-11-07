"""Preserve declared OpenMM topology data through copies and selections."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.fixture(params=["nm", "angstrom"])
def source(request):
    pytest.importorskip("openmm")
    from openmm import app, unit

    topology = app.Topology()
    for cid, gid, code, names, charges in (
        ("A", "07", "X", ["N", "C"], [1, 0]),
        ("B", "00", "Y", ["O", "H"], [-1, None]),
    ):
        group = topology.addResidue(
            "LIG", topology.addChain(cid), id=gid, insertionCode=code
        )
        for name, charge in zip(names, charges):
            topology.addAtom(
                name,
                app.element.get_by_symbol(name),
                group,
                id=str(10 + topology.getNumAtoms()),
                formalCharge=charge,
            )
    atoms = list(topology.atoms())
    topology.addBond(atoms[0], atoms[1], type=app.Double, order=2)
    topology.addBond(atoms[1], atoms[2], type=app.Aromatic)
    topology.addBond(atoms[2], atoms[3], type=app.Single, order=1)
    box = np.array([[2.0, 0.0, 0.0], [0.2, 2.1, 0.0], [-0.1, 0.2, 2.2]])
    value, length_unit = (
        (box, unit.nanometer) if request.param == "nm" else (10 * box, unit.angstrom)
    )
    topology.setPeriodicBoxVectors(value * length_unit)
    return topology


def _snapshot(topology):
    return (
        [(c.index, c.id) for c in topology.chains()],
        [(r.index, r.id, r.insertionCode) for r in topology.residues()],
        [(a.index, a.name, a.id, a.formalCharge) for a in topology.atoms()],
        [(b[0].index, b[1].index, b.type, b.order) for b in topology.bonds()],
    )


@pytest.mark.parametrize(
    ("operation", "selection"),
    [
        ("copy", "all"),
        ("extract", "all"),
        ("identity", "all"),
        ("extract", [2, 3]),
        ("extract", [3, 1, 3]),
        ("identity", [3, 2]),
        ("extract", []),
        ("structure_compatibility", "all"),
        ("structure_compatibility", [3, 1]),
    ],
)
def test_copy_and_subset_preserve_chemical_labels_box_and_dense_axes(
    source, operation, selection
):
    from openmm import app, unit

    before = _snapshot(source)
    source_box = np.asarray(
        source.getPeriodicBoxVectors().value_in_unit(unit.nanometer)
    ).copy()
    if operation == "copy":
        result = msm.copy(source)
    elif operation == "identity":
        result = msm.convert(source, to_form="openmm.Topology", selection=selection)
    else:
        kwargs = (
            {"structure_indices": [2, 0, 2]}
            if operation == "structure_compatibility"
            else {}
        )
        result = msm.extract(source, selection=selection, **kwargs)

    indices = [0, 1, 2, 3] if selection == "all" else sorted(set(selection))
    groups = sorted({i // 2 for i in indices})
    atoms = list(result.atoms())
    assert result is not source
    assert [a.index for a in atoms] == list(range(len(indices)))
    assert [a.name for a in atoms] == [["N", "C", "O", "H"][i] for i in indices]
    assert [a.id for a in atoms] == [str(10 + i) for i in indices]
    assert [a.formalCharge for a in atoms] == [[1, 0, -1, None][i] for i in indices]
    assert [c.index for c in result.chains()] == list(range(len(groups)))
    assert [c.id for c in result.chains()] == [["A", "B"][i] for i in groups]
    assert [r.index for r in result.residues()] == list(range(len(groups)))
    assert [r.id for r in result.residues()] == [["07", "00"][i] for i in groups]
    assert [r.insertionCode for r in result.residues()] == [
        ["X", "Y"][i] for i in groups
    ]
    mapping = {old: new for new, old in enumerate(indices)}
    expected = [
        (mapping[a], mapping[b], kind, order)
        for a, b, kind, order in [
            (0, 1, app.Double, 2),
            (1, 2, app.Aromatic, None),
            (2, 3, app.Single, 1),
        ]
        if a in mapping and b in mapping
    ]
    assert [
        (b[0].index, b[1].index, b.type, b.order) for b in result.bonds()
    ] == expected
    np.testing.assert_allclose(
        result.getPeriodicBoxVectors().value_in_unit(unit.nanometer), source_box
    )
    if indices:
        atoms[0].name = "changed"
        atoms[0].formalCharge = 4
    result.setPeriodicBoxVectors(2 * source_box * unit.nanometer)
    assert _snapshot(source) == before
    np.testing.assert_allclose(
        source.getPeriodicBoxVectors().value_in_unit(unit.nanometer), source_box
    )


@pytest.mark.parametrize(
    "operation", ["copy", "extract", "identity", "structure_compatibility", "alias"]
)
def test_full_topology_copy_preserves_empty_inventory_parents(operation):
    pytest.importorskip("openmm")
    from openmm import app

    source = app.Topology()
    source.addResidue("SEQ", source.addChain("E"), id="000", insertionCode="I")
    source.addChain("F")
    if operation == "copy":
        result = msm.copy(source)
    elif operation == "identity":
        result = msm.convert(source, to_form="openmm.Topology")
    elif operation in {"structure_compatibility", "alias"}:
        result = msm.extract(
            source, structure_indices=[2, 0], copy_if_all=operation != "alias"
        )
    else:
        result = msm.extract(source)
    assert (result is source) == (operation == "alias")
    assert _snapshot(result) == _snapshot(source)
    assert result.getNumAtoms() == 0


def test_unrestricted_topology_alias_policy_does_not_depend_on_structure_compatibility(
    source,
):
    result = msm.extract(source, structure_indices=[2, 0], copy_if_all=False)
    assert result is source
