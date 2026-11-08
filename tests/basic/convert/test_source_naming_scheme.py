"""Apply explicit source vocabularies without changing the original system."""

import json

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.native import MolSys, Structures, Topology


@pytest.fixture
def source():
    molsys = MolSys(n_atoms=4, n_groups=3, n_molecules=1, n_entities=1, n_chains=1)
    topology = molsys.topology
    topology.groups["group_name"] = ["GLH", "GLH", "HID"]
    topology.groups["group_type"] = ["amino acid"] * 3
    topology.groups["group_id"] = ["a", "b", "c"]
    topology.groups["molecule_index"] = pd.array([0, 0, 0], dtype="Int64")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.atoms["group_index"] = pd.array([2, 0, 2, 1], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0, 0, 0, 0], dtype="Int64")
    topology.atoms["atom_id"] = ["10", "11", "12", "13"]
    topology.chains["chain_id"] = ["A"]
    topology.set_group_naming_schemes(["amber", "legacy", None])
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(24).reshape(2, 4, 3), "nm")
    )
    return molsys


@pytest.mark.parametrize("native", ["system", "topology"])
def test_override_respects_repeated_nonconsecutive_groups_and_input(source, native):
    original = source.topology.groups.copy(deep=True)
    selected = np.array([2, 0, 2], dtype=np.int64)
    selected.flags.writeable = False
    value = source if native == "system" else source.topology
    assert (
        msm.convert(
            value,
            to_form="string:amino_acids_1",
            group_indices=selected,
            from_naming_scheme="amber",
        )
        == "HEH"
    )
    assert source.topology.group_naming_schemes == ("amber", "legacy", None)
    pd.testing.assert_frame_equal(
        original, source.topology.groups, check_frame_type=False
    )
    np.testing.assert_array_equal(selected, [2, 0, 2])


def test_mixed_stored_context_remains_effective_without_override(source):
    source.topology.set_group_naming_schemes("amber", group_indices=2)
    assert (
        msm.convert(source, to_form="string:amino_acids_1", group_indices=[2, 1, 0, 2])
        == "HQEH"
    )


@pytest.mark.parametrize("kind", ["public", "topology", "system"])
@pytest.mark.parametrize("override", [None, "amber"])
def test_native_projection_does_not_copy_any_domain(
    source, monkeypatch, kind, override
):
    source.topology.set_group_naming_schemes("amber", group_indices=2)

    def refuse(*args, **kwargs):
        raise AssertionError("Sequence projection must not copy molecular domains.")

    for cls in (Topology, MolSys, Structures):
        monkeypatch.setattr(cls, "copy", refuse)
    if kind == "public":
        value = msm.convert(
            source,
            to_form="string:amino_acids_1",
            group_indices=[2, 0],
            from_naming_scheme=override,
        )
    else:
        from molsysmt.form.molsysmt_MolSys.to_string_amino_acids_1 import (
            to_string_amino_acids_1 as system_projection,
        )
        from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
            to_string_amino_acids_1 as topology_projection,
        )

        function = system_projection if kind == "system" else topology_projection
        item = source if kind == "system" else source.topology
        value = function(item, group_indices=[2, 0], from_naming_scheme=override)
    assert value == "HE"


@pytest.mark.parametrize("bad", ["AMBER", "unknown", 0, False, [], ["amber"]])
def test_invalid_source_scheme_has_its_own_argument_diagnostic(source, bad):
    with pytest.raises(ArgumentChoiceError) as refusal:
        msm.convert(source, to_form="string:amino_acids_1", from_naming_scheme=bad)
    assert refusal.value.extra["argument"] == "from_naming_scheme"


@pytest.mark.parametrize("kind", ["public", "topology", "system"])
@pytest.mark.parametrize(
    "bad",
    [
        [0.5],
        [True],
        [0, False],
        [-1],
        [3],
        [[0]],
        [2**64],
        np.ma.array([0]),
        None,
        msm.pyunitwizard.quantity([0], "nm"),
        np.array([0], dtype=np.uint64) + np.uint64(2**63),
    ],
)
def test_group_positions_reject_before_lossy_cast(source, kind, bad):
    from molsysmt.form.molsysmt_MolSys.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as system_projection,
    )
    from molsysmt.form.molsysmt_Topology.to_string_amino_acids_1 import (
        to_string_amino_acids_1 as topology_projection,
    )

    with pytest.raises(ArgumentError) as refusal:
        if kind == "public":
            msm.convert(
                source,
                to_form="string:amino_acids_1",
                group_indices=bad,
                from_naming_scheme="amber",
            )
        else:
            function = system_projection if kind == "system" else topology_projection
            function(
                source if kind == "system" else source.topology,
                group_indices=bad,
                from_naming_scheme="amber",
            )
    assert refusal.value.extra["argument"] == "group_indices"


