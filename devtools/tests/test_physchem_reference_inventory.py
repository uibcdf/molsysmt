"""Protecting amino-acid alignment in the #485 research inventory."""

import pytest

from devtools.scripts.audit_physchem_reference_inventory import (
    matching_accessions,
    parse_aaindex1,
)


def record(
    header="A/L R/K N/M D/F C/P Q/S E/T G/W H/Y I/V", first="1 2 3 4 5 6 7 8 9 10"
):
    return f"H TEST000001\nD Synthetic axis control\nI {header}\n {first}\n 11 12 13 14 15 16 17 18 19 20\n//\n"


def test_paired_header_separates_upper_and_lower_halves():
    values = parse_aaindex1(record())[0]["values"]
    assert values["A"] == 1
    assert values["R"] == 2
    assert values["I"] == 10
    assert values["L"] == 11
    assert values["V"] == 20


def test_missing_reference_value_is_never_a_twenty_value_match():
    records = parse_aaindex1(record(first="NA 2 3 4 5 6 7 8 9 10"))
    table = dict(
        zip(
            "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
            range(1, 21),
        )
    )
    assert matching_accessions(table, records) == []


def test_twenty_value_match_requires_every_amino_acid_without_rescaling():
    records = parse_aaindex1(record())
    table = dict(
        zip(
            "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split(),
            range(1, 21),
        )
    )
    assert matching_accessions(table, records) == ["TEST000001"]
    table["VAL"] = 19
    assert matching_accessions(table, records) == []


@pytest.mark.parametrize(
    "text",
    ["", record() + record(), record(header="A/A R/K N/M D/F C/P Q/S E/T G/W H/Y I/V")],
)
def test_incomplete_or_ambiguous_reference_axis_fails(text):
    with pytest.raises(ValueError):
        parse_aaindex1(text)
