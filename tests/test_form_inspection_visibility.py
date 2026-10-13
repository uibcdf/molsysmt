"""Keep optional adapter inspection separate from scientific engine availability."""

import subprocess
import sys
import textwrap

import pytest


@pytest.mark.parametrize("show_all", [False, True])
def test_public_form_inspection_preserves_absent_engine_visibility(show_all):
    script = textwrap.dedent(
        f"""
        from unittest.mock import patch
        from depdigest import DepConfig, is_installed, temporary_package_config
        from depdigest.core import checker
        import molsysmt as msm
        from molsysmt import _depdigest
        from molsysmt._private.smonitor import LibraryNotFoundError
        from molsysmt.native import MolSys

        original = checker.find_spec
        def absent_rdkit(name, *args, **kwargs):
            if name == 'rdkit':
                return None
            return original(name, *args, **kwargs)

        configuration = DepConfig(
            libraries=_depdigest.LIBRARIES,
            mapping=_depdigest.MAPPING,
            show_all_capabilities={show_all!r},
            exception_class=LibraryNotFoundError,
        )
        with patch.object(checker, 'find_spec', absent_rdkit):
            is_installed.cache_clear()
            with temporary_package_config('molsysmt', configuration):
                assert not is_installed('rdkit')
                available = msm.supported.forms().data['Form'].tolist()
                assert ('rdkit.Mol' in available) is {show_all!r}
                assert 'molsysmt.MolSys' in available
                if {show_all!r}:
                    # Inspecting an adapter is not permission to execute its engine.
                    try:
                        msm.convert(MolSys(n_atoms=2), to_form='rdkit.Mol')
                    except LibraryNotFoundError:
                        pass
                    else:
                        raise AssertionError('Absent RDKit did not refuse scientific conversion.')
        print('inspection visibility and execution refusal verified')
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    assert (
        result.stdout.strip() == "inspection visibility and execution refusal verified"
    )
