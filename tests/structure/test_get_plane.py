"""Checking general planes independently of chemical ring interpretation."""

from importlib.util import find_spec

import numpy as np
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
from molsysmt.native import MolSys, Structures, Topology


def _coordinates():
    # Orthogonal unit vectors with a normal whose largest component is positive.
    u = np.array([1., -1., 0.]) / np.sqrt(2)
    v = np.array([1., 1., -2.]) / np.sqrt(6)
    normal = np.cross(u, v)
    xy = np.array([[-1., -1.], [1., -1.], [1., 1.], [-1., 1.]]) * .1
    xyz = xy[:, :1] * u + xy[:, 1:] * v
    translations = np.array([[0., 0., 0.], [.3, -.2, .8], [2., 1., -1.]])
    return xyz[None] + translations[:, None], normal, translations


def _system(coordinates=None, box=None):
    coordinates = _coordinates()[0] if coordinates is None else coordinates
    return Structures(
        coordinates=puw.quantity(coordinates, "nm"),
        box=None if box is None else puw.quantity(box, "nm"),
        structure_id=[str(100 + 19 * i) for i in range(len(coordinates))],
    )


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_rotated_planes_translation_source_indices_and_nonmutation(heavy_mode):
    xyz, normal, centers = _coordinates()
    source = _system()
    before_writable = source._coordinates.flags.writeable
    result = msm.structure.get_plane(source, structure_indices=[2, 0, 2], heavy_mode=heavy_mode)
    np.testing.assert_allclose(result["normals"][:, 0], np.repeat(normal[None], 3, axis=0), atol=1e-14)
    np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm")[:, 0], centers[[2, 0, 2]], atol=1e-14)
    np.testing.assert_allclose(puw.get_value(result["rms_deviation"], to_unit="nm"), 0, atol=1e-14)
    np.testing.assert_array_equal(result["structure_indices"], [2, 0, 2])
    np.testing.assert_array_equal(source._coordinates, xyz)
    assert source._coordinates.flags.writeable == before_writable
    assert result["normals"].shape == (3, 1, 3)
    assert result["method"] == "unweighted_orthogonal_least_squares"


def test_warped_plane_against_independent_covariance_oracle_and_residuals():
    xyz, normal, _ = _coordinates()
    xyz[0, 0] += .02 * normal
    result = msm.structure.get_plane(_system(xyz), structure_indices=0)
    centered = xyz[0] - xyz[0].mean(axis=0)
    _, eigenvectors = np.linalg.eigh(centered.T @ centered)
    expected = eigenvectors[:, 0]
    observed = result["normals"][0, 0]
    assert abs(np.dot(expected, observed)) == pytest.approx(1., abs=1e-13)
    residual = centered @ expected
    assert puw.get_value(result["rms_deviation"], to_unit="nm")[0, 0] == pytest.approx(np.sqrt(np.mean(residual ** 2)))
    assert puw.get_value(result["max_deviation"], to_unit="nm")[0, 0] == pytest.approx(np.max(np.abs(residual)))


def test_overlapping_groups_deduplicate_atoms_preserve_group_order():
    result = msm.structure.get_plane(_system(), selection=[[3, 2, 1, 3], [0, 1, 2, 3]])
    assert result["atom_indices"].tolist() == [1, 2, 3, 0, 1, 2, 3]
    assert result["atom_offsets"].tolist() == [0, 3, 7]
    assert result["normals"].shape == (3, 2, 3)


@pytest.mark.parametrize("selection", [[], [0], [0, 1], [0, 0, 1], [[0, 1, 2], []], [-1, 0, 1], [0, 1, 4], None])
def test_invalid_memberships_fail_explicitly(selection):
    with pytest.raises(ArgumentError):
        msm.structure.get_plane(_system(), selection=selection)


@pytest.mark.parametrize("frames", [[-1], [3], [[0], [1]], None])
def test_invalid_frame_indices_fail_explicitly(frames):
    with pytest.raises(ArgumentError):
        msm.structure.get_plane(_system(), structure_indices=frames)


@pytest.mark.parametrize("xyz", [
    np.zeros((4, 3)), np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]]),
    np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]),
    np.array([[0, 0, 0], [1, 0, 0], [0, np.nan, 0], [0, 0, 1]]),
])
def test_coincident_collinear_isotropic_and_nonfinite_geometry_rejected(xyz):
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_plane(_system(xyz[None]))


