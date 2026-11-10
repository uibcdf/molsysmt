"""Receive native graph/sequence analyses without preparing or changing a view."""

import inspect

import molsysviewer as msv
import networkx as nx
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

pytest.importorskip("molsysviewer.system_edits")

NEW_NAMES = (
    "get_peptide_termini",
    "get_rigid_fragments",
    "get_rotatable_bonds",
    "get_rings",
    "get_substructure_matches",
    "get_atom_correspondences",
    "get_sequence_alignment",
    "get_sequence_identity",
)
OLD_NAMES = (
    "get_bondgraph",
    "get_covalent_blocks",
    "get_covalent_paths",
    "get_dihedral_quartets",
)


def _namespace(parent, name):
    return (
        parent.topology
        if name in {"get_sequence_alignment", "get_sequence_identity"}
        else parent.chemical_states
    )


def assert_native(actual, expected):
    """Compare nested native values without coercing their container contracts."""
    assert type(actual) is type(expected)
    if isinstance(actual, dict):
        assert actual.keys() == expected.keys()
        for key in actual:
            assert_native(actual[key], expected[key])
    elif isinstance(actual, (tuple, list)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            assert_native(left, right)
    elif isinstance(actual, np.ndarray):
        assert actual.dtype == expected.dtype
        np.testing.assert_array_equal(actual, expected)
    else:
        assert actual == expected


@pytest.fixture
def peptide():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as view:
            yield view


@pytest.fixture
def chemistry():
    pytest.importorskip("rdkit")
    # This explicitly chosen conversion supplies declared chemistry. The addon
    # never repairs a less informative SDF/native input on the user's behalf.
    molsys = msm.convert(msm.systems["caffeine"]["caffeine.sdf"], to_form="rdkit.Mol")
    with msv.new_view(molsys) as view:
        analysis = msm.Interactions.from_records(
            [],
            n_atoms=view.molsys.get_n_atoms(),
            n_structures=1,
            evaluated_structure_indices=[0],
            method="receiving.topology.chemistry",
        )
        view.interactions.attach(analysis, name="preserve", assume_aligned=True)
        yield view


def test_peptide_endpoints_remain_native_read_only_results():
    molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    with msv.new_view(molsys) as view:
        state = view.export_state()
        native = view.molsys
        expected = msm.chemical_states.get_peptide_termini(native)
        actual = view.addons.molsysmt.chemical_states.get_peptide_termini()
        assert_native(actual, expected)
        assert actual["c_terminal_group_indices"].tolist() == [2]
        assert view.molsys is native
        assert view.export_state() == state


@pytest.mark.parametrize("name", NEW_NAMES)
def test_native_signatures_digestion_help_and_explicit_namespace(peptide, name):
    signature = inspect.signature(getattr(_namespace(msm, name), name))
    parameters = list(signature.parameters.values())[1:]
    assert signature.parameters["skip_digestion"].default is False
    bound = getattr(_namespace(peptide.addons.molsysmt, name), name)
    assert list(inspect.signature(bound).parameters.values()) == parameters
    assert bound.digestion_plan is not None
    assert "not a scene object" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    assert not hasattr(peptide.addons.molsysmt, name)
    assert set(dir(peptide.addons.molsysmt.topology)) == {
        "get_sequence_alignment",
        "get_sequence_identity",
        "get_atom_name_correspondence",
    }
    assert set(dir(peptide.addons.molsysmt.chemical_states)) == set(
        OLD_NAMES + NEW_NAMES + ("normalize_indexed_hydrogen_policy",)
    ) - {"get_sequence_alignment", "get_sequence_identity"}
    if name in {
        "get_atom_correspondences",
        "get_sequence_alignment",
        "get_sequence_identity",
    }:
        assert "\nreference_molecular_system :" in inspect.getdoc(bound)


@pytest.mark.parametrize(
    "name, arguments",
    [
        ("get_rings", {}),
        ("get_rings", {"selection": [], "structure_indices": [0, 0]}),
        ("get_rigid_fragments", {}),
        ("get_rotatable_bonds", {"method": "conjugation_restricted"}),
        ("get_rotatable_bonds", {"method": "acyclic_single", "selection": [2, 0, 2]}),
        ("get_substructure_matches", {"patterns": ["[#8]", "[#9]"]}),
        ("get_substructure_matches", {"patterns": "[#8]", "selection": []}),
    ],
)
def test_native_results_source_indices_and_chemistry_are_preserved(
    chemistry, name, arguments
):
    view = chemistry
    state = view.export_state()
    native = view.molsys.chemical_states._states[0]
    atoms, bonds = native.atom_attributes.copy(deep=True), native.bonds.copy(deep=True)
    expected = getattr(_namespace(msm, name), name)(view.molsys, **arguments)
    actual = getattr(_namespace(view.addons.molsysmt, name), name)(**arguments)
    assert_native(actual, expected)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    pd.testing.assert_frame_equal(native.atom_attributes, atoms)
    pd.testing.assert_frame_equal(native.bonds, bonds)
    np.testing.assert_array_equal(
        view.molsys.interactions["preserve"].evaluated_structure_indices, [0]
    )
    if name == "get_substructure_matches" and isinstance(arguments["patterns"], list):
        assert actual["matches"][0].shape == (2, 1)
        assert actual["matches"][1].shape == (0, 1)


def test_explicit_fragment_cuts_return_detached_labels_without_removing_bonds(
    chemistry,
):
    view = chemistry
    graph = msm.chemical_states.get_bondgraph(view.molsys)
    endpoints = next(nx.bridges(graph))
    native = view.molsys.chemical_states._states[0]
    bonds = native.bonds.copy(deep=True)
    cut = next(
        index
        for index, row in bonds.iterrows()
        if {int(row.atom1_index), int(row.atom2_index)} == set(endpoints)
    )
    arguments = dict(bond_indices=[cut, cut])
    expected = msm.chemical_states.get_rigid_fragments(view.molsys, **arguments)
    result = view.addons.molsysmt.chemical_states.get_rigid_fragments(**arguments)
    assert_native(result, expected)
    assert result["fragment_offsets"].shape == (3,)
    result["fragment_atom_indices"][:] = -1
    pd.testing.assert_frame_equal(native.bonds, bonds)
    assert not (
        msm.chemical_states.get_rigid_fragments(view.molsys, **arguments)[
            "fragment_atom_indices"
        ]
        < 0
    ).any()


def test_correspondence_reference_anchors_candidates_and_independent_outputs(chemistry):
    view = chemistry
    reference = msm.copy(view.molsys)
    n_atoms = view.molsys.get_n_atoms()
    pairs = np.column_stack((np.arange(n_atoms), np.arange(n_atoms)))
    arguments = dict(
        selection=[2, 0, 2],
        reference_molecular_system=reference,
        reference_selection=[0, 2],
        fixed_atom_correspondence=pairs,
        candidate_atom_correspondences=[[0, 0], [2, 2]],
        max_matches=1,
        structure_indices=[0],
        reference_structure_indices=[0],
    )
    before = view.export_state()
    reference_bonds = reference.chemical_states._states[0].bonds.copy(deep=True)
    expected = msm.chemical_states.get_atom_correspondences(view.molsys, **arguments)
    actual = view.addons.molsysmt.chemical_states.get_atom_correspondences(**arguments)
    assert_native(actual, expected)
    np.testing.assert_array_equal(actual["atom_correspondences"], [[[0, 0], [2, 2]]])
    pairs[:] = -1
    assert (actual["fixed_atom_correspondence"] >= 0).all()
    actual["atom_correspondences"][:] = -1
    pd.testing.assert_frame_equal(
        reference.chemical_states._states[0].bonds, reference_bonds
    )
    assert view.export_state() == before


@pytest.mark.parametrize("name", ["get_sequence_alignment", "get_sequence_identity"])
@pytest.mark.parametrize("selection", ["all", "group_type=='amino acid'"])
def test_sequences_keep_explicit_reference_scopes_and_native_group_mapping(
    peptide, name, selection
):
    pytest.importorskip("Bio")
    reference = msm.copy(peptide.molsys)
    arguments = dict(
        selection=selection,
        reference_molecular_system=reference,
        reference_selection=selection,
    )
    state = peptide.export_state()
    expected = getattr(_namespace(msm, name), name)(peptide.molsys, **arguments)
    actual = getattr(_namespace(peptide.addons.molsysmt, name), name)(**arguments)
    assert_native(actual, expected)
    assert peptide.export_state() == state
    if name == "get_sequence_identity" and selection != "all":
        assert actual[0] == 100.0
        np.testing.assert_array_equal(actual[1], [1, 2, 3, 4, 5])
        np.testing.assert_array_equal(actual[2], actual[1])


def test_prettyprint_and_native_identity_digestion(peptide, capsys):
    pytest.importorskip("Bio")
    args = dict(reference_molecular_system=peptide.molsys, prettyprint=True)
    assert msm.topology.get_sequence_alignment(peptide.molsys, **args) is None
    expected = capsys.readouterr().out
    assert peptide.addons.molsysmt.topology.get_sequence_alignment(**args) is None
    assert capsys.readouterr().out == expected
    expected = msm.topology.get_sequence_identity(
        peptide.molsys, reference_molecular_system=peptide.molsys
    )
    assert_native(
        peptide.addons.molsysmt.topology.get_sequence_identity(
            reference_molecular_system=peptide.molsys, skip_digestion=True
        ),
        expected,
    )


@pytest.mark.parametrize(
    "name, arguments",
    [
        ("get_rings", {"method": "not-a-method"}),
        ("get_rings", {"max_cyclic_block_size": 2}),
        ("get_rigid_fragments", {"bond_indices": [1000000]}),
        ("get_rotatable_bonds", {"method": "not-a-method"}),
        ("get_substructure_matches", {"patterns": "[INVALID"}),
        ("get_substructure_matches", {"patterns": "[#6]", "max_matches": 1}),
        ("get_atom_correspondences", {"max_matches": 1}),
        ("get_sequence_alignment", {"engine": "not-an-engine"}),
        ("get_sequence_identity", {"engine": "not-an-engine"}),
    ],
)
def test_native_failures_and_bounds_do_not_change_the_view(chemistry, name, arguments):
    with pytest.raises(Exception) as error:
        getattr(_namespace(msm, name), name)(chemistry.molsys, **arguments)
    state = chemistry.export_state()
    status = chemistry.addons.molsysmt.get_sync_status()
    with pytest.raises(type(error.value)):
        getattr(_namespace(chemistry.addons.molsysmt, name), name)(**arguments)
    assert chemistry.export_state() == state
    assert chemistry.addons.molsysmt.get_sync_status() == status


def test_insufficient_native_chemistry_is_never_prepared_implicitly(peptide):
    pytest.importorskip("rdkit")
    for name, arguments in [
        ("get_rotatable_bonds", {}),
        ("get_substructure_matches", {"patterns": "[#8]"}),
    ]:
        with pytest.raises(Exception) as error:
            getattr(_namespace(msm, name), name)(peptide.molsys, **arguments)
        with pytest.raises(type(error.value)):
            getattr(_namespace(peptide.addons.molsysmt, name), name)(**arguments)


@pytest.mark.parametrize("name", NEW_NAMES)
def test_boundary_controls_empty_closed_and_primary_override_are_enforced(name):
    with msv.MolSysView() as empty:
        bound = getattr(_namespace(empty.addons.molsysmt, name), name)
        args = {"patterns": "[#8]"} if name == "get_substructure_matches" else {}
        with pytest.raises(ValueError, match="Load a molecular system"):
            bound(**args)
        with pytest.raises(Exception):
            bound(**args, skip_digestion="yes")
        with pytest.raises(TypeError):
            bound(**args, molecular_system=object(), skip_digestion=True)
    with pytest.raises(RuntimeError, match="closed view"):
        bound(**args, skip_digestion=True)


def test_cached_reader_follows_load_and_reads_pending_data_without_sync(peptide):
    pytest.importorskip("Bio")
    alignment = peptide.addons.molsysmt.topology.get_sequence_alignment
    peptide.addons.molsysmt.basic.set(
        structure_indices=[2],
        coordinates=msm.get(
            peptide.molsys, element="atom", structure_indices=[2], coordinates=True
        ),
        update_view=False,
    )
    status = peptide.addons.molsysmt.get_sync_status()
    assert status["state"] == "pending"
    reference = peptide.molsys
    assert_native(
        alignment(reference_molecular_system=reference),
        msm.topology.get_sequence_alignment(
            peptide.molsys, reference_molecular_system=reference
        ),
    )
    assert peptide.addons.molsysmt.get_sync_status() == status
    peptide.addons.molsysmt.sync_view()
    with msv.demo["dialanine"] as replacement:
        peptide.load(replacement.molsys, mode="replace")
    actual = alignment(reference_molecular_system=peptide.molsys)
    assert_native(
        actual,
        msm.topology.get_sequence_alignment(
            peptide.molsys, reference_molecular_system=peptide.molsys
        ),
    )
    assert actual != ("AAAAA", "AAAAA")


def test_identity_forwards_the_native_validation_flag(peptide, monkeypatch):
    original = msm.topology.get_sequence_identity
    expected = original(peptide.molsys, reference_molecular_system=peptide.molsys)
    observed = []

    def inspect_call(source, **parameters):
        observed.append(parameters["skip_digestion"])
        return original(source, **parameters)

    monkeypatch.setattr(msm.topology, "get_sequence_identity", inspect_call)
    for skip in (False, True):
        actual = peptide.addons.molsysmt.topology.get_sequence_identity(
            reference_molecular_system=peptide.molsys, skip_digestion=skip
        )
        assert_native(actual, expected)
    assert observed == [False, True]


@pytest.fixture
def name_view():
    with msv.new_view(msm.systems["caffeine"]["caffeine.sdf"]) as view:
        assert view.molsys.topology.atoms["atom_name"].is_unique
        view.regions.add(selection=[0, 3], tag="names")
        yield view


def test_exact_name_correspondence_has_native_signature_and_read_contract(name_view):
    from argdigest import UnknownArgumentError

    call = name_view.addons.molsysmt.topology.get_atom_name_correspondence
    native = inspect.signature(msm.topology.get_atom_name_correspondence)
    assert inspect.signature(call) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert call.digestion_plan is not None
    assert "exact label match" in inspect.getdoc(call)
    assert "not" in inspect.getdoc(call)
    assert "\nmolecular_system :" not in inspect.getdoc(call)
    assert not hasattr(name_view.addons.molsysmt, "get_atom_name_correspondence")
    with pytest.raises(UnknownArgumentError):
        call(molecular_system=name_view.molsys)
    with pytest.raises(UnknownArgumentError):
        call(update_view=True)
    with pytest.raises(msm.ArgumentError):
        call(skip_digestion="yes")


@pytest.mark.parametrize(
    "selection", [[5, 0, 2], (5, 0, 2), np.array([5, 0, 2], dtype=np.int64)]
)
@pytest.mark.parametrize("skip", [False, True])
def test_exact_name_map_preserves_query_order_and_both_source_axes(
    name_view, selection, skip
):
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
        same,
        snapshot,
        unchanged,
    )

    target = name_view.molsys
    order = np.arange(target.get_n_atoms())[::-1]
    reference = msm.permute_atoms(target, order)
    reference.topology.atoms["atom_id"] = "repeated label"
    expected_reference = reference.copy()
    inverse = np.argsort(order)
    atoms = np.asarray(selection)
    before = snapshot(name_view)
    result = name_view.addons.molsysmt.topology.get_atom_name_correspondence(
        selection=selection,
        reference_molecular_system=reference.topology,
        reference_selection=inverse[atoms[::-1]],
        skip_digestion=skip,
    )
    assert result.dtype == np.int64 and result.shape == (3, 2)
    np.testing.assert_array_equal(result, np.column_stack([atoms, inverse[atoms]]))
    result[:] = -1
    np.testing.assert_array_equal(
        name_view.addons.molsysmt.topology.get_atom_name_correspondence(
            selection=selection
        ),
        np.column_stack([atoms, atoms]),
    )
    same(reference, expected_reference)
    unchanged(name_view, before)


