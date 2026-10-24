"""Literal correspondence guards for a full molecular atom permutation (#369)."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures, Topology

ORDER = [1, 5, 0, 3, 2, 4]
INVERSE = [2, 0, 4, 3, 5, 1]


def rich_system():
    top = Topology(
        n_atoms=6, n_groups=2, n_chains=2, n_molecules=2, n_entities=2, n_components=3
    )
    top.atoms["atom_id"] = ["9", "17", "4", "99", "2", "45"]
    top.atoms["atom_name"] = ["C0", "N1", "C2", "S3", "F4", "Cl5"]
    top.atoms["atom_type"] = ["C", "N", "C", "S", "F", "Cl"]
    top.atoms["group_index"] = pd.array([0, 1, 0, 1, 0, 0], dtype="Int64")
    top.atoms["chain_index"] = pd.array([0, 1, 0, 1, 0, 0], dtype="Int64")
    top.groups["molecule_index"] = pd.array([0, 1], dtype="Int64")
    top.molecules["entity_index"] = pd.array([0, 1], dtype="Int64")
    top.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 0, 2, 1],
            atom2_index=[2, 4, 5, 3],
            bond_order=[2, 1, 1, 1],
            stereochemistry=["E", None, None, None],
            stereo_atom1_index=[4, None, None, None],
            stereo_atom2_index=[5, None, None, None],
            donor_atom_index=[None, None, None, 1],
            acceptor_atom_index=[None, None, None, 3],
        )
    )
    state = top._chemical_states[0]
    state.component_indices = pd.Series(pd.array([0, 1, 0, 1, 0, 0], dtype="Int64"))
    state.set_atom_attribute("formal_charge", [0, 1, 0, -1, 0, 0])
    source = MolSys()
    source.topology = top
    state.connectivity_completeness = "complete"
    second = state.copy()
    second.state_id = "second"
    second.connectivity_completeness = "partial"
    second.set_atom_attribute("formal_charge", [1, 0, 0, -1, 0, 0])
    source.chemical_states._append_state(second)
    structures = Structures()
    structures.append(
        coordinates=msm.pyunitwizard.quantity(
            np.arange(54).reshape(3, 6, 3), "angstrom"
        ),
        box=msm.pyunitwizard.quantity(np.tile(np.eye(3) * 30, (3, 1, 1)), "angstrom"),
        time=msm.pyunitwizard.quantity([0, 2, 4], "ps"),
    )
    structures.velocities = msm.pyunitwizard.quantity(
        np.arange(54).reshape(3, 6, 3), "nm/ps"
    )
    structures.occupancy = np.arange(18).reshape(3, 6) / 18
    structures.b_factor = msm.pyunitwizard.quantity(
        np.arange(18).reshape(3, 6), "nm**2"
    )

    def site(label, xyz):
        return dict(
            location_id=[label],
            occupancy=[0.5],
            b_factor=msm.pyunitwizard.quantity([0.1], "nm**2"),
            atom_id=["alternate"],
            coordinates=msm.pyunitwizard.quantity([xyz], "nm"),
        )

    structures.alternate_location = [
        {4: site("B", [1, 2, 3])},
        {},
        {1: site("C", [4, 5, 6])},
    ]
    structures.bioassembly = {
        "1": {
            "chain_indices": [[1, 0]],
            "rotations": np.eye(3)[None],
            "translations": msm.pyunitwizard.quantity([[0.0, 0.0, 0.0]], "nm"),
        }
    }
    source.structures = structures
    source._set_structure_chemical_state_indices([1, 0, 1])
    source.molecular_mechanics.partial_charge = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    source.molecular_mechanics.atom_ff_type = ["C", "N", "C", "S", "F", "Cl"]
    records = [
        dict(
            structure_index=0,
            interaction_type="pi_pi",
            participants=[
                dict(role="ring", atom_indices=[0, 2, 4]),
                dict(role="ring", atom_indices=[1, 3, 5]),
            ],
            measurements={"distance": distance},
            images=[[0, 0, 0], [1, 0, 0]],
        )
        for distance in [0.3, 0.4]
    ]
    analysis = msm.Interactions.from_records(
        records,
        n_atoms=6,
        n_structures=3,
        evaluated_structure_indices=[0, 1],
        measure_units={"distance": "nm"},
        method="synthetic",
        atom_source_indices=[15, 14, 13, 12, 11, 10],
        source_n_atoms=16,
    )
    source.interactions = {"rings": analysis}
    return source


def test_all_domains_follow_literal_expected_axis_and_source_stays_unchanged():
    source = rich_system()
    before = source.copy()
    result = msm.permute_atoms(source, ORDER, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert report["output_to_source_atom_indices"].tolist() == ORDER
    assert report["source_to_output_atom_indices"].tolist() == INVERSE
    assert output.topology.atoms.atom_id.tolist() == ["17", "45", "9", "99", "4", "2"]
    assert output.topology.atoms.group_index.tolist() == [1, 0, 0, 1, 0, 0]
    assert output.topology.atoms.chain_index.tolist() == [1, 0, 0, 1, 0, 0]
    for name in ["groups", "chains", "molecules", "entities"]:
        pd.testing.assert_frame_equal(
            getattr(output.topology, name),
            getattr(source.topology, name),
            check_frame_type=False,
        )
    for first, second in zip(
        source.chemical_states._states, output.chemical_states._states
    ):
        pd.testing.assert_frame_equal(
            first.components, second.components, check_frame_type=False
        )
        assert len(second.components) == 3
        assert second.connectivity_completeness == first.connectivity_completeness
        assert second.component_indices.tolist() == [1, 0, 0, 1, 0, 0]
        assert (
            second.atom_attributes.formal_charge.tolist()
            == first.atom_attributes.formal_charge.iloc[ORDER].tolist()
        )
        assert second.bonds[["atom1_index", "atom2_index"]].values.tolist() == [
            [2, 4],
            [2, 5],
            [0, 3],
            [1, 4],
        ]
        assert second.bonds.loc[
            0, ["stereo_atom1_index", "stereo_atom2_index"]
        ].tolist() == [5, 1]
        assert second.bonds.loc[
            2, ["donor_atom_index", "acceptor_atom_index"]
        ].tolist() == [0, 3]
        assert second.bonds.loc[0, "stereochemistry"] == "E"
    assert output._structure_chemical_state_indices.tolist() == [1, 0, 1]
    for field, unit in [
        ("coordinates", "nm"),
        ("velocities", "nm/ps"),
        ("b_factor", "nm**2"),
    ]:
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(getattr(output.structures, field), to_unit=unit),
            msm.pyunitwizard.get_value(getattr(source.structures, field), to_unit=unit)[
                :, ORDER
            ],
        )
    np.testing.assert_array_equal(
        output.structures.occupancy, source.structures.occupancy[:, ORDER]
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.box, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.box, to_unit="nm"),
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.time, to_unit="ps"),
        msm.pyunitwizard.get_value(source.structures.time, to_unit="ps"),
    )
    assert [list(sites) for sites in output.structures.alternate_location] == [
        [5],
        [],
        [0],
    ]
    assert output.structures.alternate_location[0][5]["location_id"] == ["B"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            output.structures.alternate_location[0][5]["coordinates"], to_unit="nm"
        ),
        msm.pyunitwizard.get_value(
            source.structures.alternate_location[0][4]["coordinates"], to_unit="nm"
        ),
    )
    np.testing.assert_array_equal(
        output.structures.bioassembly["1"]["chain_indices"], [[1, 0]]
    )
    assert output.molecular_mechanics.partial_charge.tolist() == [
        0.2,
        0.6,
        0.1,
        0.4,
        0.3,
        0.5,
    ]
    analysis = output.interactions["rings"]
    assert analysis.atom_source_indices.tolist() == [14, 10, 15, 12, 13, 11]
    assert (
        analysis.query(atom_indices=[2], structure_indices=[2, 1, 0]).n_interactions
        == 2
    )
    assert analysis.query(structure_indices=[1]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert (
        analysis.query(structure_indices=[2])
        .to_dict()["evaluated_structure_indices"]
        .tolist()
        == []
    )
    assert analysis.query().to_dict()["occurrence_indices"].tolist() == [0, 1]
    np.testing.assert_array_equal(
        analysis.image_vectors, source.interactions["rings"].image_vectors
    )
    restored = msm.permute_atoms(output, INVERSE)
    pd.testing.assert_frame_equal(
        restored.topology.atoms, source.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        source.topology.atoms, before.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].bonds,
        before.chemical_states._states[0].bonds,
        check_frame_type=False,
    )
    assert source.interactions["rings"].query().to_dict()[
        "occurrence_indices"
    ].tolist() == [0, 1]
    output.topology.atoms.loc[0, "atom_name"] = "changed"
    assert source.topology.atoms.loc[1, "atom_name"] == "N1"


def test_endpoint_reversal_swaps_stereo_neighbors_but_preserves_directed_roles():
    source = rich_system()
    output = msm.permute_atoms(source, [5, 4, 3, 2, 1, 0])
    bonds = output.chemical_states._states[0].bonds
    assert bonds.loc[
        0, ["atom1_index", "atom2_index", "stereo_atom1_index", "stereo_atom2_index"]
    ].tolist() == [3, 5, 0, 1]
    assert bonds.loc[2, ["donor_atom_index", "acceptor_atom_index"]].tolist() == [4, 2]


@pytest.mark.parametrize(
    "order",
    [
        [0, 0, 2],
        [0, 1],
        [0, 1, 3],
        [0, -1, 2],
        [False, 1, 2],
        [0.0, 1.0, 2.0],
        [[0, 1, 2]],
        0,
        "all",
        None,
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_invalid_axes_are_rejected_even_at_trusted_boundary(order, skip):
    source = MolSys(n_atoms=3)
    with pytest.raises(ArgumentError):
        msm.permute_atoms(source, order, skip_digestion=skip)
    assert source.get_n_atoms() == 3


@pytest.mark.parametrize("unit", ["nm", "dimensionless"])
def test_quantities_cannot_become_indices(unit):
    with pytest.raises(ArgumentError):
        msm.permute_atoms(MolSys(n_atoms=3), msm.pyunitwizard.quantity([0, 1, 2], unit))


def test_empty_and_identity_are_independent_without_geometry_duplication():
    assert msm.permute_atoms(MolSys(n_atoms=0), []).get_n_atoms() == 0
    source = rich_system()
    result = msm.permute_atoms(source, list(range(6)))
    assert result.structures._coordinates is not source.structures._coordinates
    assert np.shares_memory(
        result.structures._coordinates._blocks[0],
        source.structures._coordinates._blocks[0],
    )
    assert result.chemical_states is result.topology._chemical_states_domain
    assert result.chemical_states is not source.chemical_states
    assert result.structures._molsys_owner_ref() is result


def test_no_dense_geometry_or_extract_fallback(monkeypatch):
    from molsysmt.native._structure_array import _StructureArray

    source = rich_system()

    def forbidden(*args, **kwargs):
        pytest.fail("Full geometry materialization/extract is not a permutation route")

    monkeypatch.setattr(_StructureArray, "_dense", forbidden)
    monkeypatch.setattr(Topology, "extract", forbidden)
    output = msm.permute_atoms(source, ORDER)
    np.testing.assert_allclose(
        output.structures._coordinates._select([0], [0]), [[[0.3, 0.4, 0.5]]]
    )


def test_budget_failure_precedes_output_copy(monkeypatch):
    source = rich_system()
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1)
    with pytest.raises(MemoryBudgetExceededError):
        msm.permute_atoms(source, ORDER)
    assert source.topology.atoms.atom_id.tolist() == ["9", "17", "4", "99", "2", "45"]


@pytest.mark.parametrize(
    "damage", ["extension", "metadata", "bad_reference", "mismatched_axis", "subclass"]
)
def test_unsupported_or_inconsistent_domains_fail_explicitly(damage):
    source = rich_system()
    if damage == "extension":
        source.extra_atom_vectors = np.arange(6)
    elif damage == "metadata":
        source.topology.atoms.attrs["atom_order"] = list(range(6))
    elif damage == "bad_reference":
        source.chemical_states._states[0].bonds.loc[0, "stereo_atom1_index"] = 77
    elif damage == "mismatched_axis":
        source.molecular_mechanics.atoms_ff = source.molecular_mechanics.atoms_ff.iloc[
            :3
        ]
    else:

        class Extended(MolSys):
            pass

        source.__class__ = Extended
    with pytest.raises(StructuralInconsistencyError):
        msm.permute_atoms(source, ORDER, skip_digestion=(damage == "subclass"))


def test_structures_only_and_foreign_form_conversion():
    coordinates = msm.pyunitwizard.quantity(np.arange(18).reshape(2, 3, 3), "angstrom")
    source = MolSys._from_partial_domains(
        structures=Structures(coordinates=coordinates)
    )
    output = msm.permute_atoms(source, [2, 0, 1])
    assert output.topology is None and output.chemical_states is None
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="angstrom"),
        np.arange(18).reshape(2, 3, 3)[:, [2, 0, 1]],
    )
    foreign = msm.permute_atoms(
        msm.systems["caffeine"]["caffeine.sdf"], list(range(23, -1, -1))
    )
    assert foreign.get_n_atoms() == 24


def test_h5msm_preserves_permuted_chemistry_structures_and_interactions(tmp_path):
    output = msm.permute_atoms(rich_system(), ORDER)
    # H5MSM 0.5 explicitly excludes experimental mechanics persistence.
    from molsysmt.native import MolecularMechanics

    output.molecular_mechanics = MolecularMechanics()
    target = tmp_path / "permuted.h5msm"
    msm.convert(output, to_form=target)
    restored = msm.convert(target, to_form="molsysmt.MolSys")
    assert restored.topology.atoms.atom_id.tolist() == ["17", "45", "9", "99", "4", "2"]
    assert restored.chemical_states.n_chemical_states == 2
    assert restored.chemical_states._states[0].bonds.loc[0, "stereo_atom2_index"] == 1
    assert restored.interactions["rings"].query().to_dict()[
        "occurrence_indices"
    ].tolist() == [0, 1]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
    )


def test_named_assignments_rebind_without_recalculation_and_stale_stays_stale():
    from tests.build.test_assign_autodock_atom_types import prepared

    source = msm.build.assign_autodock_atom_types(
        prepared("CO"), typing_scheme="autodock4"
    )
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    order = list(range(source.get_n_atoms() - 1, -1, -1))
    output = msm.permute_atoms(source, order)
    for field in ("partial_charge_assignment", "atom_type_assignment"):
        original = getattr(source.molecular_mechanics, field)
        report = getattr(output.molecular_mechanics, field)
        assert report["status"] == "projected"
        assert report["software"] == original["software"]
        assert report["method"] == original["method"]
        assert (
            report["atom_source_indices"].tolist()
            == original["atom_source_indices"][order].tolist()
        )
        assert (
            report["atom_order_transform"]["output_to_input_atom_indices"].tolist()
            == order
        )
    from molsysmt._private.partial_charges import validate_assignment

    validate_assignment(output)
    from molsysmt._private.autodock_assignment import (
        validate_assignment as validate_types,
    )

    validate_types(output, "autodock4")
    source.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] += 1
    assert (
        msm.permute_atoms(source, order).molecular_mechanics.partial_charge_assignment[
            "status"
        ]
        == "stale"
    )


def test_permutation_map_composes_with_projection_origins():
    from tests.build.test_merge_nonpolar_hydrogens import declared_methanol

    source = msm.build.merge_nonpolar_hydrogens(
        declared_methanol(), typing_scheme="autodock4", return_report=True
    )
    permuted = msm.permute_atoms(
        source["molecular_system"], [2, 0, 1], return_report=True
    )
    combined = msm.compose_atom_maps([source["report"], permuted["report"]])
    assert combined["source_to_output_atom_indices"].tolist() == [1, 2, -1, -1, -1, 0]
    assert combined["output_to_source_atom_indices"].tolist() == [5, 0, 1]
    assert combined["source_to_representative_atom_indices"].tolist() == [
        1,
        2,
        1,
        1,
        1,
        0,
    ]


@pytest.mark.parametrize(
    "smiles", ["F/C=C/Cl", "F/C=C\\Cl", "N[C@@H](C)C(=O)O", "C1CCCCC1"]
)
def test_rdkit_independently_recovers_absolute_atom_and_double_bond_stereo(smiles):
    Chem = pytest.importorskip("rdkit.Chem")

    reference = Chem.MolFromSmiles(smiles)
    source = msm.convert(reference, to_form="molsysmt.MolSys")
    output = msm.permute_atoms(source, list(range(source.get_n_atoms() - 1, -1, -1)))
    restored = msm.convert(output, to_form="rdkit.Mol")
    assert Chem.MolToSmiles(restored, isomericSmiles=True) == Chem.MolToSmiles(
        reference, isomericSmiles=True
    )


def test_partial_domains_keep_their_absence_and_maps():
    source = rich_system()
    chemistry = MolSys._from_partial_domains(
        chemical_states=source.chemical_states.copy()
    )
    output = msm.permute_atoms(chemistry, ORDER)
    assert output.topology is None and output.structures is None
    assert output.chemical_states._states[0].component_indices.tolist() == [
        1,
        0,
        0,
        1,
        0,
        0,
    ]
    interactions = MolSys._from_partial_domains(
        interactions={"rings": source.interactions["rings"]}
    )
    output = msm.permute_atoms(interactions, ORDER)
    assert output.topology is None and output.structures is None
    assert output.interactions["rings"].atom_source_indices.tolist() == [
        14,
        10,
        15,
        12,
        13,
        11,
    ]


def test_multiple_coordinate_blocks_are_bounded_and_keep_exact_structure_order(
    monkeypatch,
):
    from molsysmt._private.execution import ChunkedExecutor
    from molsysmt.native._structure_array import _BLOCK_BYTES, _StructureArray

    values = np.arange(81 * 1000 * 3, dtype=float).reshape(81, 1000, 3) / 100
    source = MolSys._from_partial_domains(
        structures=Structures(coordinates=msm.pyunitwizard.quantity(values, "nm"))
    )
    observed = []
    build = ChunkedExecutor._build_chunk

    def capture(*args, **kwargs):
        chunk = build(*args, **kwargs)
        observed.append(chunk["coordinates"].nbytes)
        return chunk

    monkeypatch.setattr(ChunkedExecutor, "_build_chunk", staticmethod(capture))
    output = msm.permute_atoms(source, np.arange(999, -1, -1))
    assert len(observed) >= 2 and max(observed) <= _BLOCK_BYTES
    assert isinstance(output.structures._coordinates, _StructureArray)
    np.testing.assert_array_equal(
        output.structures._coordinates._select([80, 0, 43], [0, 999, 30]),
        values[[80, 0, 43]][:, [999, 0, 969]],
    )


def test_atom_references_cannot_hide_in_mechanics_settings():
    source = rich_system()
    source.molecular_mechanics.constraints = [(0, 1)]
    with pytest.raises(StructuralInconsistencyError):
        msm.permute_atoms(source, ORDER)


def test_historical_preparation_maps_are_not_reinterpreted_as_current_indices():
    from tests.build.test_assign_autodock_atom_types import prepared

    source = msm.build.assign_autodock_atom_types(
        prepared("CO"), typing_scheme="autodock4"
    )
    source = msm.build.assign_partial_charges(source, method="gasteiger_marsili")
    source = msm.build.merge_nonpolar_hydrogens(source, typing_scheme="autodock4")
    original = source.molecular_mechanics.partial_charge_assignment
    output = msm.permute_atoms(source, [2, 0, 1])
    report = output.molecular_mechanics.partial_charge_assignment
    assert (
        report["source_assignment"]["software"]
        == original["source_assignment"]["software"]
    )
    assert (
        report["source_assignment"]["atom_source_indices"].tolist()
        == original["source_assignment"]["atom_source_indices"].tolist()
    )
    from molsysmt._private.partial_charges import validate_assignment

    validate_assignment(output)


def test_known_pdbqt_writer_axis_can_be_restored_without_reconstruction():
    from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
    from tests.form.file_pdbqt.test_known_source_poses import rigid_tree

    source = declared_methanol()
    text, export_map = msm.convert(
        source,
        to_form="string:pdbqt_text",
        structure_indices=[0],
        typing_scheme="autodock4",
        torsion_tree=rigid_tree(source, [1, 0, 5, 4, 3, 2]),
        return_atom_map=True,
    )
    parsed = msm.convert(text, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    restored = msm.permute_atoms(parsed, export_map["source_to_output_atom_indices"])
    assert parsed.topology.atoms.atom_id.tolist() == ["3", "17", "11", "7", "90", "45"]
    assert restored.topology.atoms.atom_id.tolist() == [
        "17",
        "3",
        "45",
        "90",
        "7",
        "11",
    ]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm")[:1],
        atol=0.00005,
    )
    assert restored.molecular_mechanics.atom_ff_type.tolist() == [
        "C",
        "OA",
        "H",
        "H",
        "H",
        "HD",
    ]
    # PDBQT's partial graph remains partial; applying an axis adds no bonds.
    assert len(restored.topology.bonds) == len(parsed.topology.bonds)


def test_structures_only_h5msm_preserves_new_atom_axis(tmp_path):
    source = MolSys._from_partial_domains(
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.arange(18).reshape(2, 3, 3), "nm")
        )
    )
    output = msm.permute_atoms(source, [2, 0, 1])
    filename = tmp_path / "only_structures.h5msm"
    msm.convert(output, to_form=filename)
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.topology is None and restored.chemical_states is None
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        np.arange(18).reshape(2, 3, 3)[:, [2, 0, 1]],
    )


def test_output_coordinate_edits_do_not_modify_or_invalidate_source():
    source = rich_system()
    output = msm.permute_atoms(source, ORDER)
    original = source.structures._coordinates._select([0], [1]).copy()
    msm.set(
        output,
        selection=[0],
        structure_indices=[0],
        coordinates=msm.pyunitwizard.quantity([[[7.0, 8.0, 9.0]]], "nm"),
    )
    np.testing.assert_array_equal(
        source.structures._coordinates._select([0], [1]), original
    )
    assert source.interactions["rings"].query(structure_indices=[0]).n_interactions == 2
    assert output.interactions["rings"].query(structure_indices=[0]).n_interactions == 0


def test_missing_canonical_atom_columns_are_rejected():
    source = MolSys(n_atoms=3)
    source.topology.atoms = pd.DataFrame({"atom_name": ["C", "N", "O"]})
    with pytest.raises(StructuralInconsistencyError):
        msm.permute_atoms(source, [2, 0, 1])
