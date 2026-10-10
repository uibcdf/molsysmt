"""Check declared chemistry, independent ideal geometry and source correspondence."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)
from molsysmt.native import Structures


def placed(smiles, coordinates):
    molecule = Chem.MolFromSmiles(smiles)
    conformer = Chem.Conformer(molecule.GetNumAtoms())
    for atom, position in enumerate(coordinates):
        conformer.SetAtomPosition(atom, tuple(float(value) for value in position))
    molecule.AddConformer(conformer)
    return molecule


def carbonyl():
    return placed("CC=O", [[0, 1, 0], [0, 0, 0], [1, 0, 0]])


@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm", "composed"])
def test_carbonyl_independent_angles_support_and_forms(form, tmp_path):
    source = carbonyl()
    if form != "rdkit":
        source = msm.convert(source, to_form="molsysmt.MolSys")
        if form == "h5msm":
            path = str(tmp_path / "directions.h5msm")
            msm.convert(source, to_form=path)
            source = path
        elif form == "composed":
            source = [source.topology, source.structures]
    result = msm.interactions.hbonds.get_hbond_site_directions(source, pbc=False)
    expected = [[0.5, np.sqrt(3) / 2, 0], [0.5, -np.sqrt(3) / 2, 0]]
    np.testing.assert_allclose(result["directions"], expected, atol=1e-14)
    np.testing.assert_allclose(np.linalg.norm(result["directions"], axis=1), 1.0)
    np.testing.assert_allclose(result["directions"] @ [-1.0, 0, 0], -0.5)
    assert result["site_atom_indices"].tolist() == [2]
    assert result["support_atom_indices"].tolist() == [2, 1, 0]
    assert result["support_atom_offsets"].tolist() == [0, 3]
    assert result["direction_indices"].tolist() == [0, 1]
    assert result["image_offsets"].tolist() == [0, 3, 6]
    assert result["status"].tolist() == [[1]]
    assert result["site_models"].tolist() == [2]
    assert result["sites"]["method"] == "smarts_donor_acceptor"
    assert "rdkit" in result["software"]
    assert any(
        item["roles"] == ["geometric_inspiration"]
        for item in result["attribution"]["items"]
    )


@pytest.mark.parametrize(
    "smiles,coordinates,model",
    [
        ("C#N", [[0, 0, 0], [1, 0, 0]], 4),
        (
            "n1ccccc1",
            [
                [1, 0, 0],
                [0.5, 0.8, 0],
                [-0.5, 0.8, 0],
                [-1, 0, 0],
                [-0.5, -0.8, 0],
                [0.5, -0.8, 0],
            ],
            3,
        ),
    ],
)
def test_nitrogen_independent_outward_direction(smiles, coordinates, model):
    result = msm.interactions.hbonds.get_hbond_site_directions(
        placed(smiles, coordinates), pbc=False
    )
    np.testing.assert_allclose(result["directions"], [[1.0, 0, 0]], atol=1e-14)
    assert result["site_models"].tolist() == [model]


def test_observed_donor_hydrogens_and_unsupported_water_acceptor():
    source = placed("[H]O[H]", [[0, 0, 0]])
    source = Chem.AddHs(source)
    source.RemoveAllConformers()
    conformer = Chem.Conformer(3)
    for atom, position in enumerate([[0, 0, 0], [1, 0, 0], [0, 1, 0]]):
        conformer.SetAtomPosition(atom, position)
    source.AddConformer(conformer)
    result = msm.interactions.hbonds.get_hbond_site_directions(source, pbc=False)
    assert result["donor_hydrogen_pairs"].tolist() == [[0, 1], [0, 2]]
    assert result["site_roles"].tolist() == [0, 0, 1]
    assert result["status"].tolist() == [[1, 1, 0]]
    np.testing.assert_allclose(result["directions"], [[1.0, 0, 0], [0, 1.0, 0]])
    subset = msm.interactions.hbonds.get_hbond_site_directions(
        source, selection=[0, 1], pbc=False
    )
    assert subset["donor_hydrogen_pairs"].tolist() == [[0, 1]]
    assert subset["status"].tolist() == [[1, 0]]


@pytest.mark.parametrize(
    "smiles",
    [
        "COC",
        "CO",
        "O",
        "CC(=O)[O-]",
        "CC(=O)O",
        "CC(=O)OC",
        "CN",
        "OP(=O)(O)O",
        "OS(=O)(=O)O",
    ],
)
def test_other_acceptor_environments_remain_explicitly_unsupported(smiles):
    molecule = Chem.MolFromSmiles(smiles)
    result = msm.interactions.hbonds.get_hbond_site_directions(
        molecule, structure_indices=[], pbc=False
    )
    assert not result["site_models"].any()
    assert result["directions"].shape == (0, 3)
    assert result["status"].shape == (0, len(result["acceptor_atom_indices"]))


@pytest.mark.parametrize("smiles", ["CC(=O)N", "c1cc[nH]c1", "c1cc[nH+]cc1"])
def test_amide_pyrrole_and_protonated_nitrogen_are_not_acceptors(smiles):
    molecule = Chem.MolFromSmiles(smiles)
    result = msm.interactions.hbonds.get_hbond_site_directions(
        molecule, structure_indices=[], pbc=False
    )
    nitrogen = {
        atom.GetIdx() for atom in molecule.GetAtoms() if atom.GetSymbol() == "N"
    }
    assert not nitrogen & set(result["acceptor_atom_indices"])


def test_selected_anchor_retains_external_support_and_is_rotation_covariant():
    source = carbonyl()
    result = msm.interactions.hbonds.get_hbond_site_directions(
        source, selection=[2], pbc=False
    )
    assert result["selected_atom_indices"].tolist() == [2]
    assert result["support_atom_indices"].tolist() == [2, 1, 0]
    rotation = np.array([[0.0, 0, 1], [1, 0, 0], [0, 1, 0]])
    original = source.GetConformer().GetPositions()
    moved = placed("CC=O", original @ rotation + [2.0, 3.0, 4.0])
    actual = msm.interactions.hbonds.get_hbond_site_directions(moved, pbc=False)
    np.testing.assert_allclose(
        actual["directions"], result["directions"] @ rotation, atol=1e-14
    )
    np.testing.assert_array_equal(source.GetConformer().GetPositions(), original)


@pytest.mark.parametrize(
    "smiles,coordinates",
    [
        ("C=O", [[0, 0, 0], [1, 0, 0]]),
        ("CC=O", [[-1, 0, 0], [0, 0, 0], [1, 0, 0]]),
        ("C#N", [[0, 0, 0], [0, 0, 0]]),
        (
            "n1ccccc1",
            [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [-1, 1, 0], [-1, 0, 0]],
        ),
    ],
)
def test_degenerate_geometry_has_no_arbitrary_direction(smiles, coordinates):
    result = msm.interactions.hbonds.get_hbond_site_directions(
        placed(smiles, coordinates), pbc=False
    )
    assert result["status"].tolist() == [[2]]
    assert result["directions"].shape == (0, 3)
    assert result["image_vectors"].shape == (0, 3)
    assert result["image_offsets"].tolist() == [0]


def test_nonconsecutive_repeated_structures_and_chunking(monkeypatch):
    from molsysmt.interactions.hbonds._hbond_directions import DirectionReducer

    source = msm.convert(carbonyl(), to_form="molsysmt.MolSys")
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(
            np.concatenate([coordinates + shift for shift in range(5)]), "nm"
        )
    )
    monkeypatch.setattr(msm.configure, "chunk_size", 1)
    eager = msm.interactions.hbonds.get_hbond_site_directions(
        source, structure_indices=[4, 1, 4], pbc=False, heavy_mode="off"
    )
    consumed = []
    original_consume = DirectionReducer.consume

    def capture(self, chunk):
        consumed.append(len(chunk["coordinates"]))
        return original_consume(self, chunk)

    monkeypatch.setattr(DirectionReducer, "consume", capture)
    chunks = msm.interactions.hbonds.get_hbond_site_directions(
        source, structure_indices=[4, 1, 4], pbc=False, heavy_mode="force"
    )
    for name in [
        "directions",
        "status",
        "direction_structure_indices",
        "direction_structure_positions",
        "image_vectors",
        "image_offsets",
    ]:
        np.testing.assert_array_equal(chunks[name], eager[name])
    assert chunks["direction_structure_indices"].tolist() == [4, 4, 1, 1, 4, 4]
    assert chunks["direction_structure_positions"].tolist() == [0, 0, 1, 1, 2, 2]
    assert chunks["execution"]["execution"] == "chunked"
    assert consumed == [1, 1, 1]
    source.chemical_states._states[0].bonds = (
        source.chemical_states._states[0].bonds.iloc[::-1].reset_index(drop=True)
    )
    reordered = msm.interactions.hbonds.get_hbond_site_directions(
        source, structure_indices=[4, 1, 4], pbc=False
    )
    np.testing.assert_array_equal(reordered["directions"], eager["directions"])


@pytest.mark.parametrize(
    "box", [np.eye(3), np.array([[1.0, 0, 0], [0.2, 1.0, 0], [0.1, 0.3, 1.0]])]
)
@pytest.mark.parametrize("form", ["native", "h5msm"])
def test_periodic_images_reconstruct_carbonyl_plane(box, form, tmp_path):
    source = msm.convert(carbonyl(), to_form="molsysmt.MolSys")
    canonical = puw.get_value(source.structures.coordinates, to_unit="nm")
    shifts = np.array([[1, -1, 0], [0, 1, 0], [-1, 0, 0]])
    wrapped = canonical + shifts @ box
    source.structures.coordinates = puw.quantity(wrapped * 10.0, "angstrom")
    source.structures.box = puw.quantity(box[None] * 10.0, "angstrom")
    before = puw.get_value(source.structures.coordinates).copy()
    input_system = source
    if form == "h5msm":
        input_system = str(tmp_path / "periodic.h5msm")
        msm.convert(source, to_form=input_system)
    result = msm.interactions.hbonds.get_hbond_site_directions(
        input_system, selection=[2], pbc=True
    )
    np.testing.assert_allclose(
        result["directions"],
        [[0.5, np.sqrt(3) / 2, 0], [0.5, -np.sqrt(3) / 2, 0]],
        atol=1e-13,
    )
    expected = shifts[2] - shifts[[2, 1, 0]]
    np.testing.assert_array_equal(result["image_vectors"], np.tile(expected, (2, 1)))
    reconstructed = wrapped[0, [2, 1, 0]] + result["image_vectors"][:3] @ box
    np.testing.assert_allclose(
        reconstructed - reconstructed[0],
        canonical[0, [2, 1, 0]] - canonical[0, 2],
        atol=1e-14,
    )
    np.testing.assert_array_equal(puw.get_value(source.structures.coordinates), before)


def test_output_units_are_presented_through_pyunitwizard():
    with puw.context(standard_units=["angstrom", "ps"]):
        result = msm.interactions.hbonds.get_hbond_site_directions(
            carbonyl(), pbc=False
        )
        np.testing.assert_allclose(
            puw.get_value(result["origins"], to_unit="angstrom"), [[1, 0, 0], [1, 0, 0]]
        )
        assert result["units"]["origins"] == str(puw.get_unit(result["origins"]))
        np.testing.assert_allclose(result["directions"][:, 0], 0.5)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"method": "unknown"},
        {"site_method": "unknown"},
        {"max_matches": 0},
        {"structure_indices": [-1]},
        {"structure_indices": [[0]]},
        {"pbc": "yes"},
    ],
)
def test_invalid_arguments_raise_at_public_boundary(kwargs):
    with pytest.raises(ArgumentError):
        msm.interactions.hbonds.get_hbond_site_directions(carbonyl(), **kwargs)


@pytest.mark.parametrize(
    "coordinates",
    [[[0, 1, 0], [0, 0, 0], [np.nan, 0, 0]], [[0, 1, 0], [0, 0, 0], [np.inf, 0, 0]]],
)
def test_nonfinite_coordinates_raise(coordinates):
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_site_directions(
            placed("CC=O", coordinates), pbc=False
        )


@pytest.mark.parametrize(
    "selection,structures,status_shape", [([], "all", (1, 0)), ("all", [], (0, 1))]
)
def test_typed_empty_results(selection, structures, status_shape):
    result = msm.interactions.hbonds.get_hbond_site_directions(
        carbonyl(), selection=selection, structure_indices=structures, pbc=False
    )
    assert result["status"].shape == status_shape and result["status"].dtype == np.uint8
    assert (
        result["directions"].shape == (0, 3)
        and result["directions"].dtype == np.float64
    )
    assert (
        result["image_vectors"].shape == (0, 3)
        and result["image_vectors"].dtype == np.int32
    )
    assert result["direction_site_indices"].dtype == np.int64
    assert result["image_offsets"].tolist() == [0]


def test_numeric_status_and_packing_budget_is_enforced():
    from molsysmt.interactions.hbonds._hbond_directions import (
        DirectionReducer,
        build_site_plan,
    )

    sites = msm.interactions.hbonds.get_hbond_sites(
        carbonyl(), method="smarts_donor_acceptor"
    )
    plan = build_site_plan(carbonyl(), sites, False, 100000)
    with pytest.raises(MemoryBudgetExceededError):
        DirectionReducer(plan, sites, np.arange(10000), False, 1024)


@pytest.mark.parametrize(
    "backend,module",
    [
        ("pint", "pint"),
        ("openmm.unit", "openmm"),
        ("unyt", "unyt"),
        ("astropy.units", "astropy"),
    ],
)
def test_length_backend_and_standard_policy_are_preserved(backend, module):
    pytest.importorskip(module)
    with puw.context(default_form=backend, standard_units=["angstrom", "ps"]):
        result = msm.interactions.hbonds.get_hbond_site_directions(
            carbonyl(), pbc=False
        )
        assert puw.get_form(result["origins"]) == backend
        assert puw.has_unit(result["origins"], "angstrom")
        np.testing.assert_allclose(
            puw.get_value(result["origins"], to_unit="nm"), [[0.1, 0, 0], [0.1, 0, 0]]
        )


def test_structure_assigned_chemistry_is_coherent_and_source_is_unchanged(tmp_path):
    from copy import deepcopy

    source = msm.convert(carbonyl(), to_form="molsysmt.MolSys")
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(np.repeat(coordinates, 3, axis=0), "nm")
    )
    source.chemical_states.append_state()
    source.chemical_states._states[1] = deepcopy(source.chemical_states._states[0])
    source._set_structure_chemical_state_indices([1, 0, 1])
    original_bonds = source.chemical_states._states[1].bonds.copy(deep=True)
    source_reference = source.chemical_states.reference_chemical_state_index
    selected = msm.interactions.hbonds.get_hbond_site_directions(
        source, structure_indices=[2, 0], chemical_state="structure", pbc=False
    )
    assert selected["chemical_state_index"] == 1
    assert selected["sites"]["chemical_state_index"] == 1
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_site_directions(
            source, structure_indices=[2, 1], chemical_state="structure", pbc=False
        )
    path = str(tmp_path / "states.h5msm")
    msm.convert(source, to_form=path)
    disk = msm.interactions.hbonds.get_hbond_site_directions(
        path,
        structure_indices=[2, 0],
        chemical_state="structure",
        pbc=False,
        heavy_mode="force",
    )
    assert disk["chemical_state_index"] == 1
    np.testing.assert_array_equal(disk["direction_structure_indices"], [2, 2, 0, 0])
    np.testing.assert_allclose(disk["directions"], selected["directions"])
    assert source.chemical_states.reference_chemical_state_index == source_reference
    assert source.chemical_states._states[1].bonds.equals(original_bonds)


def test_h5msm_delivery_does_not_materialize_full_structural_series(
    tmp_path, monkeypatch
):
    from molsysmt.form import _h5msm05_modular

    source = msm.convert(carbonyl(), to_form="molsysmt.MolSys")
    path = str(tmp_path / "lazy.h5msm")
    msm.convert(source, to_form=path)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "The direction query must use projected coordinate delivery, not full H5MSM reading."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    result = msm.interactions.hbonds.get_hbond_site_directions(
        path, structure_indices=[0], heavy_mode="force"
    )
    assert result["status"].tolist() == [[1]]


def test_singular_box_is_rejected():
    source = msm.convert(carbonyl(), to_form="molsysmt.MolSys")
    source.structures.box = puw.quantity(np.zeros((1, 3, 3)), "nm")
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_site_directions(source)


def test_metal_coordinated_acceptor_is_outside_profile():
    source = msm.convert(
        placed("C#N.[Zn+2]", [[0, 0, 0], [1, 0, 0], [2, 0, 0]]),
        to_form="molsysmt.MolSys",
    )
    import pandas as pd

    state = source.chemical_states._states[0]
    state.bonds = pd.concat(
        [
            state.bonds,
            pd.DataFrame(
                [
                    dict(
                        atom1_index=1,
                        atom2_index=2,
                        bond_type="dative",
                        order=1.0,
                        is_aromatic=False,
                    )
                ]
            ),
        ],
        ignore_index=True,
    )
    result = msm.interactions.hbonds.get_hbond_site_directions(
        source, site_method="elemental_nitrogen_oxygen", pbc=False
    )
    assert result["site_models"].tolist() == [0]
    assert result["status"].tolist() == [[0]]


def test_undefined_and_unsupported_remain_distinct_in_same_structure():
    result = msm.interactions.hbonds.get_hbond_site_directions(
        placed("C=O.O", [[0, 0, 0], [1, 0, 0], [2, 0, 0]]), pbc=False
    )
    assert result["site_models"].tolist() == [2, 0]
    assert result["status"].tolist() == [[2, 0]]
    assert result["directions"].shape == (0, 3)