@pytest.mark.parametrize("target", ["string:amino_acids_1", "file"])
def test_conflict_is_explicit_and_precedes_target_creation(source, tmp_path, target):
    path = tmp_path / "must-not-exist.h5msm"
    before = source.topology.group_naming_schemes
    with pytest.raises(ArgumentError, match="contradicts") as refusal:
        msm.convert(
            source,
            to_form=str(path) if target == "file" else target,
            from_naming_scheme="amber",
        )
    assert refusal.value.extra["argument"] == "from_naming_scheme"
    assert source.topology.group_naming_schemes == before
    assert not path.exists()


def test_selection_limits_conflict_scope(source):
    assert (
        msm.convert(
            source,
            to_form="string:amino_acids_1",
            selection="group_index in [0, 2]",
            from_naming_scheme="amber",
        )
        == "EH"
    )
    assert (
        msm.convert(
            source,
            to_form="string:amino_acids_1",
            group_indices=[],
            from_naming_scheme="amber",
        )
        == ""
    )


def test_two_selection_populations_are_rejected(source):
    with pytest.raises(ArgumentError, match="either selection"):
        msm.convert(
            source,
            to_form="string:amino_acids_1",
            group_indices=[0],
            selection="group_index==0",
            from_naming_scheme="amber",
        )


def test_explicit_atom_positions_select_molecular_groups_and_structures(source):
    result = msm.convert(
        source,
        to_form="molsysmt.MolSys",
        atom_indices=[0, 1],
        structure_indices=[1, 0],
        from_naming_scheme="amber",
    )
    assert result.topology.groups.group_name.tolist() == ["HID", "GLH"]
    assert result.topology.group_naming_schemes == ("amber", "amber")
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        np.arange(24).reshape(2, 4, 3)[[1, 0]][:, [0, 1]],
    )


@pytest.mark.parametrize("reverse_domains", [False, True])
def test_complementary_native_domains_keep_naming_owner_and_source_axes(
    source, reverse_domains
):
    domains = [source.topology, source.structures]
    if reverse_domains:
        domains.reverse()
    before_groups = source.topology.groups.copy(deep=True)
    before_coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()

    assert (
        msm.convert(
            domains,
            to_form="string:amino_acids_1",
            group_indices=[2, 0, 2],
            from_naming_scheme="amber",
        )
        == "HEH"
    )
    with pytest.raises(ArgumentError, match="contradicts"):
        msm.convert(
            domains, to_form="string:amino_acids_1", from_naming_scheme="amber"
        )

    result = msm.convert(
        domains,
        to_form="molsysmt.MolSys",
        atom_indices=[0, 1],
        structure_indices=[1, 0],
        from_naming_scheme="amber",
        get_missing_bonds=False,
    )
    assert result.topology.groups.group_name.tolist() == ["HID", "GLH"]
    assert result.topology.group_naming_schemes == ("amber", "amber")
    assert result.topology.atoms.atom_id.tolist() == ["10", "11"]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        before_coordinates[[1, 0]][:, [0, 1]],
    )
    assert source.topology.group_naming_schemes == ("amber", "legacy", None)
    pd.testing.assert_frame_equal(
        source.topology.groups, before_groups, check_frame_type=False
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        before_coordinates,
    )


def test_foreign_reader_declaration_preserves_types_names_and_explicit_chemistry():
    app = pytest.importorskip("openmm.app")
    original = app.Topology()
    chain = original.addChain("A")
    atoms = []
    for index, name in enumerate(["GLH", "HID", "GLH"]):
        group = original.addResidue(name, chain, id=f"group-{index}")
        atoms.append(
            original.addAtom("CA", app.element.carbon, group, id=str(index + 11))
        )
    original.addBond(atoms[0], atoms[1])

    result = msm.convert(
        original,
        to_form="molsysmt.MolSys",
        from_naming_scheme="amber",
        get_missing_bonds=False,
    )
    assert result.topology.group_naming_schemes == ("amber",) * 3
    assert result.topology.groups.group_name.tolist() == ["GLH", "HID", "GLH"]
    assert result.topology.groups.group_type.tolist() == ["unknown"] * 3
    assert result.topology.atoms.atom_id.tolist() == ["11", "12", "13"]
    assert msm.convert(result, to_form="string:amino_acids_1") == "EHE"
    bonds = result.chemical_states.get_bonds()
    assert bonds[["atom1_index", "atom2_index"]].values.tolist() == [[0, 1]]
    assert bonds.evidence.tolist() == ["explicit"]
    assert [group.name for group in original.residues()] == ["GLH", "HID", "GLH"]
    assert original.getNumBonds() == 1


