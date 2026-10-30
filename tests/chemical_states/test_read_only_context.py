"""Read-only chemical graph queries must not copy unrelated coordinate domains."""

from functools import wraps

import numpy as np
import pytest

import molsysmt as msm


def _cycle():
    builder = msm.MolSysBuilder()
    for i in range(6):
        builder.add_atom(atom_id=str(i), atom_name=f"C{i}", atom_type="C")
    for i in range(6):
        builder.add_bond(i, (i + 1) % 6, bond_type="covalent", bond_order=1)
    builder.set_coordinates(msm.pyunitwizard.quantity(np.zeros((3, 6, 3)), "nm"))
    molsys = builder.build()
    molsys.chemical_states._states[0].connectivity_completeness = "complete"
    return molsys


@pytest.mark.parametrize(
    "domains",
    ["chemistry", "inventory", "coordinates", "all", "dict_coordinates", "dict_all"],
)
def test_ring_queries_borrow_native_domains_without_copying_or_rebinding(
    monkeypatch, domains
):
    molsys = _cycle()
    source = {
        "chemistry": molsys.chemical_states,
        "inventory": [molsys.topology, molsys.chemical_states],
        "coordinates": [molsys.chemical_states, molsys.structures],
        "all": [molsys.topology, molsys.chemical_states, molsys.structures],
        "dict_coordinates": [
            msm.convert(molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"),
            molsys.structures,
        ],
        "dict_all": [
            molsys.topology,
            msm.convert(molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict"),
            molsys.structures,
        ],
    }[domains]
    owners = [
        domain._molsys_owner_ref()
        for domain in (molsys.topology, molsys.chemical_states, molsys.structures)
    ]

    def reject(*args, **kwargs):
        raise AssertionError("A read-only ring query must not clone native domains.")

    monkeypatch.setattr(type(molsys.chemical_states), "__deepcopy__", reject)
    monkeypatch.setattr(type(molsys.structures), "__deepcopy__", reject)
    monkeypatch.setattr(type(molsys.topology), "__deepcopy__", reject)
    result = msm.chemical_states.get_rings(source)
    assert result["atom_indices"].tolist() == list(range(6))
    assert result["atom_offsets"].tolist() == [0, 6]
    assert [
        domain._molsys_owner_ref()
        for domain in (molsys.topology, molsys.chemical_states, molsys.structures)
    ] == owners


@pytest.mark.parametrize("with_coordinates", [False, True])
def test_state_only_predicates_select_the_requested_state_without_inventory(
    with_coordinates,
):
    molsys = _cycle()
    states = molsys.chemical_states
    states.append_state()
    msm.set(states, chemical_state=0, formal_charge=[0, 1, -1, 0, 0, 0])
    msm.set(states, chemical_state=1, formal_charge=[-1, 0, 1, 0, 0, 0])
    source = [states, molsys.structures] if with_coordinates else states
    assert msm.select(source, "formal_charge!=0", chemical_state=1) == [0, 2]
    assert msm.select(source, "formal_charge!=0", chemical_state=0) == [1, 2]
    assert states.reference_chemical_state_index == 0


@pytest.fixture
def universe():
    mda = pytest.importorskip("MDAnalysis")
    source = mda.Universe.empty(6, n_residues=1, atom_resindex=[0] * 6, trajectory=True)
    for name, values in {
        "names": [f"C{i}" for i in range(6)],
        "elements": ["C"] * 6,
        "types": ["C"] * 6,
        "ids": list(range(6)),
        "resnames": ["LIG"],
        "resids": [1],
        "segids": ["A"],
        "bonds": [(i, (i + 1) % 6) for i in range(6)],
    }.items():
        source.add_TopologyAttr(name, values)
    source.load_new(np.zeros((5, 6, 3), dtype=np.float32), order="fac")
    source.trajectory[2]
    return source


@pytest.mark.parametrize("indices", ["all", [4, 1, 4]])
def test_numeric_ring_queries_on_foreign_forms_omit_structural_conversion(
    universe, monkeypatch, indices
):
    from molsysmt.form import _dict_modules, load_converter

    module = _dict_modules["MDAnalysis.Universe"]
    original = load_converter(module, module._convert_to["molsysmt.MolSys"])
    calls = []

    @wraps(original)
    def observed(item, **kwargs):
        requested = kwargs.get("structure_indices", "all")
        calls.append(requested)
        assert not isinstance(requested, str) and len(requested) == 0
        return original(item, **kwargs)

    monkeypatch.setitem(module._convert_to, "molsysmt.MolSys", observed)
    result = msm.chemical_states.get_rings(
        universe,
        selection=[5, 4, 3, 2, 1, 0],
        structure_indices=indices,
        assume_complete_connectivity=True,
    )
    assert len(calls) == 1
    assert result["atom_indices"].tolist() == list(range(6))
    assert result["atom_offsets"].tolist() == [0, 6]
    assert universe.trajectory.frame == 2


def test_invalid_foreign_structure_scope_rejects_before_chemical_conversion(
    universe, monkeypatch
):
    from molsysmt.form import _dict_modules

    def reject(*args, **kwargs):
        raise AssertionError("Validate the original structure axis before converting.")

    monkeypatch.setitem(
        _dict_modules["MDAnalysis.Universe"]._convert_to, "molsysmt.MolSys", reject
    )
    with pytest.raises(msm.ArgumentError):
        msm.chemical_states.get_rings(
            universe, structure_indices=[5], assume_complete_connectivity=True
        )


@pytest.mark.parametrize(
    "tool",
    [
        "aromaticity",
        "torsions",
        "tpsa",
        "lipophilicity",
        "typing",
        "charges",
        "stereochemistry",
        "hbond_sites",
    ],
)
@pytest.mark.parametrize("indices", ["all", [3, 1, 3]])
def test_graph_only_calculators_do_not_convert_foreign_conformers(
    monkeypatch, tool, indices
):
    from rdkit import Chem

    from molsysmt import pyunitwizard as puw
    from molsysmt.form import _dict_modules, load_converter

    source = Chem.AddHs(Chem.MolFromSmiles("c1ccccc1"))
    for _ in range(4):
        source.AddConformer(Chem.Conformer(source.GetNumAtoms()), assignId=True)
    module = _dict_modules["rdkit.Mol"]
    original = load_converter(module, module._convert_to["molsysmt.MolSys"])
    calls = []

    @wraps(original)
    def observed(item, **kwargs):
        scope = kwargs.get("structure_indices", "all")
        calls.append(scope)
        assert not isinstance(scope, str) and len(scope) == 0
        return original(item, **kwargs)

    monkeypatch.setitem(module._convert_to, "molsysmt.MolSys", observed)
    kwargs = dict(structure_indices=indices)
    if tool == "aromaticity":
        result = msm.physchem.get_aromaticity(source, **kwargs)
        assert result["atom_is_aromatic"].tolist() == [True] * 6 + [False] * 6
    elif tool == "torsions":
        result = msm.chemical_states.get_rotatable_bonds(source, **kwargs)
        assert result["rotatable_bond_indices"].tolist() == []
    elif tool == "tpsa":
        result = msm.physchem.get_tpsa(source, **kwargs)
        np.testing.assert_allclose(puw.get_value(result, to_unit="angstrom**2"), [0.0])
    elif tool == "lipophilicity":
        result = msm.physchem.get_lipophilicity(source, **kwargs)
        np.testing.assert_allclose(result, [1.6866], atol=1e-8)
    elif tool == "typing":
        result = msm.physchem.get_autodock_atom_types(
            source, typing_scheme="autodock4", **kwargs
        )
        assert len(result) == 12
    elif tool == "stereochemistry":
        result = msm.physchem.get_cip_stereochemistry(source, **kwargs)
        assert result["atom_stereochemistry"].tolist() == [None] * 12
    elif tool == "hbond_sites":
        result = msm.interactions.hbonds.get_hbond_sites(source, **kwargs)
        assert result["acceptor_atom_indices"].tolist() == []
    else:
        result = msm.physchem.get_partial_charges(
            source, method="gasteiger_marsili", **kwargs
        )
        values = puw.get_value(result, to_unit="elementary_charge")
        assert values.shape == (12,)
        np.testing.assert_allclose(values.sum(), 0.0, atol=1e-10)
    assert calls
    assert source.GetNumConformers() == 4
