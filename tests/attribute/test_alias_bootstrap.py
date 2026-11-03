"""Exercise alias admission in fresh processes without a primed decorator cache."""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "first_module",
    (
        "molsysmt._private.argdigest.normalization.attribute_synonyms",
        "molsysmt._private.argdigest.normalization.get_element_names",
        "molsysmt._private.argdigest.domain.attribute",
        "molsysmt._private.argdigest.native_queries",
        "molsysmt.attribute",
        "molsysmt.attribute.get_argument_aliases",
        "molsysmt.attribute.bonds_are_required_to_get_attribute",
        "molsysmt.native.queries",
        "molsysmt.basic",
    ),
)
def test_alias_contract_is_complete_independently_of_first_import(first_module):
    script = f"""
from importlib import import_module
import_module({first_module!r})
from argdigest import ArgumentConsistencyError, UnknownArgumentError
import molsysmt as msm
from molsysmt.native import Topology

try:
    msm.get(None, atom_names=True, atom_name=False)
except ArgumentConsistencyError:
    pass
else:
    raise AssertionError('Alias and canonical names must collide before execution')

try:
    msm.get(None, not_a_real_attribute=True)
except UnknownArgumentError:
    pass
else:
    raise AssertionError('Unknown keywords must remain rejected')

topology = Topology(n_atoms=2)
topology.atoms['atom_name'] = ['left', 'right']
assert msm.get(topology, element='atom', atom_names=True) == ['left', 'right']
assert msm.get(topology, element='atom', name=True) == ['left', 'right']
assert topology.get(element='atom', atom_names=True) == ['left', 'right']
assert topology.get(element='atom', name=True) == ['left', 'right']
assert callable(msm.attribute.bonds_are_required_to_get_attribute)
assert msm.attribute.bonds_are_required_to_get_attribute('n_bonds') is True

catalog = import_module('molsysmt.attribute.attributes')
catalog.add_attribute('bootstrap_probe', synonyms=['bootstrap_probe_alias'], topological=True)
assert msm.attribute.is_attribute('bootstrap_probe')
assert msm.attribute.attributes['bootstrap_probe']['topological'] is True
assert msm.attribute.get_argument_aliases()['attribute_synonyms']['bootstrap_probe_alias'] == 'bootstrap_probe'
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
        timeout=45,
    )
    assert result.returncode == 0, (
        f"Cold import failed after {first_module}:\n{result.stdout}\n{result.stderr}"
    )
