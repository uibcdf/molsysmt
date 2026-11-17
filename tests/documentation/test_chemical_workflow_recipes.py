"""Receive literal chemical-workflow examples with explicit prepared inputs."""

import hashlib
import json
import re
import warnings
from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm
from tests.form.file_pdbqt.test_native_contract import LIGAND

ROOT = Path(__file__).resolve().parents[2]
COOKBOOK = ROOT / "docs/content/user/cookbook"


def _blocks(name):
    page = COOKBOOK / (name + ".md")
    return page, re.findall(r"^```python\n(.*?)^```", page.read_text(), re.M | re.S)


def _execute(page, blocks, namespace=None):
    namespace = {} if namespace is None else namespace
    for block in blocks:
        exec(compile(block, str(page), "exec"), namespace)
    return namespace


def _record_file_versions(monkeypatch):
    """Read actual completed files before a recipe retires its temporary output."""
    versions = []
    convert = msm.convert

    def received(*args, **kwargs):
        result = convert(*args, **kwargs)
        if isinstance(result, (str, Path)) and str(result).endswith(".h5msm"):
            with h5py.File(result, "r") as handle:
                versions.append(str(handle.attrs["version"]))
        return result

    monkeypatch.setattr(msm, "convert", received)
    return versions


@pytest.mark.parametrize("units", [["nm", "ps"], ["pm", "fs"]])
def test_sdf_recipe_preserves_declared_chemistry_and_explicit_stereo(
    units, tmp_path, monkeypatch
):
    from rdkit import Chem
    from rdkit.Chem import rdDepictor

    source = Path(msm.systems["caffeine"]["caffeine.sdf"])
    original = source.read_bytes()
    stereo = Chem.MolFromSmiles("N[C@@H](C)C(=O)O")
    rdDepictor.Compute2DCoords(stereo)
    (tmp_path / "stereo.sdf").write_text(Chem.MolToMolBlock(stereo) + "$$$$\n")
    page, blocks = _blocks("native_sdf")
    assert len(blocks) == 6
    monkeypatch.chdir(tmp_path)
    with msm.pyunitwizard.context(standard_units=units):
        namespace = _execute(page, blocks[:4])
        assert namespace["molsys"].get(n_atoms=True) == 24
        assert namespace["molsys"].chemical_states.get(n_bonds=True) == 25
        selected = msm.convert("selected.sdf")
        assert selected.get(n_atoms=True) == 3
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(selected.structures.coordinates, to_unit="nm"),
            msm.pyunitwizard.get_value(
                namespace["molsys"].structures.coordinates, to_unit="nm"
            )[:, [0, 2, 4]],
            atol=1e-5,
        )
        _execute(page, blocks[4:], namespace)
        assert (
            msm.physchem.get_cip_stereochemistry(namespace["molsys"])[
                "atom_stereochemistry"
            ][1]
            == "S"
        )
        independent = Chem.SDMolSupplier("stereo_out.sdf", removeHs=False)[0]
        assert independent.GetAtomWithIdx(1).GetProp("_CIPCode") == "S"
    assert source.read_bytes() == original


@pytest.mark.parametrize("units", [["nm", "ps", "e"], ["pm", "fs", "coulomb"]])
def test_pdbqt_recipe_uses_supplied_types_charges_tree_and_final_byte_map(
    units, tmp_path, monkeypatch
):
    source = tmp_path / "prepared_ligand.pdbqt"
    source.write_text(LIGAND)
    page, blocks = _blocks("native_pdbqt")
    assert len(blocks) == 4
    monkeypatch.chdir(tmp_path)
    with msm.pyunitwizard.context(standard_units=units):
        namespace = _execute(page, blocks)
        molsys = namespace["molsys"]
        assert molsys.topology.atoms.atom_id.tolist() == ["17", "3", "45", "90"]
        assert molsys.chemical_states._states[0].connectivity_completeness == "partial"
        np.testing.assert_allclose(namespace["charges"], [0.125, -0.1, -0.25, 0.225])
        assert list(namespace["labels"]) == ["C", "A", "OA", "HD"]
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(namespace["coordinates"], to_unit="angstrom"),
            [[[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]],
        )
        payload = namespace["payload"].removeprefix("pdbqt_text:")
        assert (
            namespace["atom_map"]["payload_sha256"]
            == hashlib.sha256(payload.encode("utf-8")).hexdigest()
        )
        assert namespace["tree"]["torsdof"] == 2
        stored = namespace["stored"]
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                stored.structures.coordinates, to_unit="angstrom"
            ),
            [[[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]],
        )
        assert stored.chemical_states._states[0].connectivity_completeness == "partial"
        with h5py.File("prepared_values.h5msm", "r") as handle:
            assert handle.attrs["version"] == "1.0"
    assert source.read_text() == LIGAND


def test_template_reconstruction_example_retains_original_coordinate_map():
    page, blocks = _blocks("applying_chemical_templates")
    assert len(blocks) == 12
    namespace = _execute(page, [blocks[1]])
    source, result = namespace["molsys"], namespace["molsys_completed"]
    old_to_new, new_to_old = namespace["old_to_new"], namespace["new_to_old"]
    np.testing.assert_array_equal(
        new_to_old[old_to_new], np.arange(source.get_n_atoms())
    )
    assert np.all(new_to_old[namespace["generated"]] == -1)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm")[
            :, old_to_new
        ],
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )


def test_export_order_recipe_restores_correspondence_and_both_h5msm_profiles(
    monkeypatch,
):
    versions = _record_file_versions(monkeypatch)
    page, blocks = _blocks("permuting_export_order")
    namespace = _execute(page, blocks)
    source, restored = namespace["molsys"], namespace["molsys_restored"]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    assert versions == ["1.0", "0.5"]


def test_sequence_source_groups_recipe_preserves_order_without_invented_atoms():
    page, blocks = _blocks("comparing_sequence_source_groups")
    namespace = _execute(page, blocks, {"msm": msm})
    assert namespace["molsys"].topology.n_atoms == 0
    assert namespace["subset"].get(element="group", group_name=True) == ["TRP", "ALA"]
    assert namespace["subset"].topology.chain_groups == ((1, 0),)


def test_metadata_recipe_keeps_labels_squared_units_and_both_h5msm_profiles(
    monkeypatch,
):
    versions = _record_file_versions(monkeypatch)
    page = COOKBOOK / "editing_labels_and_structure_metadata.ipynb"
    notebook = json.loads(page.read_text())
    blocks = [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    ]
    with warnings.catch_warnings():
        namespace = _execute(page, blocks)
    assert namespace["labels"] == ["101", "00101"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(namespace["saved_factors"], to_unit="angstrom**2"),
        [[21, 22], [1, 2], [21, 22]],
    )
    assert versions == ["1.0", "0.5"]
