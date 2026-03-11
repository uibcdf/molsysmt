import molsysmt as msm
from molsysmt import pyunitwizard as puw
import numpy as np


def test_molsys_builder_builds_from_declared_atoms_groups_and_bonds():

    builder = msm.MolSysBuilder()
    atom_index_0 = builder.add_atom(atom_name="Na")
    atom_index_1 = builder.add_atom(atom_name="Cl")
    builder.add_group([atom_index_0], group_name="NA")
    builder.add_group([atom_index_1], group_name="CL")
    builder.add_bond(atom_index_0, atom_index_1)

    molsys = builder.build()

    assert molsys.topology.n_atoms == 2
    assert molsys.topology.n_groups == 2
    assert molsys.topology.n_components == 1
    assert molsys.topology.n_molecules == 1
    assert molsys.topology.n_entities == 1
    assert molsys.topology.n_chains == 1


def test_molsys_builder_build_creates_singleton_groups_for_orphan_atoms():

    builder = msm.MolSysBuilder()
    builder.add_atom(atom_name="Ar")
    builder.add_atom(atom_name="Ar")

    molsys = builder.build()

    assert molsys.topology.n_atoms == 2
    assert molsys.topology.n_groups == 2
    assert molsys.topology.groups["group_name"].tolist() == ["UNK", "UNK"]


def test_molsys_builder_preserves_explicit_hierarchy_and_structure_metadata():

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["N", "CA", "O"]]
    group_index_0 = builder.add_group(atom_indices[:2], group_name="ALA")
    group_index_1 = builder.add_group(atom_indices[2:], group_name="HOH")
    builder.add_chain([group_index_0, group_index_1], chain_name="A")
    molecule_index_0 = builder.add_molecule([group_index_0], molecule_name="protein 0", molecule_type="protein")
    molecule_index_1 = builder.add_molecule([group_index_1], molecule_name="water", molecule_type="water")
    builder.add_entity([molecule_index_0], entity_name="protein 0", entity_type="protein")
    builder.add_entity([molecule_index_1], entity_name="water", entity_type="water")
    builder.set_coordinates(puw.quantity(np.array([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [0.2, 0.0, 0.0]]), "nm"))
    builder.set_box(puw.quantity(np.eye(3)[np.newaxis, :, :], "nm"))
    builder.set_time(puw.quantity(np.array([0.0]), "ps"))
    builder.set_structure_id([0])

    molsys = builder.build()

    assert molsys.topology.chains["chain_name"].tolist() == ["A"]
    assert molsys.topology.molecules["molecule_name"].tolist() == ["protein 0", "water"]
    assert molsys.topology.entities["entity_name"].tolist() == ["protein 0", "water"]
    assert puw.get_value(molsys.structures.coordinates, to_unit="nm").shape == (1, 3, 3)
    assert puw.get_value(molsys.structures.box, to_unit="nm").shape == (1, 3, 3)
    assert puw.get_value(molsys.structures.time, to_unit="ps").tolist() == [0.0]
    assert molsys.structures.structure_id.tolist() == [0]


def test_molsys_builder_digesters_accept_optional_and_scalar_metadata():

    builder = msm.MolSysBuilder()
    atom_index = builder.add_atom(atom_id=7, atom_name="CA", atom_type=None)
    group_index = builder.add_group([atom_index], group_id="10", group_name="ALA", group_type=None)
    chain_index = builder.add_chain([group_index], chain_id="A", chain_name=None, chain_type=None)
    molecule_index = builder.add_molecule([group_index], molecule_id=20, molecule_name=None, molecule_type=None)
    entity_index = builder.add_entity([molecule_index], entity_id="30", entity_name=None, entity_type=None)

    assert atom_index == 0
    assert chain_index == 0
    assert entity_index == 0

    molsys = builder.build()

    assert molsys.topology.atoms["atom_id"].tolist() == ["7"]
    assert molsys.topology.groups["group_id"].tolist() == ["10"]
    assert molsys.topology.chains["chain_id"].tolist() == ["A"]
    assert molsys.topology.molecules["molecule_id"].tolist() == ["20"]
    assert molsys.topology.entities["entity_id"].tolist() == ["30"]


def test_molsys_builder_supports_declared_state_queries():

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["Ar", "Ar", "Ar"]]
    group_index = builder.add_group(atom_indices[:2], group_name="GAS")

    output = msm.get(
        builder,
        element="atom",
        selection="all",
        atom_index=True,
        atom_name=True,
        group_index=True,
        output_type="dictionary",
    )

    assert output["atom_index"] == [0, 1, 2]
    assert output["atom_name"] == ["Ar", "Ar", "Ar"]
    assert output["group_index"] == [group_index, group_index, None]
    assert msm.get(builder, element="system", n_groups=True) == 1
    assert msm.get(builder, element="system", n_molecules=True) == 0


