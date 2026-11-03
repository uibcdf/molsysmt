"""Keep edge-free OpenMM conversion finite and explicit about inference scope."""

import importlib

import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.fixture
def water():
    app = pytest.importorskip("openmm.app")

    topology = app.Topology()
    chain = topology.addChain("W")
    group = topology.addResidue("HOH", chain, id="7")
    for name, element in [
        ("O", app.element.oxygen),
        ("H1", app.element.hydrogen),
        ("H2", app.element.hydrogen),
    ]:
        topology.addAtom(name, element, group)
    return topology


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_edge_free_conversion_enters_the_native_reader_once(water, monkeypatch, target):
    module = importlib.import_module("molsysmt.form.openmm_Topology._read_native")
    original = module.read_native
    calls = []

    def bounded(*args, **kwargs):
        calls.append(args[0])
        if len(calls) > 1:
            raise RuntimeError(
                "A second read would recurse through the source converter"
            )
        return original(*args, **kwargs)

    monkeypatch.setattr(module, "read_native", bounded)
    result = msm.convert(water, to_form=target)
    assert calls == [water]
    assert msm.get(result, n_atoms=True, n_groups=True, n_chains=True) == [3, 1, 1]


def test_inference_uses_the_constructed_native_domain_without_geometry(
    water, monkeypatch
):
    original = msm.build.get_missing_bonds
    calls = []

    def observed(molecular_system, **kwargs):
        assert isinstance(molecular_system, MolSys)
        assert molecular_system.structures.coordinates is None
        assert kwargs["with_distances"] is False
        calls.append(molecular_system)
        return original(molecular_system, **kwargs)

    monkeypatch.setattr(msm.build, "get_missing_bonds", observed)
    result = msm.convert(water, to_form="molsysmt.MolSys")
    assert calls == [result]
    assert result.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[0, 1], [0, 2]]
    assert result.get(connectivity_completeness=True) == "partial"
    assert result.get(element="bond", bond_evidence=True) == ["inferred", "inferred"]
    assert water.getNumBonds() == 0


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_explicit_inference_opt_out_is_forwarded(water, monkeypatch, target):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(args)
        raise AssertionError("Inference was explicitly disabled")

    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    result = msm.convert(water, to_form=target, get_missing_bonds=False)
    assert not calls
    if target == "molsysmt.MolSys":
        assert result.get(n_bonds=True, connectivity_completeness=True) == [
            0,
            "complete",
        ]
    else:
        assert not hasattr(result, "bonds")


def test_existing_edges_bypass_inference_and_keep_explicit_evidence(water, monkeypatch):
    atoms = list(water.atoms())
    water.addBond(atoms[0], atoms[1])

    def forbidden(*args, **kwargs):
        pytest.fail("Declared bonds must not invoke empty-graph inference")

    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    result = msm.convert(water, to_form="molsysmt.MolSys")
    assert result.get(n_bonds=True) == 1
    assert result.get(element="bond", bond_evidence=True) == ["explicit"]
    assert water.getNumBonds() == 1


def test_bulk_inventory_queries_do_not_infer_bonds(water, monkeypatch):
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(args)
        raise AssertionError("Inventory piping must not request bond inference")

    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    result = msm.get(
        water,
        element="group",
        group_name=True,
        atom_index=True,
        output_type="dictionary",
    )
    assert set(result) == {"group_name", "atom_index"}
    assert result["group_name"] == ["HOH"]
    assert len(result["atom_index"]) == 1
    assert list(result["atom_index"][0]) == [0, 1, 2]
    assert not calls


def test_unknown_group_without_coordinates_keeps_unavailable_connectivity(water):
    next(water.residues()).name = "ZZZ"
    result = msm.convert(water, to_form="molsysmt.MolSys")
    assert result.get(n_atoms=True, n_bonds=True, connectivity_completeness=True) == [
        3,
        0,
        "unavailable",
    ]
    assert result.structures.coordinates is None
    assert water.getNumBonds() == 0


@pytest.mark.parametrize("failure", [MemoryError, RuntimeError])
def test_inference_failures_are_not_silently_discarded(water, monkeypatch, failure):
    error = failure("Cannot complete template inference")

    def failed(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm.build, "get_missing_bonds", failed)
    with pytest.raises(failure) as captured:
        msm.convert(water, to_form="molsysmt.MolSys")
    assert captured.value is error
    assert water.getNumAtoms() == 3
    assert water.getNumBonds() == 0
