from molsysmt.element.group.amino_acid import get_expected_heavy_atoms


def test_modified_residues_without_exact_templates_are_unassessed():
    assert get_expected_heavy_atoms("MSE", ["N", "CA", "SE"]) is None
    assert get_expected_heavy_atoms("SEP", ["N", "CA", "OG", "P"]) is None


def test_supported_protonation_variant_keeps_its_exact_template():
    expected = get_expected_heavy_atoms("HID")
    assert expected is not None
    assert {"ND1", "NE2"} <= expected
