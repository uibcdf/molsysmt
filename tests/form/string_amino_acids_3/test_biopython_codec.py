"""Keep declared sequence alphabets and original group selections through codecs."""

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, NotWithThisFormError


@pytest.mark.parametrize(
    "target", ["biopython.Seq", "biopython.SeqRecord", "string:amino_acids_1"]
)
@pytest.mark.parametrize("source", ["AlaGly", "amino_acids_3:AlaGly"])
def test_three_letter_public_conversion_is_actual_one_letter_text(source, target):
    result = msm.convert(source, to_form=target)
    assert str(result.seq if target.endswith("SeqRecord") else result) == "AG"


@pytest.mark.parametrize(
    "indices,expected", [("all", "AG"), ([2, 1, 2, 0], "GAG"), ([], ""), ([3, 0], "")]
)
@pytest.mark.parametrize("kind", ["Seq", "SeqRecord", "one_letter"])
def test_direct_three_letter_selection_uses_original_groups_before_caps(
    indices, expected, kind
):
    source = "amino_acids_3:AceAlaGlyNme"
    if kind == "one_letter":
        from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import (
            to_string_amino_acids_1 as convert,
        )
    else:
        from importlib import import_module

        convert = getattr(
            import_module(f"molsysmt.form.string_amino_acids_3.to_biopython_{kind}"),
            f"to_biopython_{kind}",
        )
    result = convert(source, group_indices=indices)
    text = str(result.seq if kind == "SeqRecord" else result)
    if kind == "one_letter":
        text = text.removeprefix("amino_acids_1:")
    assert text == expected


@pytest.mark.parametrize("source", ["AG", "amino_acids_1:AG"])
@pytest.mark.parametrize(
    "indices,expected", [("all", "AG"), ([1, 0, 1], "GAG"), ([], "")]
)
def test_one_letter_identity_and_biopython_share_selection_contract(
    source, indices, expected
):
    from molsysmt.form.string_amino_acids_1.to_biopython_Seq import to_biopython_Seq
    from molsysmt.form.string_amino_acids_1.to_string_amino_acids_1 import (
        to_string_amino_acids_1,
    )

    assert (
        to_string_amino_acids_1(source, group_indices=indices).removeprefix(
            "amino_acids_1:"
        )
        == expected
    )
    assert str(to_biopython_Seq(source, group_indices=indices)) == expected


@pytest.mark.parametrize(
    "target", ["biopython.Seq", "biopython.SeqRecord", "string:amino_acids_1"]
)
def test_public_three_letter_conversion_keeps_selected_order_and_repetitions(target):
    result = msm.convert("amino_acids_3:AlaGlySer", selection=[2, 0, 2], to_form=target)
    assert str(result.seq if target.endswith("SeqRecord") else result) == "SAS"


@pytest.mark.parametrize("bad", [[True], [0.5], [-1], [4], [[0, 1]]])
@pytest.mark.parametrize("width", [1, 3])
def test_direct_sequence_group_positions_are_strict(bad, width):
    from importlib import import_module

    convert = import_module(
        f"molsysmt.form.string_amino_acids_{width}.to_biopython_Seq"
    ).to_biopython_Seq
    with pytest.raises(ArgumentError):
        convert(
            "amino_acids_1:AG" if width == 1 else "amino_acids_3:AlaGly",
            group_indices=bad,
        )


def test_declared_extended_one_letter_alphabet_is_retained():
    assert (
        str(msm.convert("amino_acids_1:BXZJUO-*", to_form="biopython.Seq"))
        == "BXZJUO-*"
    )


def test_sequence_extractors_do_not_invent_structures():
    from molsysmt.form.string_amino_acids_1.extract import extract

    with pytest.raises(NotWithThisFormError):
        extract("AG", structure_indices=[0])


def test_three_letter_sequence_identity_keeps_original_source_groups():
    result = msm.topology.get_sequence_identity(
        "amino_acids_3:AceAlaGlyNme",
        reference_molecular_system="amino_acids_1:GA",
        selection=[2, 1],
    )
    assert result == (100.0, [2, 1], [0, 1])


def test_native_sequence_codecs_do_not_import_biopython():
    import subprocess
    import sys

    code = """
import builtins
original = builtins.__import__
def guarded(name, *args, **kwargs):
    if name == 'Bio' or name.startswith('Bio.'):
        raise ImportError('Biopython deliberately unavailable')
    return original(name, *args, **kwargs)
builtins.__import__ = guarded
import molsysmt as msm
assert msm.convert('AlaGly', to_form='string:amino_acids_1') == 'AG'
assert msm.convert('AG', to_form='string:amino_acids_3') == 'AlaGly'
"""
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr


def test_empty_native_target_keeps_its_declared_alphabet():
    assert (
        msm.convert("amino_acids_1:AG", selection=[], to_form="string:amino_acids_3")
        == "amino_acids_3:"
    )
    assert (
        msm.convert(
            "amino_acids_3:AlaGly", selection=[], to_form="string:amino_acids_1"
        )
        == "amino_acids_1:"
    )
