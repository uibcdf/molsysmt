from molsysmt.element.group.amino_acid import get_expected_heavy_atoms


def test_modified_residues_use_exact_templates():
    assert "SE" in get_expected_heavy_atoms("MSE", ["N", "CA"])
    assert "P" in get_expected_heavy_atoms("SEP", ["N", "CA", "OG"])
    assert get_expected_heavy_atoms("MSE", ["N", "CA", "SD"]) is None
    assert get_expected_heavy_atoms("SEP", ["N", "CA", "CB", "OG1"]) is None
    assert get_expected_heavy_atoms("TPO", ["N", "CA"]) is None


def test_supported_protonation_variant_keeps_its_exact_template():
    expected = get_expected_heavy_atoms("HID")
    assert expected is not None
    assert {"ND1", "NE2"} <= expected
