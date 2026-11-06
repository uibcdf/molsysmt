"""Checking declared PDB vocabulary before classification and native inference."""

import importlib
import inspect
from contextlib import contextmanager

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    NotImplementedMethodError,
    PDBBondInferenceWarning,
)
from molsysmt.native import MolSys, Topology
from tests.build.test_terminal_cap_covalent_candidates import _cap_pdb

EXPECTED_CAP_PAIRS = [
    [0, 1],
    [1, 2],
    [1, 3],
    [3, 4],
    [4, 5],
    [4, 7],
    [5, 6],
    [5, 8],
    [8, 9],
]


@contextmanager
def _source(text, route, tmp_path):
    filename = tmp_path / "context.pdb"
    filename.write_text(text)
    handler = None
    item = str(filename)
    if route == "text":
        item = text
    elif route == "handler":
        item = handler = msm.convert(filename, to_form="molsysmt.PDBFileHandler")
    try:
        yield item
        assert filename.read_text() == text
        if handler is not None:
            assert not handler.file.closed
    finally:
        if handler is not None:
            handler.close()


def _hid_pdb():
    # This intentionally tests declared label interpretation, not a complete
    # chemical inventory of either distinct compound named HID.
    lines = []
    for serial, (name, element) in enumerate(
        zip(["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"]), 1
    ):
        x = serial * 1.2
        lines.append(
            f"ATOM  {serial:5d} {name:^4} HID A  17    {x:8.3f}{0.0:8.3f}{0.0:8.3f}{1.0:6.2f}{0.0:6.2f}          {element:>2}  "
        )
    return "\n".join([*lines, "END", ""])


