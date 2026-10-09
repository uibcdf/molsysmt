"""Protect sequence copies and identity conversions through the public API."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("record", [False, True])
@pytest.mark.parametrize("operation", ["copy", "convert"])
def test_sequence_copy_and_identity_conversion_are_independent(record, operation):
    from Bio.Seq import Seq
    from Bio.SeqFeature import SeqFeature, SimpleLocation
    from Bio.SeqRecord import SeqRecord

    item = Seq("aGx")
    if record:
        item = SeqRecord(
            item,
            id="chain-z",
            name="source",
            description="source sequence",
            annotations={"note": ["original"]},
            letter_annotations={"quality": [1, 2, 3]},
            features=[
                SeqFeature(SimpleLocation(0, 2), qualifiers={"note": ["feature"]})
            ],
        )
    result = (
        msm.copy(item)
        if operation == "copy"
        else msm.convert(item, to_form=msm.get_form(item))
    )
    assert result is not item
    assert msm.get_form(result) == msm.get_form(item)
    assert msm.get(result, element="group", group_index=True, group_name=True) == [
        [0, 1, 2],
        ["a", "G", "x"],
    ]
    if record:
        assert (result.id, result.name, result.description) == (
            "chain-z",
            "source",
            "source sequence",
        )
        result.annotations["note"].append("changed")
        result.letter_annotations["quality"][0] = 99
        result.features[0].qualifiers["note"].append("changed")
        assert item.annotations == {"note": ["original"]}
        assert item.letter_annotations == {"quality": [1, 2, 3]}
        assert item.features[0].qualifiers == {"note": ["feature"]}
        assert result.features[0].location == item.features[0].location


@pytest.mark.parametrize("record", [False, True])
def test_identity_conversion_can_reuse_explicitly_requested_source(record):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    item = Seq("AGX")
    if record:
        item = SeqRecord(item)
    assert msm.convert(item, to_form=msm.get_form(item), copy_if_all=False) is item


@pytest.mark.parametrize("record", [False, True])
@pytest.mark.parametrize("undefined", [False, True])
def test_sequence_copy_preserves_empty_or_undefined_content(record, undefined):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    item = Seq(None, length=3) if undefined else Seq("")
    if record:
        item = SeqRecord(item)
    result = msm.copy(item)
    assert result is not item
    assert msm.get(result, element="group", group_index=True, group_name=True) == (
        [[0, 1, 2], None] if undefined else [[], []]
    )


def test_copy_preserves_record_without_sequence():
    from Bio.SeqRecord import SeqRecord

    item = SeqRecord(None, id="unassigned", annotations={"note": ["original"]})
    result = msm.copy(item)
    assert result is not item
    assert result.seq is None
    assert result.id == item.id
    result.annotations["note"].append("changed")
    assert item.annotations == {"note": ["original"]}


def test_sequence_identity_conversion_preserves_selected_positions():
    from Bio.Seq import Seq

    item = Seq("aGx")
    result = msm.convert(item, to_form="biopython.Seq", selection=[2, 0, 2])
    assert str(result) == "xax"
    assert str(item) == "aGx"


def test_record_selection_remains_explicitly_unsupported():
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    from molsysmt._private.smonitor import NotImplementedMethodError

    item = SeqRecord(Seq("AGX"), annotations={"note": ["original"]})
    with pytest.raises(NotImplementedMethodError):
        msm.convert(item, to_form="biopython.SeqRecord", selection=[2, 0])
    assert str(item.seq) == "AGX"
    assert item.annotations == {"note": ["original"]}


@pytest.mark.parametrize("record", [False, True])
def test_full_public_extraction_obeys_copy_policy(record):
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord

    item = SeqRecord(Seq("AGX"), id="chain-z") if record else Seq("AGX")
    result = msm.extract(item)
    assert result is not item
    assert msm.get(result, element="group", group_name=True) == ["A", "G", "X"]
    assert msm.extract(item, copy_if_all=False) is item
