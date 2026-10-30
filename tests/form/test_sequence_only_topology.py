"""Convert declared sequence groups without inventing atomic representation."""

import subprocess
import sys

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError


@pytest.mark.parametrize(
    "source", ["AGW", "amino_acids_1:AGW", "AlaGlyTrp", "amino_acids_3:AlaGlyTrp"]
)
@pytest.mark.parametrize("target", ["molsysmt.Topology", "molsysmt.MolSys"])
def test_public_sequences_preserve_groups_without_atomic_or_coordinate_rows(
    source, target
):
    converted = msm.convert(source, to_form=target)
    topology = converted.topology if target.endswith("MolSys") else converted
    assert topology.n_atoms == 0
    assert not hasattr(topology, "bonds")
    assert topology.n_groups == 3
    assert topology.groups.group_name.tolist() == ["ALA", "GLY", "TRP"]
    assert topology.groups.group_type.tolist() == ["amino acid"] * 3
    assert topology.groups.molecule_index.tolist() == [0, 0, 0]
    assert topology.n_molecules == topology.n_chains == topology.n_entities == 1
    assert topology.molecules.molecule_type.tolist() == ["peptide"]
    assert not msm.has_attribute(topology, "atom_name")
    assert msm.get(topology, connectivity_completeness=True) is None
    assert msm.get(topology, component_completeness=True) is None
    if target.endswith("MolSys"):
        assert converted.chemical_states is None
        assert converted.structures.n_structures == 0
        assert converted.structures.coordinates is None


def test_three_letter_caps_and_declared_group_order_are_not_lost():
    topology = msm.convert("amino_acids_3:AceAlaGlyNme", to_form="molsysmt.Topology")
    assert topology.groups.group_name.tolist() == ["ACE", "ALA", "GLY", "NME"]
    assert topology.groups.group_type.tolist() == [
        "terminal capping",
        "amino acid",
        "amino acid",
        "terminal capping",
    ]
    assert topology.n_atoms == 0
    assert not hasattr(topology, "bonds")


@pytest.mark.parametrize("width", [1, 3])
def test_selected_group_positions_preserve_order_and_repetitions(width):
    source = "amino_acids_1:AGS" if width == 1 else "amino_acids_3:AlaGlySer"
    topology = msm.convert(source, to_form="molsysmt.Topology", selection=[2, 0, 2])
    assert topology.groups.group_name.tolist() == ["SER", "ALA", "SER"]
    assert topology.n_atoms == 0


@pytest.mark.parametrize("width", [1, 3])
@pytest.mark.parametrize("bad", [[True], [0.5], [-1], [4], [[0, 1]]])
def test_direct_group_selection_is_strict(width, bad):
    from importlib import import_module

    converter = import_module(
        f"molsysmt.form.string_amino_acids_{width}.to_molsysmt_Topology"
    ).to_molsysmt_Topology
    with pytest.raises(ArgumentError):
        converter(
            "amino_acids_1:AG" if width == 1 else "amino_acids_3:AlaGly",
            group_indices=bad,
        )


@pytest.mark.parametrize(
    "source",
    [
        "amino_acids_1:A?",
        "amino_acids_1:A*",
        "amino_acids_1:A-G",
        "amino_acids_3:AlaGl",
        "amino_acids_3:Ala???",
    ],
)
def test_uninterpretable_sequence_does_not_create_placeholder_groups(source):
    with pytest.raises(ArgumentError):
        msm.convert(source, to_form="molsysmt.Topology")


def test_extended_native_code_table_retains_ambiguity_and_rare_amino_acids():
    topology = msm.convert("amino_acids_1:BXZJUO", to_form="molsysmt.Topology")
    assert topology.groups.group_name.tolist() == [
        "ASX",
        "XAA",
        "GLX",
        "XLE",
        "SEC",
        "PYL",
    ]
    assert topology.groups.group_type.tolist() == ["amino acid"] * 6
    assert topology.n_atoms == 0
    assert not hasattr(topology, "bonds")


@pytest.mark.parametrize("source", ["amino_acids_1:", "amino_acids_3:"])
def test_empty_declared_sequence_has_no_synthetic_members(source):
    topology = msm.convert(source, to_form="molsysmt.Topology")
    assert topology.n_atoms == topology.n_groups == 0
    assert not hasattr(topology, "bonds")


