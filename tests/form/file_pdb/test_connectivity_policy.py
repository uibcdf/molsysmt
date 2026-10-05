"""Protecting explicit PDB connectivity policy across public native routes."""

import builtins
import importlib
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys


@pytest.fixture(scope="module")
def declared_181l():
    path = Path(msm.systems["T4 lysozyme L99A"]["181l.pdb"])
    text = path.read_text()
    lines = text.splitlines()
    atoms = [line for line in lines if line.startswith(("ATOM  ", "HETATM"))]
    assert all(not line[16].strip() for line in atoms)
    serials = [str(int(line[6:11])) for line in atoms]
    assert len(set(serials)) == len(serials)
    indices = {serial: index for index, serial in enumerate(serials)}
    pairs = set()
    for line in lines:
        if line.startswith("CONECT"):
            serial = str(int(line[6:11]))
            for start in (11, 16, 21, 26):
                field = line[start : start + 5].strip()
                if field:
                    pairs.add(
                        tuple(sorted((indices[serial], indices[str(int(field))])))
                    )
    assert len(pairs) == 13
    coordinates = np.asarray(
        [[float(line[start : start + 8]) for start in (30, 38, 46)] for line in atoms]
    )
    return path, text, serials, sorted(pairs), coordinates


def _bonds(output):
    return output.topology.bonds if isinstance(output, MolSys) else output.bonds


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("route", ["file", "handler", "text"])
def test_disabled_inference_preserves_literal_edges_and_does_not_call_engine(
    declared_181l, monkeypatch, to_form, route
):
    path, text, serials, pairs, coordinates = declared_181l
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    calls = []

    def spy(item):
        calls.append(item)
        return [(0, 1)]

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", spy)
    handler = None
    item = str(path)
    if route == "handler":
        handler = msm.convert(path, to_form="molsysmt.PDBFileHandler")
        item = handler
    elif route == "text":
        item = text
    try:
        with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
            output = msm.convert(item, to_form=to_form, get_missing_bonds=False)
        assert calls == []
        assert msm.get(output, element="atom", atom_id=True) == serials
        bonds = _bonds(output)
        assert (
            bonds[["atom1_index", "atom2_index"]].to_records(index=False).tolist()
            == pairs
        )
        assert bonds["evidence"].tolist() == ["explicit"] * 13
        if to_form == "molsysmt.MolSys":
            values = msm.pyunitwizard.get_value(
                output.structures.coordinates, to_unit="angstrom"
            )
            np.testing.assert_allclose(values[0], coordinates, rtol=0, atol=1e-10)
            assert values.shape == (1, len(serials), 3)
        assert path.read_text() == text
    finally:
        if handler is not None:
            assert not handler.file.closed
            handler.close()


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("explicit_option", [False, True])
def test_default_and_enabled_policy_preserve_engine_edges_and_declared_evidence(
    declared_181l, monkeypatch, to_form, explicit_option
):
    path, _, _, pairs, _ = declared_181l
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    calls = []

    def spy(item):
        calls.append(item)
        return [(0, 1), pairs[0]]

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", spy)
    options = {"get_missing_bonds": True} if explicit_option else {}
    output = msm.convert(path, to_form=to_form, **options)
    assert len(calls) == 1
    bonds = _bonds(output)
    assert bonds[["atom1_index", "atom2_index"]].to_records(
        index=False
    ).tolist() == sorted([(0, 1), *pairs])
    assert bonds["evidence"].tolist() == ["inferred", *(["explicit"] * 13)]


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_disabled_policy_survives_atom_selection(declared_181l, to_form):
    path, _, serials, pairs, coordinates = declared_181l
    selected = sorted({atom for pair in pairs for atom in pair})
    local_indices = {atom: index for index, atom in enumerate(selected)}
    expected = [(local_indices[a], local_indices[b]) for a, b in pairs]
    output = msm.convert(
        path, to_form=to_form, selection=selected, get_missing_bonds=False
    )
    assert msm.get(output, element="atom", atom_id=True) == [
        serials[index] for index in selected
    ]
    assert (
        _bonds(output)[["atom1_index", "atom2_index"]].to_records(index=False).tolist()
        == expected
    )
    if to_form == "molsysmt.MolSys":
        values = msm.pyunitwizard.get_value(
            output.structures.coordinates, to_unit="angstrom"
        )
        np.testing.assert_allclose(values[0], coordinates[selected], rtol=0, atol=1e-10)


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_disabled_policy_does_not_attempt_optional_imports(
    declared_181l, monkeypatch, to_form
):
    path, _, _, pairs, _ = declared_181l
    original_import = builtins.__import__
    attempted = []

    def block_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            attempted.append(name)
            raise ModuleNotFoundError("OpenMM is blocked in this control")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", block_openmm)
    output = msm.convert(path, to_form=to_form, get_missing_bonds=False)
    assert attempted == []
    assert (
        _bonds(output)[["atom1_index", "atom2_index"]].to_records(index=False).tolist()
        == pairs
    )


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("value", [None, 0, "False"])
def test_policy_is_validated_at_public_boundary(declared_181l, to_form, value):
    with pytest.raises(ArgumentError):
        msm.convert(declared_181l[0], to_form=to_form, get_missing_bonds=value)


@pytest.mark.parametrize("name", ["to_molsysmt_MolSys", "to_molsysmt_Topology"])
def test_adapter_preserves_positional_skip_argument(declared_181l, name):
    module = importlib.import_module("molsysmt.form.file_pdb." + name)
    converter = getattr(module, name)
    arguments = [str(declared_181l[0]), "all"]
    if name == "to_molsysmt_MolSys":
        arguments.append("all")
    arguments.append(True)
    output = converter(*arguments, get_missing_bonds=False)
    assert len(_bonds(output)) == 13


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_reader_owned_handler_closes_after_delegated_failure(
    declared_181l, monkeypatch, to_form
):
    factory = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler"
    )
    builder = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    original_factory = factory.to_molsysmt_PDBFileHandler
    handlers = []

    def capture(*args, **kwargs):
        handler = original_factory(*args, **kwargs)
        handlers.append(handler)
        return handler

    def fail(*args, **kwargs):
        raise RuntimeError("Injected conversion failure")

    monkeypatch.setattr(factory, "to_molsysmt_PDBFileHandler", capture)
    monkeypatch.setattr(builder, "_build_topology_from_content", fail)
    with pytest.raises(RuntimeError, match="Injected conversion failure"):
        msm.convert(declared_181l[0], to_form=to_form, get_missing_bonds=False)
    assert len(handlers) == 1
    assert handlers[0].file.closed
    assert declared_181l[0].read_text() == declared_181l[1]
