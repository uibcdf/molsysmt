"""
Catalog / template wiring integrity.

SMONITOR_GUIDE.md states two non-negotiable rules:

  1. Zero String Hardcoding — if it's a warning or error, it belongs in the catalog.
  4. Template Wiring Integrity — every emitted catalog code must have a matching
     template in the active configuration.

Nothing enforced them. `FormatError` (MSM-ERR-IO-003) shipped with no template and
raised with an empty message, and `GpuNotAvailableWarning` (MSM-WARN-GPU-001) had
none either, producing the repr of its own class as the user-facing text. That went
unnoticed because the emission sites hardcoded the message, which masked the hole:
removing the hardcoded string would have exposed it.

These tests close both directions of the wiring.
"""

import re
import string

import pytest

from molsysmt._private.smonitor.catalog import CATALOG, CODES

AUDIENCES = ['user', 'dev', 'qa', 'agent']

# Placeholders the diagnostics layer always injects, so a template may use them
# without the raise site having to pass them.
AMBIENT_PLACEHOLDERS = {'doc_url', 'issues_url', 'caller', 'message', 'package', 'version'}


CATALOG_SECTIONS = ('exceptions', 'warnings', 'info', 'debug')


def _catalog_entries():
    for kind in CATALOG_SECTIONS:
        for key, meta in CATALOG.get(kind, {}).items():
            yield kind, key, meta['code']


def _placeholders(template):
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


@pytest.mark.parametrize('kind, key, code', list(_catalog_entries()),
                         ids=[f'{k}:{key}' for k, key, _ in _catalog_entries()])
def test_every_catalog_entry_has_a_template(kind, key, code):
    assert code in CODES, (
        f"{key} ({kind}) emits {code}, but CODES has no template for it. "
        f"Without one the message resolves to an empty string or to the class repr.")


@pytest.mark.parametrize('code', sorted(CODES))
def test_every_template_has_a_catalog_entry(code):
    declared = {entry_code for _, _, entry_code in _catalog_entries()}
    assert code in declared, f"CODES defines {code}, but no catalog entry emits it."


@pytest.mark.parametrize('code', sorted(CODES))
def test_every_template_serves_all_audiences(code):
    entry = CODES[code]
    for audience in AUDIENCES:
        assert f'{audience}_message' in entry, f"{code} has no {audience}_message."
        assert entry[f'{audience}_message'], f"{code} has an empty {audience}_message."


@pytest.mark.parametrize('code', sorted(CODES))
def test_template_has_a_title(code):
    assert CODES[code].get('title'), f"{code} has no title."


def test_the_two_codes_that_were_missing_a_template():
    # regression: these are the entries that shipped unwired
    assert 'MSM-ERR-IO-003' in CODES      # FormatError
    assert 'MSM-WARN-GPU-001' in CODES    # GpuNotAvailableWarning
