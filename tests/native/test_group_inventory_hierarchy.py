"""Exercise native sequence hierarchy without treating groups as atoms."""

import json

import h5py
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology


@pytest.fixture
def group_system(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "library.fasta"
    path.write_text(
        ">first complete\nAG\n>second\nW\n>first complete\nAG\n>empty\n",
        encoding="utf-8",
    )
    return msm.convert(str(path), to_form="molsysmt.MolSys")


def test_generated_fasta_chain_ids_are_not_record_identifiers(group_system):
    topology = group_system.topology
    assert topology.chains.chain_id.tolist() == ["A", "B", "C", "D"]
    assert topology.molecules.molecule_name.tolist() == [
        "first",
        "second",
        "first",
        "empty",
    ]
    assert topology.entities.entity_name.tolist() == [
        "first complete",
        "second",
        "first complete",
        "empty",
    ]
    assert topology.n_atoms == 0


def test_declared_ordered_membership_is_a_native_relation(group_system):
    topology = group_system.topology
    assert topology.chain_groups == ((0, 1), (2,), (3, 4), ())
    assert msm.get(topology, element="chain", group_index=True) == [
        [0, 1],
        [2],
        [3, 4],
        [],
    ]
    assert msm.get(topology, element="group", chain_index=True) == [0, 0, 1, 2, 2]
    assert msm.get(topology, element="group", chain_id=True) == [
        "A",
        "A",
        "B",
        "C",
        "C",
    ]
    assert msm.get(topology, element="chain", n_groups=True) == [2, 1, 2, 0]
    assert msm.get(
        topology, element="chain", selection=[2, 0, 2], group_index=True
    ) == [[3, 4], [0, 1], [3, 4]]


def test_available_group_positions_and_parent_projections(group_system):
    assert msm.has_attribute(group_system, "group_index")
    assert msm.has_attribute(group_system, "chain_index")
    assert group_system.get(element="molecule", group_index=True) == [
        [0, 1],
        [2],
        [3, 4],
        [],
    ]
    assert msm.get(group_system, element="entity", group_index=True) == [
        [0, 1],
        [2],
        [3, 4],
        [],
    ]
    assert msm.get(group_system, element="molecule", chain_index=True)[:3] == [0, 1, 2]


def test_text_queries_evaluate_known_groups_and_parents(group_system):
    assert msm.select(group_system, element="group", selection="group_name=='ALA'") == [
        0,
        3,
    ]
    assert msm.select(
        group_system,
        element="group",
        selection="chain_id=='C' and group_type=='amino acid'",
    ) == [3, 4]
    assert msm.select(
        group_system, element="molecule", selection="molecule_name=='first'"
    ) == [0, 2]
    assert msm.select(group_system, element="chain", selection="chain_id=='D'") == [3]
    assert msm.select(
        group_system, element="group", selection="group_name=='ALA'", mask=[3, 4]
    ) == [3]
    selected_ids = ["A", "C"]  # noqa: F841 -- resolved by the public @variable selector
    assert msm.select(
        group_system, element="group", selection="chain_id in @selected_ids"
    ) == [0, 1, 3, 4]


def test_group_and_chain_extraction_keep_known_hierarchy_and_source(group_system):
    source = group_system.topology
    result = msm.extract(group_system, element="group", selection=[4, 2])
    assert result.topology.groups.group_name.tolist() == ["GLY", "TRP"]
    assert result.topology.chains.chain_id.tolist() == ["B", "C"]
    assert result.get(element="group", chain_id=True) == ["C", "B"]
    assert result.topology.n_atoms == result.structures.n_structures == 0
    assert source.groups.group_name.tolist() == ["ALA", "GLY", "TRP", "ALA", "GLY"]
    empty_record = msm.extract(group_system, element="chain", selection="chain_id=='D'")
    assert empty_record.topology.n_groups == 0
    assert empty_record.topology.chains.chain_id.tolist() == ["D"]
    assert source.n_chains == 4


def test_dictionary_and_h5msm_preserve_native_membership(group_system, tmp_path):
    topology = group_system.topology
    payload = msm.convert(topology, to_form="molsysmt.TopologyDict")
    data = json.loads(json.dumps(payload.to_dict()))
    assert data["version"] == "0.2"
    assert data["chain_groups"] == [[0, 1], [2], [3, 4], []]
    restored = msm.convert(msm.TopologyDict(data=data), to_form="molsysmt.Topology")
    assert restored.chain_groups == topology.chain_groups
    assert restored.chains.chain_id.tolist() == ["A", "B", "C", "D"]
    path = str(tmp_path / "membership.h5msm")
    msm.convert(group_system, to_form=path)
    with h5py.File(path) as file:
        assert file["topology"].attrs["schema_version"] == 2
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert loaded.topology.chain_groups == topology.chain_groups
    assert loaded.get(element="group", chain_id=True) == ["A", "A", "B", "C", "C"]


def test_builder_can_stage_group_inventory_and_preserve_it_at_build():
    builder = msm.MolSysBuilder()
    group = builder.add_group([], group_name="ALA", group_type="amino acid")
    builder.add_chain([group])
    result = builder.build()
    assert result.topology.n_atoms == 0
    assert result.topology.groups.group_name.tolist() == ["ALA"]
    assert result.topology.chains.chain_id.tolist() == ["A"]
    assert result.topology.chain_groups == ((0,),)
    assert result.topology.n_molecules == 1


@pytest.mark.parametrize(
    "groups",
    [
        [[5], [], [], []],
        [[0, 0], [], [], []],
        [[0.5], [], [], []],
        [[True], [], [], []],
        [[0]],
    ],
)
def test_invalid_membership_is_rejected_without_publication(group_system, groups):
    topology = group_system.topology
    before = topology.chain_groups
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        topology.set_chain_groups(groups)
    assert topology.chain_groups == before


def test_shared_group_membership_retains_ambiguity_without_changing_atoms(group_system):
    topology = group_system.topology
    topology.set_chain_groups([[1, 0], [2, 0], [3, 4], []])
    assert msm.get(topology, element="chain", selection=[0], group_index=True) == [
        [1, 0]
    ]
    assert msm.get(topology, element="group", selection=[0], chain_index=True) == [
        [0, 1]
    ]
    assert topology.n_atoms == 0


def test_generated_chain_ids_cross_alphabet_boundaries(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "many.fasta"
    path.write_text("".join(f">record_{i}\nA\n" for i in range(704)), encoding="utf-8")
    topology = msm.convert(str(path), to_form="molsysmt.Topology")
    ids = topology.chains.chain_id.tolist()
    assert ids[:3] == ["A", "B", "C"]
    assert ids[25:29] == ["Z", "AA", "AB", "AC"]
    assert ids[51:54] == ["AZ", "BA", "BB"]
    assert ids[701:] == ["ZZ", "AAA", "AAB"]
    assert topology.n_groups == 704 and topology.n_atoms == 0


def test_native_rebuild_keeps_declared_membership_and_empty_chains(group_system):
    topology = group_system.topology.copy()
    topology.rebuild_chains()
    assert topology.chain_groups == ((0, 1), (2,), (3, 4), ())
    assert topology.chains.chain_id.tolist() == ["A", "B", "C", "D"]
    assert topology.chains.chain_type.tolist()[-1] == "unknown"
    topology.chains.loc[0, "chain_id"] = "explicit"
    topology.rebuild_chains(redefine_ids=False)
    assert topology.chains.chain_id.tolist()[0] == "explicit"


def test_group_inventory_get_select_extract_are_form_agnostic(group_system, tmp_path):
    filename = str(tmp_path / "source.h5msm")
    msm.convert(group_system, to_form=filename)
    dictionary = msm.convert(group_system.topology, to_form="molsysmt.TopologyDict")
    for source in (group_system, group_system.topology, dictionary, filename):
        assert msm.get(source, element="chain", group_index=True) == [
            [0, 1],
            [2],
            [3, 4],
            [],
        ]
        assert msm.select(source, element="group", selection="chain_id=='B'") == [2]
        subset = msm.extract(
            source, element="group", selection=[4, 0], to_form="molsysmt.Topology"
        )
        assert subset.groups.group_name.tolist() == ["GLY", "ALA"]
        assert subset.chain_groups == ((1,), (0,))


def test_group_inventory_default_extraction_and_invalid_repetitions(group_system):
    selected = msm.extract(group_system, selection="group_name=='TRP'")
    assert selected.topology.groups.group_name.tolist() == ["TRP"]
    assert selected.topology.chains.chain_id.tolist() == ["B"]
    with pytest.raises(ArgumentError):
        msm.extract(group_system, element="group", selection=[0, 0])
    with pytest.raises(ArgumentError):
        msm.extract(group_system, element="group", selection=[5])


def test_declared_membership_must_include_observed_atom_pairs():
    topology = Topology(n_atoms=2, n_groups=1, n_chains=2)
    topology.atoms["group_index"] = [0, 0]
    topology.atoms["chain_index"] = [0, 1]
    topology.set_chain_groups([[0], [0]])
    assert msm.get(topology, element="group", chain_index=True) == [[0, 1]]
    with pytest.raises(StructuralInconsistencyError):
        topology.set_chain_groups([[0], []])
    assert topology.chain_groups == ((0,), (0,))


def test_topology_layer_one_still_writes_without_explicit_relation(tmp_path):
    topology = Topology(n_atoms=1)
    path = str(tmp_path / "legacy_layer.h5msm")
    msm.convert(topology, to_form=path)
    with h5py.File(path) as file:
        assert file["topology"].attrs["schema_version"] == 1
        assert "chain_groups" not in file["topology"]
    loaded = msm.convert(path, to_form="molsysmt.Topology")
    assert loaded.n_atoms == 1
    assert loaded._chain_group_membership is None


def test_corrupt_membership_is_rejected(group_system, tmp_path):
    path = str(tmp_path / "invalid.h5msm")
    msm.convert(group_system, to_form=path)
    with h5py.File(path, "r+") as file:
        file["topology/chain_groups/offsets"][2] = 500
    with pytest.raises((ValueError, msm._private.smonitor.FormatError)):
        msm.convert(path, to_form="molsysmt.MolSys")


def test_builder_empty_chain_and_explicit_ids_are_retained():
    builder = msm.MolSysBuilder()
    builder.add_chain([], chain_id="source")
    assert builder.add_chain([]) == 1
    output = builder.build()
    assert output.topology.chains.chain_id.tolist() == ["source", "B"]
    assert output.topology.chain_groups == ((), ())
    assert output.topology.n_groups == output.topology.n_atoms == 0


def test_inventory_add_offsets_membership_and_preserves_occurrences(group_system):
    output = group_system.topology.copy()
    output.add(group_system.topology)
    assert output.chain_groups == ((0, 1), (2,), (3, 4), (), (5, 6), (7,), (8, 9), ())
    assert output.n_molecules == output.n_entities == output.n_chains == 8
    assert output.groups.molecule_index.tolist() == [0, 0, 1, 2, 2, 4, 4, 5, 6, 6]
    assert output.molecules.entity_index.tolist() == list(range(8))
    assert output.chains.chain_id.tolist() == ["A", "B", "C", "D"] * 2
    assert group_system.topology.n_groups == 5


def test_atom_extraction_remaps_explicit_membership():
    topology = Topology(n_atoms=3, n_groups=2, n_chains=2)
    topology.atoms["group_index"] = [0, 0, 1]
    topology.atoms["chain_index"] = [0, 0, 1]
    topology.set_chain_groups([[0], [1]])
    subset = topology.extract(atom_indices=[2])
    assert subset.n_atoms == subset.n_groups == subset.n_chains == 1
    assert subset.chain_groups == ((0,),)
    assert topology.chain_groups == ((0,), (1,))


def test_inventory_molecule_rebuild_preserves_empty_declared_slots(group_system):
    topology = group_system.topology.copy()
    topology.rebuild_molecules()
    assert topology.groups.molecule_index.tolist() == [0, 0, 1, 2, 2]
    assert topology.n_molecules == 4
    assert topology.n_groups == 5 and topology.n_atoms == 0
    assert not hasattr(topology, "_chemical_states_domain")


def test_atomic_builder_can_keep_a_group_without_stored_atoms():
    builder = msm.MolSysBuilder()
    atom = builder.add_atom(atom_name="C", atom_type="C")
    realized = builder.add_group([atom], group_name="LIG", group_type="small molecule")
    unbuilt = builder.add_group([], group_name="ALA", group_type="amino acid")
    builder.add_chain([realized, unbuilt])
    built = builder.build().topology
    assert built.n_atoms == 1 and built.n_groups == 2
    assert built.chain_groups == ((0, 1),)
    assert built.groups.group_name.tolist() == ["LIG", "ALA"]


def test_builder_rejects_reassignment_before_inserting_a_chain():
    builder = msm.MolSysBuilder()
    group = builder.add_group([], group_name="ALA")
    builder.add_chain([group])
    with pytest.raises(StructuralInconsistencyError):
        builder.add_chain([group])
    assert builder.topology.n_chains == 1
    builder.add_chain([group], allow_reassign=True)
    assert builder.topology.chain_groups == ((), (0,))


def test_empty_record_axes_are_available_even_without_children(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "empty_record.fasta"
    path.write_text(">empty\n", encoding="utf-8")
    system = msm.convert(str(path), to_form="molsysmt.MolSys")
    for element in ("chain", "molecule", "entity"):
        assert msm.has_attribute(system, element + "_index")
        assert msm.get(system, element=element, **{element + "_index": True}) == [0]
    assert system.topology.chain_groups == ((),)


def test_explicit_atomic_hierarchy_extraction_keeps_ordinary_atoms():
    builder = msm.MolSysBuilder()
    for name in ("C", "O", "N"):
        atom = builder.add_atom(atom_name=name, atom_type=name)
        group = builder.add_group([atom], group_name="LIG", group_type="small molecule")
        builder.add_chain([group])
    source = builder.build()
    subset = msm.extract(source, element="chain", selection=[2, 0])
    assert subset.topology.atoms.atom_name.tolist() == ["C", "N"]
    assert subset.topology.chains.chain_id.tolist() == ["A", "C"]
    assert source.topology.n_atoms == 3


def test_atom_permutation_preserves_explicit_group_axis():
    builder = msm.MolSysBuilder()
    first = builder.add_atom(atom_name="C", atom_type="C")
    second = builder.add_atom(atom_name="O", atom_type="O")
    group = builder.add_group(
        [first, second], group_name="LIG", group_type="small molecule"
    )
    builder.add_chain([group])
    source = builder.build()
    source.topology.set_chain_groups([[0]])
    result = msm.permute_atoms(source, [1, 0])
    assert result.topology.chain_groups == ((0,),)
    assert result.topology.atoms.atom_name.tolist() == ["O", "C"]
    assert source.topology.atoms.atom_name.tolist() == ["C", "O"]


def test_inventory_selectors_do_not_interpret_words_inside_labels(group_system):
    group_system.topology.entities.loc[0, "entity_name"] = (
        "protein within atom_name source@private"
    )
    assert msm.select(
        group_system,
        element="entity",
        selection="entity_name == 'protein within atom_name source@private'",
    ) == [0]


def test_group_extraction_preserves_optional_absence(group_system, tmp_path):
    path = str(tmp_path / "topology_only.h5msm")
    msm.h5msm.write_layers(path, topology=group_system.topology)
    source = msm.convert(path, to_form="molsysmt.MolSys")
    subset = msm.extract(source, element="group", selection=[2])
    assert subset.topology.groups.group_name.tolist() == ["TRP"]
    assert subset.topology.chain_groups == ((0,),)
    assert subset.structures is None
    assert subset.chemical_states is None
    assert source.topology.n_groups == 5


def test_group_and_structure_extraction_respect_both_axes(group_system):
    import numpy as np

    from molsysmt.native import Structures

    source = group_system.copy()
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.empty((3, 0, 3)), "nm"),
        time=msm.pyunitwizard.quantity([1, 2, 3], "ps"),
    )
    subset = msm.extract(
        source, element="group", selection=[2], structure_indices=[2, 0]
    )
    assert subset.topology.groups.group_name.tolist() == ["TRP"]
    assert subset.structures.n_structures == 2
    assert msm.pyunitwizard.get_value(
        subset.structures.time, to_unit="ps"
    ).tolist() == [3, 1]
    assert source.structures.n_structures == 3


def test_molsys_dict_round_trip_preserves_empty_occurrences_and_unknown_chemistry(
    group_system,
):
    payload = msm.convert(group_system, to_form="molsysmt.MolSysDict")
    restored = msm.convert(payload, to_form="molsysmt.MolSys")
    assert restored.topology.chain_groups == group_system.topology.chain_groups
    assert restored.topology.chains.chain_name.tolist() == [
        "first",
        "second",
        "first",
        "empty",
    ]
    assert restored.topology.n_molecules == restored.topology.n_entities == 4
    assert group_system.chemical_states is None
    assert restored.chemical_states is None


def test_fasta_extraction_uses_groups_when_the_form_has_no_atomic_axis(
    group_system, tmp_path
):
    source = str(tmp_path / "library.fasta")
    subset = msm.extract(
        source, element="group", selection="chain_id=='B'", to_form="molsysmt.Topology"
    )
    assert subset.groups.group_name.tolist() == ["TRP"]
    assert subset.chains.chain_id.tolist() == ["B"]
    assert subset.chain_groups == ((0,),)
