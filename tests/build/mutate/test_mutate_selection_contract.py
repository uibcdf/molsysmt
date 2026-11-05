"""Atom selections and mutation targets must resolve before either engine edits."""

from importlib import import_module

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    StructuralInconsistencyError,
)


@pytest.fixture(scope="module")
def peptide():
    return msm.build.build_peptide("AlaValPro", engine="MolSysMT")


def assert_source_preserved(source, original):
    pd.testing.assert_frame_equal(source.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(source.topology.groups, original.topology.groups)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(original.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
@pytest.mark.parametrize("kind", ["native", "mdtraj", "indices", "partial", "repeated"])
def test_equivalent_atom_selections_mutate_same_group(peptide, engine, kind):
    if engine == "PDBFixer":
        pytest.importorskip("pdbfixer")
    original = peptide.copy()
    indices = msm.select(peptide, "group_index==1")
    selection, syntax = {
        "native": ("group_index==1", "MolSysMT"),
        "mdtraj": ("resid 1", "MDTraj"),
        "indices": (indices, "MolSysMT"),
        "partial": ([indices[0]], "MolSysMT"),
        "repeated": ([indices[-1], indices[0], indices[-1]], "MolSysMT"),
    }[kind]
    result = msm.build.mutate(
        peptide,
        mutations={"VAL": "GLY"},
        keys="group_name",
        selection=selection,
        syntax=syntax,
        engine=engine,
    )
    assert msm.get(result, element="group", group_name=True) == ["ALA", "GLY", "PRO"]
    assert set(
        msm.get(result, selection='group_index==1 and atom_type!="H"', atom_name=True)
    ) == {"N", "CA", "C", "O"}
    for row in peptide.topology.atoms.itertuples():
        if row.group_index == 1 and row.atom_name not in {"N", "CA", "C", "O"}:
            continue
        query = f'group_index=={row.group_index} and atom_name=="{row.atom_name}"'
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                msm.get(result, selection=query, coordinates=True), to_unit="nm"
            ),
            msm.pyunitwizard.get_value(
                msm.get(peptide, selection=query, coordinates=True), to_unit="nm"
            ),
            # The optional provider route uses PDB text at 0.001 angstrom.
            atol=5e-5 if engine == "PDBFixer" else 0,
            rtol=0,
        )
    assert_source_preserved(peptide, original)


@pytest.mark.parametrize(
    "spec,keys",
    [
        ({1: "GLY"}, "group_index"),
        ({"1": "GLY"}, "group_id"),
        ({"VAL": "GLY"}, "group_name"),
        (["VAL-1-GLY"], "group_index"),
    ],
)
def test_disjoint_selection_filters_every_target_kind(peptide, spec, keys):
    result = msm.build.mutate(peptide, mutations=spec, keys=keys, selection=[0])
    assert result is not peptide
    assert_source_preserved(result, peptide)


@pytest.mark.parametrize("selection", [[], "group_name=='ABSENT'"])
def test_empty_selection_is_independent_noop_without_reconstruction(
    peptide, selection, monkeypatch
):
    def unexpected(*args, **kwargs):
        pytest.fail("An empty mutation plan must not enter a reconstruction engine.")

    for name in ("add_missing_heavy_atoms", "add_missing_hydrogens"):
        monkeypatch.setattr(import_module(f"molsysmt.build.{name}"), name, unexpected)
    result = msm.build.mutate(
        peptide, mutations={"VAL": "GLY"}, keys="group_name", selection=selection
    )
    assert_source_preserved(result, peptide)
    result.topology.groups.at[0, "group_name"] = "CHANGED"
    assert peptide.topology.groups.at[0, "group_name"] == "ALA"


@pytest.mark.parametrize("selection", [[-1], [1000], [0.5]])
def test_invalid_atom_indices_are_rejected(peptide, selection):
    with pytest.raises(ArgumentError):
        msm.build.mutate(
            peptide, mutations={"VAL": "GLY"}, keys="group_name", selection=selection
        )


@pytest.mark.parametrize("index", [-1, 3, True, 1.5, "1"])
def test_invalid_group_keys_are_rejected_before_editing(peptide, index):
    original = peptide.copy()
    with pytest.raises(ArgumentError):
        msm.build.mutate(peptide, mutations={index: "GLY"})
    assert_source_preserved(peptide, original)


@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
def test_duplicate_ids_require_selection_disambiguation(peptide, engine):
    if engine == "PDBFixer":
        pytest.importorskip("pdbfixer")
    source = peptide.copy()
    source.topology.groups["group_id"] = ["same", "same", "tail"]
    with pytest.raises(StructuralInconsistencyError):
        msm.build.mutate(
            source, mutations={"same": "GLY"}, keys="group_id", engine=engine
        )
    # Non-numeric group labels are supported by the native engine; the optional
    # provider retains its own mutation-string label restrictions.
    if engine == "MolSysMT":
        result = msm.build.mutate(
            source,
            mutations={"same": "GLY"},
            keys="group_id",
            selection=msm.select(source, "group_index==1"),
        )
        assert result.topology.groups["group_name"].tolist() == ["ALA", "GLY", "PRO"]


@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
def test_source_name_mismatch_is_rejected_before_engine(peptide, engine):
    original = peptide.copy()
    with pytest.raises(ArgumentChoiceError):
        msm.build.mutate(peptide, mutations=["VAL-1-GLY", "GLY-0-ALA"], engine=engine)
    assert_source_preserved(peptide, original)


