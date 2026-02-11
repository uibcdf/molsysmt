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


def test_xyz_is_form_rejects_non_quantity_string():
    """XYZ form detection must reject non-quantity strings."""
    xyz_is_form = importlib.import_module("molsysmt.form.XYZ.is_form").is_form
    assert xyz_is_form("1BRS") is False


def test_string_pdb_id_is_form_local_patterns():
    """PDB id detection should rely on local patterns only."""
    pdb_is_form = importlib.import_module("molsysmt.form.string_pdb_id.is_form").is_form

    assert pdb_is_form("1BRS") is True
    assert pdb_is_form("pdb_id:1BRS") is True
    assert pdb_is_form("pdb_1BRS") is True
    assert pdb_is_form("BRS1") is False


def test_string_alphafold_id_is_form_local_patterns():
    """AlphaFold id detection should rely on local patterns only."""
    af_is_form = importlib.import_module("molsysmt.form.string_alphafold_id.is_form").is_form

    assert af_is_form("AF-P05067-F1") is True
    assert af_is_form("alphafold_id:AF-P05067-F1") is True
    assert af_is_form("AF-P05067-F1-model_v4") is True
    assert af_is_form("AF-invalid") is False