def test_matching_parent_letter_does_not_remove_a_vocabulary_conflict(source):
    source.topology.groups.loc[0, "group_name"] = "HIP"
    with pytest.raises(ArgumentError, match="contradicts"):
        msm.convert(
            source,
            to_form="string:amino_acids_1",
            group_indices=[0],
            from_naming_scheme="legacy",
        )


def test_topology_free_native_has_no_source_naming_interpretation():
    source = MolSys._from_partial_domains(
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
        )
    )
    with pytest.raises(ArgumentError, match="requires a topology") as refusal:
        msm.convert(source, to_form="string:amino_acids_1", from_naming_scheme="amber")
    assert refusal.value.extra["argument"] == "from_naming_scheme"


@pytest.mark.parametrize(
    "target",
    [
        "molsysmt.Topology",
        "molsysmt.MolSys",
        "molsysmt.TopologyDict",
        "molsysmt.MolSysDict",
        "file",
    ],
)
def test_native_outputs_persist_selected_declaration_without_mutation(
    source, tmp_path, target
):
    result = msm.convert(
        source,
        to_form=str(tmp_path / "declared.h5msm") if target == "file" else target,
        selection=[0, 1],
        structure_indices=[1, 0],
        from_naming_scheme="amber",
    )
    restored = msm.convert(result, to_form="molsysmt.Topology")
    assert restored.groups.group_name.tolist() == ["HID", "GLH"]
    assert restored.group_naming_schemes == ("amber", "amber")
    assert msm.convert(restored, to_form="string:amino_acids_1") == "HE"
    assert source.topology.group_naming_schemes == ("amber", "legacy", None)
    assert source.structures.n_atoms == 4


@pytest.mark.parametrize("form", ["topology_dict", "system_dict", "file"])
def test_foreign_containers_preserve_known_context_and_original_indices(
    source, tmp_path, form
):
    target = {
        "topology_dict": "molsysmt.TopologyDict",
        "system_dict": "molsysmt.MolSysDict",
    }.get(form)
    value = msm.convert(source, to_form=target or str(tmp_path / "source.h5msm"))
    assert (
        msm.convert(
            value,
            to_form="string:amino_acids_1",
            group_indices=[2, 0, 2],
            from_naming_scheme="amber",
        )
        == "HEH"
    )
    with pytest.raises(ArgumentError, match="contradicts"):
        msm.convert(value, to_form="string:amino_acids_1", from_naming_scheme="amber")


def test_pdb_text_uses_native_reader_and_explicit_context_without_optional_inference():
    text = (
        "ATOM      1  CA  GLH A   1       0.000   0.000   0.000  1.00  0.00           C  \n"
        "ATOM      2  CA  HID A   2       1.000   0.000   0.000  1.00  0.00           C  \n"
        "END\n"
    )
    assert (
        msm.convert(
            text,
            to_form="string:amino_acids_1",
            from_naming_scheme="amber",
            get_missing_bonds=False,
        )
        == "EH"
    )


@pytest.mark.parametrize(
    "target", ["string:amino_acids_1", "molsysmt.Topology", "molsysmt.MolSys"]
)
def test_source_sequence_declaration_precedes_constructor_default(target):
    result = msm.convert(
        "amino_acids_3:AlaGlhHid", to_form=target, from_naming_scheme="amber"
    )
    if target == "string:amino_acids_1":
        assert result == "AEH"
    else:
        topology = result if target == "molsysmt.Topology" else result.topology
        assert topology.group_naming_schemes == ("amber",) * 3
        assert topology.n_atoms == 0
        assert topology.groups.group_name.tolist() == ["ALA", "GLH", "HID"]


def test_multiple_targets_forward_the_same_explicit_interpretation():
    values, reports = msm.convert(
        "amino_acids_3:GlhHid",
        to_form=["string:amino_acids_1", "molsysmt.Topology"],
        from_naming_scheme="amber",
        return_report=True,
    )
    assert values[0] == "EH"
    assert values[1].group_naming_schemes == ("amber", "amber")
    assert len(reports) == 2
    assert reports[0].from_form == "string:amino_acids_3"


