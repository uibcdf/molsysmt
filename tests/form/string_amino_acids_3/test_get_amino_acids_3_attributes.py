import molsysmt as msm


def test_get_group_attributes():
    item = 'amino_acids_3:AlaArgGly'

    output = msm.get(item, element='group', group_index=True, group_name=True)

    assert output == [[0, 1, 2], ['ALA', 'ARG', 'GLY']]


def test_get_group_attributes_with_selection():
    item = 'amino_acids_3:AlaArgGly'

    output = msm.get(
        item,
        element='group',
        selection=[0, 2],
        group_index=True,
        group_name=True,
    )

    assert output == [[0, 2], ['ALA', 'GLY']]
