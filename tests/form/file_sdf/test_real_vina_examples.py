"""Checking supported stereo and deliberate limits on original Vina SDF inputs."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError

LIGANDS = ["1iep", "1s63", "5x72-p59", "5x72-p69"]
STEREO_CASES = ["5x72-p59", "5x72-p69"]


@pytest.mark.parametrize("case_name", LIGANDS)
def test_original_native_profile_rejects_unrepresented_source_semantics(
    vina_reference_corpus, case_name
):
    root, records = vina_reference_corpus
    record = records[case_name]
    path = root / record["files"]["sdf"]["filename"]
    expected = {
        "unsupported_valence": "atom flag on atom 32",
        "unsupported_versionless": "explicitly versioned",
        "requires_explicit_stereo_engine": "counts flag",
    }[record["sdf_status"]]
    with pytest.raises(FormatError, match=expected):
        msm.convert(path, to_form="molsysmt.MolSys", discard_properties=True)


@pytest.mark.parametrize("case_name", ["1iep", "1s63"])
def test_explicit_stereo_provider_does_not_hide_other_format_limits(
    vina_reference_corpus, case_name
):
    root, records = vina_reference_corpus
    path = root / records[case_name]["files"]["sdf"]["filename"]
    expected = "atom flag on atom 32" if case_name == "1iep" else "explicitly versioned"
    with pytest.raises(FormatError, match=expected):
        msm.convert(
            path,
            to_form="molsysmt.MolSys",
            discard_properties=True,
            stereo_engine="rdkit",
        )


@pytest.mark.parametrize("case_name", LIGANDS)
def test_original_sdf_identity_copies_keep_unsupported_flags_and_properties(
    vina_reference_corpus, case_name, tmp_path
):
    root, records = vina_reference_corpus
    path = root / records[case_name]["files"]["sdf"]["filename"]
    output = tmp_path / "copy.sdf"
    msm.convert(path, to_form=output, strict=True)
    assert output.read_bytes() == path.read_bytes()


@pytest.mark.parametrize("case_name", STEREO_CASES)
@pytest.mark.parametrize("version", ["V2000", "V3000"])
def test_real_stereoisomers_preserve_chemistry_coordinates_and_source(
    vina_reference_corpus, case_name, version, tmp_path
):
    Chem = pytest.importorskip("rdkit.Chem")
    rdCIPLabeler = pytest.importorskip("rdkit.Chem.rdCIPLabeler")
    root, records = vina_reference_corpus
    record = records[case_name]
    path = root / record["files"]["sdf"]["filename"]
    reference = Chem.SDMolSupplier(str(path), removeHs=False, strictParsing=True)[0]
    assert reference is not None
    rdCIPLabeler.AssignCIPLabels(reference)
    expected_labels = {
        atom.GetIdx(): atom.GetProp("_CIPCode")
        for atom in reference.GetAtoms()
        if atom.HasProp("_CIPCode")
    }
    assert expected_labels == {
        int(index): label for index, label in record["sdf_atom_stereochemistry"].items()
    }
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        native = msm.convert(
            path,
            to_form="molsysmt.MolSys",
            discard_properties=True,
            stereo_engine="rdkit",
        )
        assert native.topology.n_atoms == record["sdf_n_atoms"]
        assert native.topology.n_bonds == record["sdf_n_bonds"]
        assert native.topology.atoms.atom_type.tolist() == [
            atom.GetSymbol() for atom in reference.GetAtoms()
        ]
        assert msm.get(native, formal_charge=True) == [
            atom.GetFormalCharge() for atom in reference.GetAtoms()
        ]
        assert (
            sum(msm.get(native, formal_charge=True)) == record["sdf_net_formal_charge"]
        )
        assert msm.get(native, connectivity_completeness=True) == ["complete"]
        assert not msm.has_attribute(native, "partial_charge")
        assert not msm.has_attribute(native, "atom_ff_type")
        expected_coordinates = np.asarray(reference.GetConformer().GetPositions())
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                native.structures.coordinates, to_unit="angstrom"
            )[0],
            expected_coordinates,
            atol=1e-10,
            rtol=0,
        )
        for index, label in expected_labels.items():
            assert msm.physchem.get_cip_stereochemistry(native, selection=[index])[
                "atom_stereochemistry"
            ].tolist() == [label]
        before_atoms = native.topology.atoms.copy(deep=True)
        before_bonds = native.topology.bonds.copy(deep=True)
        before_coordinates = msm.pyunitwizard.get_value(
            native.structures.coordinates
        ).copy()
        output = tmp_path / "roundtrip.sdf"
        msm.convert(
            native, to_form=output, ctfile_version=version, stereo_engine="rdkit"
        )
        restored = msm.convert(output, to_form="molsysmt.MolSys", stereo_engine="rdkit")
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(
                restored.structures.coordinates, to_unit="angstrom"
            )[0],
            expected_coordinates,
            atol=5.1e-5,
            rtol=0,
        )
        assert restored.topology.n_atoms == record["sdf_n_atoms"]
        assert restored.topology.n_bonds == record["sdf_n_bonds"]
        output_reference = Chem.SDMolSupplier(
            str(output), removeHs=False, strictParsing=True
        )[0]
        assert output_reference is not None
        assert Chem.MolToSmiles(
            output_reference, isomericSmiles=True
        ) == Chem.MolToSmiles(reference, isomericSmiles=True)
        labels = msm.physchem.get_cip_stereochemistry(restored)["atom_stereochemistry"]
        assert {
            i: value for i, value in enumerate(labels) if value is not None
        } == expected_labels
        pd.testing.assert_frame_equal(native.topology.atoms, before_atoms)
        pd.testing.assert_frame_equal(native.topology.bonds, before_bonds)
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(native.structures.coordinates),
            before_coordinates,
        )


def test_real_pair_has_same_graph_and_distinct_cip_labels(vina_reference_corpus):
    Chem = pytest.importorskip("rdkit.Chem")
    root, records = vina_reference_corpus
    sources = [
        root / records[name]["files"]["sdf"]["filename"] for name in STEREO_CASES
    ]
    systems = [
        msm.convert(
            path,
            to_form="molsysmt.MolSys",
            stereo_engine="rdkit",
            discard_properties=True,
        )
        for path in sources
    ]
    # Source bond IDs and aromatic Kekule encodings differ. Independently
    # normalize for this equivalence check; native source assignments stay intact.
    pairs = [
        system.topology.bonds[["atom1_index", "atom2_index"]] for system in systems
    ]
    pd.testing.assert_frame_equal(*pairs)
    molecules = [msm.convert(system, to_form="rdkit.Mol") for system in systems]
    assert Chem.MolToSmiles(molecules[0], isomericSmiles=False) == Chem.MolToSmiles(
        molecules[1], isomericSmiles=False
    )
    assert [
        msm.physchem.get_cip_stereochemistry(system, selection=[7])[
            "atom_stereochemistry"
        ].tolist()
        for system in systems
    ] == [["R"], ["S"]]


def test_original_unsupported_chemistry_is_not_a_malformed_reference(
    vina_reference_corpus,
):
    Chem = pytest.importorskip("rdkit.Chem")
    root, records = vina_reference_corpus
    for name in ("1iep", "1s63"):
        record = records[name]
        path = root / record["files"]["sdf"]["filename"]
        reference = Chem.SDMolSupplier(str(path), removeHs=False, strictParsing=True)[0]
        assert reference is not None
        assert reference.GetNumAtoms() == record["sdf_n_atoms"]
        assert reference.GetNumBonds() == record["sdf_n_bonds"]
        assert (
            sum(atom.GetFormalCharge() for atom in reference.GetAtoms())
            == record["sdf_net_formal_charge"]
        )
    one_iep = (
        (root / records["1iep"]["files"]["sdf"]["filename"]).read_text().splitlines()
    )
    assert int(one_iep[4 + 31][48:51]) == 4
    assert "M  CHG  1  32   1" in one_iep
    one_s63 = (
        (root / records["1s63"]["files"]["sdf"]["filename"]).read_text().splitlines()
    )
    assert "V2000" not in one_s63[3] and "V3000" not in one_s63[3]
