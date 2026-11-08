"""Receiving real source/H-generation composition without relaxing graph labels."""

import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from tests.chemical_states.test_normalize_indexed_hydrogen_policy import (
    normalize,
    water,
)
from tests.native.test_preparation_history import assert_tree

pytest.importorskip("rdkit.Chem")
puw = msm.pyunitwizard
DATA = Path(__file__).resolve().parents[1] / "form" / "data" / "vina_examples"


def interpreted(filename):
    source = msm.convert(
        DATA / filename,
        to_form="molsysmt.MolSys",
        stereo_engine="rdkit",
        discard_properties=True,
    )
    return msm.convert(
        msm.convert(source, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )


def witness(source, reference):
    return msm.chemical_states.get_atom_correspondences(
        source,
        selection=msm.select(source, selection="atom_type!='H'"),
        reference_molecular_system=reference,
        reference_selection=msm.select(reference, selection="atom_type!='H'"),
        max_matches=4096,
    )


@pytest.mark.parametrize(
    "units", [["nm", "ps", "elementary_charge"], ["pm", "fs", "coulomb"]]
)
def test_original_p59_producers_require_explicit_policy_and_survive_persistence(
    units, tmp_path, monkeypatch
):
    manifest = json.loads((DATA / "manifest.json").read_text())
    heavy = manifest["additional_files"]["5x72_ligand_p59.sdf"]
    hydrogenated = next(
        row for row in manifest["records"] if row["name"] == "5x72-p59"
    )["files"]["sdf"]
    for filename, record in [
        ("5x72_ligand_p59.sdf", heavy),
        ("5x72_ligand_p59H.sdf", hydrogenated),
    ]:
        assert (
            hashlib.sha256((DATA / filename).read_bytes()).hexdigest()
            == record["sha256"]
        )
    with puw.context(standard_units=units):
        policy = str(puw.get_unit(puw.standardize(puw.quantity(1, "nm"))))
        source, reference = (
            interpreted("5x72_ligand_p59H.sdf"),
            interpreted("5x72_ligand_p59.sdf"),
        )
        originals = [item.copy() for item in (source, reference)]
        original_payloads = [
            msm.convert(item, to_form="molsysmt.MolSysDict").data
            for item in (source, reference)
        ]
        added = msm.build.add_missing_hydrogens(
            reference,
            pH=None,
            mode="fixed_chemical_state",
            engine="RDKit",
            return_report=True,
            structure_indices=0,
            chemical_state="structure",
        )
        assert added["report"]["n_added_hydrogens"] == 15
        generated = added["molecular_system"]
        np.testing.assert_allclose(
            puw.get_value(generated.structures.coordinates, to_unit="angstrom")[:, :24],
            puw.get_value(reference.structures.coordinates, to_unit="angstrom"),
            rtol=0,
            atol=1e-12,
        )
        before = witness(source, generated)
        assert before["search_complete"] is True
        assert before["n_candidate_matches"] == 2
        assert before["atom_correspondences"].shape == (0, 24, 2)
        old_histories = [
            item.chemical_states.get_preparation_history()
            for item in (source, generated)
        ]
        results = [normalize(item) for item in (source, generated)]
        assert [result["report"]["status"] for result in results] == [
            "normalized",
            "unchanged",
        ]
        np.testing.assert_array_equal(
            results[0]["report"]["changed_atom_indices"], np.arange(24, 39)
        )
        assert results[1]["report"]["changed_atom_indices"].size == 0
        outputs = [result["molecular_system"] for result in results]
        admitted = witness(*outputs)
        assert admitted["search_complete"] is True
        assert admitted["n_candidate_matches"] == 2
        assert admitted["atom_correspondences"].shape == (2, 24, 2)
        for original, current, payload in zip(
            originals, (source, reference), original_payloads
        ):
            pd.testing.assert_frame_equal(
                original.topology.atoms, current.topology.atoms
            )
            pd.testing.assert_frame_equal(
                original.chemical_states._states[0].atom_attributes,
                current.chemical_states._states[0].atom_attributes,
            )
            pd.testing.assert_frame_equal(
                original.chemical_states.get_bonds(),
                current.chemical_states.get_bonds(),
                # Pandas copies can drop an internal table subclass; field dtypes remain strict.
                check_frame_type=False,
            )
            assert_tree(
                msm.convert(current, to_form="molsysmt.MolSysDict").data, payload
            )
            np.testing.assert_array_equal(
                puw.get_value(original.structures.coordinates),
                puw.get_value(current.structures.coordinates),
            )
            assert_tree(
                original.chemical_states.get_preparation_history(),
                current.chemical_states.get_preparation_history(),
            )
        paths = []
        for i, (result, old_history) in enumerate(zip(results, old_histories)):
            output = result["molecular_system"]
            assert (
                output.chemical_states._states[0].atom_attributes.at[
                    7, "stereochemistry"
                ]
                == "R"
            )
            pd.testing.assert_frame_equal(
                output.chemical_states._states[0].atom_attributes.drop(
                    columns="allows_implicit_hydrogens"
                ),
                (source, generated)[i]
                .chemical_states._states[0]
                .atom_attributes.drop(columns="allows_implicit_hydrogens"),
            )
            np.testing.assert_array_equal(
                puw.get_value(output.structures.coordinates),
                puw.get_value((source, generated)[i].structures.coordinates),
            )
            history = output.chemical_states.get_preparation_history()
            assert_tree(history[:-1], old_history)
            assert_tree(history[-1]["report"], result["report"])
            path = tmp_path / f"normalized-{i}.h5msm"
            msm.h5msm.write(output, path)
            paths.append(path)
        monkeypatch.setattr(msm, "__version__", "999.loading-version")
        restored = [msm.h5msm.read(path) for path in paths]
        for result, loaded in zip(results, restored):
            assert_tree(
                loaded.chemical_states.get_preparation_history()[-1]["report"],
                result["report"],
            )
            assert (
                loaded.chemical_states.get_preparation_history()[-1]["report"][
                    "software"
                ]["molsysmt"]
                != "999.loading-version"
            )
        np.testing.assert_array_equal(
            witness(*restored)["atom_correspondences"], admitted["atom_correspondences"]
        )
        assert str(puw.get_unit(puw.standardize(puw.quantity(1, "nm")))) == policy


def test_real_isotope_difference_is_not_erased_by_policy_normalization():
    hydrogen, deuterium = water(), water(isotopes=(None, 2, None))
    outputs = [normalize(item)["molecular_system"] for item in (hydrogen, deuterium)]
    result = witness(*outputs)
    assert result["search_complete"] is True
    assert result["atom_correspondences"].shape == (0, 1, 2)
    assert pd.isna(outputs[0].topology.atoms.at[1, "isotope"])
    assert outputs[1].topology.atoms.at[1, "isotope"] == 2


def test_optional_rdkit_form_uses_the_existing_converter():
    native = water(structures=False)
    item = msm.convert(native, to_form="rdkit.Mol")
    result = normalize(item)
    assert result["report"]["hydrogen_atom_indices"].tolist() == [1, 2]
    assert msm.get(
        result["molecular_system"], element="atom", allows_implicit_hydrogens=True
    )[1:] == [False, False]


@pytest.mark.parametrize(
    "page",
    [
        "docs/content/user/tools/chemical_states/normalize_indexed_hydrogen_policy.md",
        "docs/content/user/cookbook/aligning_stored_hydrogen_policies.md",
    ],
)
@pytest.mark.parametrize(
    "units", [["nm", "ps", "elementary_charge"], ["pm", "fs", "coulomb"]]
)
def test_documented_policy_examples_execute_with_the_declared_units(
    page, units, tmp_path, monkeypatch
):
    repository = Path(__file__).resolve().parents[2]
    blocks = re.findall(
        r"^```python\n(.*?)^```",
        (repository / page).read_text(),
        re.MULTILINE | re.DOTALL,
    )
    assert len(blocks) == (1 if "/tools/" in page else 3)
    monkeypatch.chdir(tmp_path)
    namespace = {"__name__": "__document_receiving__"}
    with puw.context(standard_units=units):
        policy = str(puw.get_unit(puw.standardize(puw.quantity(1, "nm"))))
        for block in blocks:
            exec(compile(block, page, "exec"), namespace)
        assert str(puw.get_unit(puw.standardize(puw.quantity(1, "nm")))) == policy
