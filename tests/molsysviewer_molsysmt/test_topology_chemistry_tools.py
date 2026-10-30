"""Receive native graph/sequence analyses without preparing or changing a view."""

import inspect

import molsysviewer as msv
import networkx as nx
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")

NEW_NAMES = (
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
    }
    assert set(dir(peptide.addons.molsysmt.chemical_states)) == set(
        OLD_NAMES + NEW_NAMES
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
