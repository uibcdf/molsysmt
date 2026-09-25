"""Contract tests for native one-to-three-letter sequence conversion."""

import builtins

import pytest

import molsysmt as msm


def test_conversion_of_standard_sequence_and_default_builder():
    assert msm.get_form("GG") == "string:amino_acids_1"
    assert msm.convert("GG", to_form="string:amino_acids_3") == "GlyGly"
    assert msm.build.build_peptide("GG").topology.groups.shape[0] == 2


def test_conversion_and_default_builder_work_when_biopython_is_unavailable(monkeypatch):
    from depdigest.core import checker

    import_module = builtins.__import__
    is_installed = checker.is_installed

    def without_biopython(name, *args, **kwargs):
        if name == "Bio" or name.startswith("Bio."):
            raise ModuleNotFoundError("Biopython is unavailable in this test")
        return import_module(name, *args, **kwargs)

    with monkeypatch.context() as patcher:
        patcher.setattr(builtins, "__import__", without_biopython)
        patcher.setattr(
            checker,
            "is_installed",
            lambda name: False if name == "Bio" else is_installed(name),
        )
        assert msm.convert("GG", to_form="string:amino_acids_3") == "GlyGly"
        assert msm.get(msm.build.build_peptide("GG"), n_groups=True) == 2


def test_conversion_normalizes_lowercase_and_accepts_explicit_prefix():
    assert msm.convert("gg", to_form="string:amino_acids_3") == "GlyGly"
    assert msm.convert("amino_acids_1:GG", to_form="string:amino_acids_3") == "GlyGly"


@pytest.mark.parametrize("sequence", ["ACDEFGHIKLMNPQRSTVWY", "BZXJUO*", "GG"])
def test_conversion_matches_biopython_on_uppercase_codes(sequence):
    seq_utils = pytest.importorskip("Bio.SeqUtils")

    assert msm.convert(
        f"amino_acids_1:{sequence}", to_form="string:amino_acids_3"
    ) == seq_utils.seq3(sequence)


def test_unknown_code_preserves_xaa_conversion_policy():
    assert msm.convert("amino_acids_1:A?", to_form="string:amino_acids_3") == "AlaXaa"
