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


def test_molsysmt_ambiguous_structure_warning_exposes_count_and_caller():
    """Ambiguous structure warnings should expose caller and structure count."""
    import smonitor
    from molsysmt._private.smonitor import CODES, message_from_catalog

    smonitor.configure(profile="qa", codes=CODES)

    text = message_from_catalog(
        {"code": "MSM-WARN-STRUCT-002"},
        extra={"caller": "molsysmt.form.openmm_Topology.to_string_pdb_text", "count": 4},
    )

    assert "4" in text
    assert "to_string_pdb_text" in text



def test_molsysmt_model_mismatch_warning_exposes_model_count():
    """Model mismatch warnings should expose the number of incompatible models."""
    import smonitor
    from molsysmt._private.smonitor import CODES, message_from_catalog

    smonitor.configure(profile="qa", codes=CODES)

    text = message_from_catalog(
        {"code": "MSM-WARN-STRUCT-004"},
        extra={"caller": "molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys", "count": 3},
    )

    assert "3" in text
    assert "to_molsysmt_MolSys" in text



def test_molsysmt_cross_chain_bond_warning_exposes_pair_count():
    """Cross-chain bond warnings should expose caller and pair count."""
    import smonitor
    from molsysmt._private.smonitor import CODES, message_from_catalog

    smonitor.configure(profile="qa", codes=CODES)

    text = message_from_catalog(
        {"code": "MSM-WARN-STRUCT-001"},
        extra={
            "caller": "molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys",
            "count": 2,
            "pairs": [("CA 1 in ALA1 with atom_index 0", "SG 3 in CYS2 with atom_index 8")],
        },
    )

    assert "2" in text
    assert "to_molsysmt_MolSys" in text