@pytest.mark.parametrize(
    "selection,syntax",
    [("atom_type=='C'", "MolSysMT"), ("element C", "MDTraj"), ([], "MolSysMT")],
)
def test_exact_names_preserve_syntax_empty_axes_and_native_reference_defaults(
    name_view, selection, syntax
):
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
        snapshot,
        unchanged,
    )

    before = snapshot(name_view)
    expected = (
        np.flatnonzero(name_view.molsys.topology.atoms["atom_type"].to_numpy() == "C")
        if selection
        else np.array([], dtype=int)
    )
    result = name_view.addons.molsysmt.topology.get_atom_name_correspondence(
        selection=selection, syntax=syntax
    )
    assert result.dtype == np.int64 and result.shape == (len(expected), 2)
    np.testing.assert_array_equal(result, np.column_stack([expected, expected]))
    unchanged(name_view, before)


@pytest.mark.parametrize("selection", [[0, 0], [-1], [10000]])
def test_exact_name_selection_errors_are_native_and_nonmutating(name_view, selection):
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
        snapshot,
        unchanged,
    )

    before = snapshot(name_view)
    with pytest.raises(Exception) as native:
        msm.topology.get_atom_name_correspondence(name_view.molsys, selection=selection)
    with pytest.raises(type(native.value)) as actual:
        name_view.addons.molsysmt.topology.get_atom_name_correspondence(
            selection=selection
        )
    assert str(actual.value) == str(native.value)
    unchanged(name_view, before)


