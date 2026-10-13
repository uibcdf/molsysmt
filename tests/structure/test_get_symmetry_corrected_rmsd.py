"""Protect unaligned pose geometry, reusable mappings and bounded delivery."""

from copy import deepcopy

import numpy as np
import pytest
from rdkit import Chem
from rdkit.Chem import rdMolAlign

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


def system(smiles="c1ccccc1", n_structures=4):
    molsys = msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")
    count = molsys.topology.n_atoms
    phase = np.arange(count) * 2 * np.pi / count
    xyz = np.column_stack((np.cos(phase), np.sin(phase), np.zeros(count))) * 0.14
    structures = np.repeat(xyz[None], n_structures, axis=0)
    if n_structures > 1:
        structures[1] = xyz[np.roll(np.arange(count), -1)]
    if n_structures > 2:
        structures[2] += [0, 0, 0.2]
    molsys.structures.append(coordinates=msm.pyunitwizard.quantity(structures, "nm"))
    return molsys


def identity(count):
    return np.column_stack((np.arange(count), np.arange(count)))


def test_anchored_and_supplied_minima_are_not_the_unrestricted_minimum():
    molsys = system()
    options = dict(
        selection="all",
        structure_indices=[1, 2, 1],
        baseline_atom_correspondence=identity(6),
    )
    unconstrained = msm.structure.get_symmetry_corrected_rmsd(molsys, **options)
    anchored = msm.structure.get_symmetry_corrected_rmsd(
        molsys,
        fixed_atom_correspondence=[[0, 0], [1, 1]],
        **options,
    )
    supplied = msm.structure.get_symmetry_corrected_rmsd(
        molsys,
        candidate_atom_correspondences=identity(6)[::-1],
        **options,
    )
    assert unconstrained["search_scope"] == "all_chemical_correspondences"
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(unconstrained["rmsd"], to_unit="nm"),
        [0, 0.2, 0],
        atol=1e-14,
    )
    for result in (anchored, supplied):
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"),
            [0.14, 0.2, 0.14],
            atol=1e-14,
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"),
            msm.pyunitwizard.get_value(result["raw_rmsd"], to_unit="nm"),
            atol=1e-14,
        )
        assert result["correspondence_indices"].tolist() == [0, 0, 0]
    assert supplied["search_scope"] == "supplied_atom_correspondences"
    assert anchored["search_scope"] == "anchored_chemical_correspondences"


def test_multiple_proposed_maps_choose_the_analytic_pose_mapping():
    molsys = system()
    correct = np.column_stack((np.arange(6), np.roll(np.arange(6), -1)))
    result = msm.structure.get_symmetry_corrected_rmsd(
        molsys,
        selection="all",
        structure_indices=[1, 0],
        candidate_atom_correspondences=[correct, identity(6)],
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"), [0, 0], atol=1e-14
    )
    assert result["correspondence_indices"].tolist() == [1, 0]
    assert result["n_near_optimal_correspondences"].tolist() == [1, 1]


def test_valid_baseline_excluded_by_constraints_can_be_smaller_than_corrected():
    molsys = system()
    baseline = np.column_stack((np.arange(6), np.roll(np.arange(6), -1)))
    for constraints in (
        dict(fixed_atom_correspondence=[[0, 0], [1, 1]]),
        dict(candidate_atom_correspondences=identity(6)),
    ):
        result = msm.structure.get_symmetry_corrected_rmsd(
            molsys,
            selection="all",
            structure_indices=[1],
            baseline_atom_correspondence=baseline,
            **constraints,
        )
        assert msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm")[
            0
        ] == pytest.approx(0.14)
        assert msm.pyunitwizard.get_value(result["raw_rmsd"], to_unit="nm")[0] < 1e-14


def test_constrained_cache_reuses_search_and_rejects_mutated_constraints(monkeypatch):
    molsys = system()
    cached = msm.topology.get_atom_correspondences(
        molsys,
        candidate_atom_correspondences=identity(6),
        fixed_atom_correspondence=[[0, 0]],
    )
    monkeypatch.setattr(
        msm.topology,
        "get_atom_correspondences",
        lambda *a, **k: pytest.fail("enumeration repeated"),
    )
    observed = msm.structure.get_symmetry_corrected_rmsd(
        molsys, selection="all", correspondences=cached
    )
    assert observed["search_scope"] == "supplied_atom_correspondences"
    for name in ("fixed_atom_correspondence", "candidate_atom_correspondences"):
        altered = deepcopy(cached)
        altered[name].flat[-1] = 1
        with pytest.raises(ArgumentError):
            msm.structure.get_symmetry_corrected_rmsd(
                molsys, selection="all", correspondences=altered
            )
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys,
            selection="all",
            correspondences=cached,
            fixed_atom_correspondence=[[0, 0]],
        )
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys,
            selection="all",
            correspondences=cached,
            candidate_atom_correspondences=identity(6),
        )


