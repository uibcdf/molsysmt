"""Qualifying declared peptide chemistry independently of its source fragments."""

import gzip
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

SIDE_CHARGES = {
    "ALA": 0,
    "ARG": 1,
    "ASN": 0,
    "ASP": -1,
    "ASH": 0,
    "CYS": 0,
    "CYM": -1,
    "GLN": 0,
    "GLU": -1,
    "GLH": 0,
    "GLY": 0,
    "HID": 0,
    "HIE": 0,
    "HIP": 1,
    "ILE": 0,
    "LEU": 0,
    "LYS": 1,
    "LYN": 0,
    "MET": 0,
    "PHE": 0,
    "PRO": 0,
    "SER": 0,
    "THR": 0,
    "TRP": 0,
    "TYR": 0,
    "VAL": 0,
}


def construct(names, **extra):
    return msm.physchem.get_peptide_chemical_template(
        names, n_terminal_state="ammonium", c_terminal_state="carboxylate", **extra
    )


@pytest.mark.parametrize("variant,expected_charge", SIDE_CHARGES.items())
@pytest.mark.parametrize("position", ["monomer", "middle"])
def test_declared_side_state_charge_and_closed_valence(
    variant, expected_charge, position
):
    # RDKit validates the assembled whole graph; fragment implicit ports must not
    # survive as extra hydrogens or radicals. This is an installed optional oracle.
    pytest.importorskip("rdkit")
    from rdkit import Chem

    result = construct([variant] if position == "monomer" else ["GLY", variant, "PRO"])
    template = result["template"]
    values = msm.get(template, element="atom", formal_charge=True)
    # Stored formal charges are integer multiples of e, not a session-unit quantity.
    charges = np.asarray(values, dtype=np.int64)
    assert result["report"]["units"]["formal_charge"] == "elementary_charge"
    assert charges.sum() == expected_charge
    molecule = msm.convert(template, to_form="rdkit.Mol")
    Chem.SanitizeMol(molecule)
    for _, bond in template.chemical_states._states[0].bonds.iterrows():
        oracle = molecule.GetBondBetweenAtoms(
            int(bond["atom1_index"]), int(bond["atom2_index"])
        )
        assert bool(bond["is_conjugated"]) == oracle.GetIsConjugated()
    assert all(atom.GetNumRadicalElectrons() == 0 for atom in molecule.GetAtoms())
    assert molecule.GetNumAtoms() == template.get_n_atoms()
    assert all(atom.GetNumImplicitHs() == 0 for atom in molecule.GetAtoms())
    assert (
        sum(atom.GetTotalNumHs() for atom in molecule.GetAtoms())
        == result["report"]["n_stored_hydrogens"]
    )
    assert (
        template.chemical_states._states[0].component_indices.tolist()
        == [0] * template.get_n_atoms()
    )


@pytest.mark.parametrize(
    "n_terminal,c_terminal,charge,hydrogens",
    [
        ("ammonium", "carboxylate", 0, 8),
        ("amine", "carboxylate", -1, 7),
        ("ammonium", "carboxylic_acid", 1, 9),
        ("amine", "carboxylic_acid", 0, 8),
    ],
)
def test_glycylglycine_terminal_choices(n_terminal, c_terminal, charge, hydrogens):
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = msm.physchem.get_peptide_chemical_template(
            ["GLY", "GLY"], n_terminal, c_terminal
        )
        template = result["template"]
        q = msm.get(template, element="atom", formal_charge=True)
        assert np.asarray(q, dtype=np.int64).sum() == charge
    assert template.get_n_atoms() == 9  # C4N2O3, independently of its eight stored H.
    assert result["report"]["n_stored_hydrogens"] == hydrogens
    assert result["report"]["peptide_bond_pairs"].tolist() == [[0, 7]]
    assert result["report"]["disulfide_bond_pairs"].shape == (0, 2)
    assert result["report"]["disulfide_bond_pairs"].dtype == np.int64
    assert result["template_provenance"]["stereochemistry"] == "unspecified"


def test_proline_and_declared_disulfide_inventory():
    peptide = construct(["GLY", "PRO", "GLY"])
    assert peptide["report"]["n_stored_hydrogens"] == 15  # C9H15N3O4.
    table = peptide["template"].topology.atoms
    nitrogen = np.flatnonzero(
        (table["group_index"] == 1) & (table["atom_name"] == "N")
    )[0]
    assert (
        peptide["template"]
        .chemical_states._states[0]
        .atom_attributes.at[nitrogen, "n_explicit_hydrogens"]
        == 0
    )
    assert construct(["PRO"])["report"]["n_stored_hydrogens"] == 9
    disulfide = construct(["CYX", "GLY", "CYX"], disulfide_group_pairs=[[2, 0]])
    assert disulfide["report"]["n_stored_hydrogens"] == 13  # C8H13N3O4S2.
    assert disulfide["report"]["disulfide_bond_pairs"].shape == (1, 2)
    molsys = disulfide["template"]
    sulfur = np.flatnonzero(molsys.topology.atoms["atom_type"] == "S")
    assert set(disulfide["report"]["disulfide_bond_pairs"][0]) == set(sulfur)
    pairs = msm.get(molsys, bonded_atom_pairs=True)
    assert tuple(sulfur) in {tuple(pair) for pair in pairs}


