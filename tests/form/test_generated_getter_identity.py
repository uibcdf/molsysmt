"""Identity contracts for getter functions generated with ``exec``."""

from importlib import import_module
from pathlib import Path

import pytest

from molsysmt._private.smonitor import ArgumentError


GENERATED_GETTER_MODULES = (
    'molsysmt.form.MDAnalysis_Topology.get_topological_attributes',
    'molsysmt.form.file_molsys_yaml.get_structural_attributes',
    'molsysmt.form.file_molsys_yaml.get_topological_attributes',
    'molsysmt.form.file_structures_yaml.get_structural_attributes',
    'molsysmt.form.file_structures_yaml.get_topological_attributes',
    'molsysmt.form.file_topology_yaml.get_topological_attributes',
    'molsysmt.form.molsysmt_MolSysDict.get_structural_attributes',
    'molsysmt.form.molsysmt_MolSysDict.get_topological_attributes',
    'molsysmt.form.molsysmt_TopologyDict.get_topological_attributes',
)

FORM_ROOT = Path(__file__).resolve().parents[2] / 'molsysmt' / 'form'


def test_exec_based_form_generators_seed_the_module_name():
    offenders = []
    for path in FORM_ROOT.rglob('*.py'):
        source = path.read_text(encoding='utf-8')
        if 'exec(source, namespace)' not in source or '@arg_digest' not in source:
            continue
        if "'__name__': __name__" not in source and '"__name__": __name__' not in source:
            offenders.append(path.relative_to(FORM_ROOT).as_posix())

    assert offenders == []


@pytest.mark.parametrize('module_name', GENERATED_GETTER_MODULES)
def test_generated_getters_carry_their_defining_module(module_name):
    module = import_module(module_name)
    offenders = {
        name: getattr(module, name).__module__
        for name in module.__all__
        if getattr(module, name).__module__ != module.__name__
    }

    assert offenders == {}


def test_generated_getter_diagnostics_name_the_real_caller():
    module = import_module(
        'molsysmt.form.molsysmt_TopologyDict.get_topological_attributes'
    )

    with pytest.raises(ArgumentError) as caught:
        module.get_atom_id_from_atom(object())

    assert caught.value.extra['caller'] == (
        'molsysmt.form.molsysmt_TopologyDict.get_topological_attributes.'
        'get_atom_id_from_atom'
    )
