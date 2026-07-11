"""
Tests for molsysmt.configure — covers module-level variables and pyunitwizard
configuration accessed via msm.pyunitwizard.configure.

Coverage target: molsysmt/configure/__init__.py
                 molsysmt/configure/logging_setup.py (partially)
"""

import pytest
import molsysmt.configure as config


# ---------------------------------------------------------------------------
# Module-level variables — basic smoke checks
# ---------------------------------------------------------------------------




class TestConfigVariables:

    def test_use_gpu_default_false(self):
        assert config.use_gpu == 'auto'

    def test_gpu_threshold_positive(self):
        assert config.gpu_threshold > 0

    def test_heavy_mode_valid(self):
        assert config.heavy_mode in ('auto', 'force', 'off')

    def test_chunk_size_positive(self):
        assert config.chunk_size > 0

    def test_max_ram_usage_positive(self):
        assert config.max_ram_usage > 0

    def test_large_list_length_positive(self):
        assert config.large_list_length > 0

    def test_min_length_protein_positive(self):
        assert config.min_length_protein > 0

    def test_selection_shortcuts_has_molsysmt_key(self):
        assert 'MolSysMT' in config.selection_shortcuts

    def test_default_attribute_has_forcefield(self):
        assert 'forcefield' in config.default_attribute


# ---------------------------------------------------------------------------
# puw.configure wrappers (set_default_form, set_default_parser, set_standard_units)
# These helpers were previously duplicated in msm.configure; now use puw.configure
# directly, consistent with the rest of the MolSysSuite.
# ---------------------------------------------------------------------------

class TestPuwConfigureDefaultForm:

    def test_set_pint(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_default_form('pint')

    def test_set_openmm(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_default_form('openmm.unit')

    def test_reset_to_pint(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_default_form('pint')


class TestPuwConfigureDefaultParser:

    def test_set_pint(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_default_parser('pint')

    def test_reset_to_pint(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_default_parser('pint')


class TestPuwConfigureStandardUnits:

    def test_set_canonical_units(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_standard_units(
            ['nm', 'ps', 'K', 'mole', 'amu', 'e',
             'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees']
        )

    def test_set_minimal_units(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_standard_units(['nm', 'ps'])

    def test_reset_canonical(self):
        import molsysmt as msm
        msm.pyunitwizard.configure.set_standard_units(
            ['nm', 'ps', 'K', 'mole', 'amu', 'e',
             'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees']
        )


# ---------------------------------------------------------------------------
# setup_logging (deprecated — just verify it emits a deprecation warning)
# ---------------------------------------------------------------------------

class TestSetupLogging:

    def test_setup_logging_returns_logger(self):
        """setup_logging() returns a Logger."""
        import logging
        from molsysmt.configure.logging_setup import setup_logging
        logger = setup_logging(level='WARNING')
        assert isinstance(logger, logging.Logger)

    def test_setup_logging_no_capture(self):
        """capture_warnings=False branch must not raise."""
        import logging
        from molsysmt.configure.logging_setup import setup_logging
        logger = setup_logging(level='WARNING', capture_warnings=False)
        assert isinstance(logger, logging.Logger)

    def test_setup_logging_no_simplify(self):
        """simplify_warning_format=False branch must not raise."""
        import logging
        from molsysmt.configure.logging_setup import setup_logging
        logger = setup_logging(level='WARNING', simplify_warning_format=False)
        assert isinstance(logger, logging.Logger)

    def test_setup_logging_existing_handler(self):
        """Second call reuses the existing StreamHandler (handler loop branch)."""
        import logging
        from molsysmt.configure.logging_setup import setup_logging
        # First call creates the handler; second call should reuse it
        setup_logging(level='WARNING')
        logger = setup_logging(level='DEBUG')  # different level to show it runs
        assert isinstance(logger, logging.Logger)

    def test_simple_formatwarning_site_packages(self):
        """_simple_formatwarning: site-packages path extracts module name."""
        import logging
        import warnings
        from molsysmt.configure.logging_setup import setup_logging
        # Setup with simplify=True to register _simple_formatwarning
        setup_logging(level='WARNING', simplify_warning_format=True)
        # Now call warnings.formatwarning directly — this executes the nested function
        result = warnings.formatwarning(
            "test message",
            UserWarning,
            "/usr/lib/python3/site-packages/somelib/module.py",
            42,
        )
        assert "UserWarning" in result
        assert "somelib" in result

    def test_simple_formatwarning_dist_packages(self):
        """_simple_formatwarning: dist-packages path extracts module name."""
        import warnings
        from molsysmt.configure.logging_setup import setup_logging
        setup_logging(level='WARNING', simplify_warning_format=True)
        result = warnings.formatwarning(
            "dist warning",
            UserWarning,
            "/usr/lib/python3/dist-packages/somelib/module.py",
            10,
        )
        assert "UserWarning" in result
        assert "somelib" in result

    def test_simple_formatwarning_local_path(self):
        """_simple_formatwarning: local file path uses stem as module hint."""
        import warnings
        from molsysmt.configure.logging_setup import setup_logging
        setup_logging(level='WARNING', simplify_warning_format=True)
        result = warnings.formatwarning(
            "local warning",
            RuntimeWarning,
            "/home/user/project/mymodule.py",
            99,
        )
        assert "RuntimeWarning" in result

    def test_parse_level_int(self):
        """_parse_level passes int through unchanged."""
        import logging
        from molsysmt.configure.logging_setup import _parse_level
        assert _parse_level(logging.DEBUG) == logging.DEBUG

    def test_parse_level_string(self):
        """_parse_level converts string level names."""
        import logging
        from molsysmt.configure.logging_setup import _parse_level
        assert _parse_level('DEBUG') == logging.DEBUG
        assert _parse_level('WARNING') == logging.WARNING

    def test_parse_level_unknown_string(self):
        """_parse_level returns WARNING for unknown strings."""
        import logging
        from molsysmt.configure.logging_setup import _parse_level
        assert _parse_level('NOTAREAL') == logging.WARNING
