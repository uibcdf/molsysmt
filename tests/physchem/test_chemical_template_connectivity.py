"""Checking explicit graph completion without guessing polymer chemistry."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Topology

PROVENANCE = dict(
    identity="Explicit zwitterionic glycylglycine control",
    version="1",
    source_uri="analytical:glycylglycine",
    checksum="declared:analytical-glycylglycine-1",
    hydrogen_policy="stored_counts",
    terminal_states={"N": "ammonium", "C": "carboxylate"},
)


def peptide_template():
    """Declare C4H8N2O3, including a peptide bond and terminal charge choices."""
    topology = Topology(n_atoms=9, n_groups=2)
    topology.atoms["atom_type"] = ["N", "C", "C", "O", "N", "C", "C", "O", "O"]
    topology.atoms["atom_name"] = ["N", "CA", "C", "O", "N", "CA", "C", "O", "OXT"]
    topology.atoms["atom_id"] = [str(i + 1) for i in range(9)]
    topology.atoms["group_index"] = [0] * 4 + [1] * 5
    topology.groups["group_name"] = ["GLY", "GLY"]
    topology.groups["group_id"] = ["10", "11"]
    topology.groups["group_type"] = ["amino acid"] * 2
    topology.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 1, 2, 2, 4, 5, 6, 6],
            atom2_index=[1, 2, 3, 4, 5, 6, 7, 8],
            bond_type=["covalent"] * 8,
            bond_order=[1, 1, 2, 1, 1, 1, 2, 1],
            is_aromatic=[False] * 8,
            is_conjugated=[False, False, True, True, False, False, True, True],
            evidence=["user_defined"] * 8,
        )
    )
    state = topology._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    for field, values in {
        "formal_charge": [1, 0, 0, 0, 0, 0, 0, 0, -1],
        "is_aromatic": [False] * 9,
        "n_unpaired_electrons": [0] * 9,
        "n_implicit_hydrogens": [0] * 9,
        "n_explicit_hydrogens": [3, 2, 0, 0, 1, 2, 0, 0, 0],
        "allows_implicit_hydrogens": [False] * 9,
    }.items():
        state.set_atom_attribute(field, values)
    return topology


def peptide_source(*, missing=((2, 4),), frames=2):
    template = peptide_template()
    source = msm.convert(template, to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    pairs = list(zip(state.bonds["atom1_index"], state.bonds["atom2_index"]))
    state.bonds = state.bonds.loc[[pair not in missing for pair in pairs]].copy()
    state.bonds.reset_index(drop=True, inplace=True)
    state.atom_attributes = pd.DataFrame(index=range(9))
    state.connectivity_completeness = "partial"
    source.topology.rebuild_components(redefine_types=False, redefine_names=False)
    source.structures.append(
        # These values test preservation; they do not describe an optimized pose.
        coordinates=msm.pyunitwizard.quantity(
            np.arange(frames * 27).reshape(frames, 9, 3) / 10, "angstrom"
        ),
        box=msm.pyunitwizard.quantity(np.tile(np.eye(3) * 100, (frames, 1, 1)), "pm"),
        time=msm.pyunitwizard.quantity(np.arange(frames), "fs"),
    )
    return source, template


def options(template, **extra):
    return dict(
        template=template,
        atom_correspondence=np.column_stack((np.arange(9), np.arange(9))),
        template_provenance=PROVENANCE,
        **extra,
    )


def test_explicit_peptide_completion_preserves_pose_states_and_old_bond_identity(
    tmp_path,
):
    source, template = peptide_source()
    assert source.chemical_states._states[0].component_indices.nunique() == 2
    original = source.copy()
    source.chemical_states.append_state()
    other = source.chemical_states._states[1].copy()
    source.interactions = {
        "evaluated-empty": msm.Interactions.from_records(
            [],
            n_atoms=9,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    args = options(template, connectivity_policy="complete_from_template")
    default = msm.physchem.assess_chemical_template(source, **options(template))
    assert default["status"] == "conflict"
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        assessment = msm.physchem.assess_chemical_template(source, **args)
        assert assessment["status"] == "compatible"
        assert len(assessment["added_bonds"]) == 1
        proposed = assessment["added_bonds"][0]
        assert (proposed["atom1_index"], proposed["atom2_index"]) == (2, 4)
        assert proposed["bond_order"] == 1 and proposed["evidence"] == "user_defined"
        output = msm.physchem.apply_chemical_template(source, **args)
    result, report = output["molecular_system"], output["report"]
    state = result.chemical_states._states[0]
    assert report["coverage"]["graph"] == "completion_from_declared_template"
    assert state.connectivity_completeness == "complete"
    assert state.component_indices.tolist() == [0] * 9
    assert state.component_completeness == "complete"
    assert state.atom_attributes["formal_charge"].tolist() == [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        -1,
    ]
    assert state.atom_attributes["n_explicit_hydrogens"].sum() == 8
    assert report["invalidated_analysis_names"] == ["evaluated-empty"]
    assert result.interactions["evaluated-empty"].evaluated_structure_indices.size == 0
    assert source.interactions[
        "evaluated-empty"
    ].evaluated_structure_indices.tolist() == [0, 1]
    for field in ("atoms", "groups", "molecules", "chains", "entities"):
        pd.testing.assert_frame_equal(
            getattr(result.topology, field), getattr(source.topology, field)
        )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].bonds,
        original.chemical_states._states[0].bonds,
    )
    pd.testing.assert_frame_equal(result.chemical_states._states[1].bonds, other.bonds)
    for field in ("coordinates", "box", "time"):
        before = getattr(source.structures, field)
        after = getattr(result.structures, field)
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(after), msm.pyunitwizard.get_value(before)
        )
        assert msm.pyunitwizard.get_unit(after) == msm.pyunitwizard.get_unit(before)
    for old_index, new_index in report["source_bond_correspondence"]:
        old = original.chemical_states._states[0].bonds.iloc[old_index]
        new = state.bonds.iloc[new_index]
        assert (old["atom1_index"], old["atom2_index"]) == (
            new["atom1_index"],
            new["atom2_index"],
        )
    assert report["added_bonds"][0]["bond_index"] == 3
    path = tmp_path / "completed-peptide.h5msm"
    msm.convert(result, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert restored.chemical_states._states[0].bonds["bond_order"].tolist() == [
        1,
        1,
        2,
        1,
        1,
        1,
        2,
        1,
    ]
    assert restored.chemical_states._states[0].component_indices.tolist() == [0] * 9
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates),
        msm.pyunitwizard.get_value(source.structures.coordinates),
    )


@pytest.mark.parametrize(
    "defect",
    [
        "unexpected_edge",
        "complete_source",
        "partial_template",
        "disconnected_template",
        "formal_charge_conflict",
        "missing_atom",
    ],
)
def test_completion_does_not_override_conflicts_or_incomplete_templates(defect):
    source, template = peptide_source()
    state = source.chemical_states._states[0]
    if defect == "unexpected_edge":
        source.topology.add_bonds([[0, 8]])
    elif defect == "complete_source":
        state.connectivity_completeness = "complete"
    elif defect == "partial_template":
        template._chemical_states_domain._states[
            0
        ].connectivity_completeness = "partial"
    elif defect == "disconnected_template":
        template.remove_bonds([3])
        template._chemical_states_domain._states[
            0
        ].connectivity_completeness = "complete"
    elif defect == "formal_charge_conflict":
        state.set_atom_attribute("formal_charge", [0] * 9)
    elif defect == "missing_atom":
        source = msm.extract(source, selection=list(range(8)))
    before = source.copy()
    args = options(template, connectivity_policy="complete_from_template")
    with pytest.raises((StructuralInconsistencyError, ArgumentError)):
        msm.physchem.apply_chemical_template(source, **args)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].bonds, before.chemical_states._states[0].bonds
    )
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes,
        before.chemical_states._states[0].atom_attributes,
    )


def test_permuted_map_and_coordinate_free_native_forms(tmp_path):
    source, template = peptide_source()
    order = [8, 2, 6, 0, 7, 1, 5, 3, 4]
    # Reorder the fixture independently; a public selection may normalize its order.
    permuted = source.topology.copy()
    permuted.atoms = permuted.atoms.iloc[order].reset_index(drop=True)
    inverse = np.argsort(order)
    bonds = permuted.bonds.copy()
    for column in ("atom1_index", "atom2_index"):
        bonds[column] = inverse[bonds[column].to_numpy(dtype=np.int64)]
    permuted.bonds = Topology._coerce_bond_table(bonds)
    permuted.rebuild_components(redefine_types=False, redefine_names=False)
    mapping = np.column_stack((np.arange(9), inverse))
    kwargs = options(template, connectivity_policy="complete_from_template")
    kwargs["atom_correspondence"] = mapping
    result = msm.physchem.apply_chemical_template(permuted, **kwargs)
    prepared = result["molecular_system"]
    bond = result["report"]["added_bonds"][0]
    assert (bond["atom1_index"], bond["atom2_index"]) == tuple(
        sorted((int(np.argsort(order)[2]), int(np.argsort(order)[4])))
    )
    assert prepared.chemical_states._states[0].atom_attributes[
        "formal_charge"
    ].tolist() == [-1, 0, 0, 1, 0, 0, 0, 0, 0]
    path = tmp_path / "partial-peptide.h5msm"
    msm.convert(source, to_form=path)
    from_file = msm.physchem.apply_chemical_template(
        path, **options(template, connectivity_policy="complete_from_template")
    )
    assert len(from_file["molecular_system"].chemical_states._states[0].bonds) == 8


@pytest.mark.parametrize("policy", [None, True, "infer", 1, []])
def test_connectivity_policy_is_validated_at_public_boundary(policy):
    source, template = peptide_source()
    with pytest.raises(ArgumentError):
        msm.physchem.assess_chemical_template(
            source, **options(template, connectivity_policy=policy)
        )


def test_repeat_completion_does_not_add_edges_or_invalidate_again():
    source, template = peptide_source()
    kwargs = options(template, connectivity_policy="complete_from_template")
    first = msm.physchem.apply_chemical_template(source, **kwargs)["molecular_system"]
    first.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=9,
            n_structures=2,
            evaluated_structure_indices=[0, 1],
            method="control",
        )
    }
    result = msm.physchem.apply_chemical_template(first, **kwargs)
    assert result["report"]["added_bonds"] == []
    assert result["report"]["invalidated_analysis_names"] == []
    assert result["molecular_system"].interactions[
        "empty"
    ].evaluated_structure_indices.tolist() == [0, 1]


def test_completion_targets_nonreference_state_even_without_source_edges():
    source, template = peptide_source(
        missing=(
            (0, 1),
            (1, 2),
            (2, 3),
            (2, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (6, 8),
        )
    )
    state = source.chemical_states._states[0].copy()
    source.chemical_states.append_state()
    source.chemical_states._states[1] = state
    reference = deepcopy(source.chemical_states._states[0])
    result = msm.physchem.apply_chemical_template(
        source,
        **options(
            template, chemical_state=1, connectivity_policy="complete_from_template"
        ),
    )["molecular_system"]
    assert len(result.chemical_states._states[1].bonds) == 8
    assert result.chemical_states._states[1].component_indices.tolist() == [0] * 9
    pd.testing.assert_frame_equal(
        result.chemical_states._states[0].bonds, reference.bonds
    )
    pd.testing.assert_frame_equal(
        result.chemical_states._states[0].atom_attributes, reference.atom_attributes
    )


def test_added_double_bond_remaps_stereo_references_with_endpoint_orientation():
    # A declared trans-2-butene heavy graph; H counts do not create H coordinates.
    template = Topology(n_atoms=4)
    template.atoms["atom_type"] = ["C"] * 4
    template.bonds = pd.DataFrame(
        dict(
            atom1_index=[0, 1, 2],
            atom2_index=[1, 2, 3],
            bond_type=["covalent"] * 3,
            bond_order=[1, 2, 1],
            is_aromatic=[False] * 3,
            stereochemistry=[None, "E", None],
            stereo_atom1_index=[None, 0, None],
            stereo_atom2_index=[None, 3, None],
        )
    )
    state = template._chemical_states_domain._states[0]
    state.connectivity_completeness = "complete"
    for field, values in {
        "formal_charge": [0] * 4,
        "is_aromatic": [False] * 4,
        "n_unpaired_electrons": [0] * 4,
        "n_implicit_hydrogens": [0] * 4,
        "n_explicit_hydrogens": [3, 1, 1, 3],
        "allows_implicit_hydrogens": [False] * 4,
    }.items():
        state.set_atom_attribute(field, values)
    # Independently reverse the order: methyl, alkene carbon, alkene carbon, methyl.
    source = Topology(n_atoms=4)
    source.atoms["atom_type"] = ["C"] * 4
    source.bonds = pd.DataFrame(dict(atom1_index=[0, 2], atom2_index=[1, 3]))
    result = msm.physchem.apply_chemical_template(
        source,
        template=template,
        atom_correspondence=np.array([[0, 3], [1, 2], [2, 1], [3, 0]]),
        template_provenance=dict(
            PROVENANCE,
            identity="trans-2-butene control",
            source_uri="analytical:trans-2-butene",
        ),
        connectivity_policy="complete_from_template",
    )
    bond = result["report"]["added_bonds"][0]
    assert (bond["atom1_index"], bond["atom2_index"]) == (1, 2)
    assert bond["stereochemistry"] == "E"
    assert (bond["stereo_atom1_index"], bond["stereo_atom2_index"]) == (0, 3)
    stored = result["molecular_system"].chemical_states._states[0].bonds.iloc[1]
    assert stored["bond_order"] == 2 and stored["stereochemistry"] == "E"
    assert (stored["stereo_atom1_index"], stored["stereo_atom2_index"]) == (0, 3)
