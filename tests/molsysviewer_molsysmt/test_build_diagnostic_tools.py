"""Receive native build diagnostics without preparing or editing a view."""

import inspect
from copy import deepcopy

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError

import molsysmt as msm

puw = msm.pyunitwizard
NAMES = (
    "get_residue_chemical_coverage",
    "get_covalent_bond_candidates",
    "get_peptide_bond_candidates",
)


def same(actual, expected):
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same(actual[key], expected[key])
    elif puw.is_quantity(expected):
        assert puw.get_unit(actual) == puw.get_unit(expected)
        np.testing.assert_equal(puw.get_value(actual), puw.get_value(expected))
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            same(a, e)
    else:
        np.testing.assert_equal(actual, expected)


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            result.regions.add(selection=[0, 2], tag="source")
            result.interactions.attach(
                msm.Interactions.from_records(
                    [],
                    n_atoms=result.molsys.get_n_atoms(),
                    n_structures=3,
                    evaluated_structure_indices=[0, 1, 2],
                    method="receiving.build",
                ),
                name="preserve",
                assume_aligned=True,
            )
            yield result


@pytest.mark.parametrize("name", NAMES)
def test_explicit_signature_native_help_and_no_unreceived_editors(view, name):
    method = getattr(view.addons.molsysmt.build, name)
    native = inspect.signature(getattr(msm.build, name))
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert set(NAMES).issubset(dir(view.addons.molsysmt.build))
    assert not hasattr(view.addons.molsysmt, name)
    assert not hasattr(view.addons.molsysmt.build, "infer_covalent_bonds")
    doc = inspect.getdoc(method)
    assert "current view.molsys" in doc and "not a scene object" in doc
    for kwargs in [
        dict(update_view=False),
        dict(molecular_system=view.molsys),
        dict(prepare=True),
    ]:
        with pytest.raises(UnknownArgumentError):
            method(**kwargs)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_actual_current_structure_is_explicit_and_source_scene_remain_unchanged(
    view, name, skip
):
    primary = view.molsys
    atoms = primary.topology.atoms.copy(deep=True)
    bonds = primary.chemical_states._states[0].bonds.copy(deep=True)
    xyz = puw.get_value(primary.structures.coordinates).copy()
    coverage = deepcopy(primary.interactions["preserve"].to_dict())
    before = view.export_state()
    args = dict(structure_indices=[2], skip_digestion=skip)
    actual = getattr(view.addons.molsysmt.build, name)(**args)
    same(actual, getattr(msm.build, name)(primary, **args))
    assert primary is view.molsys and before == view.export_state()
    pd.testing.assert_frame_equal(atoms, primary.topology.atoms)
    pd.testing.assert_frame_equal(bonds, primary.chemical_states._states[0].bonds)
    np.testing.assert_array_equal(xyz, puw.get_value(primary.structures.coordinates))
    same(coverage, primary.interactions["preserve"].to_dict())
    with pytest.raises(Exception) as expected:
        getattr(msm.build, name)(primary)
    with pytest.raises(type(expected.value)):
        getattr(view.addons.molsysmt.build, name)()


@pytest.mark.parametrize("selection", [[1, 1], "group_index==1", []])
def test_group_diagnostic_selection_is_sorted_unique_and_supports_empty(
    view, selection
):
    actual = view.addons.molsysmt.build.get_residue_chemical_coverage(
        selection=selection, structure_indices=[0]
    )
    same(
        actual,
        msm.build.get_residue_chemical_coverage(
            view.molsys, selection=selection, structure_indices=[0]
        ),
    )
    assert len(actual["groups"]) == (0 if selection == [] else 1)
    assert not any(
        g.get("status") not in {"assessed", "incomplete", "unassessed"}
        for g in actual["groups"]
    )


def test_covalent_candidates_have_literal_alanine_pairs_without_adding_bonds(view):
    report = view.addons.molsysmt.build.get_covalent_bond_candidates(
        selection="group_index==1", structure_indices=[0]
    )
    names = msm.get(view.molsys, element="atom", atom_name=True)
    actual = {frozenset((names[a], names[b])) for a, b in report["bonded_atom_pairs"]}
    assert actual == {
        frozenset(pair) for pair in [("N", "CA"), ("CA", "C"), ("C", "O"), ("CA", "CB")]
    }
    assert report["bonded_atom_pairs"].dtype == np.int64
    assert report["missing_mask"].dtype == np.bool_
    one_atom = msm.select(view.molsys, selection="group_index==1 and atom_name=='CA'")
    assert view.addons.molsysmt.build.get_covalent_bond_candidates(
        selection=one_atom, structure_indices=[0]
    )["bonded_atom_pairs"].shape == (0, 2)


def _assert_peptide_distance_roles(view):
    with puw.context(standard_units=["angstrom", "fs", "e"]):
        report = view.addons.molsysmt.build.get_peptide_bond_candidates(
            structure_indices=[0], max_bond_length=puw.quantity(0.2, "nm"), pbc=False
        )
    c, n = report["carbon_atom_indices"], report["nitrogen_atom_indices"]
    assert len(c) > 0 and len(c) == len(n)
    names = msm.get(view.molsys, element="atom", atom_name=True)
    assert all(names[i] == "C" for i in c) and all(names[i] == "N" for i in n)
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[0]
    distances = np.linalg.norm(xyz[c] - xyz[n], axis=1)
    np.testing.assert_allclose(
        puw.get_value(report["distances"], to_unit="nm"), distances, atol=1e-12
    )
    assert np.max(distances) <= 0.153 + 1e-12


def test_peptide_candidates_preserve_named_roles_and_real_distance_units():
    # The bundled PDB carries declared chain membership. The legacy pentalanine
    # H5MSM fixture has unknown atom-chain indices and cannot certify this route.
    with msv.demo["181L"] as view:
        _assert_peptide_distance_roles(view)


def test_legacy_unknown_chain_metadata_remains_unassessed_without_inference(view):
    assert (view.molsys.topology.atoms["chain_index"] < 0).all()
    report = view.addons.molsysmt.build.get_peptide_bond_candidates(
        structure_indices=[0]
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (view.molsys.topology.atoms["chain_index"] < 0).all()


@pytest.mark.parametrize("name", NAMES)
def test_pending_read_replacement_empty_and_closed_lifetime(view, name):
    method = getattr(view.addons.molsysmt.build, name)
    view.addons.molsysmt.structure.translate(
        translation=puw.quantity([1, 0, 0], "nm"), in_place=True, update_view=False
    )
    status = view.addons.molsysmt.get_sync_status()
    method(structure_indices=[0])
    assert (
        view.addons.molsysmt.get_sync_status() == status
        and status["state"] == "pending"
    )
    with pytest.raises(SystemEditPendingError):
        view.export_state()
    view.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    same(
        method(structure_indices=[0]),
        getattr(msm.build, name)(view.molsys, structure_indices=[0]),
    )
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(structure_indices=[0])
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.build, name)(structure_indices=[0])
