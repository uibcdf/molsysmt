"""Cross-repo SMonitor contract tests.

These tests guard diagnostics wiring between pyunitwizard/depdigest and smonitor.
"""

import pytest


def test_pyunitwizard_parser_error_has_message():
    """Parser exceptions should resolve to non-empty catalog-backed messages."""
    from pyunitwizard.parse import parse
    from pyunitwizard._private.exceptions import LibraryWithoutParserError

    with pytest.raises(LibraryWithoutParserError) as excinfo:
        parse("1 nm", parser="openmm.unit")

    message = str(excinfo.value)
    assert isinstance(message, str)
    assert message.strip() != ""
    assert "parser" in message.lower()


def test_depdigest_missing_dependency_raises_readable_error():
    """Missing dependencies should raise a readable exception message."""
    from depdigest.core.checker import check_dependency

    with pytest.raises(ImportError) as excinfo:
        check_dependency("definitely_nonexistent_pkg_zzz", caller="test")

    message = str(excinfo.value)
    assert isinstance(message, str)
    assert message.strip() != ""
    assert "required" in message.lower()


def test_molsysmt_download_warning_resolves_with_context():
    """MolSysMT download warnings should expose actionable QA/developer context."""
    import smonitor
    from molsysmt._private.smonitor import CODES, message_from_catalog

    smonitor.configure(profile="qa", codes=CODES)

    text = message_from_catalog(
        {"code": "MSM-WARN-DL-001"},
        extra={
            "caller": "molsysmt.form.file_bcif_gz.download",
            "message": "Network issue while downloading 181l.bcif.gz (timed out). Retrying in 2.0s…",
            "resource": "181l.bcif.gz",
            "provider": "RCSB PDB",
            "attempt": 2,
            "retries": 5,
            "reason": "timed out",
        },
    )

    assert "181l.bcif.gz" in text
    assert "2/5" in text
    assert "timed out" in text