@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
def test_unsorted_target_dictionary_keeps_group_association(peptide, engine):
    if engine == "PDBFixer":
        pytest.importorskip("pdbfixer")
    result = msm.build.mutate(peptide, mutations={2: "ALA", 0: "GLY"}, engine=engine)
    assert msm.get(result, element="group", group_name=True) == ["GLY", "VAL", "ALA"]


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
def test_boolean_selection_has_atom_axis(peptide, syntax):
    mask = np.zeros(peptide.get_n_atoms(), dtype=bool)
    mask[10] = True
    result = msm.build.mutate(peptide, {1: "GLY"}, selection=mask, syntax=syntax)
    assert result.topology.groups["group_name"].tolist() == ["ALA", "GLY", "PRO"]


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("selection", [[True, 1], [[10]], [1.5], None, [True]])
def test_selection_validation_does_not_coerce_invalid_masks(peptide, syntax, selection):
    with pytest.raises(ArgumentError):
        msm.build.mutate(peptide, {1: "GLY"}, selection=selection, syntax=syntax)


@pytest.mark.parametrize("mutations", [{}, []])
@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
def test_empty_requests_copy_without_reconstruction(peptide, mutations, engine):
    result = msm.build.mutate(peptide, mutations, engine=engine)
    assert result is not peptide
    assert_source_preserved(result, peptide)


@pytest.mark.parametrize("label", ['chain"quoted', "A-01", "-1"])
def test_literal_group_labels_are_not_selection_expressions(peptide, label):
    source = peptide.copy()
    source.topology.groups.at[1, "group_id"] = label
    for mutations in ({label: "GLY"}, [f"VAL-{label}-GLY"]):
        result = msm.build.mutate(source, mutations, keys="group_id")
        assert result.topology.groups["group_name"].tolist() == ["ALA", "GLY", "PRO"]
        assert result.topology.groups.at[1, "group_id"] == label


@pytest.mark.parametrize(
    "mutations",
    [
        ["VAL-1-GLY", "VAL-1-ALA"],
        ["VAL"],
        [1],
        {1: None},
        {1: ""},
        {1: " GLY"},
        {"missing": "GLY"},
    ],
)
@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
def test_invalid_requests_preserve_source(peptide, mutations, engine):
    original = peptide.copy()
    with pytest.raises(ArgumentError):
        msm.build.mutate(
            peptide,
            mutations,
            keys="group_id" if "missing" in mutations else "group_index",
            engine=engine,
        )
    assert_source_preserved(peptide, original)


def test_duplicate_identical_requests_are_applied_once(peptide):
    result = msm.build.mutate(peptide, ["VAL-1-GLY", "VAL-1-GLY"])
    assert result.topology.groups["group_name"].tolist() == ["ALA", "GLY", "PRO"]
    assert len(result.topology.groups) == 3


def test_native_mutation_does_not_rebuild_unselected_heavy_gap(peptide):
    source = msm.remove(
        peptide, selection='atom_type=="H" or (group_index==0 and atom_name=="CB")'
    )
    result = msm.build.mutate(source, {1: "GLY"})
    assert msm.build.get_missing_heavy_atoms(result) == {0: ["CB"]}
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(
            msm.get(source, selection="group_index==0", coordinates=True), to_unit="nm"
        ),
        msm.pyunitwizard.get_value(
            msm.get(result, selection="group_index==0", coordinates=True), to_unit="nm"
        ),
    )


@pytest.mark.parametrize("form", ["mdtraj.Trajectory", "pdbfixer.PDBFixer"])
def test_foreign_input_keeps_form_and_source_independent(peptide, form):
    pytest.importorskip("mdtraj" if form == "mdtraj.Trajectory" else "pdbfixer")
    source = msm.convert(peptide, to_form=form)
    result = msm.build.mutate(
        source,
        {"VAL": "GLY"},
        keys="group_name",
        selection=msm.select(source, "group_index==1"),
    )
    assert msm.get_form(result) == form
    assert msm.get(result, element="group", group_name=True) == ["ALA", "GLY", "PRO"]
    assert msm.get(source, element="group", group_name=True) == ["ALA", "VAL", "PRO"]


def test_provider_refuses_duplicate_effective_addresses_even_after_selection(peptide):
    pytest.importorskip("pdbfixer")
    source = peptide.copy()
    source.topology.groups["group_id"] = ["1", "1", "2"]
    with pytest.raises(StructuralInconsistencyError):
        msm.build.mutate(source, {1: "GLY"}, selection=[10], engine="PDBFixer")
    assert source.topology.groups["group_name"].tolist() == ["ALA", "VAL", "PRO"]


def test_trusted_boundary_still_checks_target_indices(peptide):
    result = msm.build.mutate(peptide, {1: "GLY"}, selection=[10], skip_digestion=True)
    assert result.topology.groups["group_name"].tolist() == ["ALA", "GLY", "PRO"]
    with pytest.raises(ArgumentError):
        msm.build.mutate(peptide, {-1: "GLY"}, skip_digestion=True)


@pytest.mark.parametrize("engine", ["MolSysMT", "PDBFixer"])
@pytest.mark.parametrize("with_hydrogens", [False, True])
def test_all_group_mutations_use_source_hydrogen_presence(
    peptide, engine, with_hydrogens
):
    if engine == "PDBFixer":
        pytest.importorskip("pdbfixer")
    source = (
        peptide if with_hydrogens else msm.remove(peptide, selection='atom_type=="H"')
    )
    result = msm.build.mutate(source, {0: "GLY", 1: "GLY", 2: "GLY"}, engine=engine)
    assert msm.get(result, element="group", group_name=True) == ["GLY", "GLY", "GLY"]
    assert bool(msm.select(result, 'atom_type=="H"')) is with_hydrogens
    assert msm.get(source, element="group", group_name=True) == ["ALA", "VAL", "PRO"]
