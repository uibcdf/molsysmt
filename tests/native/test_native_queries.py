"""Protect native query semantics, validation and direct provider execution."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, MolSysBuilder, Structures, Topology


@pytest.fixture
def molsys():
    result = MolSys(n_atoms=4)
    result.topology.atoms["atom_name"] = ["C0", "O1", "N2", "H3"]
    result.topology.atoms["atom_id"] = ["10", "20", "30", "40"]
    result.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(36).reshape(3, 4, 3), "nm"),
        time=msm.pyunitwizard.quantity([0, 2, 4], "ps"),
        box=msm.pyunitwizard.quantity(np.tile(np.eye(3), (3, 1, 1)), "nm"),
    )
    return result


def objects(molsys):
    interactions = msm.Interactions.from_records(
        [],
        n_atoms=4,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="native_query_test",
    )
    return [
        molsys,
        molsys.topology,
        molsys.structures,
        molsys.chemical_states,
        MolSysBuilder(molsys),
        interactions,
    ]


@pytest.mark.parametrize("position", range(6))
def test_common_metadata_empty_queries_and_representations(molsys, position):
    obj = objects(molsys)[position]
    assert obj.get(n_atoms=True) == 4
    assert obj.get() == []
    assert obj.get(output_type="dictionary") == {}
    assert obj.get(n_atoms=False, output_type="dictionary") == {}
    for output_type in ["dataframe", "styler", "dictionary"]:
        result = obj.info(output_type=output_type)
        if output_type == "styler":
            result = result.data
        expected = msm.info(obj, output_type="dataframe")
        if output_type == "dictionary":
            assert result == expected.to_dict(orient="records")
        else:
            pd.testing.assert_frame_equal(result, expected)
        assert expected["n_atoms"].tolist() == [4]


@pytest.mark.parametrize("position", range(6))
@pytest.mark.parametrize(
    "options",
    [
        {"output_type": "invalid"},
        {"skip_digestion": "yes"},
        {"n_atoms": "yes"},
        {"get_missing_bonds": "yes"},
    ],
)
def test_all_native_boundaries_reject_invalid_values(molsys, position, options):
    with pytest.raises(ArgumentError):
        objects(molsys)[position].get(**{"n_atoms": True, **options})


@pytest.mark.parametrize("position", range(6))
def test_all_native_boundaries_reject_unknown_keywords_and_bad_info(molsys, position):
    from argdigest.core.errors import UnknownArgumentError

    obj = objects(molsys)[position]
    with pytest.raises(UnknownArgumentError):
        obj.get(not_an_attribute=True)
    with pytest.raises(UnknownArgumentError):
        obj.info(unknown=True)
    for options in [{"skip_digestion": "yes"}, {"output_type": "invalid"}]:
        with pytest.raises(ArgumentError):
            obj.info(**options)


@pytest.mark.parametrize("position", [0, 1, 2, 4])
def test_aliases_indices_mask_order_and_bounds(molsys, position):
    obj = objects(molsys)[position]
    assert obj.get(element="ATOMS", selection=[3, 0, 3], atom_index=True) == [3, 0, 3]
    assert obj.get(
        element="atom", selection=[3, 0, 2], mask=[2, 3], atom_index=True
    ) == [2, 3]
    assert obj.get(
        element="atom",
        selection=[3, 0, 2],
        mask=[True, False, True, False],
        atom_index=True,
    ) == [0, 2]
    assert obj.get(element="atom", selection=[], atom_index=True) == []
    with pytest.raises(ArgumentError):
        obj.get(element="atom", selection=[4], atom_index=True)
    with pytest.raises(ArgumentError):
        obj.get(element="atom", mask=[True], atom_index=True)


@pytest.mark.parametrize("position", [0, 2, 4])
def test_quantities_selected_axes_mixed_levels_and_copy(molsys, position):
    obj = objects(molsys)[position]
    with msm.pyunitwizard.context(standard_units=["angstrom", "ps"]):
        result = obj.get(
            element="atom",
            selection=[3, 1],
            structure_indices=[2, 0, 2],
            output_type="dictionary",
            coordinates=True,
            time=True,
        )
    assert list(result) == ["coordinates", "time"]
    assert result["coordinates"].shape == (3, 2, 3)
    assert msm.pyunitwizard.get_unit(result["coordinates"]) == msm.pyunitwizard.unit(
        "angstrom"
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result["coordinates"]),
        [
            [[330, 340, 350], [270, 280, 290]],
            [[90, 100, 110], [30, 40, 50]],
            [[330, 340, 350], [270, 280, 290]],
        ],
    )
    np.testing.assert_array_equal(msm.pyunitwizard.get_value(result["time"]), [4, 0, 4])
    stored = obj.structures if hasattr(obj, "structures") else obj
    assert not np.shares_memory(
        msm.pyunitwizard.get_value(result["coordinates"]), stored._coordinates
    )
    empty = obj.get(
        element="atom", selection=[], structure_indices=[], coordinates=True
    )
    assert empty.shape == (0, 0, 3)
    with pytest.raises(ArgumentError):
        obj.get(structure_indices=[3], coordinates=True)


def test_explicit_native_queries_do_not_discover_convert_or_select(molsys, monkeypatch):
    source_objects = objects(molsys)

    def forbidden(*args, **kwargs):
        raise AssertionError("explicit native queries must use known providers")

    for namespace in [msm, msm.basic]:
        for name in [
            "get",
            "info",
            "get_form",
            "where_is_attribute",
            "select",
            "convert",
        ]:
            monkeypatch.setattr(namespace, name, forbidden)
    for obj in source_objects:
        assert obj.get(n_atoms=True) == 4
        assert obj.info(output_type="dataframe")["n_atoms"].tolist() == [4]
    for obj in [molsys, molsys.topology, molsys.structures]:
        assert obj.get(
            element="atom", selection=[3, 1], mask=[1, 2, 3], index=True
        ) == [1, 3]
        assert obj.info(element="atom", selection=[2, 0], output_type="dataframe")[
            "index"
        ].tolist() == [2, 0]
    assert molsys.get(
        element="atom", selection=[3], structure_indices=[2], coordinates=True
    ).shape == (1, 1, 3)


def test_state_resolution_preserves_reference_and_structure_associations(molsys):
    msm.set(molsys, element="atom", formal_charge=[0, 0, 0, 0])
    second = molsys.chemical_states._states[0].copy()
    second.set_atom_attribute("formal_charge", [1, -1, 0, 0])
    molsys.chemical_states._states.append(second)
    molsys._set_structure_chemical_state_indices([1, 0, 1])
    for obj in [molsys, molsys.topology]:
        assert obj.get(element="atom", chemical_state=1, formal_charge=True) == [
            1,
            -1,
            0,
            0,
        ]
        assert obj.get(element="atom", formal_charge=True) == [0, 0, 0, 0]
    assert molsys.get(
        element="atom",
        structure_indices=[2, 0],
        chemical_state="structure",
        formal_charge=True,
    ) == [1, -1, 0, 0]
    with pytest.raises(StructuralInconsistencyError):
        molsys.get(
            structure_indices=[0, 1], chemical_state="structure", formal_charge=True
        )
    assert molsys.chemical_states.get(n_chemical_states=True) == 2


def test_expression_selection_uses_existing_parser(molsys):
    assert molsys.get(element="atom", selection='atom_name == "N2"', index=True) == [2]
    assert molsys.info(
        element="atom", selection='atom_name == "N2"', output_type="dataframe"
    )["index"].tolist() == [2]


def test_partial_empty_and_edited_domains_do_not_cache_counts(molsys):
    partial = MolSys._from_partial_domains(structures=molsys.structures)
    assert partial.get(n_atoms=True, n_structures=True, atom_name=True) == [4, 3, None]
    assert partial.info(output_type="dictionary")[0]["n_atoms"] == 4
    assert Structures().get(n_atoms=True, n_structures=True) == [0, 0]
    time_only = Structures(time=msm.pyunitwizard.quantity([1, 2], "ps"))
    assert time_only.get(n_atoms=True, n_structures=True) == [0, 2]
    velocities = Structures(
        velocities=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm/ps")
    )
    assert velocities.get(n_atoms=True, n_structures=True) == [3, 2]
    assert msm.get(velocities, n_atoms=True) == 3
    builder = MolSysBuilder()
    assert builder.get(n_atoms=True) == 0
    builder.add_atom(atom_name="C", atom_type="C")
    assert builder.get(n_atoms=True) == 1
    assert builder.info(output_type="dataframe")["n_atoms"].tolist() == [1]


def test_inherited_native_boundary_keeps_its_attribute_contract(molsys):
    from argdigest.core.errors import UnknownArgumentError

    class CustomTopology(Topology):
        pass

    topology = CustomTopology(n_atoms=2, skip_digestion=True)
    assert topology.get(element="atom", selection=1, index=True) == [1]
    with pytest.raises(UnknownArgumentError):
        topology.get(unknown=True)
    assert topology.info(output_type="dataframe")["n_atoms"].tolist() == [2]


def test_sparse_specialized_methods_and_views_remain_available(molsys):
    result = objects(molsys)[-1]
    selected = result.query(structure_indices=[2, 1, 2])
    assert selected.get(n_atoms=True, n_structures=True) == [4, 3]
    assert selected.n_interactions == 0
    assert selected.to_dict()["evaluated_structure_indices"].tolist() == [2]


@pytest.mark.parametrize("argument", ["selection", "mask"])
def test_info_spatial_scope_is_shared_by_native_and_general_paths(molsys, argument):
    values = np.zeros((2, 4, 3))
    values[:, :, 0] = [[0, 0.1, 2, 3], [0, 2, 0.1, 3]]
    molsys.structures = Structures(coordinates=msm.pyunitwizard.quantity(values, "nm"))
    expression = "atom_index != 0 within 0.3 nm of atom_index == 0"
    options = {argument: expression}
    for operation in [molsys.info, lambda **kwargs: msm.info(molsys, **kwargs)]:
        selected = operation(
            element="atom", structure_indices=[1], output_type="dataframe", **options
        )
        assert selected["index"].tolist() == [2]
        assert operation(structure_indices=[1], output_type="dataframe", **options)[
            "n_atoms"
        ].tolist() == [1]


@pytest.mark.parametrize("native", [False, True])
def test_selected_hierarchy_counts_exclude_missing_membership(native):
    molsys = MolSys(n_atoms=4)
    operation = molsys.get if native else lambda **kwargs: msm.get(molsys, **kwargs)
    assert operation(
        element="atom",
        selection=[2, 0],
        n_groups=True,
        n_molecules=True,
        n_entities=True,
        n_chains=True,
    ) == [0, 0, 0, 0]
    table = molsys.info(selection=[2, 0], output_type="dataframe")
    assert table["n_atoms"].tolist() == [2]
    assert table[
        ["n_groups", "n_molecules", "n_entities", "n_chains"]
    ].values.tolist() == [[0, 0, 0, 0]]


def test_hierarchy_counts_follow_only_explicit_parent_links():
    topology = Topology(n_atoms=5, n_groups=3, n_molecules=2, n_entities=1, n_chains=1)
    topology.atoms["group_index"] = pd.array([0, None, 1, 2, 0], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0, None, None, None, 0], dtype="Int64")
    topology.groups["molecule_index"] = pd.array([0, 1, None], dtype="Int64")
    topology.groups["group_type"] = ["ion", "water", "small molecule"]
    topology.molecules["entity_index"] = pd.array([0, None], dtype="Int64")
    topology.molecules["molecule_type"] = ["protein", "peptide"]
    flags = dict(
        n_groups=True,
        n_molecules=True,
        n_entities=True,
        n_chains=True,
        n_ions=True,
        n_waters=True,
        n_small_molecules=True,
        n_proteins=True,
        n_peptides=True,
    )
    for operation in [topology.get, lambda **kwargs: msm.get(topology, **kwargs)]:
        assert operation(element="atom", selection=[1, 2, 3, 4, 4], **flags) == [
            3,
            2,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ]
        assert operation(element="atom", selection=[1], **flags) == [0] * 9
        assert operation(element="atom", selection=[], **flags) == [0] * 9


@pytest.mark.parametrize("native", [False, True])
def test_plain_scalar_counts_do_not_probe_quantity_backends(
    molsys, monkeypatch, native
):
    def forbidden(value):
        raise AssertionError("a plain atom count needs no quantity-backend probe")

    monkeypatch.setattr(msm.pyunitwizard, "is_quantity", forbidden)
    operation = molsys.get if native else lambda **kwargs: msm.get(molsys, **kwargs)
    assert operation(n_atoms=True) == 4
