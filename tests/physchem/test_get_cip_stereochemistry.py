"""Protecting scientific labels, source axes and read-only CIP analysis."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

Chem = pytest.importorskip("rdkit.Chem")


def test_query_and_non_tetrahedral_sources_are_rejected():
    with pytest.raises(StructuralInconsistencyError, match="concrete chemical graph"):
        msm.physchem.get_cip_stereochemistry(Chem.MolFromSmarts("[C,N]"))
    source = Chem.MolFromSmiles("Cl[Pt@SP1](Cl)(N)N")
    with pytest.raises(StructuralInconsistencyError, match="tetrahedral"):
        msm.physchem.get_cip_stereochemistry(source)


def test_broken_ackredit_preserves_completed_science(monkeypatch):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    def broken():
        raise ImportError("broken test provider")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with pytest.warns(AckreditTrackingWarning, match="broken test provider"):
        result = msm.physchem.get_cip_stereochemistry(
            Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
        )
    assert result["atom_stereochemistry"][1] == "S"


@pytest.mark.parametrize(
    "diagnostic_failure", [None, "import", "construction", "emission"]
)
def test_real_ackredit_failure_preserves_recognition_under_strict_warnings(
    monkeypatch, caplog, diagnostic_failure
):
    import warnings

    import smonitor
    from smonitor.handlers import MemoryHandler

    ackredit = pytest.importorskip("ackredit")
    source = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    source_bytes = source.ToBinary()

    def failed_provider(**kwargs):
        raise RuntimeError("controlled real Ackredit registration failure")

    def failed_diagnostic(*args, **kwargs):
        raise RuntimeError(f"controlled diagnostic {diagnostic_failure} failure")

    monkeypatch.setattr(ackredit, "register_item", failed_provider)
    if diagnostic_failure == "import":
        import builtins

        original_import = builtins.__import__

        def blocked_import(name, *args, **kwargs):
            if name == "molsysmt._private.smonitor.emitter":
                return failed_diagnostic()
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", blocked_import)
    elif diagnostic_failure == "construction":
        from molsysmt._private.smonitor import warnings as catalog_warnings

        monkeypatch.setattr(
            catalog_warnings, "AckreditTrackingWarning", failed_diagnostic
        )
    elif diagnostic_failure == "emission":
        from molsysmt._private.smonitor import emitter

        monkeypatch.setattr(emitter, "warn", failed_diagnostic)
    manager = smonitor.get_manager()
    handler = MemoryHandler()
    manager.add_handler(handler)
    try:
        with ackredit.session("provider recognition failure"):
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                result = msm.physchem.get_cip_stereochemistry(source)
            assert not ackredit.get_used_items()
    finally:
        manager.remove_handler(handler)
    assert result["atom_stereochemistry"][1] == "S"
    assert result["references"][0]["doi"] == "10.1021/acs.jcim.8b00324"
    assert source.ToBinary() == source_bytes
    if diagnostic_failure is None:
        events = [
            event
            for event in handler.events
            if event.get("code") == "MSM-WARN-ATTR-001"
        ]
        assert len(events) == 1
        assert "registration failure" in events[0]["extra"]["reason"]
    else:
        events = [
            record
            for record in caplog.records
            if getattr(record, "code", None) == "MSM-WARN-ATTR-001"
        ]
        assert len(events) == 1
        assert events[0].operation == "record scientific references"
        assert "registration failure" in events[0].provider_error
        assert diagnostic_failure in events[0].diagnostic_error


def test_lazy_import_and_genuine_ackredit_absence():
    import subprocess
    import sys

    script = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'ackredit' or fullname.startswith('ackredit.'):
            raise ModuleNotFoundError('Ackredit deliberately unavailable')
sys.meta_path.insert(0, Absent())
import molsysmt as msm
assert 'ackredit' not in sys.modules
assert 'rdkit' not in sys.modules
from rdkit import Chem
result = msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles('N[C@@H](C)C(=O)O'))
assert result['atom_stereochemistry'][1] == 'S'
assert result['references'][0]['doi'] == '10.1021/acs.jcim.8b00324'
assert 'ackredit' not in sys.modules
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr


def test_pseudoasymmetry_uses_unselected_dependencies():
    # Independent expected labels: RDKit CIPLabeler para-stereochemistry,
    # example 1 (Salome Rieder), Code/GraphMol/CIPLabeler/catch_tests.cpp.
    source = Chem.MolFromSmiles(r"C\C=C/[C@@H](\C=C\O)[C@H](C)[C@H](\C=C/C)\C=C\O")
    result = msm.physchem.get_cip_stereochemistry(source, selection=[3, 7, 9])
    assert result["atom_stereochemistry"].tolist() == ["R", "r", "S"]
    native = msm.convert(source, to_form="molsysmt.MolSys")
    assert (
        native.chemical_states._states[0].atom_attributes.loc[7, "stereochemistry"]
        == "r"
    )
    assert msm.physchem.get_cip_stereochemistry(native, selection=[7])[
        "atom_stereochemistry"
    ].tolist() == ["r"]


def test_real_ackredit_reused_references_and_enclosing_workflow():
    ackredit = pytest.importorskip("ackredit")
    paper = "doi:10.1021/acs.jcim.8b00324"
    with ackredit.session("CIP workflow"):
        with ackredit.scope("dockingmt.ligand_analysis"):
            first = msm.physchem.get_cip_stereochemistry(
                Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
            )
            second = msm.physchem.get_cip_stereochemistry(
                Chem.MolFromSmiles("CC"), selection=[]
            )
        assert paper in ackredit.get_used_items()
        for result in (first, second):
            assert paper in {item["id"] for item in result["attribution"]["items"]}
        tree = ackredit.current_session().usage_tree
        assert (
            "molsysmt.physchem.get_cip_stereochemistry"
            in tree["dockingmt.ligand_analysis"]["children"]
        )


@pytest.mark.parametrize(
    "smiles,index,label",
    [
        ("N[C@@H](C)C(=O)O", 1, "S"),  # L-alanine
        ("N[C@@H](CS)C(=O)O", 1, "R"),  # L-cysteine: sulfur changes priority
        ("[C@H](F)(Cl)Br", 0, "S"),
        ("[C@@H](F)(Cl)Br", 0, "R"),
        ("[C@]([H])([2H])(F)Cl", 0, "S"),  # isotope rule breaks the H/H tie
    ],
)
def test_absolute_labels_and_native_source(smiles, index, label):
    source = Chem.MolFromSmiles(smiles, sanitize=True)
    before = source.ToBinary()
    report = msm.physchem.get_cip_stereochemistry(source, selection=[index])
    assert report["atom_indices"].tolist() == [index]
    assert report["atom_stereochemistry"].tolist() == [label]
    assert source.ToBinary() == before
    native = msm.convert(source, to_form="molsysmt.MolSys")
    states = native.chemical_states.copy()
    assert msm.physchem.get_cip_stereochemistry(native, selection=[index])[
        "atom_stereochemistry"
    ].tolist() == [label]
    pd.testing.assert_frame_equal(
        native.chemical_states._states[0].atom_attributes,
        states._states[0].atom_attributes,
    )


@pytest.mark.parametrize("smiles,label", [("F/C=C/F", "E"), ("F/C=C\\F", "Z")])
def test_double_bond_labels_and_reference_geometry(smiles, label):
    report = msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles(smiles))
    mask = report["bond_stereochemistry"] == label
    assert mask.sum() == 1
    assert report["bond_stereo_atom_indices"][mask].tolist() == [[0, 3]]
    assert report["bond_reference_stereochemistry"][mask].tolist() == [
        "trans" if label == "E" else "cis"
    ]


def test_selection_uses_full_graph_and_empty_shapes():
    source = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    selected = msm.physchem.get_cip_stereochemistry(source, selection=[3, 1, 1])
    assert selected["atom_indices"].tolist() == [1, 3]
    assert selected["atom_stereochemistry"].tolist() == ["S", None]
    assert selected["bonded_atom_pairs"].tolist() == [[1, 3]]
    empty = msm.physchem.get_cip_stereochemistry(source, selection=[])
    assert empty["atom_indices"].shape == (0,)
    assert empty["bonded_atom_pairs"].shape == (0, 2)
    assert empty["bond_stereo_atom_indices"].shape == (0, 2)
    assert empty["atom_stereochemistry"].dtype == object


def test_incomplete_or_ambiguous_native_chemistry_fails():
    source = msm.convert(Chem.MolFromSmiles("CC"), to_form="molsysmt.MolSys")
    source.chemical_states._states[0].connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_cip_stereochemistry(source)
    source.chemical_states._states[0].connectivity_completeness = "complete"
    source.topology.atoms.loc[0, "atom_type"] = "CA"
    with pytest.raises(StructuralInconsistencyError, match="element"):
        msm.physchem.get_cip_stereochemistry(source)
    source.topology.atoms.loc[0, "atom_type"] = "C"
    source.chemical_states._states[0].bonds.loc[0, "bond_order"] = pd.NA
    with pytest.raises(StructuralInconsistencyError, match="bond orders"):
        msm.physchem.get_cip_stereochemistry(source)


@pytest.mark.parametrize(
    "kwargs", [{"engine": "guess"}, {"from_coordinates": "yes"}, {"selection": [-1]}]
)
def test_public_digestion(kwargs):
    with pytest.raises(ArgumentError):
        msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles("CC"), **kwargs)


def test_coordinate_inference_uses_selected_structure_and_explicit_units():
    source = msm.convert(Chem.MolFromSmiles("FC(Cl)(Br)I"), to_form="molsysmt.MolSys")
    positions = np.array(
        [[1, 1, 1], [0, 0, 0], [-1, -1, 1], [-1, 1, -1], [1, -1, -1]], dtype=float
    )
    from molsysmt.native import Structures

    source.structures = Structures()
    source.structures.append(
        coordinates=msm.pyunitwizard.quantity(
            np.stack([positions, -positions]), "angstrom"
        )
    )
    result = msm.physchem.get_cip_stereochemistry(
        source, structure_indices=[1], from_coordinates=True
    )
    assert result["structure_index"] == 1
    assert result["evidence"] == "coordinates"
    assert result["atom_stereochemistry"][1] in {"R", "S"}
    other = msm.physchem.get_cip_stereochemistry(
        source, structure_indices=[0], from_coordinates=True
    )
    assert other["atom_stereochemistry"][1] != result["atom_stereochemistry"][1]
    source.structures.coordinates = msm.pyunitwizard.convert(
        source.structures.coordinates, to_unit="picometer"
    )
    alternate = msm.physchem.get_cip_stereochemistry(
        source, structure_indices=[1], from_coordinates=True
    )
    np.testing.assert_array_equal(
        alternate["atom_stereochemistry"], result["atom_stereochemistry"]
    )
    msm.pyunitwizard.configure.set_standard_units(["angstrom", "ps", "e", "radians"])
    nondefault = msm.physchem.get_cip_stereochemistry(
        source, structure_indices=[1], from_coordinates=True
    )
    np.testing.assert_array_equal(
        nondefault["atom_stereochemistry"], result["atom_stereochemistry"]
    )
    with pytest.raises(StructuralInconsistencyError, match="exactly one"):
        msm.physchem.get_cip_stereochemistry(source, from_coordinates=True)


def test_attribution_is_detached_and_failure_does_not_destroy_result(monkeypatch):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    first = msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles("CC"))
    assert first["method"] == "hanson_2018"
    assert first["references"][0]["doi"] == "10.1021/acs.jcim.8b00324"
    assert "rdkit" in first["software"]
    first["attribution"]["items"][0]["title"] = "changed by caller"
    second = msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles("CC"))
    assert second["attribution"]["items"][0]["title"] != "changed by caller"