def test_molsys_builder_converts_from_and_to_molsys():

    original = msm.convert(msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"], to_form="molsysmt.MolSys")
    builder = msm.convert(original, to_form="molsysmt.MolSysBuilder")
    rebuilt = msm.convert(builder, to_form="molsysmt.MolSys")

    assert rebuilt.topology.atoms["atom_id"].tolist() == original.topology.atoms["atom_id"].tolist()
    assert rebuilt.topology.atoms["atom_name"].tolist() == original.topology.atoms["atom_name"].tolist()
    assert rebuilt.topology.atoms["atom_type"].tolist() == original.topology.atoms["atom_type"].tolist()
    assert rebuilt.topology.groups["group_id"].tolist() == original.topology.groups["group_id"].tolist()
    assert rebuilt.topology.groups["group_name"].tolist() == original.topology.groups["group_name"].tolist()
    assert rebuilt.topology.groups["group_type"].tolist() == original.topology.groups["group_type"].tolist()
    assert rebuilt.topology.molecules["molecule_id"].tolist() == original.topology.molecules["molecule_id"].tolist()
    assert rebuilt.topology.molecules["molecule_name"].tolist() == original.topology.molecules["molecule_name"].tolist()
    assert rebuilt.topology.molecules["molecule_type"].tolist() == original.topology.molecules["molecule_type"].tolist()
    assert rebuilt.topology.chains["chain_id"].tolist() == original.topology.chains["chain_id"].tolist()
    assert rebuilt.topology.chains["chain_name"].tolist() == original.topology.chains["chain_name"].tolist()
    assert rebuilt.topology.chains["chain_type"].tolist() == original.topology.chains["chain_type"].tolist()
    assert rebuilt.topology.entities["entity_id"].tolist() == original.topology.entities["entity_id"].tolist()
    assert rebuilt.topology.entities["entity_name"].tolist() == original.topology.entities["entity_name"].tolist()
    assert rebuilt.topology.entities["entity_type"].tolist() == original.topology.entities["entity_type"].tolist()
    assert rebuilt.topology.bonds[["atom1_index", "atom2_index"]].values.tolist() == original.topology.bonds[["atom1_index", "atom2_index"]].values.tolist()
    assert np.allclose(
        puw.get_value(rebuilt.structures.coordinates, to_unit="nm"),
        puw.get_value(original.structures.coordinates, to_unit="nm"),
    )
    assert rebuilt.structures.box is original.structures.box is None
    if original.structures.time is None:
        assert rebuilt.structures.time is None
    else:
        assert np.allclose(
            puw.get_value(rebuilt.structures.time, to_unit="ps"),
            puw.get_value(original.structures.time, to_unit="ps"),
        )
    if original.structures.structure_id is None:
        assert rebuilt.structures.structure_id is None
    else:
        assert rebuilt.structures.structure_id.tolist() == original.structures.structure_id.tolist()


def test_molsys_builder_roundtrips_through_molsysdict_as_declared_state():

    builder = msm.MolSysBuilder()
    atom_index_0 = builder.add_atom(atom_id="10", atom_name="CA", atom_type=None)
    atom_index_1 = builder.add_atom(atom_name="CB")
    group_index = builder.add_group([atom_index_0, atom_index_1], group_name="ALA", group_type=None)
    builder.add_bond(atom_index_0, atom_index_1)
    builder.add_chain([group_index], chain_id="A")
    molecule_index = builder.add_molecule([group_index], molecule_name=None, molecule_type=None)
    builder.add_entity([molecule_index], entity_name=None, entity_type=None)
    builder.set_coordinates(puw.quantity(np.array([[0.0, 0.0, 0.0], [0.1, 0.0, 0.0]]), "nm"))
    builder.set_time(puw.quantity(np.array([0.0]), "ps"))
    builder.set_structure_id([3])

    molsys_dict = msm.convert(builder, to_form="molsysmt.MolSysDict")
    rebuilt_builder = msm.convert(molsys_dict, to_form="molsysmt.MolSysBuilder")

    assert msm.get(rebuilt_builder, element="atom", atom_name=True) == ["CA", "CB"]
    assert msm.get(rebuilt_builder, element="group", group_name=True) == ["ALA"]
    assert msm.get(rebuilt_builder, element="chain", chain_id=True) == ["A"]
    assert msm.get(rebuilt_builder, element="molecule", molecule_index=True) == [0]
    assert msm.get(rebuilt_builder, element="system", n_entities=True) == 1
    assert puw.get_value(rebuilt_builder.structures.coordinates, to_unit="nm").shape == (1, 2, 3)
    assert puw.get_value(rebuilt_builder.structures.time, to_unit="ps").tolist() == [0.0]
    assert rebuilt_builder.structures.structure_id.tolist() == [3]


def test_molsys_builder_remove_bonds_updates_declared_bond_count():

    builder = msm.MolSysBuilder()
    atom_indices = [builder.add_atom(atom_name=name) for name in ["N", "CA", "C"]]
    builder.add_group(atom_indices, group_name="ALA")
    builder.add_bond(atom_indices[0], atom_indices[1])
    builder.add_bond(atom_indices[1], atom_indices[2])

    builder.remove_bonds([0])

    assert builder.n_bonds == 1
    assert builder.topology.bonds[["atom1_index", "atom2_index"]].values.tolist() == [[1, 2]]


def test_molsys_builder_assign_groups_to_new_chain_reassigns_declared_membership():

    original = msm.convert(msm.systems["T4 lysozyme L99A"]["181l.h5msm"], to_form="molsysmt.MolSys")
    builder = msm.MolSysBuilder(original)

    water_group_indices = msm.select(
        builder,
        element="group",
        selection='group_type=="water"',
        syntax="MolSysMT",
    )

    new_chain_index = builder.assign_groups_to_new_chain(
        water_group_indices,
        chain_id="W",
        chain_name="waters",
        chain_type="water",
    )

    assert new_chain_index == builder.n_chains - 1
    assert msm.get(builder, element="chain", chain_id=True)[new_chain_index] == "W"
    assert msm.get(builder, element="chain", chain_name=True)[new_chain_index] == "waters"
    assert msm.get(builder, element="group", selection=water_group_indices[:3], chain_index=True) == [new_chain_index] * min(3, len(water_group_indices[:3]))
