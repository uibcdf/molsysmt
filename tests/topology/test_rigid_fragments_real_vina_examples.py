"""Checking chosen source-bond cuts against published Vina ligand fragments."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form.file_pdbqt import get_torsion_tree

CASES = ["1iep", "1s63", "5x72-p59", "5x72-p69"]


@pytest.mark.parametrize("case_name", CASES)
def test_explicit_fragments_match_real_trees_with_declared_atom_projection(case_name):
    Chem = pytest.importorskip("rdkit.Chem")
    root = Path(__file__).parents[1] / "form/data/vina_examples"
    records = json.loads((root / "manifest.json").read_text())["records"]
    record = next(item for item in records if item["name"] == case_name)
    for file in record["files"].values():
        assert (
            hashlib.sha256((root / file["filename"]).read_bytes()).hexdigest()
            == file["sha256"]
        )
    sdf_path = root / record["files"]["sdf"]["filename"]
    pdbqt_path = root / record["files"]["pdbqt"]["filename"]
    # This is an independent, explicitly chosen source route, not a fallback
    # hidden in the SDF adapter for currently unsupported CTAB semantics.
    source = Chem.SDMolSupplier(str(sdf_path), removeHs=False, strictParsing=True)[0]
    assert source is not None
    native = msm.convert(source, to_form="molsysmt.MolSys")
    prepared = msm.convert(
        pdbqt_path, to_form="molsysmt.MolSys", discard_torsion_tree=True
    )
    observed = msm.pyunitwizard.get_value(
        prepared.structures.coordinates, to_unit="angstrom"
    )[0]
    source_xyz = np.asarray(source.GetConformer().GetPositions())
    source_symbols = np.asarray([atom.GetSymbol() for atom in source.GetAtoms()])
    observed_symbols = prepared.topology.atoms.atom_type.to_numpy()
    projected = np.full(len(observed), -1, dtype=np.int64)
    for index, (symbol, xyz) in enumerate(zip(observed_symbols, observed)):
        matches = np.flatnonzero(
            (source_symbols == symbol)
            & (np.linalg.norm(source_xyz - xyz, axis=1) <= 0.002)
        )
        if matches.size == 0:
            assert case_name == "1s63" and symbol == "H"
            continue
        assert matches.size == 1, (
            "The pinned coordinate projection must be unambiguous."
        )
        projected[index] = matches[0]
    assert np.count_nonzero(projected < 0) == (1 if case_name == "1s63" else 0)
    retained = projected[projected >= 0]
    assert np.unique(retained).size == retained.size

    tree = get_torsion_tree(pdbqt_path)
    selected_pairs = projected[tree["branch_atom_pairs"]]
    assert (selected_pairs >= 0).all()
    source_pairs = native.topology.bonds[["atom1_index", "atom2_index"]].to_numpy()
    pair_to_index = {tuple(sorted(pair)): i for i, pair in enumerate(source_pairs)}
    bond_indices = [pair_to_index[tuple(sorted(pair))] for pair in selected_pairs]
    before = msm.convert(
        native.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    partition = msm.topology.get_rigid_fragments(native, bond_indices=bond_indices)
    np.testing.assert_array_equal(
        partition["bonded_atom_pairs"], source_pairs[sorted(bond_indices)]
    )
    members = partition["fragment_atom_indices"]
    offsets = partition["fragment_offsets"]
    source_fragments = {
        frozenset(members[start:end]) & frozenset(retained)
        for start, end in zip(offsets[:-1], offsets[1:])
    }
    expected_members = projected[tree["fragment_atom_indices"]]
    expected_offsets = tree["fragment_offsets"]
    expected_fragments = {
        frozenset(index for index in expected_members[start:end] if index >= 0)
        for start, end in zip(expected_offsets[:-1], expected_offsets[1:])
    }
    assert source_fragments == expected_fragments
    assert len(source_fragments) == record["n_branches"] + 1
    if case_name == "1s63":
        assert frozenset((26, 27)) in {frozenset(pair) for pair in selected_pairs}
    np.testing.assert_equal(
        msm.convert(
            native.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
        before,
    )