@pytest.mark.parametrize("route", ["file", "text", "handler"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_cap_context_reaches_native_inference_before_any_output_projection(
    route, target, tmp_path, monkeypatch
):
    original = msm.build.infer_covalent_bonds
    calls = []

    def receive(molsys, **kwargs):
        assert molsys.topology.group_naming_schemes == ("amber",) * 3
        output = original(molsys, **kwargs)
        calls.append(
            output.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
            .to_numpy()
            .tolist()
        )
        return output

    monkeypatch.setattr(msm.build, "infer_covalent_bonds", receive)
    with _source(_cap_pdb(), route, tmp_path) as source:
        output = msm.convert(
            source,
            to_form=target,
            get_missing_bonds=True,
            bond_inference_engine="MolSysMT",
            from_naming_scheme="amber",
        )
    topology = output if isinstance(output, Topology) else output.topology
    assert topology.group_naming_schemes == ("amber",) * 3
    assert topology.atoms.atom_id.tolist() == [str(i) for i in range(1, 11)]
    assert calls == [EXPECTED_CAP_PAIRS]
    if isinstance(output, MolSys):
        history = output.chemical_states.get_preparation_history()
        assert history[0]["report"]["source_naming_scheme"] == "amber"
        assert (
            history[-1]["report"]["heavy_groups"][0]["template"]["naming_scheme"]
            == "amber"
        )
    else:
        assert not hasattr(output, "bonds")


@pytest.mark.parametrize(
    "scheme,kind",
    [(None, "unknown"), ("amber", "amino acid"), ("ccd", "small molecule")],
)
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize("route", ["file", "text", "handler"])
def test_explicit_context_precedes_group_classification_without_inference(
    scheme, kind, target, route, tmp_path
):
    with _source(_hid_pdb(), route, tmp_path) as source:
        output = msm.convert(
            source, to_form=target, get_missing_bonds=False, from_naming_scheme=scheme
        )
    topology = output if isinstance(output, Topology) else output.topology
    assert topology.groups.group_name.tolist() == ["HID"]
    assert topology.groups.group_type.tolist() == [kind]
    assert topology.group_naming_schemes == (scheme,)


@pytest.mark.parametrize("route", ["file", "text", "handler"])
@pytest.mark.parametrize("scheme,expected", [("amber", 5), ("ccd", 0)])
def test_semantic_selection_uses_declared_context_before_selecting_atoms(
    route, scheme, expected, tmp_path
):
    with _source(_hid_pdb(), route, tmp_path) as source:
        output = msm.convert(
            source,
            get_missing_bonds=False,
            from_naming_scheme=scheme,
            selection="group_type=='amino acid'",
        )
    assert output.topology.n_atoms == expected
    assert output.topology.group_naming_schemes == ((scheme,) if expected else ())


@pytest.mark.parametrize("route", ["file", "text", "handler"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_direct_converter_validates_the_source_scheme(route, target, tmp_path):
    source_module = {
        "file": "file_pdb",
        "text": "string_pdb_text",
        "handler": "molsysmt_PDBFileHandler",
    }[route]
    function = getattr(
        importlib.import_module(
            f"molsysmt.form.{source_module}.to_{target.replace('.', '_')}"
        ),
        f"to_{target.replace('.', '_')}",
    )
    with _source(_cap_pdb(), route, tmp_path) as source:
        with pytest.raises(ArgumentChoiceError) as failure:
            function(source, get_missing_bonds=False, from_naming_scheme="AMBER")
    assert failure.value.extra["argument"] == "from_naming_scheme"


def test_one_handler_can_supply_independent_naming_interpretations(tmp_path):
    with _source(_hid_pdb(), "handler", tmp_path) as source:
        first = msm.convert(source, get_missing_bonds=False, from_naming_scheme="amber")
        second = msm.convert(source, get_missing_bonds=False, from_naming_scheme="ccd")
        third = msm.convert(source, get_missing_bonds=False)
    assert first.topology.groups.group_type.tolist() == ["amino acid"]
    assert second.topology.groups.group_type.tolist() == ["small molecule"]
    assert third.topology.groups.group_type.tolist() == ["unknown"]
    assert first.topology.group_naming_schemes == ("amber",)


def test_explicit_cap_context_and_history_survive_h5msm_roundtrip(tmp_path):
    molsys = msm.convert(
        _cap_pdb(),
        get_missing_bonds=True,
        bond_inference_engine="MolSysMT",
        from_naming_scheme="amber",
    )
    filename = str(tmp_path / "context.h5msm")
    msm.convert(molsys, to_form=filename)
    loaded = msm.convert(filename)
    assert loaded.topology.group_naming_schemes == ("amber",) * 3
    assert (
        loaded.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
        .to_numpy()
        .tolist()
        == EXPECTED_CAP_PAIRS
    )
    loaded.topology.set_group_naming_schemes("legacy")
    assert (
        loaded.chemical_states.get_preparation_history()[0]["report"][
            "source_naming_scheme"
        ]
        == "amber"
    )


@pytest.mark.parametrize("scheme", ["amber", "ccd"])
def test_contextual_external_inference_requires_an_adapter_and_never_runs_implicitly(
    scheme, monkeypatch
):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )

    def reject(*args, **kwargs):
        pytest.fail("Unsupported source interpretation reached OpenMM")

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", reject)
    with pytest.raises(NotImplementedMethodError):
        msm.convert(
            _hid_pdb(),
            get_missing_bonds=True,
            bond_inference_engine="OpenMM",
            from_naming_scheme=scheme,
        )
    with pytest.warns(PDBBondInferenceWarning):
        output = msm.convert(
            _hid_pdb(), get_missing_bonds=True, from_naming_scheme=scheme
        )
    assert output.chemical_states.get_bonds().empty
    report = output.chemical_states.get_preparation_history()[0]["report"]
    assert report["status"] == "failed"
    assert report["error"]["type"] == "NotImplementedMethodError"
    assert report["source_naming_scheme"] == scheme


def test_openmm_does_not_reinterpret_ccd_cap_labels_as_legacy_caps(monkeypatch):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )

    def reject(*args, **kwargs):
        pytest.fail("Unsupported CCD cap interpretation reached OpenMM")

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", reject)
    with pytest.raises(NotImplementedMethodError):
        msm.convert(
            _cap_pdb(),
            get_missing_bonds=True,
            bond_inference_engine="OpenMM",
            from_naming_scheme="ccd",
        )


def test_output_selection_does_not_hide_contextual_labels_from_full_source_inference(
    monkeypatch,
):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )

    def reject(*args, **kwargs):
        pytest.fail(
            "Output filtering hid unsupported source naming from the engine boundary"
        )

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", reject)
    with pytest.raises(NotImplementedMethodError):
        msm.convert(
            _cap_pdb().replace("ACE", "HID"),
            selection="group_name=='ALA'",
            from_naming_scheme="amber",
            get_missing_bonds=True,
            bond_inference_engine="OpenMM",
        )


@pytest.mark.parametrize("engine", [None, "OpenMM"])
def test_supported_declared_context_keeps_optional_and_explicit_external_dispatch(
    engine, monkeypatch
):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    calls = []

    def external(item):
        calls.append(item)
        return [(1, 3)]

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", external)
    output = msm.convert(
        _cap_pdb(),
        get_missing_bonds=True,
        bond_inference_engine=engine,
        from_naming_scheme="amber",
    )
    assert len(calls) == 1
    assert output.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].to_numpy().tolist() == [[1, 3]]
    report = output.chemical_states.get_preparation_history()[0]["report"]
    assert report["actual_engine"] == "OpenMM"
    assert report["source_naming_scheme"] == "amber"


@pytest.mark.parametrize("engine", ["MolSysMT", "OpenMM"])
def test_actual_engines_match_the_independent_literal_capped_peptide_graph(engine):
    if engine == "OpenMM":
        pytest.importorskip("openmm")
    output = msm.convert(
        _cap_pdb(),
        get_missing_bonds=True,
        bond_inference_engine=engine,
        from_naming_scheme="amber",
    )
    assert (
        output.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
        .to_numpy()
        .tolist()
        == EXPECTED_CAP_PAIRS
    )


