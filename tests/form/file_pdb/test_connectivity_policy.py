"""Protecting explicit PDB connectivity policy across public native routes."""

import builtins
import importlib
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentConflictError,
    ArgumentError,
    PDBBondInferenceWarning,
)
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


@pytest.mark.parametrize("to_form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("route", ["file", "handler", "text"])
def test_explicit_native_reader_preserves_declared_edges_without_openmm(
    declared_181l,
    monkeypatch,
    tmp_path,
    to_form,
    route,
):
    path, text, serials, declared, coordinates = declared_181l
    original = builtins.__import__

    def reject(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("Native PDB inference imported OpenMM")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject)
    handler = (
        msm.convert(path, to_form="molsysmt.PDBFileHandler")
        if route == "handler"
        else None
    )
    item = handler if handler is not None else text if route == "text" else path
    try:
        with msm.pyunitwizard.context(standard_units=["pm", "ps"]):
            output = msm.convert(
                item,
                to_form=to_form,
                get_missing_bonds=True,
                bond_inference_engine="molsysmt",
            )
        assert msm.get(output, element="atom", atom_id=True) == serials
        bonds = _bonds(output)
        assert len(bonds) == 1322
        by_pair = {
            tuple(pair): index
            for index, pair in enumerate(
                bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
            )
        }
        assert all(
            bonds.iloc[by_pair[pair]]["evidence"] == "explicit" for pair in declared
        )
        assert bonds["evidence"].eq("inferred").sum() == 1309
        states = (
            output.chemical_states
            if isinstance(output, MolSys)
            else output._chemical_states_domain
        )
        history = states.get_preparation_history()
        assert [record["report"]["schema"] for record in history] == [
            "molsysmt.pdb_connectivity@1",
            "molsysmt.covalent_inference@1",
        ]
        assert history[0]["report"]["status"] == "disabled"
        assert history[1]["report"]["engine"] == "MolSysMT"
        assert (
            bonds.loc[bonds["evidence"].eq("inferred"), "provenance_index"].tolist()
            == [1] * 1309
        )
        if isinstance(output, MolSys):
            np.testing.assert_allclose(
                msm.pyunitwizard.get_value(
                    output.structures.coordinates, to_unit="angstrom"
                )[0],
                coordinates,
                rtol=0,
                atol=1e-10,
            )
            filename = str(tmp_path / "native.h5msm")
            msm.convert(output, to_form=filename)
            loaded = msm.convert(filename, to_form="molsysmt.MolSys")
            assert len(loaded.chemical_states.get_preparation_history()) == 2
            assert (
                loaded.chemical_states.get_preparation_history()[1]["report"][
                    "software"
                ]
                == history[1]["report"]["software"]
            )
        assert path.read_text() == text
    finally:
        if handler is not None:
            assert not handler.file.closed
            handler.close()


@pytest.mark.parametrize("status", ["unavailable", "failed"])
def test_legacy_failure_warns_and_archives_cause_but_explicit_engine_raises(
    declared_181l, monkeypatch, status
):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    error = (
        ModuleNotFoundError("Missing OpenMM control", name="openmm")
        if status == "unavailable"
        else RuntimeError("Broken engine control")
    )

    def fail(item):
        raise error

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", fail)
    with pytest.warns(PDBBondInferenceWarning, match=status):
        output = msm.convert(declared_181l[0], to_form="molsysmt.MolSys")
    assert len(output.topology.bonds) == 13
    report = output.chemical_states.get_preparation_history()[0]["report"]
    assert report["status"] == status
    assert report["attempted_engine"] == "OpenMM"
    assert report["actual_engine"] is None
    assert report["error"]["type"] == type(error).__name__
    with pytest.raises(type(error), match=str(error)):
        msm.convert(
            declared_181l[0], to_form="molsysmt.MolSys", bond_inference_engine="OpenMM"
        )


@pytest.mark.parametrize("engine", [True, "rdkit", "auto"])
def test_unknown_pdb_engine_is_rejected(declared_181l, engine):
    with pytest.raises(ArgumentError):
        msm.convert(
            declared_181l[0], to_form="molsysmt.MolSys", bond_inference_engine=engine
        )


def test_disabled_inference_cannot_silently_ignore_an_explicit_engine(declared_181l):
    with pytest.raises(ArgumentConflictError):
        msm.convert(
            declared_181l[0],
            to_form="molsysmt.MolSys",
            get_missing_bonds=False,
            bond_inference_engine="MolSysMT",
        )


def test_native_selected_atoms_keep_historical_indices_and_remap_current_bonds(
    declared_181l,
):
    path, _, serials, _, _ = declared_181l
    selected = [6, 0, 1]
    output = msm.convert(
        path,
        to_form="molsysmt.MolSys",
        selection=selected,
        bond_inference_engine="MolSysMT",
    )
    # Public atom selection normalizes explicit lists to unique source order.
    assert msm.get(output, element="atom", atom_id=True) == [
        serials[index] for index in [0, 1, 6]
    ]
    history = output.chemical_states.get_preparation_history()
    assert history[-1]["output"]["n_atoms"] == len(serials)
    assert history[-1]["index_scope"] == "operation"
    assert output.topology.bonds[["atom1_index", "atom2_index"]].to_numpy().max(
        initial=0
    ) < len(selected)
