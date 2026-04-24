"""Tests for string_pdb_id form recognition and PDB ID extraction."""

import pytest
from molsysmt.form.string_pdb_id.is_form import is_form
from molsysmt.form.string_pdb_id import _extract_pdb_id


# --- is_form ---

class TestIsFormLegacyIds:

    def test_bare_lowercase(self):
        assert is_form('181l') is True

    def test_bare_uppercase(self):
        assert is_form('181L') is True

    def test_pdb_id_prefix(self):
        assert is_form('pdb_id:181l') is True

    def test_pdb_id_prefix_uppercase(self):
        assert is_form('PDB_ID:181L') is True

    def test_pdb_underscore_prefix(self):
        assert is_form('pdb_181l') is True

    def test_pdb_underscore_prefix_uppercase(self):
        assert is_form('PDB_181L') is True

    def test_pdb_colon_prefix_tolerance(self):
        # 'pdb:' is NOT official syntax — accepted silently as user-friendliness alias
        assert is_form('pdb:181l') is True

    def test_pdb_colon_prefix_uppercase_tolerance(self):
        assert is_form('PDB:181L') is True

    def test_non_pdb_string_rejected(self):
        assert is_form('not_a_pdb_id') is False

    def test_too_short_rejected(self):
        assert is_form('1AB') is False

    def test_too_long_bare_rejected(self):
        assert is_form('1ABCDE') is False

    def test_non_string_rejected(self):
        assert is_form(1234) is False
        assert is_form(None) is False


class TestIsFormExtendedIds:
    """Extended 8-char PDB IDs (wwPDB post-2028 format: pdb_0000XXXX)."""

    def test_extended_lowercase(self):
        assert is_form('pdb_0000181l') is True

    def test_extended_uppercase(self):
        assert is_form('PDB_0000181L') is True

    def test_extended_mixed_case(self):
        assert is_form('Pdb_0000181l') is True

    def test_bare_extended_not_recognized(self):
        # Bare 8-char code without prefix is not a recognized form
        assert is_form('0000181l') is False


# --- _extract_pdb_id ---

class TestExtractPdbId:

    def test_bare_id_lowercased(self):
        assert _extract_pdb_id('181L') == '181l'

    def test_pdb_id_prefix_stripped(self):
        assert _extract_pdb_id('pdb_id:181L') == '181l'

    def test_pdb_id_prefix_uppercase_stripped(self):
        assert _extract_pdb_id('PDB_ID:181L') == '181l'

    def test_pdb_underscore_prefix_stripped(self):
        assert _extract_pdb_id('pdb_181L') == '181l'

    def test_pdb_underscore_prefix_uppercase_stripped(self):
        assert _extract_pdb_id('PDB_181L') == '181l'

    def test_pdb_colon_prefix_stripped(self):
        assert _extract_pdb_id('pdb:181L') == '181l'

    def test_pdb_colon_prefix_uppercase_stripped(self):
        assert _extract_pdb_id('PDB:181L') == '181l'

    def test_extended_id_stripped(self):
        assert _extract_pdb_id('pdb_0000181l') == '0000181l'

    def test_extended_id_uppercase_stripped(self):
        assert _extract_pdb_id('PDB_0000181L') == '0000181l'
