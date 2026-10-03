"""Checking native PDBQT fidelity on unmodified, pinned Vina preparations."""

import copy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.form.file_pdbqt import get_torsion_tree

CASES = ["1iep", "1s63", "5x72-p59", "5x72-p69", "1iep-receptor"]


@pytest.fixture(params=CASES, ids=CASES)
def pdbqt_case(vina_reference_corpus, request):
    root, records = vina_reference_corpus
    record = records[request.param]
    return root / record["files"]["pdbqt"]["filename"], record


def _declared_atom_fields(path):
    lines = [
        line
        for line in path.read_text().splitlines()
        if line.startswith(("ATOM  ", "HETATM"))
    ]
    return {
        "atom_id": [str(int(line[6:11])) for line in lines],
        "atom_ff_type": [line[77:].strip() for line in lines],
        "partial_charge": np.asarray([float(line[68:76]) for line in lines]),
        "coordinates": np.asarray(
            [
                [float(line[start : start + 8]) for start in (30, 38, 46)]
                for line in lines
            ]
        ),
    }


def _tree_serials(tree):
    if tree is None:
        return [], []
    atom_ids = tree["atom_ids"].astype(int)
    branches = atom_ids[tree["branch_atom_pairs"]].tolist()
    members = atom_ids[tree["fragment_atom_indices"]]
    fragments = [
        members[start:end].tolist()
        for start, end in zip(
            tree["fragment_offsets"][:-1], tree["fragment_offsets"][1:]
        )
    ]
    return branches, fragments


def test_real_getters_preserve_declared_fields_and_partial_chemistry(pdbqt_case):
    path, record = pdbqt_case
    declared = _declared_atom_fields(path)
    values = msm.get(
        path,
        element="atom",
        atom_id=True,
        atom_type=True,
        atom_ff_type=True,
        partial_charge=True,
        coordinates=True,
        output_type="dictionary",
    )
    assert values["atom_id"] == declared["atom_id"]
    np.testing.assert_array_equal(values["atom_ff_type"], declared["atom_ff_type"])
    np.testing.assert_array_equal(values["partial_charge"], declared["partial_charge"])
    assert values["coordinates"].shape == (1, record["pdbqt_n_atoms"], 3)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(values["coordinates"], to_unit="angstrom")[0],
        declared["coordinates"],
        atol=1e-10,
        rtol=0,
    )
    assert values["atom_type"] == msm.element.atom.get_atom_type_from_atom_ff_type(
        declared["atom_ff_type"], typing_scheme="autodock4"
    )
    native = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    assert native.topology.n_atoms == record["pdbqt_n_atoms"]
    assert native.topology.n_bonds == record["n_branches"]
    assert msm.get(native, connectivity_completeness=True) == ["partial"]
    for attribute in ("bond_order", "formal_charge", "atom_is_aromatic"):
        assert not msm.has_attribute(native, attribute)
    tree = get_torsion_tree(path)
    branches, fragments = _tree_serials(tree)
    assert branches == record["branch_serial_pairs"]
    assert fragments == record["fragment_serials"]
    if tree is not None:
        assert tree["torsdof"] == record["torsdof"]


@pytest.mark.parametrize("length_unit", ["nm", "pm"])
def test_real_native_roundtrip_preserves_atoms_tree_charges_and_source(
    pdbqt_case, tmp_path, length_unit
):
    path, record = pdbqt_case
    declared = _declared_atom_fields(path)
    with msm.pyunitwizard.context(standard_units=[length_unit, "fs"]):
        native = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
        tree = get_torsion_tree(path)
        saved_tree = copy.deepcopy(tree)
        saved_atoms = native.topology.atoms.copy(deep=True)
        saved_mechanics = native.molecular_mechanics.atoms_ff.copy(deep=True)
        saved_coords = msm.pyunitwizard.get_value(native.structures.coordinates).copy()
        output = tmp_path / "roundtrip.pdbqt"
        msm.convert(
            native, to_form=output, typing_scheme="autodock4", torsion_tree=tree
        )
        restored = _declared_atom_fields(output)
        # Tree traversal may reorder atoms. Serial IDs align the observed fields.
        assert set(restored["atom_id"]) == set(declared["atom_id"])
        index = {serial: i for i, serial in enumerate(restored["atom_id"])}
        alignment = [index[serial] for serial in declared["atom_id"]]
        np.testing.assert_array_equal(
            np.asarray(restored["atom_ff_type"])[alignment], declared["atom_ff_type"]
        )
        np.testing.assert_allclose(
            restored["coordinates"][alignment],
            declared["coordinates"],
            atol=1e-10,
            rtol=0,
        )
        np.testing.assert_array_equal(
            restored["partial_charge"][alignment], declared["partial_charge"]
        )
        assert _tree_serials(get_torsion_tree(output)) == (
            record["branch_serial_pairs"],
            record["fragment_serials"],
        )
        if tree is not None:
            assert get_torsion_tree(output)["torsdof"] == record["torsdof"]
            for name, value in tree.items():
                np.testing.assert_equal(value, saved_tree[name])
        pd.testing.assert_frame_equal(native.topology.atoms, saved_atoms)
        pd.testing.assert_frame_equal(
            native.molecular_mechanics.atoms_ff, saved_mechanics
        )
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(native.structures.coordinates), saved_coords
        )


def test_real_identity_file_string_file_preserves_original_bytes(pdbqt_case, tmp_path):
    path, _ = pdbqt_case
    text, report = msm.convert(
        path, to_form="string:pdbqt_text", strict=True, return_report=True
    )
    assert report.is_exhaustive and not report.is_lossy
    output = tmp_path / "copy.pdbqt"
    msm.convert(text, to_form=output, strict=True)
    assert output.read_bytes() == path.read_bytes()


def test_real_source_and_native_output_against_mdanalysis(pdbqt_case, tmp_path):
    mda = pytest.importorskip("MDAnalysis")
    path, _ = pdbqt_case
    native = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    output = tmp_path / "independent.pdbqt"
    msm.convert(
        native,
        to_form=output,
        typing_scheme="autodock4",
        torsion_tree=get_torsion_tree(path),
    )
    for filename in (path, output):
        reference = mda.Universe(str(filename), to_guess=())
        declared = _declared_atom_fields(filename)
        np.testing.assert_array_equal(
            reference.atoms.ids.astype(str), declared["atom_id"]
        )
        np.testing.assert_array_equal(reference.atoms.types, declared["atom_ff_type"])
        np.testing.assert_allclose(
            reference.atoms.charges, declared["partial_charge"], atol=1e-7, rtol=0
        )
        np.testing.assert_allclose(
            reference.atoms.positions, declared["coordinates"], atol=2e-5, rtol=0
        )


def test_real_native_output_is_accepted_by_vina_parser(pdbqt_case, tmp_path):
    vina = pytest.importorskip("vina")
    path, record = pdbqt_case
    native = msm.convert(path, to_form="molsysmt.MolSys", discard_torsion_tree=True)
    tree = get_torsion_tree(path)
    engine = vina.Vina(cpu=1, verbosity=0)
    if record["name"] == "1iep-receptor":
        output = tmp_path / "receptor.pdbqt"
        msm.convert(native, to_form=output, typing_scheme="autodock4")
        engine.set_receptor(str(output))
    else:
        text = msm.convert(
            native,
            to_form="string:pdbqt_text",
            typing_scheme="autodock4",
            torsion_tree=tree,
        )
        engine.set_ligand_from_string(text[len("pdbqt_text:") :])
