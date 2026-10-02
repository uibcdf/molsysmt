"""Protect exact two-water paths, their nine roles and observed images."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MemoryBudgetExceededError


def _chain(left_donates=True, right_donates=True, middle_forward=True, n_frames=3):
    molecule = Chem.AddHs(Chem.MolFromSmiles("O.O.N.N"))
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    xyz = np.zeros((molecule.GetNumAtoms(), 3))
    xyz[:, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
    xyz[:4] = [[0, 0, 0], [0.3, 0, 0], [-0.3, 0, 0], [0.6, 0, 0]]
    hs = [
        sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(i).GetNeighbors())
        for i in range(4)
    ]
    xyz[hs[0]] = [[0, 0.1, 0], [0, -0.1, 0]]
    xyz[hs[1]] = [[0.3, 0.1, 0], [0.3, -0.1, 0]]
    if left_donates:
        xyz[hs[2][0]] = [-0.2, 0, 0]
        left = [2, hs[2][0], 0]
    else:
        xyz[hs[0][0]] = [-0.1, 0, 0]
        left = [0, hs[0][0], 2]
    if right_donates:
        xyz[hs[3][0]] = [0.5, 0, 0]
        right = [3, hs[3][0], 1]
    else:
        xyz[hs[1][0]] = [0.4, 0, 0]
        right = [1, hs[1][0], 3]
    if middle_forward:
        xyz[hs[0][1]] = [0.1, 0, 0]
        middle = [0, hs[0][1], 1]
    else:
        xyz[hs[1][1]] = [0.2, 0, 0]
        middle = [1, hs[1][1], 0]
    frames = np.repeat(xyz[None], n_frames, axis=0)
    if n_frames == 3:
        frames[1, [3, *hs[3]]] += [2, 2, 2]
    source.structures.append(coordinates=puw.quantity(frames, "nm"))
    return source, np.array([*left, *middle, *right], dtype=np.int64)


@pytest.mark.parametrize("left", [False, True])
@pytest.mark.parametrize("right", [False, True])
@pytest.mark.parametrize("forward", [False, True])
@pytest.mark.parametrize(
    "method,profile",
    [
        ("baker_hubbard", None),
        ("wernet_nilsson", None),
        ("donor_acceptor_distance_angle", "smarts_donor_acceptor"),
    ],
)
def test_exact_three_leg_analytic_truth(left, right, forward, method, profile):
    source, atoms = _chain(left, right, forward)
    result = msm.interactions.water_bridges.get_water_bridges(
        source, order=2, pbc=False, hbond_method=method, hbond_profile=profile
    )
    assert len(result.relation_types) == 1 and result.n_interactions == 2
    np.testing.assert_array_equal(result.participant_atoms, atoms)
    assert result.occurrence_structures.tolist() == [0, 2]
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert len(result.participant_roles) == 9
    assert result.parameters["method"] == "hbond_water_path"
    assert result.parameters["mediator_order"] == 2 and not source.interactions
    for branch in range(1, 4):
        np.testing.assert_allclose(
            result.measurements[f"leg_{branch}_donor_acceptor_distance"], 0.3
        )
        np.testing.assert_allclose(
            result.measurements[f"leg_{branch}_hydrogen_acceptor_distance"], 0.2
        )
        np.testing.assert_allclose(
            result.measurements[f"leg_{branch}_dha_angle"], np.pi
        )
    assert (
        msm.interactions.water_bridges.get_water_bridges(
            source, pbc=False
        ).n_interactions
        == 0
    )


@pytest.mark.parametrize(
    "box", [np.eye(3), np.array([[1, 0.1, 0], [0, 1, 0.1], [0, 0, 1.0]])]
)
@pytest.mark.parametrize("forward", [False, True])
def test_three_observed_geometries_nondefault_units_and_periodic_images(
    box, forward, tmp_path
):
    source, atoms = _chain(False, False, forward, n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    shifts = np.zeros((msm.get(source, n_atoms=True), 3), dtype=int)
    actual = np.unique(atoms)
    shifts[actual] = [[i % 3 - 1, i % 2, -i % 2] for i in range(len(actual))]
    xyz[0] += shifts @ box
    source.structures.coordinates = puw.quantity(xyz * 10, "angstrom")
    source.structures.box = puw.quantity(box[None] * 10, "angstrom")
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = msm.interactions.water_bridges.get_water_bridges(
            source,
            order=2,
            distance_threshold="2.5 angstrom",
            angle_threshold="120 degrees",
        )
    assert result.n_interactions == 1 and result.image_vectors.shape == (9, 3)
    observed = xyz[0, result.participant_atoms] + result.image_vectors @ box
    for branch in range(1, 4):
        d, h, a = observed[(branch - 1) * 3 : branch * 3]
        np.testing.assert_allclose(np.linalg.norm(d - a), 0.3)
        np.testing.assert_allclose(np.linalg.norm(h - a), 0.2)
    for atom in actual:
        images = result.image_vectors[result.participant_atoms == atom]
        assert np.all(images == images[0])
    assert not np.any(result.image_vectors[0])
    source.interactions = {"periodic-two-waters": result}
    path = str(tmp_path / "periodic.h5msm")
    msm.convert(source, to_form=path)
    saved = msm.convert(path, to_form="molsysmt.MolSys").interactions[
        "periodic-two-waters"
    ]
    np.testing.assert_array_equal(saved.image_vectors, result.image_vectors)
    np.testing.assert_array_equal(saved.occurrence_image_offsets, [0, 9])
    assert saved.parameters == result.parameters


def test_actual_atom_scopes_queries_reversal_and_alternative_hydrogens():
    source, atoms = _chain()
    actual = np.unique(atoms)
    for kwargs in [
        dict(selection=actual),
        dict(selection=[2], selection_mode="incident"),
        dict(
            selection=[2],
            selection_2=np.setdiff1d(actual, [2]),
            selection_mode="between",
        ),
    ]:
        result = msm.interactions.water_bridges.get_water_bridges(
            source, order=2, structure_indices=[2, 0, 2], pbc=False, **kwargs
        )
        assert result.n_interactions == 2
        assert result.query(atom_indices=[1], mode="incident").n_interactions == 2
        assert result.query(atom_indices=[1], mode="cross").n_interactions == 2
        assert result.query(atom_indices=[1], mode="internal").n_interactions == 0
        assert result.query(atom_indices=actual, mode="internal").n_interactions == 2
    assert (
        msm.interactions.water_bridges.get_water_bridges(
            source, order=2, selection=[2, 3], pbc=False
        ).n_interactions
        == 0
    )
    # Reverse the two external source indices: traversal reverses, directed DHA does not.
    perm = np.arange(msm.get(source, n_atoms=True))
    perm[2:4] = [3, 2]
    reversed_source = Chem.RenumberAtoms(
        msm.convert(source, to_form="rdkit.Mol"), perm.tolist()
    )
    reversed_result = msm.interactions.water_bridges.get_water_bridges(
        reversed_source, order=2, pbc=False
    )
    old_to_new = np.argsort(perm)
    np.testing.assert_array_equal(
        reversed_result.participant_atoms, old_to_new[atoms.reshape(3, 3)[::-1].ravel()]
    )
    # A second indexed donor H produces a second distinguishable middle-leg path.
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    molecule = msm.convert(source, to_form="rdkit.Mol")
    other_h = next(
        a.GetIdx()
        for a in molecule.GetAtomWithIdx(0).GetNeighbors()
        if a.GetIdx() != atoms[4]
    )
    xyz[:, other_h] = [0.1, 0.01, 0]
    source.structures.coordinates = puw.quantity(xyz, "nm")
    alternatives = msm.interactions.water_bridges.get_water_bridges(
        source, order=2, pbc=False
    )
    assert len(alternatives.relation_types) == 2 and alternatives.n_interactions == 4


@pytest.mark.parametrize("form", ["native", "rdkit", "composite", "h5msm"])
def test_two_water_form_parity_named_persistence_extraction_and_removal(form, tmp_path):
    source, atoms = _chain()
    result = msm.interactions.water_bridges.get_water_bridges(
        source, order=2, pbc=False
    )
    source.interactions = {"two-waters": result}
    path = str(tmp_path / "two-waters.h5msm")
    msm.convert(source, to_form=path)
    inputs = {
        "native": source,
        "rdkit": msm.convert(source, to_form="rdkit.Mol"),
        "composite": [source.topology, source.structures],
        "h5msm": path,
    }
    typed = msm.interactions.water_bridges.get_water_bridges(
        inputs[form], order=2, pbc=False, output_type="molsysmt.InteractionsDict"
    )
    restored = msm.convert(typed, to_form="molsysmt.Interactions")
    np.testing.assert_array_equal(restored.participant_atoms, atoms)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    saved = loaded.interactions["two-waters"]
    assert saved.parameters == result.parameters and saved.software == result.software
    np.testing.assert_array_equal(
        saved.to_dict()["occurrence_indices"], result.to_dict()["occurrence_indices"]
    )
    selected = msm.extract(
        loaded, selection=np.unique(atoms)[::-1], structure_indices=[2, 1, 0]
    )
    assert selected.interactions["two-waters"].occurrence_structures.tolist() == [0, 2]
    for oxygen in [0, 1]:
        remaining = np.setdiff1d(np.arange(msm.get(loaded, n_atoms=True)), [oxygen])
        assert (
            msm.extract(loaded, selection=remaining)
            .interactions["two-waters"]
            .n_interactions
            == 0
        )


def test_simultaneity_empty_shapes_and_streaming_budget(monkeypatch, tmp_path):
    source, atoms = _chain(n_frames=2)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, atoms[1]] += 2
    xyz[1, atoms[-2]] += 2
    source.structures.coordinates = puw.quantity(xyz, "nm")
    empty = msm.interactions.water_bridges.get_water_bridges(source, order=2, pbc=False)
    assert empty.n_interactions == 0 and empty.evaluated_structure_indices.tolist() == [
        0,
        1,
    ]
    assert len(empty.measurements) == 15
    assert all(
        value.shape == (0,) and value.dtype == np.float64
        for value in empty.measurements.values()
    )
    source, _ = _chain(n_frames=50)
    path = str(tmp_path / "many.h5msm")
    msm.convert(source, to_form=path)
    from molsysmt.form import _h5msm05_modular

    monkeypatch.setattr(
        _h5msm05_modular,
        "read_molsys_file",
        lambda *a, **k: pytest.fail("Full file read"),
    )
    monkeypatch.setattr(msm.configure, "chunk_size", 7)
    for item in [source, path]:
        result = msm.interactions.water_bridges.get_water_bridges(
            item, order=2, pbc=False, heavy_mode="force"
        )
        assert (
            result.n_interactions == 50
            and result.execution_records[0]["details"]["execution_chunks"] == 8
        )
    selected = msm.interactions.water_bridges.get_water_bridges(
        path, order=2, structure_indices=[49, 0, 25, 49], pbc=False, heavy_mode="force"
    )
    assert selected.occurrence_structures.tolist() == [0, 25, 49]
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.interactions.water_bridges.get_water_bridges(source, order=2, pbc=False)


@pytest.mark.parametrize("value", [0, 3, -1, True, False, 2.0, "2", None, [2]])
def test_unsupported_or_untyped_order_fails(value):
    with pytest.raises(msm.ArgumentError):
        msm.interactions.water_bridges.get_water_bridges(
            _chain()[0], order=value, pbc=False
        )


def test_legacy_method_retains_its_exact_single_water_meaning():
    source, _ = _chain()
    assert (
        msm.interactions.water_bridges.get_water_bridges(
            source, method="two_hbonds_one_water", pbc=False
        ).parameters["method"]
        == "two_hbonds_one_water"
    )
    with pytest.raises(msm.ArgumentError):
        msm.interactions.water_bridges.get_water_bridges(
            source, method="two_hbonds_one_water", order=2, pbc=False
        )


def test_repeated_external_endpoint_is_not_a_two_water_path():
    source, atoms = _chain(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    molecule = msm.convert(source, to_form="rdkit.Mol")
    hs = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(2).GetNeighbors())
    xyz[0, 2] = [0.15, 0, 0]
    xyz[0, hs[:2]] = [[0.05, 0, 0], [0.25, 0, 0]]
    xyz[0, [3, atoms[-2]]] += 2
    source.structures.coordinates = puw.quantity(xyz, "nm")
    legs = msm.interactions.hbonds.get_hbonds(source, pbc=False)
    assert legs.n_interactions >= 3
    assert (
        msm.interactions.water_bridges.get_water_bridges(
            source, order=2, pbc=False
        ).n_interactions
        == 0
    )


def test_two_water_dense_endpoint_fanout_fails_its_resident_budget(monkeypatch):
    molecule = Chem.AddHs(Chem.MolFromSmiles("O.O." + ".".join(["N"] * 80)))
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    xyz = np.zeros((1, molecule.GetNumAtoms(), 3))
    xyz[0, :, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
    xyz[0, :2] = [[0, 0, 0], [0.3, 0, 0]]
    hs = [
        sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(i).GetNeighbors())
        for i in range(2)
    ]
    xyz[0, hs[0]] = [[0, 0.1, 0], [0.1, 0, 0]]
    xyz[0, hs[1]] = [[0.3, 0.1, 0], [0.3, -0.1, 0]]
    for atom in range(2, 82):
        hydrogen = min(a.GetIdx() for a in molecule.GetAtomWithIdx(atom).GetNeighbors())
        xyz[0, atom], xyz[0, hydrogen] = (
            ([-0.3, 0, 0], [-0.2, 0, 0]) if atom < 42 else ([0.6, 0, 0], [0.5, 0, 0])
        )
    source.structures.append(coordinates=puw.quantity(xyz, "nm"))
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1_000_000)
    with pytest.raises(MemoryBudgetExceededError, match="sparse-result"):
        msm.interactions.water_bridges.get_water_bridges(source, order=2, pbc=False)
