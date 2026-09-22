"""Check that the ViewerJSON export declaration names real objects."""

import molsysmt.form.molsysmt_ViewerJSON as viewerjson_form


def test_declared_exports_exist():
    """Every declared export must be available on the adapter package."""
    missing = set(viewerjson_form.__all__) - set(vars(viewerjson_form))
    assert not missing