def test_empty_frame_selection_does_not_open_coordinates(monkeypatch):
    import molsysmt.form.molsysmt_Structures as form

    def forbidden(*args, **kwargs):
        pytest.fail("Empty plane traversal opened structural data.")

    monkeypatch.setattr(form, "StructuresIterator", forbidden)
    result = msm.structure.get_plane(_system(), structure_indices=[], heavy_mode="force")
    assert result["normals"].shape == (0, 1, 3)
    assert result["rms_deviation"].shape == (0, 1)
    assert result["structure_indices"].dtype == np.int64


def test_explicit_units_and_session_standardization():
    source = _system()
    source.coordinates = puw.quantity(_coordinates()[0] * 10, "angstrom")
    original = list(puw.configure.get_standard_units())
    try:
        puw.configure.set_standard_units(["angstrom", "ps", "Da", "kelvin", "e", "mole", "radian"])
        result = msm.structure.get_plane(source, structure_indices=1)
        assert puw.get_unit(result["centers"]) == puw.get_unit(puw.quantity(1., "angstrom"))
        np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm")[0, 0], [.3, -.2, .8], atol=1e-14)
    finally:
        puw.configure.set_standard_units(original)


def test_pbc_whole_group_and_shift_preserve_observed_plane():
    box = np.repeat((2 * np.eye(3))[None], 3, axis=0)
    source = _system(box=box)
    result = msm.structure.get_plane(source, pbc=True)
    np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm")[:, 0], _coordinates()[2], atol=1e-14)
    xyz = _coordinates()[0]
    xyz[0, 0] += box[0, 0]
    with pytest.raises(NotImplementedMethodError):
        msm.structure.get_plane(_system(xyz, box), pbc=True)
    # Raw geometry remains a valid explicit option, with a different observed fit.
    msm.structure.get_plane(_system(xyz, box), pbc=False)


@pytest.mark.parametrize("box", [None, np.zeros((3, 3, 3)), np.full((3, 3, 3), np.nan)])
def test_missing_or_invalid_requested_box_fails(box):
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_plane(_system(box=box), pbc=True)


@pytest.mark.parametrize("scale", [1e-6, 1., 1e6])
def test_pbc_box_validation_is_invariant_to_uniform_length_scaling(scale):
    xyz, normal, _ = _coordinates()
    box = np.repeat((2 * scale * np.eye(3))[None], 3, axis=0)
    result = msm.structure.get_plane(_system(xyz * scale, box), pbc=True)
    np.testing.assert_allclose(result["normals"][:, 0], np.repeat(normal[None], 3, axis=0), atol=1e-13)


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.StructuresDict"])
def test_form_agnostic_native_and_dictionary_parity(form):
    source = _system()
    converted = MolSys._from_partial_domains(structures=source) if form == "molsysmt.MolSys" else msm.convert(source, to_form=form)
    result = msm.structure.get_plane(converted, structure_indices=[2, 0])
    expected = msm.structure.get_plane(source, structure_indices=[2, 0])
    np.testing.assert_allclose(result["normals"], expected["normals"])


def test_coordinate_only_quantity_form():
    result = msm.structure.get_plane(puw.quantity(_coordinates()[0] * 10, "angstrom"), structure_indices=[2, 0])
    expected = msm.structure.get_plane(_system(), structure_indices=[2, 0])
    np.testing.assert_allclose(result["normals"], expected["normals"], atol=1e-13)
    np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm"), puw.get_value(expected["centers"], to_unit="nm"), atol=1e-14)


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
@pytest.mark.parametrize("other_domains", [False, True])
def test_h5msm05_projection_without_materializing_other_domains(tmp_path, monkeypatch, heavy_mode, other_domains):
    import molsysmt.form._h5msm05_modular as modular

    source = _system()
    if other_domains:
        molsys = MolSys()
        molsys.topology = Topology(n_atoms=4)
        molsys.structures = source
        molsys.interactions = {"saved": msm.Interactions.from_records(
            [], n_atoms=4, n_structures=3, evaluated_structure_indices=[0, 1, 2], method="fixture",
        )}
    else:
        molsys = source
    filename = str(tmp_path / "planes.h5msm")
    msm.convert(molsys, to_form=filename)

    def forbidden(*args, **kwargs):
        pytest.fail("Numeric plane selection materialized unrelated domains or full structures.")

    monkeypatch.setattr(modular, "read_molsys_file", forbidden)
    monkeypatch.setattr(modular, "read_independent_structures", forbidden)
    monkeypatch.setattr(modular, "read_named_analyses", forbidden)
    result = msm.structure.get_plane(filename, selection=[[0, 2, 3], [0, 1, 2, 3]], structure_indices=[2, 0, 2], heavy_mode=heavy_mode)
    expected = msm.structure.get_plane(source, selection=[[0, 2, 3], [0, 1, 2, 3]], structure_indices=[2, 0, 2])
    np.testing.assert_allclose(result["normals"], expected["normals"])
    np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm"), puw.get_value(expected["centers"], to_unit="nm"))


