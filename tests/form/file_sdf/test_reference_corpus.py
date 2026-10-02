"""Checking a committed synthetic ligand corpus without a runtime toolkit."""

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError

CORPUS = json.loads((Path(__file__).parent / "data/reference_corpus.json").read_text())


def _case_id(record):
    return f"{record['name']}-{record['version']}-{record['aromatic_encoding']}"


def _native_bonds(molsys):
    bonds = []
    for _, row in molsys.topology.bonds.iterrows():
        aromatic = row.get("is_aromatic", pd.NA)
        order = 4 if pd.notna(aromatic) and aromatic else int(row.bond_order)
        bonds.append([int(row.atom1_index), int(row.atom2_index), order])
    return sorted(bonds)


def _assert_assignments(molsys, record):
    assert molsys.topology.n_atoms == record["n_atoms"]
    assert molsys.topology.n_bonds == record["n_bonds"]
    assert molsys.topology.atoms.atom_type.tolist() == record["symbols"]
    assert molsys.topology.atoms.isotope.fillna(0).tolist() == record["isotopes"]
    assert msm.get(molsys, formal_charge=True) == record["formal_charges"]
    assert sum(record["formal_charges"]) == record["total_charge"]
    assert msm.get(molsys, n_unpaired_electrons=True) == record["radicals"]
    assert _native_bonds(molsys) == record["bonds"]


@pytest.fixture(params=CORPUS["records"], ids=_case_id)
def source(tmp_path, request):
    path = tmp_path / "source.sdf"
    path.write_text(request.param["sdf"], encoding="utf-8")
    return path, request.param


@pytest.mark.parametrize("output_version", ["V2000", "V3000"])
def test_corpus_preserves_declared_chemistry_and_all_hydrogens(
    source, tmp_path, output_version
):
    path, record = source
    molsys = msm.convert(path, to_form="molsysmt.MolSys")
    _assert_assignments(molsys, record)
    assert not msm.has_attribute(molsys, "n_implicit_hydrogens")
    output = tmp_path / "roundtrip.sdf"
    msm.convert(molsys, to_form=output, ctfile_version=output_version)
    restored = msm.convert(output, to_form="molsysmt.MolSys")
    _assert_assignments(restored, record)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="angstrom"),
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="angstrom"),
        atol=5e-5 if output_version == "V2000" else 1e-10,
        rtol=0,
    )


def test_corpus_selection_preserves_atom_assignments_and_induced_graph(source):
    path, record = source
    selection = list(range(0, record["n_atoms"], 2))
    remap = {old: new for new, old in enumerate(selection)}
    molsys = msm.convert(
        path, selection=list(reversed(selection)), to_form="molsysmt.MolSys"
    )
    assert molsys.topology.atoms.atom_id.tolist() == [str(i + 1) for i in selection]
    assert molsys.topology.atoms.atom_type.tolist() == [
        record["symbols"][i] for i in selection
    ]
    assert msm.get(molsys, formal_charge=True) == [
        record["formal_charges"][i] for i in selection
    ]
    assert _native_bonds(molsys) == sorted(
        [
            [remap[a], remap[b], order]
            for a, b, order in record["bonds"]
            if a in remap and b in remap
        ]
    )


@pytest.mark.parametrize(
    "record", CORPUS["unsupported_valence_records"], ids=lambda record: record["name"]
)
def test_corpus_valence_overrides_fail_instead_of_becoming_defaults(tmp_path, record):
    path = tmp_path / "unsupported.sdf"
    path.write_text(record["sdf"], encoding="utf-8")
    with pytest.raises(FormatError, match="atom property.*VAL"):
        msm.convert(path, to_form="molsysmt.MolSys")


@pytest.mark.skipif(
    importlib.util.find_spec("rdkit") is None, reason="optional live RDKit comparison"
)
def test_corpus_against_independent_live_reader(source, tmp_path):
    from rdkit import Chem

    path, record = source
    molsys = msm.convert(path, to_form="molsysmt.MolSys")
    output = tmp_path / "reference.sdf"
    msm.convert(molsys, to_form=output, ctfile_version="V3000")
    for filename in [path, output]:
        # Sanitization can change aromaticity. This comparison checks what the
        # CTAB declares; the adapter does not claim RDKit chemical perception.
        reference = Chem.SDMolSupplier(
            str(filename), sanitize=False, removeHs=False, strictParsing=True
        )[0]
        assert reference is not None
        assert [atom.GetSymbol() for atom in reference.GetAtoms()] == record["symbols"]
        assert [atom.GetFormalCharge() for atom in reference.GetAtoms()] == record[
            "formal_charges"
        ]
        assert [atom.GetIsotope() for atom in reference.GetAtoms()] == record[
            "isotopes"
        ]
        assert [
            atom.GetNumRadicalElectrons() for atom in reference.GetAtoms()
        ] == record["radicals"]
        reference_bonds = sorted(
            [
                [
                    *sorted((bond.GetBeginAtomIdx(), bond.GetEndAtomIdx())),
                    4 if bond.GetIsAromatic() else int(bond.GetBondTypeAsDouble()),
                ]
                for bond in reference.GetBonds()
            ]
        )
        assert reference_bonds == record["bonds"]
