"""Checking sequence identity against the groups that actually supply letters."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Topology


def molecular_groups(names, types):
    topology = Topology(
        n_atoms=len(names), n_groups=len(names), n_chains=1, n_molecules=1, n_entities=1
    )
    topology.atoms["atom_id"] = [str(10 + i) for i in range(len(names))]
    topology.atoms["atom_name"] = ["CA"] * len(names)
    topology.atoms["atom_type"] = ["C"] * len(names)
    topology.atoms["group_index"] = np.arange(len(names))
    topology.atoms["chain_index"] = [0] * len(names)
    topology.groups["group_id"] = [str(100 + i) for i in range(len(names))]
    topology.groups["group_name"] = names
    topology.groups["group_type"] = types
    topology.groups["molecule_index"] = [0] * len(names)
    topology.molecules["entity_index"] = [0]
    return MolSys._from_partial_domains(
        topology=topology, chemical_states=topology._chemical_states_domain
    )


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Topology", "file:h5msm"])
def test_capped_mixed_groups_return_exact_source_correspondence(form, tmp_path):
    source = molecular_groups(
        ["HOH", "ACE", "ALA", "NA", "GLY", "NME", "LIG"],
        [
            "water",
            "terminal capping",
            "amino acid",
            "ion",
            "amino acid",
            "terminal capping",
            "small molecule",
        ],
    )
    if form == "molsysmt.Topology":
        source = source.topology
    elif form == "file:h5msm":
        path = str(tmp_path / "inventory.h5msm")
        msm.convert(source, to_form=path)
        source = path
    identity, groups, reference = msm.topology.get_sequence_identity(
        source, reference_molecular_system=source
    )
    assert identity == 100.0
    assert groups == [2, 4]
    assert reference == [2, 4]


def test_capped_bundled_pentalanine_is_identical_to_itself():
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"], structure_indices=[0]
    )
    result = msm.topology.get_sequence_identity(
        source, reference_molecular_system=source
    )
    assert result == (100.0, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5])


def test_gaps_keep_independent_source_indices_and_query_denominator():
    query = molecular_groups(
        ["ACE", "ALA", "HOH", "GLY", "SER", "NME"],
        [
            "terminal capping",
            "amino acid",
            "water",
            "amino acid",
            "amino acid",
            "terminal capping",
        ],
    )
    reference = molecular_groups(
        ["HOH", "ALA", "SER", "NME"],
        ["water", "amino acid", "amino acid", "terminal capping"],
    )
    identity, groups, other = msm.topology.get_sequence_identity(
        query, reference_molecular_system=reference
    )
    assert identity == pytest.approx(200 / 3)
    assert groups == [1, 4]
    assert other == [1, 2]
    identity, groups, other = msm.topology.get_sequence_identity(
        reference, reference_molecular_system=query
    )
    assert identity == 100.0
    assert groups == [1, 2]
    assert other == [1, 4]


def test_reordered_and_repeated_group_selections_are_not_renumbered():
    query = molecular_groups(
        ["HOH", "ALA", "NA", "GLY"], ["water", "amino acid", "ion", "amino acid"]
    )
    reference = molecular_groups(
        ["SER", "GLY", "ALA", "HOH"],
        ["amino acid", "amino acid", "amino acid", "water"],
    )
    identity, groups, other = msm.topology.get_sequence_identity(
        query,
        selection=[3, 0, 1, 3],
        reference_molecular_system=reference,
        reference_selection=[1, 3, 2, 1],
    )
    assert identity == 100.0
    assert groups == [3, 1, 3]
    assert other == [1, 2, 1]


@pytest.mark.parametrize("kind", ["text", "seq", "record"])
def test_sequence_only_inputs_preserve_selected_positions(kind):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    query, reference = "AGST", "TGAS"
    if kind == "seq":
        query, reference = Seq(query), Seq(reference)
    elif kind == "record":
        query, reference = SeqRecord(Seq(query)), SeqRecord(Seq(reference))
    actual = msm.topology.get_sequence_identity(
        query,
        selection=[1, 0, 1],
        reference_molecular_system=reference,
        reference_selection=[1, 2, 1],
    )
    assert actual == (100.0, [1, 0, 1], [1, 2, 1])


def test_three_letter_sequence_groups_and_caps_have_source_positions():
    actual = msm.topology.get_sequence_identity(
        "AceAlaGlyNme", reference_molecular_system="AlaGly"
    )
    assert actual == (100.0, [1, 2], [0, 1])


def test_substitutions_and_explicit_group_predicates():
    query = molecular_groups(
        ["ACE", "ALA", "GLY", "SER", "NME"],
        [
            "terminal capping",
            "amino acid",
            "amino acid",
            "amino acid",
            "terminal capping",
        ],
    )
    reference = molecular_groups(
        ["HOH", "ALA", "THR", "SER", "NME"],
        ["water", "amino acid", "amino acid", "amino acid", "terminal capping"],
    )
    actual = msm.topology.get_sequence_identity(
        query,
        selection="group_index in [0,1,2,3]",
        reference_molecular_system=reference,
        reference_selection="group_index in [1,2,3,4]",
    )
    assert actual[0] == pytest.approx(200 / 3)
    assert actual[1:] == ([1, 3], [1, 3])


@pytest.mark.parametrize(
    "case", ["no_letters", "empty_query", "empty_reference", "gapped", "undefined"]
)
def test_empty_or_unmappable_sequences_have_an_explicit_policy(case):
    from Bio.Seq import Seq

    from molsysmt._private.smonitor import ArgumentError

    source = molecular_groups(
        ["ACE", "ALA", "HOH"], ["terminal capping", "amino acid", "water"]
    )
    options = dict(reference_molecular_system=source)
    if case == "no_letters":
        options["selection"] = [0, 2]
    elif case == "empty_query":
        options["selection"] = []
    elif case == "empty_reference":
        options["reference_selection"] = []
    elif case == "gapped":
        source = Seq("A-G")
    else:
        source = Seq(None, length=2)
    with pytest.raises(ArgumentError):
        msm.topology.get_sequence_identity(source, **options)


def test_default_reference_and_trusted_boundary():
    source = molecular_groups(
        ["ACE", "ALA", "GLY", "NME"],
        ["terminal capping", "amino acid", "amino acid", "terminal capping"],
    )
    expected = (100.0, [1, 2], [1, 2])
    assert msm.topology.get_sequence_identity(source) == expected
    assert msm.topology.get_sequence_identity(source, skip_digestion=True) == expected
    # The historical six positional slots remain callable with their meanings.
    assert (
        msm.topology.get_sequence_identity(
            source, [1, 2], source, [1, 2], "MolSysMT", "Biopython"
        )
        == expected
    )
    with pytest.raises(msm.ArgumentError):
        msm.topology.get_sequence_identity(source, skip_digestion="true")
    with pytest.raises(TypeError):
        msm.topology.get_sequence_identity(
            source, "all", source, "all", "MolSysMT", "Biopython", True
        )


def test_native_sequence_converter_shares_the_same_letter_projection():
    source = molecular_groups(
        ["ACE", "ALA", "HOH", "MSE", "NME"],
        ["terminal capping", "amino acid", "water", "amino acid", "terminal capping"],
    )
    assert msm.convert(source, to_form="string:amino_acids_1") == "AM"
    assert msm.topology.get_sequence_identity(source) == (100.0, [1, 3], [1, 3])


def test_real_ackredit_credits_reused_reference_and_executed_version():
    from Bio import __version__ as version

    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("sequence-projection"):
        with ackredit.scope("consumer.sequence_compare"):
            first = msm.topology.get_sequence_identity(
                "AG", reference_molecular_system="AG"
            )
            second = msm.topology.get_sequence_identity(
                "AS", reference_molecular_system="AS"
            )
        assert first == second == (100.0, [0, 1], [0, 1])
        used = ackredit.get_used_items()
        assert set(used) == {
            "ensembler-sequence-identity-reference",
            f"software:biopython:{version}",
        }
        assert len(used["ensembler-sequence-identity-reference"]) == 1
        assert (
            "molsysmt.topology.get_sequence_identity"
            in ackredit.current_session().usage_tree["consumer.sequence_compare"][
                "children"
            ]
        )


def test_absent_or_failing_attribution_does_not_replace_science(monkeypatch):
    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    expected = msm.topology.get_sequence_identity("AG", reference_molecular_system="AS")

    def broken():
        raise RuntimeError("provider unavailable")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with pytest.warns(AckreditTrackingWarning):
        actual = msm.topology.get_sequence_identity(
            "AG", reference_molecular_system="AS"
        )
    assert actual == expected


def test_rejected_sequences_do_not_claim_attribution():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("invalid-sequence"):
        with pytest.raises(msm.ArgumentError):
            msm.topology.get_sequence_identity(
                "AG", selection=[], reference_molecular_system="AG"
            )
        assert ackredit.get_used_items() == {}


def test_fresh_import_and_real_provider_absence():
    import subprocess
    import sys

    code = """
import importlib.abc
import sys
class Absent(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == 'ackredit' or fullname.startswith('ackredit.'):
            raise ModuleNotFoundError('Ackredit deliberately unavailable')
sys.meta_path.insert(0, Absent())
import molsysmt as msm
assert 'ackredit' not in sys.modules
assert msm.topology.get_sequence_identity('AG', reference_molecular_system='AG') == (100., [0, 1], [0, 1])
assert 'ackredit' not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