def test_template_composes_with_mapped_source_and_public_h5msm(tmp_path):
    from tests.physchem.test_chemical_template_connectivity import peptide_source

    source, _ = peptide_source()
    before = source.copy()
    bundle = construct(["GLY", "GLY"])
    mapping = np.column_stack((np.arange(9), [2, 3, 1, 0, 6, 7, 5, 4, 8]))
    kwargs = dict(
        template=bundle["template"],
        atom_correspondence=mapping,
        template_provenance=bundle["template_provenance"],
        connectivity_policy="complete_from_template",
    )
    prepared = msm.physchem.apply_chemical_template(source, **kwargs)[
        "molecular_system"
    ]
    attrs = prepared.chemical_states._states[0].atom_attributes
    assert attrs["formal_charge"].tolist() == [1, 0, 0, 0, 0, 0, 0, 0, -1]
    assert attrs["n_explicit_hydrogens"].tolist() == [3, 2, 0, 0, 1, 2, 0, 0, 0]
    assert len(prepared.chemical_states._states[0].bonds) == 8
    for field in ("coordinates", "box", "time"):
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(getattr(prepared.structures, field)),
            msm.pyunitwizard.get_value(getattr(before.structures, field)),
        )
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].bonds, before.chemical_states._states[0].bonds
    )
    for molsys, name in [(bundle["template"], "template"), (prepared, "prepared")]:
        path = tmp_path / f"{name}.h5msm"
        msm.convert(molsys, to_form=path)
        restored = msm.convert(path, to_form="molsysmt.MolSys")
        pd.testing.assert_frame_equal(
            restored.chemical_states._states[0].atom_attributes,
            molsys.chemical_states._states[0].atom_attributes,
        )
    # No OXT or heavy atom is silently added to a source during assignment.
    incomplete = msm.extract(source, selection=list(range(8)))
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.physchem.apply_chemical_template(incomplete, **kwargs)


@pytest.mark.parametrize(
    "names,n_terminal,c_terminal,links",
    [
        ([], "ammonium", "carboxylate", None),
        ("GLY", "ammonium", "carboxylate", None),
        (["HIS"], "ammonium", "carboxylate", None),
        (["MSE"], "ammonium", "carboxylate", None),
        (["GLY"], None, "carboxylate", None),
        (["GLY"], "ammonium", "auto", None),
        (["CYX", "CYX"], "ammonium", "carboxylate", None),
        (["CYS", "CYS"], "ammonium", "carboxylate", [[0, 1]]),
        (["CYX", "CYX"], "ammonium", "carboxylate", [[0, 2]]),
        (["CYX", "CYX"], "ammonium", "carboxylate", [[0, 0]]),
        (["CYX", "CYX"], "ammonium", "carboxylate", [[0, 1], [1, 0]]),
        (["CYX", "CYX"], "ammonium", "carboxylate", [[False, True]]),
        (["CYX", "CYX"], "ammonium", "carboxylate", [[0.0, 1.0]]),
        (np.array("GLY"), "ammonium", "carboxylate", None),
    ],
)
def test_ambiguous_states_and_invalid_ports_fail(names, n_terminal, c_terminal, links):
    with pytest.raises(ArgumentError):
        msm.physchem.get_peptide_chemical_template(
            names, n_terminal, c_terminal, disulfide_group_pairs=links
        )


def test_recuration_from_original_bytes_preserves_chemistry_and_producer_identity():
    pytest.importorskip("rdkit")
    from rdkit import rdBase

    path = Path("molsysmt/data/_make/make_peptide_chemical_templates.py")
    spec = importlib.util.spec_from_file_location("peptide_curation", path)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    regenerated = generator.curate()
    stored = json.loads(generator.OUTPUT.read_text())
    assert regenerated["residues"] == stored["residues"]
    assert regenerated["source"] == stored["source"]
    assert (
        regenerated["units"]
        == stored["units"]
        == {"formal_charge": "elementary_charge"}
    )
    assert regenerated["curation"] == dict(
        stored["curation"], rdkit_version=rdBase.rdkitVersion
    )
    assert stored["curation"]["rdkit_version"] == "2025.09.5"
    import hashlib

    assert (
        hashlib.sha256(gzip.decompress(generator.SOURCE.read_bytes())).hexdigest()
        == generator.SOURCE_SHA256
    )


