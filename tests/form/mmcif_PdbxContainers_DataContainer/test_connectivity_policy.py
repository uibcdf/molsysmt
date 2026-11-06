"""Keeping declared CIF connectivity distinct from optional reader inference."""

import builtins
import importlib
from copy import deepcopy

import numpy as np
import pytest
from mmcif.api.DataCategory import DataCategory

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

from .test_primary_occupancy import _as_file, _container


def _declared_source():
    source = _container([[0.8, 1.0], [0.7, 0.6], [0.9, 0.5]])
    source.append(
        DataCategory(
            "chem_comp_bond",
            attributeNameList=["comp_id", "atom_id_1", "atom_id_2", "value_order"],
            rowList=[["LIG", "C1", "O1", "DOUB"]],
        )
    )
    return source


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_disabled_inference_never_calls_candidate_tools(
    tmp_path, monkeypatch, form, target
):
    source = _container([[0.8, 1.0]])
    original = deepcopy(source.getObj("atom_site").getRowList())
    item = source if form == "container" else _as_file(source, tmp_path, form)
    before = None if form == "container" else item.read_bytes()

    def forbidden(*args, **kwargs):
        raise AssertionError("Disabled reader inference called a candidate tool")

    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    monkeypatch.setattr(msm.element.group, "get_bonded_atom_pairs", forbidden)
    result = msm.convert(item, to_form=target, get_missing_bonds=False)
    topology = result.topology if target == "molsysmt.MolSys" else result
    assert topology.atoms.atom_name.tolist() == ["C1", "O1"]
    assert topology.atoms.atom_id.tolist() == ["1", "2"]
    assert source.getObj("atom_site").getRowList() == original
    if before is not None:
        assert item.read_bytes() == before
    if target == "molsysmt.MolSys":
        assert msm.get(result, n_bonds=True) == 0
        assert msm.get(result, connectivity_completeness=True) == "partial"


@pytest.mark.parametrize("form", ["container", "cif", "cif.gz", "bcif", "bcif.gz"])
def test_explicit_bonds_and_observations_survive_disabled_inference(tmp_path, form):
    source = _declared_source()
    item = source if form == "container" else _as_file(source, tmp_path, form)
    with puw.context(standard_units=["angstrom", "fs"]):
        result = msm.convert(
            item, get_missing_bonds=False, structure_indices=[2, 0], selection=[1, 0]
        )
    # The external reader retains selected atoms in source order.
    assert result.topology.atoms.atom_name.tolist() == ["C1", "O1"]
    assert result.topology.atoms.atom_id.tolist() == ["1", "2"]
    assert result.structures.n_structures == 2
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        [[[3.0, 0, 0], [3.1, 0, 0]], [[1.0, 0, 0], [1.1, 0, 0]]],
    )
    np.testing.assert_allclose(result.structures.occupancy, [[0.9, 0.5], [0.8, 1.0]])
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert bonds.bond_order.tolist() == [2.0]
    assert bonds.evidence.tolist() == ["explicit"]


def test_partial_reference_mapping_retains_each_declared_edge(monkeypatch):
    source = _container([[0.8, 1.0]])
    category = source.getObj("atom_site")
    row = list(category.getRowList()[0])
    columns = {name: i for i, name in enumerate(category.getAttributeList())}
    for name, value in {
        "id": "3",
        "type_symbol": "H",
        "label_atom_id": "HX",
        "auth_atom_id": "HX",
    }.items():
        row[columns[name]] = value
    category.append(row)
    source.append(
        DataCategory(
            "chem_comp_bond",
            attributeNameList=["comp_id", "atom_id_1", "atom_id_2", "value_order"],
            rowList=[["LIG", "C1", "O1", "DOUB"]],
        )
    )
    # A candidate method returning no extra edges cannot erase deposited evidence.
    monkeypatch.setattr(msm.build, "get_missing_bonds", lambda *args, **kwargs: [])
    result = msm.convert(source)
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert bonds.bond_order.tolist() == [2.0]
    assert bonds.evidence.tolist() == ["explicit"]


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_public_identifier_forwards_disabled_policy_without_download(
    monkeypatch, target
):
    source = _container([[0.8, 1.0]])
    reader = importlib.import_module(
        "molsysmt.form.string_pdb_id.to_mmcif_PdbxContainers_DataContainer"
    )
    requested = []

    def local_source(item, **kwargs):
        requested.append(item)
        return source

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Disabled identifier reading invoked connectivity inference"
        )

    monkeypatch.setattr(reader, "to_mmcif_PdbxContainers_DataContainer", local_source)
    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    monkeypatch.setattr(msm.element.group, "get_bonded_atom_pairs", forbidden)
    result = msm.convert("1abc", to_form=target, get_missing_bonds=False)
    assert requested == ["1abc"]
    topology = result.topology if target == "molsysmt.MolSys" else result
    assert topology.n_atoms == 2


@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("policy", [None, 0, "False"])
def test_policy_rejects_nonbooleans_before_inference(monkeypatch, target, policy):
    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid policy reached connectivity inference")

    monkeypatch.setattr(msm.build, "get_missing_bonds", forbidden)
    with pytest.raises(ArgumentError) as error:
        msm.convert(_container([[0.8, 1.0]]), to_form=target, get_missing_bonds=policy)
    assert error.value.extra["argument"] == "get_missing_bonds"


def test_disabled_real_bcif_has_only_deposited_edges_and_no_optional_engine(
    monkeypatch,
):
    source = msm.systems["chicken villin HP35"]["1vii.bcif.gz"]
    ordinary_import = builtins.__import__

    def no_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            raise AssertionError("Explicit-only BCIF reading imported OpenMM")
        return ordinary_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_openmm)
    result = msm.convert(source, get_missing_bonds=False)
    bonds = result.chemical_states.get_bonds()
    assert result.topology.n_atoms == 596
    assert len(bonds) > 0
    assert set(bonds.evidence) == {"explicit"}
    assert msm.get(result, connectivity_completeness=True) == "partial"


def test_omitted_and_true_policy_have_the_same_graph_and_observations():
    source = msm.systems["chicken villin HP35"]["1vii.bcif.gz"]
    default = msm.convert(source)
    explicit = msm.convert(source, get_missing_bonds=True)
    assert default.topology.atoms.equals(explicit.topology.atoms)
    assert default.chemical_states.get_bonds().equals(
        explicit.chemical_states.get_bonds()
    )
    assert "inferred" in set(default.chemical_states.get_bonds().evidence)
    np.testing.assert_equal(
        puw.get_value(default.structures.coordinates, to_unit="nm"),
        puw.get_value(explicit.structures.coordinates, to_unit="nm"),
    )
