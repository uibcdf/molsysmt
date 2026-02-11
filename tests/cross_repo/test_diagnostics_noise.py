"""Cross-repo diagnostics integration tests.

These tests track interactions between molsysmt, pyunitwizard, and smonitor.
"""
import importlib

def _contains_unit_registry_noise(text):
    return "is not defined in the unit registry" in text


def test_get_form_pdb_id_is_functional(capfd):
    """Getting form from a valid PDB id should work."""
    import molsysmt as msm

    capfd.readouterr()
    # Explicit prefix avoids network probing in string_pdb_id form detection.
    form = msm.get_form("pdb_id:1BRS")
    captured = capfd.readouterr()

    assert form == "string:pdb_id"
    assert isinstance(captured.err, str)


def test_get_form_pdb_id_emits_no_unit_registry_noise(capfd):
    """Form probing should not leak unit-registry parse errors to user stderr."""
    import molsysmt as msm

    capfd.readouterr()
    msm.get_form("1BRS")
    captured = capfd.readouterr()

    assert not _contains_unit_registry_noise(captured.err)


def test_xyz_is_form_accepts_quantity_string():
    """XYZ form detection must accept quantity-like strings."""
    xyz_is_form = importlib.import_module("molsysmt.form.XYZ.is_form").is_form
    assert xyz_is_form("[[0,0,0],[1,1,1]] nm") is True


def test_xyz_is_form_rejects_non_quantity_string():
    """XYZ form detection must reject non-quantity strings."""
    xyz_is_form = importlib.import_module("molsysmt.form.XYZ.is_form").is_form
    assert xyz_is_form("1BRS") is False
