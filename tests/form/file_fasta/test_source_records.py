"""Retain submitted FASTA text and every occurrence before scientific admission."""

import json
import subprocess
import sys

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, FormatError


def parse(text, **kwargs):
    return msm.form.file_fasta.parse_records(text, **kwargs)


@pytest.mark.parametrize("ending", ["\n", "\r\n", "\r"])
def test_source_text_headers_and_every_record_are_preserved(ending):
    text = ending + ending.join(
        [">raw header  ", " acD ", "A*", ">repeat", "MABC", ">repeat", "MABC", ">", ""]
    )
    result = parse(text, source_label="submitted-library")
    assert result["schema"] == "molsysmt.fasta_source@1"
    assert result["source"] == "submitted-library"
    assert result["preamble"] == ending
    records = result["records"]
    assert [r["record_index"] for r in records] == [0, 1, 2, 3]
    assert [r["header"] for r in records] == ["raw header  ", "repeat", "repeat", ""]
    assert [r["sequence"] for r in records] == [" acD A*", "MABC", "MABC", ""]
    assert result["preamble"] + "".join(r["raw_record"] for r in records) == text
    for record in records:
        first, stop = record["source_span"]
        assert text[first:stop] == record["raw_record"]
    assert json.loads(json.dumps(result)) == result


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", []),
        (" \r\n\t\n", []),
        (">empty", [""]),
        (">a\r\n Ac\nD\r>β\nM[mod]\t*?", [" AcD", "M[mod]\t*?"]),
        (">unicode\nA\u2028>still-sequence\n", ["A\u2028>still-sequence"]),
        (">a\n;comment-is-retained\n", [";comment-is-retained"]),
    ],
)
def test_no_silent_character_or_record_normalization(text, expected):
    result = parse(text)
    assert [r["sequence"] for r in result["records"]] == expected
    assert (
        result["preamble"] + "".join(r["raw_record"] for r in result["records"]) == text
    )


@pytest.mark.parametrize(
    "text",
    ["ACD\n>named\nG\n", "\n#comment\n>a\nG", " >indented\nACD", "\ufeff>a\nACD"],
)
def test_unnamed_nonblank_content_rejects_instead_of_disappearing(text):
    with pytest.raises(FormatError, match="before the first header"):
        parse(text)


@pytest.mark.parametrize("value", [None, b">a\nACD", [">a"], 3])
def test_nontext_input_raises_public_argument_error(value):
    with pytest.raises(ArgumentError):
        parse(value)


def test_invalid_source_label_is_rejected():
    with pytest.raises(ArgumentError):
        parse(">a\nACD", source_label=42)


def test_file_read_keeps_newlines_source_label_and_bytes(tmp_path):
    path = tmp_path / "submitted.fasta"
    original = ">β full description  \r\n acD \nA*\r>β\r\n"
    path.write_bytes(original.encode("utf-8"))
    result = msm.form.file_fasta.read_records(path)
    assert result == parse(original, source_label=str(path))
    assert path.read_bytes() == original.encode("utf-8")


def test_missing_file_and_invalid_utf8_are_explicit(tmp_path):
    with pytest.raises(FileNotFoundError):
        msm.form.file_fasta.read_records(tmp_path / "missing.fasta")
    path = tmp_path / "invalid.fasta"
    path.write_bytes(b">a\n\xff\n")
    with pytest.raises(FormatError) as caught:
        msm.form.file_fasta.read_records(path)
    assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_records_are_independent_between_calls():
    first, second = parse(">a\nM\n>a\nM"), parse(">a\nM\n>a\nM")
    first["records"][0]["source_span"][0] = -1
    first["records"][0]["header"] = "changed"
    assert second["records"][0]["source_span"][0] == 0
    assert second["records"][0]["header"] == "a"
    assert first["records"][1]["header"] == "a"


def test_native_reading_does_not_import_biopython(tmp_path):
    path = tmp_path / "native.fasta"
    path.write_bytes(b">a\n acD \nA*\n")
    script = """
import sys
from importlib.abc import MetaPathFinder
class DenyBio(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "Bio" or fullname.startswith("Bio."):
            raise AssertionError("Native FASTA ingestion attempted a Bio import")
sys.meta_path.insert(0, DenyBio())
import molsysmt as msm
result = msm.form.file_fasta.read_records(sys.argv[1])
assert result["records"][0]["sequence"] == " acD A*"
assert not any(name == "Bio" or name.startswith("Bio.") for name in sys.modules)
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(path)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_existing_public_normalized_conversion_is_unchanged(tmp_path):
    pytest.importorskip("Bio")
    path = tmp_path / "normalized.fasta"
    path.write_bytes(b">raw header\n acD \nA*\n>repeat\nMABC\n>repeat\nMABC\n>empty\n")
    records = msm.convert(str(path), to_form="biopython.SeqRecord")
    assert [str(r.seq) for r in records] == ["acDA*", "MABC", "MABC", ""]
    assert [r.description for r in records] == [
        "raw header",
        "repeat",
        "repeat",
        "empty",
    ]