def test_fasta_records_are_distinct_occurrences_without_fake_ca(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "records.fasta"
    original = (
        b">same complete header\nAG\n>other\nW\n>same complete header\nAG\n>empty\n"
    )
    path.write_bytes(original)
    topology = msm.convert(str(path), to_form="molsysmt.Topology")
    assert topology.n_atoms == 0
    assert not hasattr(topology, "bonds")
    assert topology.n_groups == 5
    assert topology.n_molecules == topology.n_chains == topology.n_entities == 4
    assert topology.groups.group_name.tolist() == ["ALA", "GLY", "TRP", "ALA", "GLY"]
    assert topology.groups.molecule_index.tolist() == [0, 0, 1, 2, 2]
    assert topology.chains.chain_id.tolist() == ["A", "B", "C", "D"]
    assert topology.entities.entity_name.tolist() == [
        "same complete header",
        "other",
        "same complete header",
        "empty",
    ]
    assert path.read_bytes() == original


def test_supported_copy_and_h5msm_keep_represented_tables(tmp_path):
    topology = msm.convert("amino_acids_3:AceAlaGlyNme", to_form="molsysmt.Topology")
    copy = topology.copy()
    assert copy.n_atoms == 0 and copy.groups.equals(topology.groups)
    path = str(tmp_path / "sequence.h5msm")
    msm.convert(topology, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert restored.topology.n_atoms == restored.structures.n_structures == 0
    assert restored.topology.groups.group_name.tolist() == ["ACE", "ALA", "GLY", "NME"]
    assert restored.topology.groups.molecule_index.tolist() == [0, 0, 0, 0]


def test_native_string_conversion_has_no_biopython_dependency():
    script = """
import sys
from importlib.abc import MetaPathFinder
class DenyBio(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "Bio" or fullname.startswith("Bio."):
            raise AssertionError("Sequence topology attempted a Bio import")
sys.meta_path.insert(0, DenyBio())
import molsysmt as msm
for source in ("amino_acids_1:AG", "amino_acids_3:AceAlaGlyNme"):
    molsys = msm.convert(source, to_form="molsysmt.MolSys")
    assert molsys.topology.n_atoms == 0
    assert molsys.topology.n_groups in (2,4)
assert not any(x == "Bio" or x.startswith("Bio.") for x in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("source", ["amino_acids_1:AG", "amino_acids_3:AlaGly"])
@pytest.mark.parametrize("target", ["molsysmt.Topology", "molsysmt.MolSys"])
def test_public_sequence_conversion_rejects_coordinate_structure_requests(
    source, target
):
    with pytest.raises(NotWithThisFormError):
        msm.convert(source, to_form=target, structure_indices=[0])


def test_fasta_public_molsys_has_multiple_molecules_and_zero_structures(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "multiple.fasta"
    path.write_text(">first\nAG\n>second\nW\n", encoding="utf-8")
    molsys = msm.convert(str(path), to_form="molsysmt.MolSys")
    assert molsys.topology.n_molecules == 2
    assert molsys.topology.n_atoms == molsys.structures.n_structures == 0
    assert molsys.topology.groups.molecule_index.tolist() == [0, 0, 1]
    with pytest.raises(NotWithThisFormError):
        msm.convert(str(path), to_form="molsysmt.MolSys", structure_indices=[0])
    from molsysmt.form.file_fasta.to_molsysmt_Topology import to_molsysmt_Topology

    with pytest.raises(ArgumentError):
        to_molsysmt_Topology(str(path), atom_indices=[0])


def test_unknown_three_letter_group_remains_declared_not_fabricated():
    topology = msm.convert("amino_acids_3:AlaJjjGly", to_form="molsysmt.Topology")
    assert topology.groups.group_name.tolist() == ["ALA", "JJJ", "GLY"]
    assert topology.groups.group_type.tolist() == [
        "amino acid",
        "unknown",
        "amino acid",
    ]
    assert topology.n_atoms == 0


@pytest.mark.parametrize("text,count", [("", 0), (">empty\n", 1)])
def test_empty_fasta_inventory_and_declared_empty_occurrence_are_distinct(
    tmp_path, text, count
):
    pytest.importorskip("Bio")
    path = tmp_path / "empty.fasta"
    path.write_text(text, encoding="utf-8")
    molsys = msm.convert(str(path), to_form="molsysmt.MolSys")
    assert molsys.topology.n_atoms == molsys.topology.n_groups == 0
    assert molsys.topology.n_molecules == molsys.topology.n_chains == count
    assert molsys.structures.n_structures == 0
