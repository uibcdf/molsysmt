"""Keep PDB models, inventory and selected coordinate axes coherent."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_model_queries_preserve_explicit_order_duplicates_and_box(
    openmm_pdb_ensemble, length, time
):
    from openmm import unit

    item = openmm_pdb_ensemble
    expected = np.array(
        [
            item.getPositions(asNumpy=True, frame=i).value_in_unit(unit.nanometer)
            for i in range(3)
        ]
    )
    with puw.context(standard_units=[length, time, "radians"]):
        assert msm.get(item, n_structures=True) == 3
        coordinates = msm.get(item, element="atom", coordinates=True)
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="nm"), expected, rtol=0, atol=1e-12
        )
        selected = msm.get(
            item,
            element="atom",
            selection=[3, 1, 1],
            structure_indices=[2, 0, 2],
            coordinates=True,
        )
        np.testing.assert_allclose(
            puw.get_value(selected, to_unit="nm"),
            expected[[2, 0, 2]][:, [3, 1, 1]],
            rtol=0,
            atol=1e-12,
        )
        box = msm.get(item, structure_indices=[2, 0], box=True)
        assert box.shape == (2, 3, 3)
        np.testing.assert_allclose(
            puw.get_value(box, to_unit="nm"),
            np.repeat(np.diag([4, 5, 6])[None], 2, axis=0),
            rtol=0,
            atol=1e-12,
        )


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
@pytest.mark.parametrize("operation", ["extract", "convert"])
def test_same_form_subset_keeps_source_order_and_all_requested_models(
    openmm_pdb_ensemble, length, time, operation
):
    from openmm import unit

    item = openmm_pdb_ensemble
    xyz = np.array(
        [
            item.getPositions(asNumpy=True, frame=i).value_in_unit(unit.nanometer)
            for i in range(3)
        ]
    )
    names = [a.name for a in item.topology.atoms()]
    with puw.context(standard_units=[length, time, "radians"]):
        arguments = dict(selection=[3, 1, 1], structure_indices=[2, 0, 2])
        result = (
            msm.extract(item, **arguments)
            if operation == "extract"
            else msm.convert(item, to_form="openmm.PDBFile", **arguments)
        )
        assert msm.get_form(result) == "openmm.PDBFile"
        assert result is not item
        assert [a.name for a in result.topology.atoms()] == [names[1], names[3]]
        assert result.getNumFrames() == 3
        for index, original in enumerate([2, 0, 2]):
            np.testing.assert_allclose(
                result.getPositions(asNumpy=True, frame=index).value_in_unit(
                    unit.nanometer
                ),
                xyz[original, [1, 3]],
                rtol=0,
                atol=1e-12,
            )
    assert item.topology.getNumAtoms() == 4
    assert item.getNumFrames() == 3


def test_adapter_identity_conversion_obeys_copy_policy(openmm_pdb_ensemble):
    from molsysmt.form.openmm_PDBFile.to_openmm_PDBFile import to_openmm_PDBFile

    source = openmm_pdb_ensemble
    independent = to_openmm_PDBFile(source)
    assert independent is not source
    assert independent.topology is not source.topology
    assert to_openmm_PDBFile(source, copy_if_all=False) is source


@pytest.mark.parametrize("form", ["openmm.PDBFile", "openmm.Modeller"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_native_projection_deduplicates_inventory_and_coordinates_together(
    openmm_pdb_ensemble, form, length, time
):
    from openmm import unit
    from openmm.app import Modeller

    source = openmm_pdb_ensemble
    structures = [2, 0]
    if form == "openmm.Modeller":
        source = Modeller(source.topology, source.positions)
        structures = [0]
    expected = np.array(
        [
            openmm_pdb_ensemble.getPositions(frame=i).value_in_unit(unit.nanometer)
            for i in structures
        ]
    )[:, [1, 2]]
    names = [atom.name for atom in source.topology.atoms()]
    with puw.context(standard_units=[length, time, "radians"]):
        result = msm.convert(
            source,
            to_form="molsysmt.MolSys",
            selection=[2, 1, 1],
            structure_indices=structures,
        )
        assert result.topology.n_atoms == 2
        assert result.topology.atoms["atom_name"].tolist() == [names[1], names[2]]
        assert result.structures.coordinates.shape == (len(structures), 2, 3)
        np.testing.assert_allclose(
            puw.get_value(result.structures.coordinates, to_unit="nm"),
            expected,
            rtol=0,
            atol=1e-12,
        )
        np.testing.assert_array_equal(
            msm.get(result, element="bond", bonded_atom_pairs=True), [[0, 1]]
        )


def test_projection_replaces_openmm_position_caches_without_aliases(
    openmm_pdb_ensemble,
):
    from openmm import unit

    source = openmm_pdb_ensemble
    before = (
        source.getPositions(asNumpy=True, frame=2).value_in_unit(unit.nanometer).copy()
    )
    result = msm.extract(source, selection=[3, 1], structure_indices=[2, 0, 2])
    cached = result.getPositions(asNumpy=True, frame=0).value_in_unit(unit.nanometer)
    np.testing.assert_allclose(cached, before[[1, 3]], rtol=0, atol=1e-12)
    result.positions[0, 0] = 99 * unit.nanometer
    np.testing.assert_array_equal(
        source.getPositions(asNumpy=True, frame=2).value_in_unit(unit.nanometer), before
    )
    assert result.getPositions(frame=2)[0, 0] != 99 * unit.nanometer


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_mdtraj_projection_preserves_models_and_box(openmm_pdb_ensemble, length, time):
    from openmm import unit

    source = openmm_pdb_ensemble
    expected = np.array(
        [
            source.getPositions(frame=index).value_in_unit(unit.nanometer)
            for index in [2, 0, 2]
        ]
    )[:, [1, 3]]
    with puw.context(standard_units=[length, time, "radians"]):
        result = msm.convert(
            source,
            to_form="mdtraj.Trajectory",
            selection=[3, 1, 1],
            structure_indices=[2, 0, 2],
        )
        assert result.n_frames == 3 and result.n_atoms == 2
        np.testing.assert_array_equal(result.xyz, expected.astype("float32"))
        np.testing.assert_array_equal(
            result.unitcell_vectors, np.repeat(np.diag([4, 5, 6])[None], 3, axis=0)
        )


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_modeller_projection_uses_first_selected_pose(
    openmm_pdb_ensemble, length, time
):
    from openmm import unit

    source = openmm_pdb_ensemble
    with puw.context(standard_units=[length, time, "radians"]):
        result = msm.convert(
            source,
            to_form="openmm.Modeller",
            selection=[3, 1, 1],
            structure_indices=[2, 0],
        )
        np.testing.assert_allclose(
            puw.get_value(result.positions, to_unit="nm"),
            source.getPositions(asNumpy=True, frame=2).value_in_unit(unit.nanometer)[
                [1, 3]
            ],
            rtol=0,
            atol=1e-12,
        )
        assert result.topology.getNumAtoms() == 2