def test_constructed_outputs_do_not_mutate_cached_reference_data():
    first = construct(["GLY"])
    original = first["template_provenance"]["checksum"]
    first["template"].chemical_states._states[0].set_atom_attribute(
        "formal_charge", [5] * 5
    )
    first["template_provenance"]["source"]["sha256"] = "changed"
    second = construct(["GLY"])
    assert second["template_provenance"]["checksum"] == original
    assert (
        second["template_provenance"]["source"]["sha256"]
        == "535dc75a2cc5db579a3114090c9ab1273892c556cb7cc1a850ce2c4cd57c7cde"
    )
    assert (
        second["template"]
        .chemical_states._states[0]
        .atom_attributes["formal_charge"]
        .sum()
        == 0
    )


def test_factory_needs_neither_rdkit_nor_meeko_nor_ackredit():
    script = """
import importlib.abc, sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit','meeko','ackredit'}:
            raise ModuleNotFoundError(fullname)
sys.meta_path.insert(0,Absent())
import molsysmt as msm
result = msm.physchem.get_peptide_chemical_template(['GLY','HID','GLY'],
    n_terminal_state='ammonium',c_terminal_state='carboxylate')
assert result['report']['status'] == 'constructed'
assert result['report']['n_indexed_hydrogens'] == 0
assert result['report']['attribution']['items'][1]['type'] == 'dataset'
assert not any(name in sys.modules for name in ('rdkit','meeko','ackredit'))
"""
    run = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert run.returncode == 0, run.stderr


def test_real_attribution_records_data_without_executing_the_data_provider():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("peptide chemistry"):
        with ackredit.scope("consumer.prepare"):
            first = construct(["HID"])
            second = construct(["HIE"])
        items = first["report"]["attribution"]["items"]
        assert items == second["report"]["attribution"]["items"]
        assert items[0]["roles"] == ["executed_software"]
        assert items[1]["roles"] == ["chemical_reference_data"]
        assert set(item["id"] for item in items).issubset(ackredit.get_used_items())
        assert (
            "molsysmt.physchem.get_peptide_chemical_template"
            in ackredit.current_session().usage_tree["consumer.prepare"]["children"]
        )
    with ackredit.session("failed peptide construction"):
        with pytest.raises(ArgumentError):
            construct(["HIS"])
        assert not ackredit.get_used_items()


def test_histidine_states_preserve_distinct_ring_hydrogen_and_charge_choices():
    expected = {"HID": (1, 0, 0), "HIE": (0, 1, 0), "HIP": (1, 1, 1)}
    for variant, (nd1_h, ne2_h, charge) in expected.items():
        result = construct([variant])
        template = result["template"]
        by_name = dict(
            zip(
                template.topology.atoms["atom_name"],
                template.chemical_states._states[0].atom_attributes[
                    "n_explicit_hydrogens"
                ],
            )
        )
        assert (by_name["ND1"], by_name["NE2"]) == (nd1_h, ne2_h)
        assert (
            template.chemical_states._states[0].atom_attributes["formal_charge"].sum()
            == charge
        )
        rings = msm.physchem.get_aromatic_rings(template)
        assert rings["atom_offsets"].tolist() == [0, 5]


def test_fragment_reader_rejects_wrong_charge_units(monkeypatch, tmp_path):
    from molsysmt._private import peptide_chemical_template as implementation

    payload = json.loads(
        Path(
            "molsysmt/data/databases/peptide_templates/residue_fragments.json"
        ).read_text()
    )
    payload["units"]["formal_charge"] = "coulomb"
    path = tmp_path / "databases/peptide_templates/residue_fragments.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(payload))
    implementation._fragments.cache_clear()
    monkeypatch.setattr(implementation, "files", lambda package: tmp_path)
    try:
        with pytest.raises(StructuralInconsistencyError, match="formal-charge unit"):
            construct(["GLY"])
    finally:
        implementation._fragments.cache_clear()


@pytest.mark.parametrize(
    "names,pairs", [(["GLY"], None), (["CYX", "GLY", "CYX"], [[2, 0]])]
)
def test_trusted_delegation_preserves_valid_default_and_list_inputs(names, pairs):
    kwargs = dict(
        residue_names=names,
        n_terminal_state="ammonium",
        c_terminal_state="carboxylate",
        disulfide_group_pairs=pairs,
    )
    validated = msm.physchem.get_peptide_chemical_template(**kwargs)
    delegated = msm.physchem.get_peptide_chemical_template(
        **kwargs, skip_digestion=True
    )
    assert delegated["template_provenance"] == validated["template_provenance"]
    pd.testing.assert_frame_equal(
        delegated["template"].chemical_states._states[0].bonds,
        validated["template"].chemical_states._states[0].bonds,
    )