def test_constrained_empty_structures_and_no_compatible_anchor():
    molsys = system("CCO")
    empty = msm.structure.get_symmetry_corrected_rmsd(
        molsys, structure_indices=[], fixed_atom_correspondence=[[0, 0]]
    )
    assert empty["rmsd"].shape == (0,) and empty["correspondence_indices"].shape == (0,)
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys, fixed_atom_correspondence=[[0, 2]]
        )


def test_prior_unconstrained_schema_one_cache_retains_unrestricted_meaning():
    from molsysmt.topology._atom_correspondences import correspondence_digest

    molsys = system()
    cached = msm.topology.get_atom_correspondences(molsys)
    for name in (
        "search_scope",
        "fixed_atom_correspondence",
        "candidate_atom_correspondences",
    ):
        del cached[name]
    cached["correspondence_digest"] = correspondence_digest(cached)
    result = msm.structure.get_symmetry_corrected_rmsd(
        molsys, selection="all", structure_indices=[1], correspondences=cached
    )
    assert result["search_scope"] == "all_chemical_correspondences"
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"), [0], atol=1e-14
    )


def test_proposed_geometry_matches_independent_rdkit_explicit_map():
    molsys = system()
    external = msm.convert(molsys, to_form="rdkit.Mol")
    proposed = np.column_stack((np.arange(6), np.arange(6)[::-1]))
    observed = msm.structure.get_symmetry_corrected_rmsd(
        molsys,
        selection="all",
        structure_indices=[1],
        candidate_atom_correspondences=proposed,
    )
    probe, reference = Chem.Mol(external), Chem.Mol(external)
    conformers = list(external.GetConformers())
    probe.RemoveAllConformers()
    reference.RemoveAllConformers()
    probe.AddConformer(Chem.Conformer(conformers[1]), assignId=True)
    reference.AddConformer(Chem.Conformer(conformers[0]), assignId=True)
    expected = (
        rdMolAlign.CalcRMS(
            probe,
            reference,
            prbId=0,
            refId=0,
            map=[proposed.tolist()],
            symmetrizeConjugatedTerminalGroups=False,
        )
        / 10
    )
    assert msm.pyunitwizard.get_value(observed["rmsd"], to_unit="nm")[
        0
    ] == pytest.approx(expected)


def test_constrained_h5msm_streaming_matches_eager_and_uses_active_units(tmp_path):
    molsys = system()
    path = str(tmp_path / "anchored.h5msm")
    msm.convert(molsys, to_form=path)
    options = dict(
        selection="all",
        structure_indices=[2, 1, 0, 1],
        fixed_atom_correspondence=[[0, 0]],
        candidate_atom_correspondences=identity(6),
    )
    eager = msm.structure.get_symmetry_corrected_rmsd(
        molsys, heavy_mode="off", **options
    )
    with msm.pyunitwizard.context(standard_units=["angstrom", "ps"]):
        streamed = msm.structure.get_symmetry_corrected_rmsd(
            path, heavy_mode="force", **options
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(streamed["rmsd"]),
            msm.pyunitwizard.get_value(eager["rmsd"], to_unit="nm") * 10,
            atol=1e-13,
        )
    assert streamed["execution"]["execution"] == "chunked"
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(streamed["rmsd"], to_unit="angstrom"),
        msm.pyunitwizard.get_value(eager["rmsd"], to_unit="nm") * 10,
        atol=1e-13,
    )
    np.testing.assert_array_equal(
        streamed["correspondences"]["atom_correspondences"],
        eager["correspondences"]["atom_correspondences"],
    )