def test_exact_names_do_not_guess_different_reference_scope_or_duplicate_labels(
    name_view,
):
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
        snapshot,
        unchanged,
    )

    reference = msm.permute_atoms(
        name_view.molsys, np.arange(name_view.molsys.get_n_atoms())[::-1]
    )
    call = name_view.addons.molsysmt.topology.get_atom_name_correspondence
    before = snapshot(name_view)
    # None means the same positional selection, not all of a different reference.
    with pytest.raises(StructuralInconsistencyError):
        call(selection=[0], reference_molecular_system=reference)
    reference.topology.atoms.loc[1, "atom_name"] = reference.topology.atoms.loc[
        0, "atom_name"
    ]
    with pytest.raises(StructuralInconsistencyError):
        call(reference_molecular_system=reference)
    unchanged(name_view, before)


def test_exact_name_cached_reader_follows_replacement_pending_removal_and_close(
    name_view,
):
    from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
        snapshot,
        unchanged,
    )

    call = name_view.addons.molsysmt.topology.get_atom_name_correspondence
    reference = name_view.molsys
    order = np.arange(reference.get_n_atoms())[::-1]
    name_view.load(msm.permute_atoms(reference, order), mode="replace")
    before = snapshot(name_view)
    result = call(reference_molecular_system=reference)
    np.testing.assert_array_equal(
        result, np.column_stack([np.arange(len(order)), order])
    )
    unchanged(name_view, before)
    name_view.addons.molsysmt.basic.remove(
        selection=[len(order) - 1], in_place=True, update_view=False
    )
    before = snapshot(name_view)
    assert before[3]["state"] == "pending"
    result = call(reference_molecular_system=reference, reference_selection=order[:-1])
    np.testing.assert_array_equal(
        result, np.column_stack([np.arange(len(order) - 1), order[:-1]])
    )
    unchanged(name_view, before)
    name_view.close()
    for skip in (False, True):
        with pytest.raises(RuntimeError, match="closed view"):
            call(skip_digestion=skip)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.topology.get_atom_name_correspondence()
