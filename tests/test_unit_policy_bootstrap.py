"""Preserve an existing Pint registry while adopting an otherwise absent policy."""

import json
import subprocess
import sys

import pytest


@pytest.mark.parametrize("mode", ["cold", "used_without_policy", "active_application"])
def test_cache_setup_is_effective_and_preserves_existing_registry(mode):
    program = r"""
import importlib, json, sys, warnings
import pyunitwizard as puw
mode = sys.argv[1]
puw.configure.set_pint_registry_cache(False)
original = None
if mode != 'cold':
    original = puw.quantity(1.0, 'nm', form='pint')
if mode == 'active_application':
    puw.configure.set_standard_units(['angstrom'], provenance='application')
assert puw.configure.has_active_policy() is (mode == 'active_application')
before_cache = puw.configure.get_pint_registry_cache()
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter('always')
    importlib.import_module('molsysmt._pyunitwizard')
after = puw.quantity(1.0, 'nm', form='pint')
cache_warnings = [str(item.message) for item in caught if 'set_pint_registry_cache' in str(item.message)]
assert not cache_warnings, cache_warnings
if original is not None:
    assert after._REGISTRY is original._REGISTRY
    assert puw.configure.get_pint_registry_cache() == before_cache
else:
    assert puw.configure.get_pint_registry_cache() is not None
report = puw.configure.report()
if mode == 'active_application':
    assert report['provenance'] == 'application'
    assert 'angstrom' in report['standard_units']
    assert abs(puw.get_value(puw.standardize(after)) - 10.0) < 1e-12
else:
    assert report['provenance'] == 'molsysmt'
    assert 'nm' in report['standard_units'] and 'radians' in report['standard_units']
assert 'nanometers' in report['fast_tracks']
assert puw.get_value(after, to_unit='nm') == 1.0
print(json.dumps({'mode': mode, 'cache_warnings': cache_warnings}))
"""
    result = subprocess.run(
        [sys.executable, "-c", program, mode],
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout.splitlines()[-1])["mode"] == mode