def test_corrected_raw_rmsd_and_maps_preserve_nonconsecutive_repeated_structures():
    molsys = system()
    options = dict(
        selection="all",
        structure_indices=[2, 1, 0, 2],
        baseline_atom_correspondence=identity(6),
    )
    result = msm.structure.get_symmetry_corrected_rmsd(molsys, **options)
    puw = msm.pyunitwizard
    np.testing.assert_allclose(
        puw.get_value(result["rmsd"], to_unit="nm"), [0.2, 0, 0, 0.2], atol=1e-14
    )
    np.testing.assert_allclose(
        puw.get_value(result["raw_rmsd"], to_unit="nm"), [0.2, 0.14, 0, 0.2], atol=1e-14
    )
    assert result["structure_indices"].tolist() == [2, 1, 0, 2]
    maps = result["correspondences"]["atom_correspondences"]
    for structure, chosen in zip([2, 1, 0, 2], result["correspondence_indices"]):
        xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm")
        direct = np.sqrt(
            np.mean(
                np.sum(
                    (xyz[structure, maps[chosen, :, 0]] - xyz[0, maps[chosen, :, 1]])
                    ** 2,
                    axis=1,
                )
            )
        )
        assert direct == pytest.approx(
            puw.get_value(result["rmsd"], to_unit="nm")[
                list([2, 1, 0, 2]).index(structure)
            ]
        )
    assert result["alignment"] == result["periodic_imaging"] == "none"


def test_translation_and_rotation_of_asymmetric_ligand_are_not_removed():
    molsys = system("CCO", n_structures=1)
    moved = msm.copy(molsys)
    xyz = msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm")
    turned = xyz.copy()
    turned[:, :, :2] *= -1
    msm.set(moved, coordinates=msm.pyunitwizard.quantity(turned + [0, 0, 0.3], "nm"))
    result = msm.structure.get_symmetry_corrected_rmsd(
        moved, reference_molecular_system=molsys
    )
    expected = np.sqrt(np.mean(np.sum((turned[0] + [0, 0, 0.3] - xyz[0]) ** 2, axis=1)))
    assert msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm")[0] == pytest.approx(
        expected
    )
    assert expected > 0.3
    assert result["raw_rmsd"] is None


def test_benzamidinium_nitrogen_coordinate_swap_is_not_a_chemical_symmetry():
    molsys = system("NC(=[NH2+])c1ccccc1", n_structures=1)
    moved = msm.copy(molsys)
    xyz = msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm")
    permuted = xyz.copy()
    permuted[:, [0, 2]] = xyz[:, [2, 0]]
    msm.set(moved, coordinates=msm.pyunitwizard.quantity(permuted, "nm"))
    result = msm.structure.get_symmetry_corrected_rmsd(
        moved, reference_molecular_system=molsys
    )
    expected = np.sqrt(2 * np.sum((xyz[0, 0] - xyz[0, 2]) ** 2) / 9)
    assert expected > 0
    assert msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm")[0] == pytest.approx(
        expected
    )


def test_rdkit_structure_positions_do_not_use_conformer_ids():
    molsys = system()
    reference = msm.structure.get_symmetry_corrected_rmsd(
        molsys, structure_indices=[2, 0, 1]
    )
    external = msm.convert(molsys, to_form="rdkit.Mol")
    for index, conformer in enumerate(external.GetConformers()):
        conformer.SetId(100 + 10 * index)
    observed = msm.structure.get_symmetry_corrected_rmsd(
        external, structure_indices=[2, 0, 1]
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed["rmsd"], to_unit="nm"),
        msm.pyunitwizard.get_value(reference["rmsd"], to_unit="nm"),
        atol=1e-14,
    )
    assert observed["structure_indices"].tolist() == [2, 0, 1]


def test_reference_reordering_uses_paired_indices_without_selection_sorting():
    molsys = system("CCO", n_structures=1)
    rdkit = msm.convert(molsys, to_form="rdkit.Mol")
    reference = Chem.RenumberAtoms(rdkit, [2, 0, 1])
    result = msm.structure.get_symmetry_corrected_rmsd(
        molsys, reference_molecular_system=reference
    )
    assert msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm")[0] < 1e-14
    assert result["correspondences"]["atom_correspondences"].tolist() == [
        [[0, 1], [1, 2], [2, 0]]
    ]


def test_cached_maps_reuse_graph_search_and_reject_changed_chemistry(monkeypatch):
    molsys = system()
    cached = msm.topology.get_atom_correspondences(molsys)
    original = deepcopy(cached)
    monkeypatch.setattr(
        msm.topology,
        "get_atom_correspondences",
        lambda *a, **k: pytest.fail("graph search repeated"),
    )
    result = msm.structure.get_symmetry_corrected_rmsd(
        molsys, selection="all", correspondences=cached
    )
    assert result["rmsd"].shape == (4,)
    np.testing.assert_array_equal(
        cached["atom_correspondences"], original["atom_correspondences"]
    )
    molsys.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 1
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys, selection="all", correspondences=cached
        )