@pytest.mark.parametrize("scale", [1e-100, 1., 1e100])
def test_plane_fit_scale_invariance_without_covariance_overflow(scale):
    xyz, normal, _ = _coordinates()
    result = msm.structure.get_plane(_system(xyz * scale))
    np.testing.assert_allclose(result["normals"][:, 0], np.repeat(normal[None], 3, axis=0), atol=1e-13)


def test_rich_selection_syntax_and_triclinic_box():
    molsys = MolSys()
    molsys.topology = Topology(n_atoms=4)
    molsys.topology.atoms["atom_name"] = ["A", "B", "C", "D"]
    box = np.repeat(np.array([[2., 0., 0.], [.3, 2., 0.], [.2, -.1, 2.]])[None], 3, axis=0)
    molsys.structures = _system(box=box)
    result = msm.structure.get_plane(molsys, selection=['atom_name in ["A", "B", "C"]', 'all'], pbc=True)
    assert result["atom_offsets"].tolist() == [0, 3, 7]
    assert result["normals"].shape == (3, 2, 3)


def test_numerical_budget_caps_coordinate_blocks_and_dense_output(monkeypatch):
    import molsysmt.configure as configure
    import molsysmt.structure._plane as kernel

    source = _system(np.repeat(_coordinates()[0][:1], 80, axis=0))
    monkeypatch.setattr(configure, "max_ram_usage", 14000)
    monkeypatch.setattr(configure, "chunk_size", 100)
    sizes = []
    original = kernel.fit_planes

    def record(coordinates, *args, **kwargs):
        sizes.append(len(coordinates))
        return original(coordinates, *args, **kwargs)

    monkeypatch.setattr(kernel, "fit_planes", record)
    result = msm.structure.get_plane(source)
    assert result["normals"].shape == (80, 1, 3)
    assert len(sizes) > 1 and max(sizes) < 80
    with pytest.raises(MemoryBudgetExceededError):
        msm.structure.get_plane(source, heavy_mode="off")
    monkeypatch.setattr(configure, "max_ram_usage", 1000)
    with pytest.raises(MemoryBudgetExceededError):
        msm.structure.get_plane(source)


@pytest.mark.skipif(find_spec("mdtraj") is None, reason="Optional MDTraj form")
def test_mdtraj_form_without_placeholder_iteration():
    import mdtraj as md

    topology = md.Topology()
    residue = topology.add_residue("UNK", topology.add_chain())
    for _ in range(4):
        topology.add_atom("C", md.element.carbon, residue)
    source = md.Trajectory(_coordinates()[0], topology)
    result = msm.structure.get_plane(source, structure_indices=[2, 0])
    np.testing.assert_allclose(result["normals"], msm.structure.get_plane(_system(), structure_indices=[2, 0])["normals"], atol=1e-6)
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.structure.get_plane(source, heavy_mode="force")


@pytest.mark.skipif(find_spec("rdkit") is None, reason="Optional RDKit form")
def test_rdkit_conformer_form_with_angstrom_coordinates():
    from rdkit import Chem

    source = Chem.MolFromSmiles("CCCC")
    conformer = Chem.Conformer(4)
    xyz = _coordinates()[0][0] + [.3, -.2, .8]
    for atom, point in enumerate(xyz * 10):
        conformer.SetAtomPosition(atom, point.tolist())
    source.AddConformer(conformer)
    result = msm.structure.get_plane(source)
    np.testing.assert_allclose(puw.get_value(result["centers"], to_unit="nm")[0, 0], [.3, -.2, .8], atol=1e-14)
    np.testing.assert_allclose(result["normals"][0, 0], _coordinates()[1], atol=1e-14)