def test_naming_conversion_invalidates_only_the_result_analysis(source):
    source.topology.set_group_naming_schemes(None)
    source.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=4,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="fixture",
        )
    }
    snapshot = source.interactions["empty"]
    result = msm.convert(
        source, to_form="molsysmt.MolSys", from_naming_scheme="amber", copy_if_all=False
    )
    assert result is not source
    assert result.topology.group_naming_schemes == ("amber",) * 3
    assert result.interactions["empty"].evaluated_structure_indices.tolist() == []
    assert source.interactions["empty"] is snapshot
    assert snapshot.evaluated_structure_indices.tolist() == [0, 1]
    assert source.topology.group_naming_schemes == (None,) * 3


def test_query_retains_a_detached_dictionary_input(source):
    value = msm.convert(source, to_form="molsysmt.TopologyDict")
    before = json.dumps(value.to_dict(), sort_keys=True)
    msm.convert(
        value,
        to_form="string:amino_acids_1",
        group_indices=[2],
        from_naming_scheme="amber",
    )
    assert json.dumps(value.to_dict(), sort_keys=True) == before


@pytest.mark.parametrize("sequence", ["amino_acids_1:JXa", "aC", "amino_acids_1:"])
def test_one_letter_identity_keeps_source_text_envelope(sequence):
    expected = msm.convert(sequence, to_form="string:amino_acids_1")
    assert (
        msm.convert(
            sequence, to_form="string:amino_acids_1", from_naming_scheme="sequence"
        )
        == expected
    )


@pytest.mark.parametrize(
    "contents,expected",
    [
        (">a\nAG\n>b\nWX\n", ["AG", "WX"]),
        (">a\nAG\n", "AG"),
        (">a\nAG\n>empty\n>b\nWX\n", ["AG", "", "WX"]),
    ],
)
def test_fasta_queries_keep_record_occurrences_and_empty_sequences(
    tmp_path, contents, expected
):
    path = tmp_path / "source.fasta"
    path.write_text(contents)
    assert msm.convert(str(path), to_form="string:amino_acids_1") == expected
    assert (
        msm.convert(
            str(path), to_form="string:amino_acids_1", from_naming_scheme="sequence"
        )
        == expected
    )


@pytest.mark.parametrize(
    "argument,target",
    [
        ("selection", "molsysmt.Topology"),
        ("selection", "molsysmt.MolSys"),
        ("selection", "molsysmt.TopologyDict"),
        ("selection", "molsysmt.MolSysDict"),
        ("selection", "file"),
        ("group_indices", "molsysmt.Topology"),
        ("group_indices", "molsysmt.MolSys"),
        ("group_indices", "file"),
    ],
)
def test_group_only_molecular_conversion_preserves_ordered_repeated_positions(
    tmp_path, target, argument
):
    result = msm.convert(
        "amino_acids_3:GlhHidGlh",
        to_form=str(tmp_path / "group-only.h5msm") if target == "file" else target,
        from_naming_scheme="amber",
        **{argument: [2, 1, 2]},
    )
    topology = msm.convert(result, to_form="molsysmt.Topology")
    assert topology.n_atoms == 0
    assert topology.groups.group_name.tolist() == ["GLH", "HID", "GLH"]
    assert topology.groups.group_id.tolist() == ["0", "1", "2"]
    assert topology.group_naming_schemes == ("amber",) * 3
    assert msm.convert(topology, to_form="string:amino_acids_1") == "EHE"


def test_group_only_source_does_not_acquire_an_atomic_selection_axis():
    with pytest.raises(ArgumentError, match="no atomic") as refusal:
        msm.convert(
            "amino_acids_3:GlhHid",
            to_form="molsysmt.Topology",
            from_naming_scheme="amber",
            atom_indices=[0],
        )
    assert refusal.value.extra["argument"] == "atom_indices"


@pytest.mark.parametrize("positions", [[2, 1], [2, 1, 2]])
def test_existing_group_inventory_keeps_its_source_ids_and_unique_extraction_contract(
    positions,
):
    source = msm.convert("amino_acids_3:GlhHidGlh", to_form="molsysmt.Topology")
    if len(positions) != len(set(positions)):
        with pytest.raises(ArgumentError, match="must be unique"):
            msm.convert(
                source,
                to_form="molsysmt.Topology",
                selection=positions,
                from_naming_scheme="amber",
            )
    else:
        result = msm.convert(
            source,
            to_form="molsysmt.Topology",
            selection=positions,
            from_naming_scheme="amber",
        )
        assert result.groups.group_name.tolist() == ["GLH", "HID"]
        assert result.groups.group_id.tolist() == ["2", "1"]
        assert result.group_naming_schemes == ("amber", "amber")
    assert source.group_naming_schemes == (None,) * 3