def test_modified_cache_and_wrong_baseline_are_refused():
    molsys = system()
    cached = msm.topology.get_atom_correspondences(molsys)
    cached["atom_correspondences"][0, 0, 1] = 1
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys, selection="all", correspondences=cached
        )
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(
            molsys, baseline_atom_correspondence=[[0, 1]]
        )


def test_units_follow_user_policy_and_coordinate_input_units():
    molsys = system()
    puw = msm.pyunitwizard
    msm.set(
        molsys,
        coordinates=puw.convert(molsys.structures.coordinates, to_unit="angstrom"),
    )
    with puw.context(standard_units=["angstrom", "ps"]):
        result = msm.structure.get_symmetry_corrected_rmsd(
            molsys, structure_indices=[2], tie_tolerance="0.01 angstrom"
        )
        assert puw.get_value(result["rmsd"])[0] == pytest.approx(2)
        assert puw.get_value(
            result["tie_tolerance"], to_unit="angstrom"
        ) == pytest.approx(0.01)


def test_eager_chunked_h5msm_parity_and_empty_structures(tmp_path, monkeypatch):
    molsys = system(n_structures=7)
    monkeypatch.setattr(msm.configure, "chunk_size", 2)
    source = tmp_path / "symmetry.h5msm"
    msm.convert(molsys, to_form="file:h5msm", output_filename=str(source))
    options = dict(
        structure_indices=[6, 1, 4, 0, 2], baseline_atom_correspondence=identity(6)
    )
    eager = msm.structure.get_symmetry_corrected_rmsd(
        molsys, heavy_mode="off", **options
    )
    for source_input in (molsys, str(source)):
        chunked = msm.structure.get_symmetry_corrected_rmsd(
            source_input, heavy_mode="force", **options
        )
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(eager["rmsd"]),
            msm.pyunitwizard.get_value(chunked["rmsd"]),
        )
        np.testing.assert_array_equal(
            eager["correspondence_indices"], chunked["correspondence_indices"]
        )
        assert chunked["execution"]["execution"] == "chunked"
        assert chunked["execution"]["n_blocks"] == 3
    empty = msm.structure.get_symmetry_corrected_rmsd(molsys, structure_indices=[])
    assert empty["rmsd"].shape == empty["correspondence_indices"].shape == (0,)
    assert empty["correspondence_indices"].dtype == np.int64


def test_rdkit_in_place_oracle_with_explicit_qualified_maps():
    molsys = system()
    result = msm.structure.get_symmetry_corrected_rmsd(molsys)
    rdkit = msm.convert(molsys, to_form="rdkit.Mol")
    maps = result["correspondences"]["atom_correspondences"].tolist()
    expected = []
    conformers = list(rdkit.GetConformers())
    for conformer in conformers:
        probe, reference = Chem.Mol(rdkit), Chem.Mol(rdkit)
        probe.RemoveAllConformers()
        reference.RemoveAllConformers()
        probe.AddConformer(Chem.Conformer(conformer), assignId=True)
        reference.AddConformer(Chem.Conformer(conformers[0]), assignId=True)
        expected.append(
            rdMolAlign.CalcRMS(
                probe, reference, map=maps, symmetrizeConjugatedTerminalGroups=False
            )
            / 10
        )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result["rmsd"], to_unit="nm"), expected, atol=1e-14
    )


def test_exact_ties_are_lexical_and_near_ties_do_not_replace_minimum():
    molsys = system(n_structures=1)
    msm.set(molsys, coordinates=msm.pyunitwizard.quantity(np.zeros((1, 6, 3)), "nm"))
    result = msm.structure.get_symmetry_corrected_rmsd(molsys)
    assert result["correspondence_indices"].tolist() == [0]
    assert result["n_near_optimal_correspondences"].tolist() == [12]


@pytest.mark.parametrize(
    "options",
    [
        {"structure_indices": [-1]},
        {"structure_indices": True},
        {"structure_indices": [True, 2]},
        {"structure_indices": "bad"},
        {"structure_indices": [1.5]},
        {"reference_structure_index": -1},
        {"reference_structure_index": True},
        {"tie_tolerance": "1 ps"},
        {"tie_tolerance": "-1 nm"},
    ],
)
def test_invalid_public_geometry_arguments_fail(options):
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(system(), **options)


def test_unknown_cached_rule_version_is_refused():
    molsys = system()
    cached = msm.topology.get_atom_correspondences(molsys)
    cached["rule_version"] = "declared_graph_isomorphism@999"
    with pytest.raises(ArgumentError):
        msm.structure.get_symmetry_corrected_rmsd(molsys, correspondences=cached)