@pytest.mark.parametrize("route", ["file", "text", "handler"])
def test_declared_name_projection_does_not_run_automatic_bond_inference(
    route, tmp_path, monkeypatch
):
    from molsysmt._private import amino_acid_templates

    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )

    def reject(*args, **kwargs):
        pytest.fail("A name-only projection requested bond inference")

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", reject)
    monkeypatch.setattr(msm.build, "infer_covalent_bonds", reject)
    monkeypatch.setattr(amino_acid_templates, "check_external_preparation", reject)
    with _source(_hid_pdb(), route, tmp_path) as source:
        assert (
            msm.convert(
                source, to_form="string:amino_acids_1", from_naming_scheme="amber"
            )
            == "H"
        )


def test_a_name_projection_keeps_an_explicit_inference_request(monkeypatch):
    backend = importlib.import_module(
        "molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys"
    )
    calls = []

    def external(item):
        calls.append(item)
        return EXPECTED_CAP_PAIRS

    monkeypatch.setattr(backend, "_get_bonded_atom_pairs_from_openmm_pdb", external)
    result = msm.convert(
        _cap_pdb(),
        to_form="string:amino_acids_1",
        from_naming_scheme="amber",
        get_missing_bonds=True,
    )
    assert result == "A"
    assert len(calls) == 1


@pytest.mark.parametrize("route", ["file", "text", "handler"])
def test_source_context_retains_nonconsecutive_structures_units_and_atom_maps(
    route, tmp_path
):
    original = [line for line in _cap_pdb().splitlines() if line.startswith("ATOM  ")]
    base = np.asarray(
        [[float(line[i : i + 8]) for i in (30, 38, 46)] for line in original]
    )
    lines = []
    for index in range(3):
        lines.append(f"MODEL     {index + 1:4d}")
        for line, xyz in zip(original, base + index):
            lines.append(
                line[:30] + "".join(f"{value:8.3f}" for value in xyz) + line[54:]
            )
        lines.append("ENDMDL")
    text = "\n".join([*lines, "END", ""])
    selected = [1, 3, 5, 8, 9]
    with _source(text, route, tmp_path) as source:
        with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
            output = msm.convert(
                source,
                selection=selected,
                structure_indices=[2, 0],
                get_missing_bonds=True,
                bond_inference_engine="MolSysMT",
                from_naming_scheme="amber",
            )
    assert output.topology.atoms.atom_id.tolist() == [str(i + 1) for i in selected]
    assert output.topology.group_naming_schemes == ("amber",) * 3
    assert output.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].to_numpy().tolist() == [[0, 1], [2, 3], [3, 4]]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="angstrom"),
        np.stack([base[selected] + 2, base[selected]]),
    )
    history = output.chemical_states.get_preparation_history()
    assert history[-1]["report"]["structure_index"] == 0
    assert history[-1]["report"]["n_atoms"] == 10
    assert history[-1]["report"]["n_structures"] == 3


def test_conflicting_selector_arguments_are_refused_before_reading_or_inference(
    monkeypatch,
):
    import molsysmt.form as forms

    module = forms._dict_modules["string:pdb_text"]
    original = forms.load_converter
    calls = []

    def inspect_only(owner, route):
        converter = original(owner, route)
        if owner is module and converter.__name__ == "to_molsysmt_MolSys":

            def refuse(*args, **kwargs):
                calls.append(True)
                pytest.fail("A conflicting selection reached the reader")

            refuse.__signature__ = inspect.signature(converter)
            return refuse
        return converter

    monkeypatch.setattr(forms, "load_converter", inspect_only)
    with pytest.raises(ArgumentError) as failure:
        msm.convert(
            _hid_pdb(),
            selection="group_type=='amino acid'",
            atom_indices=[0],
            get_missing_bonds=False,
            from_naming_scheme="amber",
        )
    assert failure.value.extra["argument"] == "atom_indices"
    assert calls == []


@pytest.mark.parametrize("route", ["file", "text", "handler"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Topology"])
def test_source_context_is_keyword_only_and_keeps_prior_positions_and_defaults(
    route, target
):
    source_module = {
        "file": "file_pdb",
        "text": "string_pdb_text",
        "handler": "molsysmt_PDBFileHandler",
    }[route]
    name = f"to_{target.replace('.', '_')}"
    function = getattr(
        importlib.import_module(f"molsysmt.form.{source_module}.{name}"), name
    )
    parameters = inspect.signature(function).parameters
    positions = ["item", "atom_indices"]
    if target == "molsysmt.MolSys":
        positions.append("structure_indices")
    if route != "file":
        positions.append("get_missing_bonds")
    positions.append("skip_digestion")
    assert [
        name
        for name, value in parameters.items()
        if value.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
    ] == positions
    assert parameters["skip_digestion"].default is False
    expected = not (route == "text" and target == "molsysmt.MolSys")
    assert parameters["get_missing_bonds"].default is expected
    assert parameters["bond_inference_engine"].default is None
    assert parameters["from_naming_scheme"].default is None
    assert parameters["from_naming_scheme"].kind == inspect.Parameter.KEYWORD_ONLY
