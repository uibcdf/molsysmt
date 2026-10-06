"""Checking explicit aromatic ring geometry, coverage and persistence contracts."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import MolSys, Topology


def _hexagon():
    angles = np.arange(6) * np.pi / 3
    return np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6)))


def _system(coordinates, *, box=None, groups=None, extra_bonds=()):
    xyz = np.asarray(coordinates, dtype=float)
    n_atoms = xyz.shape[1]
    groups = (
        groups
        if groups is not None
        else [list(range(i, i + 6)) for i in range(0, n_atoms, 6)]
    )
    aromatic = {
        tuple(sorted((a, b)))
        for group in groups
        for a, b in zip(group, group[1:] + group[:1])
    }
    edges = sorted(aromatic | {tuple(sorted(pair)) for pair in extra_bonds})
    topology = Topology(n_atoms=n_atoms)
    topology.atoms["atom_type"] = "C"
    topology.atoms["atom_id"] = [str(1000 + i) for i in range(n_atoms)]
    topology.bonds = pd.DataFrame(
        {
            "atom1_index": [a for a, _ in edges],
            "atom2_index": [b for _, b in edges],
            "bond_type": "covalent",
            "is_aromatic": [pair in aromatic for pair in edges],
        }
    )
    topology._set_chemical_state_atom_attribute("is_aromatic", [True] * n_atoms)
    topology._reference_chemical_state.connectivity_completeness = "complete"
    molsys = MolSys()
    molsys.topology = topology
    molsys.structures.append(
        coordinates=puw.quantity(xyz, "nm"),
        box=None if box is None else puw.quantity(np.asarray(box), "nm"),
    )
    molsys.structures.structure_id = np.array(
        [f"frame-{90 - i}" for i in range(len(xyz))]
    )
    return molsys


def _ensemble():
    ring = _hexagon()
    edge = ring[:, [2, 1, 0]]
    return _system(
        [
            np.concatenate((ring, ring + [0, 0, 0.35])),
            np.concatenate((ring, ring + [0, 0, 2.0])),
            np.concatenate((ring, edge + [0, 0, 0.4])),
        ]
    )


def _calculate(source, **kwargs):
    options = dict(
        distance_threshold=".6 nm",
        angle_threshold="30 degrees",
        offset_threshold=".2 nm",
        planarity_threshold=".02 nm",
        pbc=False,
    )
    options.update(kwargs)
    return msm.interactions.pi_pi.get_pi_pi_interactions(source, **options)


def _assert_same(actual, expected):
    for name in (
        "participant_atoms",
        "participant_atom_offsets",
        "occurrence_structures",
        "occurrence_relations",
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
    ):
        np.testing.assert_array_equal(getattr(actual, name), getattr(expected, name))
    assert actual.relation_types == expected.relation_types
    assert actual.participant_roles == expected.participant_roles
    # Evidence codes are local categorical encodings; compare the preserved labels.
    np.testing.assert_array_equal(
        np.asarray(actual.evidence_labels)[actual.occurrence_evidence],
        np.asarray(expected.evidence_labels)[expected.occurrence_evidence],
    )
    assert (
        actual.measure_units == expected.measure_units
        and actual.software == expected.software
    )
    for name in expected.measurements:
        np.testing.assert_allclose(
            actual.measurements[name], expected.measurements[name], atol=1e-12, rtol=0
        )
    np.testing.assert_array_equal(actual.image_vectors, expected.image_vectors)


def test_parallel_edge_and_evaluated_empty_frames_reuse_one_relation():
    molsys = _ensemble()
    result = _calculate(molsys, structure_indices=[2, 0, 2, 1])
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.n_interactions == 2 and len(result.relation_types) == 1
    assert result.occurrence_structures.tolist() == [0, 2]
    assert result.occurrence_evidence.tolist() == [0, 1]
    assert result.relation_types == ("pi_pi",) and result.participant_roles == (
        "ring_a",
        "ring_b",
    )
    np.testing.assert_allclose(result.measurements["distance"], [0.35, 0.4], atol=1e-12)
    np.testing.assert_allclose(
        result.measurements["plane_angle"], [0, np.pi / 2], atol=1e-12
    )
    np.testing.assert_allclose(result.measurements["offset_a"], [0, 0], atol=1e-12)
    np.testing.assert_allclose(result.measurements["offset_b"], [0, 0.4], atol=1e-12)
    empty = result.query(structure_indices=1)
    assert empty.n_interactions == 0 and empty.to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert result.atom_source_indices.tolist() == list(range(12))
    assert result.software["molsysmt"] == msm.__version__
    assert result.parameters["chemical_state_index"] == 0
    assert not molsys.interactions


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_composite_chemical_and_structural_domains_share_public_conversion(
    dictionary, reverse
):
    molsys = _ensemble()
    chemistry = (
        msm.convert(molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else molsys.chemical_states
    )
    source = (
        [molsys.structures, chemistry] if reverse else [chemistry, molsys.structures]
    )
    expected = _calculate(molsys, structure_indices=[2, 0], chemical_state="structure")
    result = _calculate(source, structure_indices=[2, 0], chemical_state="structure")
    _assert_same(result, expected)
    rings = msm.physchem.get_aromatic_rings(source)
    assert rings["atom_offsets"].tolist() == [0, 6, 12]
    assert rings["atom_indices"].tolist() == list(range(12))
    covalent_rings = msm.topology.get_rings(source)
    np.testing.assert_array_equal(covalent_rings["atom_indices"], rings["atom_indices"])
    assert molsys.chemical_states.reference_chemical_state_index == 0
    assert not molsys.interactions


@pytest.mark.parametrize(
    ("geometry", "frames"), [("parallel", [0]), ("edge_to_face", [2]), ("both", [0, 2])]
)
def test_geometric_class_selection(geometry, frames):
    assert (
        _calculate(_ensemble(), geometry=geometry).occurrence_structures.tolist()
        == frames
    )


@pytest.mark.parametrize(
    ("angle", "x", "z", "accepted"),
    [
        (0, 0.199, 0.35, True),
        (0, 0.201, 0.35, False),
        (0, 0, 0.6, True),
        (0, 0, 0.600001, False),
        (29, 0, 0.3, True),
        (31, 0, 0.3, False),
        (59, 0, 0.3, False),
        (61, 0, 0.3, True),
        (90, 0.21, 0.3, False),
    ],
)
def test_distance_angle_and_both_or_one_offset_near_misses(angle, x, z, accepted):
    theta = np.deg2rad(angle)
    rotation = np.array(
        [
            [np.cos(theta), 0, -np.sin(theta)],
            [0, 1, 0],
            [np.sin(theta), 0, np.cos(theta)],
        ]
    )
    ring = _hexagon()
    result = _calculate(_system([np.concatenate((ring, ring @ rotation + [x, 0, z]))]))
    assert bool(result.n_interactions) == accepted


def test_warped_ring_rejection_is_distinct_from_degenerate_plane_failure():
    ring = _hexagon()
    warped = ring.copy()
    warped[:, 2] = np.array([1, -1, 1, -1, 1, -1]) * 0.03
    molsys = _system([np.concatenate((ring, warped + [0, 0, 0.35]))])
    assert _calculate(molsys).n_interactions == 0
    result = _calculate(molsys, planarity_threshold=".04 nm")
    assert result.n_interactions == 1
    np.testing.assert_allclose(
        result.measurements["max_deviation_b"], [0.03], atol=1e-12
    )
    np.testing.assert_allclose(
        result.measurements["rms_deviation_b"], [0.03], atol=1e-12
    )
    coordinates = np.concatenate(
        (ring, np.column_stack((np.arange(6), np.zeros((6, 2)))))
    )
    with pytest.raises(StructuralInconsistencyError):
        _calculate(_system([coordinates]))


@pytest.mark.parametrize(
    ("mode", "first", "second", "count"),
    [
        ("internal", list(range(6)), None, 0),
        ("internal", list(range(12)), None, 1),
        ("incident", list(range(6, 12)), None, 2),
        ("between", list(range(12, 18)), list(range(6)), 0),
        ("between", list(range(12, 18)), list(range(6, 12)), 1),
    ],
)
def test_whole_ring_calculation_scopes_and_queries(mode, first, second, count):
    ring = _hexagon()
    molsys = _system([np.concatenate([ring + [0, 0, z] for z in (0, 0.35, 0.7)])])
    result = _calculate(
        molsys, selection=first, selection_2=second, selection_mode=mode
    )
    assert result.n_interactions == count
    assert result.evaluation_mode == mode
    if count:
        assert (
            result.query(atom_indices=[6], mode="involving_selection").n_interactions
            == count
        )
        assert (
            result.query(
                atom_indices=list(range(6, 12)), mode="within_selection"
            ).n_interactions
            == 0
        )
        assert (
            result.query(
                atom_indices=[6], mode="across_selection_boundary"
            ).n_interactions
            == count
        )
        if mode == "between":
            assert result.relation(0)["participants"][0][
                "atom_indices"
            ].tolist() == list(range(6, 12))


def test_partial_ring_and_invalid_between_scopes_fail():
    for kwargs in (
        {"selection": [0]},
        {"selection": list(range(6)), "selection_mode": "between"},
        {"selection_2": list(range(6))},
        {"selection_mode": "between", "selection_2": [6]},
        {"selection_mode": "between", "selection_2": list(range(6))},
    ):
        with pytest.raises(ArgumentError):
            _calculate(_ensemble(), **kwargs)


def test_fused_and_directly_bonded_rings_are_excluded_without_residue_inference():
    ring = _hexagon()
    linked = _system(
        [np.concatenate((ring, ring + [0, 0, 0.35]))], extra_bonds=[(0, 6)]
    )
    assert _calculate(linked).n_interactions == 0
    linked.chemical_states._states[0].bonds.loc[
        (linked.topology.bonds.atom1_index == 0)
        & (linked.topology.bonds.atom2_index == 6),
        "bond_type",
    ] = "dative"
    assert _calculate(linked).n_interactions == 1
    groups = [list(range(6)), [4, 5, 6, 7, 8, 9]]
    angles = np.arange(10) * 2 * np.pi / 10
    xyz = np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(10)))
    fused = _system([xyz], groups=groups)
    assert _calculate(fused).n_interactions == 0
    with pytest.raises(ArgumentError):
        _calculate(fused, selection=list(range(6)))


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3) * 2,
        np.array([[0, 2.0, 0], [-2.0, 0, 0], [0, 0, 2.0]]),
        np.array([[2.0, 0, 0], [0.3, 2.0, 0], [0.1, 0.2, 2.0]]),
    ],
)
@pytest.mark.parametrize("reverse", [False, True])
def test_observed_periodic_images_and_canonical_ring_order(box, reverse):
    ring = _hexagon()
    xyz = np.concatenate((ring, ring + [0, 0, 0.35] + box[0]))
    molsys = _system([xyz], box=[box])
    kwargs = (
        {}
        if not reverse
        else dict(
            selection=list(range(6, 12)),
            selection_2=list(range(6)),
            selection_mode="between",
        )
    )
    result = _calculate(molsys, pbc=True, **kwargs)
    assert result.n_interactions == 1
    assert result.image_vectors.tolist() == [[0, 0, 0], [-1, 0, 0]]
    observed = [
        xyz[part["atom_indices"]] + shift @ box
        for part, shift in zip(result.relation(0)["participants"], result.image_vectors)
    ]
    np.testing.assert_allclose(
        np.linalg.norm(observed[1].mean(axis=0) - observed[0].mean(axis=0)),
        result.measurements["distance"][0],
        atol=1e-12,
    )
    assert _calculate(molsys, **kwargs).n_interactions == 0
    xyz[1] += box[0]
    msm.set(molsys, coordinates=puw.quantity([xyz], "nm"))
    with pytest.raises(NotImplementedMethodError):
        _calculate(molsys, pbc=True, **kwargs)


def test_named_h5msm_dictionary_and_remapped_round_trip(tmp_path):
    molsys = _ensemble()
    result = _calculate(molsys)
    dictionary = _calculate(molsys, output_type="molsysmt.InteractionsDict")
    _assert_same(msm.convert(dictionary, to_form="molsysmt.Interactions"), result)
    molsys.interactions = {"pi": result}
    path = str(tmp_path / "pi.h5msm")
    msm.convert(molsys, to_form=path)
    saved = msm.convert(path, to_form="molsysmt.MolSys").interactions["pi"]
    _assert_same(saved, result)
    assert saved.parameters == result.parameters
    np.testing.assert_array_equal(
        saved.query().to_dict()["occurrence_indices"],
        result.query().to_dict()["occurrence_indices"],
    )
    with msm.configure.context(chunk_size=1):
        _assert_same(_calculate(path, heavy_mode="force"), result)
    extracted = msm.extract(
        molsys, selection=list(range(6, 12)) + list(range(6)), structure_indices=[2, 0]
    )
    remapped = extracted.interactions["pi"]
    assert remapped.n_interactions == 2
    # Public atom selections are normalized; explicit analysis reordering uses remap.
    assert remapped.atom_source_indices.tolist() == list(range(12))
    assert remapped.structure_source_indices.tolist() == [2, 0]
    assert remapped.query(atom_indices=[0]).n_interactions == 2
    reordered = result.remap(
        atom_indices=list(range(6, 12)) + list(range(6)), structure_indices=[2, 0]
    )
    assert reordered.atom_source_indices.tolist() == list(range(6, 12)) + list(range(6))
    assert reordered.structure_source_indices.tolist() == [2, 0]
    assert reordered.query(atom_indices=[0]).n_interactions == 2


@pytest.mark.parametrize("topology", [True, False])
@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_projected_file_and_native_parity_without_saved_analysis_loading(
    tmp_path, monkeypatch, topology, heavy_mode
):
    from molsysmt.form import _h5msm05_modular

    molsys = _ensemble()
    expected = _calculate(molsys, structure_indices=[2, 1, 2, 0])
    molsys.interactions = {"saved": expected}
    if not topology:
        molsys = MolSys._from_partial_domains(
            chemical_states=molsys.chemical_states,
            structures=molsys.structures,
            interactions=molsys.interactions,
        )
    path = str(tmp_path / "projected.h5msm")
    msm.convert(molsys, to_form=path)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Pi-pi detection must not materialize saved structural series or analyses."
        )

    original = _h5msm05_modular._read_calculation_chemistry
    calls = []

    def counted(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_named_analyses", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "_read_calculation_chemistry", counted)
    with msm.configure.context(chunk_size=1):
        _assert_same(
            _calculate(path, heavy_mode=heavy_mode, structure_indices=[2, 0, 2, 1]),
            expected,
        )
        _assert_same(_calculate(molsys, heavy_mode=heavy_mode), expected)
    assert len(calls) == 1


def test_nondefault_length_angle_policy_and_mixed_source_units():
    molsys = _ensemble()
    expected = _calculate(molsys)
    with puw.context(
        standard_units=[
            "angstrom",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
            "degrees",
        ]
    ):
        molsys.structures.coordinates = puw.quantity(
            puw.get_value(molsys.structures.coordinates, to_unit="angstrom"), "angstrom"
        )
        actual = _calculate(
            molsys,
            distance_threshold="6 angstrom",
            offset_threshold="2 angstrom",
            planarity_threshold="20 pm",
            angle_threshold=puw.quantity(np.pi / 6, "radians"),
        )
    _assert_same(actual, expected)
    assert actual.parameters["angle_threshold"]["unit"] == "radians"
    assert actual.measure_units["distance"] == "nm"


@pytest.mark.parametrize(
    "options",
    [
        {"distance_threshold": 0.6},
        {"distance_threshold": "0 nm"},
        {"angle_threshold": "45 degrees"},
        {"angle_threshold": "-1 degrees"},
        {"angle_threshold": "1 nm"},
        {"offset_threshold": "-1 nm"},
        {"offset_threshold": "1 ps"},
        {"planarity_threshold": "nan nm"},
        {"planarity_threshold": puw.quantity([0.02, 0.03], "nm")},
        {"geometry": "energy"},
        {"method": "energy"},
        {"output_type": "tuple"},
        {"structure_indices": [4]},
        {"structure_indices": [-1]},
    ],
)
def test_invalid_parameters_fail_without_plausible_empty_results(options):
    with pytest.raises((ArgumentError, ValueError)):
        _calculate(_ensemble(), **options)


def test_missing_chemistry_and_nonfinite_geometry_fail():
    molsys = _ensemble()
    msm.set(molsys, element="atom", atom_is_aromatic=[None] + [True] * 11)
    with pytest.raises(StructuralInconsistencyError):
        _calculate(molsys)
    molsys = _ensemble()
    coords = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    coords[2, 0, 0] = np.nan
    molsys.structures.coordinates = puw.quantity(coords, "nm")
    with pytest.raises(StructuralInconsistencyError):
        _calculate(molsys, heavy_mode="force")


def test_typed_empty_selections_and_preflight_budget():
    for options in ({"structure_indices": []}, {"selection": []}):
        result = _calculate(_ensemble(), **options)
        assert result.n_interactions == 0
        assert all(
            column.shape == (0,) and column.dtype == np.float64
            for column in result.measurements.values()
        )
    with msm.configure.context(max_ram_usage=1):
        with pytest.raises(MemoryBudgetExceededError):
            _calculate(_ensemble())
    with msm.configure.context(max_ram_usage=4096):
        with pytest.raises(UnsupportedHeavyOperationError):
            _calculate(_ensemble())


def test_selected_structure_states_must_resolve_to_one_state():
    molsys = _ensemble()
    state = molsys.chemical_states.append_state()
    record = molsys.chemical_states._states[state]
    record.bonds = molsys.chemical_states._states[0].bonds.copy()
    record.atom_attributes = molsys.chemical_states._states[0].atom_attributes.copy()
    record.connectivity_completeness = "complete"
    molsys._set_structure_chemical_state_indices([0, state, 0])
    assert (
        _calculate(
            molsys, chemical_state="structure", structure_indices=[0, 2]
        ).n_interactions
        == 2
    )
    with pytest.raises(StructuralInconsistencyError):
        _calculate(molsys, chemical_state="structure")


def test_rdkit_form_uses_its_coordinate_getter_and_declared_chemistry():
    Chem = pytest.importorskip("rdkit.Chem")

    molecule = Chem.MolFromSmiles("c1ccccc1.c1ccccc1")
    xyz = np.concatenate((_hexagon(), _hexagon() + [0, 0, 0.35]))
    conformer = Chem.Conformer(12)
    for atom, position in enumerate(xyz * 10):
        conformer.SetAtomPosition(atom, position)
    molecule.AddConformer(conformer)
    result = _calculate(molecule)
    assert result.n_interactions == 1
    np.testing.assert_allclose(result.measurements["distance"], [0.35], atol=1e-12)
    with pytest.raises(UnsupportedHeavyOperationError):
        _calculate(molecule, heavy_mode="force")


def test_periodic_named_analysis_retains_images_and_query_occurrence_indices(tmp_path):
    ring = _hexagon()
    box = np.array([[2.0, 0, 0], [0.3, 2.0, 0], [0.1, 0.2, 2.0]])
    molsys = _system([np.concatenate((ring, ring + [0, 0, 0.35] + box[0]))], box=[box])
    result = _calculate(molsys, pbc=True)
    molsys.interactions = {"pi": result}
    filename = str(tmp_path / "periodic.h5msm")
    msm.convert(molsys, to_form=filename)
    saved = msm.convert(filename, to_form="molsysmt.MolSys").interactions["pi"]
    _assert_same(saved, result)
    np.testing.assert_array_equal(
        saved.query().to_dict()["occurrence_indices"],
        result.query().to_dict()["occurrence_indices"],
    )


def test_dense_accepted_result_budget_fails_before_finalization(monkeypatch):
    from molsysmt.interactions.pi_pi._reducer import _PiPiReducer

    ring = _hexagon()
    xyz = np.concatenate([ring + [0, 0, i * 0.01] for i in range(20)])
    molsys = _system(np.repeat(xyz[None], 10, axis=0))

    def forbidden(self):
        raise AssertionError(
            "An over-budget sparse accumulation must not finalize a partial analysis."
        )

    monkeypatch.setattr(_PiPiReducer, "finalize", forbidden)
    with msm.configure.context(
        max_ram_usage=1024**2, chunk_size=2, emit_heavy_telemetry=False
    ):
        with pytest.raises(MemoryBudgetExceededError, match="resident sparse-result"):
            _calculate(molsys, heavy_mode="force")


def test_late_invalid_coordinate_block_never_finalizes_partial_observations(
    monkeypatch,
):
    from molsysmt.interactions.pi_pi._reducer import _PiPiReducer

    molsys = _ensemble()
    xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    xyz[2, 0, 0] = np.nan
    molsys.structures.coordinates = puw.quantity(xyz, "nm")

    def forbidden(self):
        raise AssertionError(
            "Invalid later blocks must not finalize earlier observations."
        )

    monkeypatch.setattr(_PiPiReducer, "finalize", forbidden)
    with msm.configure.context(chunk_size=1):
        with pytest.raises(StructuralInconsistencyError):
            _calculate(molsys, heavy_mode="force")


def test_rich_h5msm_selections_do_not_materialize_a_source_for_forced_streaming(
    tmp_path, monkeypatch
):
    from molsysmt.form import _h5msm05_modular

    filename = str(tmp_path / "rich.h5msm")
    msm.convert(_ensemble(), to_form=filename)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "A rejected file route must fail before source materialization."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    with pytest.raises(UnsupportedHeavyOperationError, match="atom-index selections"):
        _calculate(filename, selection="atom_type=='C'", heavy_mode="force")


def test_chemistry_only_source_without_a_structure_axis_fails_clearly():
    with pytest.raises(StructuralInconsistencyError, match="structure axes"):
        _calculate(_ensemble().topology)


def test_roundoff_cannot_make_parallel_and_edge_classes_overlap(monkeypatch):
    from molsysmt.interactions.pi_pi import _reducer

    ring = _hexagon()
    half = np.sqrt(0.5)
    rotation = np.array([[half, 0, -half], [0, 1, 0], [half, 0, half]])
    molsys = _system([np.concatenate((ring, ring @ rotation + [0, 0, 0.35]))])

    def ideal_planes(coordinates, offsets, positions, *, caller):
        # Independent exact 45-degree geometry isolates the acceptance boundary
        # from an arbitrary last-bit perturbation in the plane solver.
        centers = np.array([[[0.0, 0, 0], [0.0, 0, 0.35]]])
        normals = np.array([[[0.0, 0, 1], [half, 0, half]]])
        return centers, normals, np.zeros((1, 2)), np.zeros((1, 2))

    monkeypatch.setattr(_reducer, "fit_planes", ideal_planes)
    threshold = puw.quantity(np.nextafter(np.pi / 4, -np.inf), "radians")
    result = _calculate(molsys, angle_threshold=threshold, offset_threshold="1 nm")
    assert result.n_interactions == 0
