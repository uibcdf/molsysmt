"""Exercise real sequence input forms through the public facade."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("record", [False, True])
@pytest.mark.parametrize(
    "selection, indices, names",
    [
        ("all", [0, 1, 2], ["a", "G", "x"]),
        ([2, 0, 2], [2, 0, 2], ["x", "a", "x"]),
        (1, [1], ["G"]),
        ([], [], []),
    ],
)
def test_real_biopython_sequence_group_queries(record, selection, indices, names):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    sequence = Seq("aGx")
    item = (
        SeqRecord(sequence, id="chain-z", annotations={"note": ["unchanged"]})
        if record
        else sequence
    )
    expected_form = "biopython.SeqRecord" if record else "biopython.Seq"
    assert msm.get_form(item) == expected_form
    assert msm.get(
        item, element="group", selection=selection, group_index=True, group_name=True
    ) == [indices, names]
    assert msm.get(
        item,
        element="group",
        selection=selection,
        output_type="dictionary",
        group_name=True,
        group_index=True,
    ) == {"group_name": names, "group_index": indices}
    assert str(sequence) == "aGx"
    if record:
        assert item.id == "chain-z"
        assert item.annotations == {"note": ["unchanged"]}


@pytest.mark.parametrize("record", [False, True])
def test_empty_sequences_preserve_known_empty_groups(record):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    sequence = Seq("")
    item = SeqRecord(sequence) if record else sequence
    assert msm.get(item, element="group", group_index=True, group_name=True) == [[], []]


@pytest.mark.parametrize("record", [False, True])
def test_undefined_sequence_retains_positions_without_inventing_names(record):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    sequence = Seq(None, length=3)
    item = SeqRecord(sequence) if record else sequence
    assert msm.get(item, element="group", group_index=True, group_name=True) == [
        [0, 1, 2],
        None,
    ]
    assert msm.has_attribute(item, attribute="group_name") is False
    assert msm.has_attribute(item, attribute="group_name", include_none=True) is True


def test_record_without_sequence_reports_missing_groups():
    from Bio.SeqRecord import SeqRecord

    item = SeqRecord(None, id="unassigned")
    assert msm.get(item, element="group", group_index=True, group_name=True) == [
        None,
        None,
    ]
    assert msm.has_attribute(item, attribute="group_index") is False
