"""Protect selective loading and host dispatch through the provider registry."""

import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _run_case(script):
    result = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(script)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout


@pytest.mark.parametrize(
    "target", ["molsysmt.MolSys", "MOLSYSMT.MOLSYS", "molsysmt.structure"]
)
def test_cold_public_conversion_excludes_unrelated_adapters(target):
    _run_case(
        f"""
        import importlib.abc
        import sys
        import molsysmt as msm
        from molsysmt.form import _dict_modules, catalogue

        class UnrelatedAdapterSentinel(importlib.abc.MetaPathFinder):
            hits = []
            prefixes = ('molsysmt.form.file_dcd', 'molsysmt.form.file_sdf',
                        'molsysmt.form.rdkit_Mol', 'molsysmt.form.mdtraj_Trajectory')
            def find_spec(self, fullname, path=None, target=None):
                if any(fullname == prefix or fullname.startswith(prefix + '.')
                       for prefix in self.prefixes):
                    self.hits.append(fullname)
                    raise AssertionError('An unrelated adapter was requested: ' + fullname)

        sentinel = UnrelatedAdapterSentinel()
        sys.meta_path.insert(0, sentinel)
        names = tuple(_dict_modules)
        assert 'molsysmt.MolSys' in names
        assert catalogue.forms_lowercase()['molsysmt.molsys'] == 'molsysmt.MolSys'
        assert _dict_modules.loaded_keys() == ()
        molsys = msm.convert('molsysmt/data/pdb/181l.pdb', to_form={target!r})
        assert msm.get(molsys, n_atoms=True) == 1441
        assert msm.get(molsys, n_structures=True) == 1
        assert sentinel.hits == [], sentinel.hits
        assert not any(name == prefix or name.startswith(prefix + '.')
                       for name in sys.modules for prefix in sentinel.prefixes)
        """
    )


def test_registry_override_removal_and_manual_identity_reach_host_dispatch():
    _run_case(
        """
        from types import ModuleType
        import molsysmt as msm
        from molsysmt.form import _dict_modules, catalogue
        from molsysmt._private.argdigest.argument.to_form import digest_to_form
        from molsysmt._private.form_tier import FORM_TIERS

        original = catalogue.module_of('file:pdb')
        replacement = ModuleType(original.__name__)
        replacement.form_name = 'file:pdb'
        replacement.form_type = 'file'
        replacement.is_form = lambda value: value == 'probe.pdb'
        _dict_modules['file:pdb'] = replacement
        assert catalogue.module_of('file:pdb') is replacement
        assert msm.get_form('probe.pdb') == 'file:pdb'
        del _dict_modules['file:pdb']
        assert catalogue.module_of('file:pdb') is None
        assert 'file:pdb' not in catalogue.forms_lowercase()
        _dict_modules['file:pdb'] = original
        assert catalogue.module_of('file:pdb') is original

        class RegisteredToken:
            pass
        manual = ModuleType('molsysmt.form.registered_token')
        manual.form_name = 'registered.Token'
        manual.form_type = 'class'
        manual.is_form = lambda value: isinstance(value, RegisteredToken)
        _dict_modules[manual.form_name] = manual
        # Host admission still requires an explicit support tier.
        FORM_TIERS[manual.form_name] = 3
        assert catalogue.module_of(manual.form_name) is manual
        assert catalogue.form_type(manual.form_name) == 'class'
        assert digest_to_form('REGISTERED.TOKEN') == manual.form_name
        assert msm.get_form(RegisteredToken()) == manual.form_name
        del _dict_modules[manual.form_name]
        assert catalogue.module_of(manual.form_name) is None
        assert manual.form_name not in catalogue.forms_lowercase()
        """
    )


def test_adapter_failure_preserves_cause_and_requires_explicit_retry():
    _run_case(
        """
        import importlib.abc
        import sys
        import molsysmt as msm
        from molsysmt.form import _dict_modules, catalogue

        cause = ImportError('controlled adapter import failure')
        class FailingAdapter(importlib.abc.MetaPathFinder):
            calls = 0
            def find_spec(self, fullname, path=None, target=None):
                if fullname == 'molsysmt.form.file_pdb_gz':
                    self.calls += 1
                    raise cause
        failure = FailingAdapter()
        sys.meta_path.insert(0, failure)
        for operation in (
            lambda: catalogue.module_of('file:pdb.gz'),
            lambda: msm.get_form('probe.pdb.gz'),
        ):
            try:
                operation()
            except KeyError as error:
                assert error.__cause__ is cause
            else:
                raise AssertionError('A real adapter failure was hidden.')
        assert failure.calls == 1
        assert 'file:pdb.gz' in _dict_modules
        assert 'file:pdb.gz' not in _dict_modules.loaded_keys()
        sys.meta_path.remove(failure)
        try:
            catalogue.module_of('file:pdb.gz')
        except KeyError as error:
            assert error.__cause__ is cause
        else:
            raise AssertionError('An adapter failure retried implicitly.')
        _dict_modules.retry('file:pdb.gz')
        molsys = msm.convert('tests/form/file_pdb_gz/data/3PTB.pdb.gz',
                             to_form='molsysmt.MolSys', get_missing_bonds=False)
        assert msm.get(molsys, n_atoms=True) == 1701
        assert 'file:pdb.gz' in _dict_modules.loaded_keys()
        """
    )


def test_cold_concurrent_public_gzip_reads_preserve_independent_results():
    _run_case(
        """
        from concurrent.futures import ThreadPoolExecutor
        from threading import Barrier
        import hashlib
        from pathlib import Path
        import molsysmt as msm
        from molsysmt.form import _dict_modules

        path = Path('tests/form/file_pdb_gz/data/3PTB.pdb.gz')
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        assert _dict_modules.loaded_keys() == ()
        barrier = Barrier(4)
        def read():
            barrier.wait(timeout=10)
            return msm.convert(path, to_form='molsysmt.MolSys', get_missing_bonds=False)
        with ThreadPoolExecutor(max_workers=4) as pool:
            tasks = [pool.submit(read) for _ in range(4)]
            results = [task.result(timeout=90) for task in tasks]
        assert all(msm.get(result, n_atoms=True) == 1701 for result in results)
        assert all(msm.get(result, n_structures=True) == 1 for result in results)
        results[0].topology.atoms.iloc[0, 0] = 'independent-result'
        assert all(result.topology.atoms.iloc[0, 0] != 'independent-result'
                   for result in results[1:])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == before
        """
    )


@pytest.mark.parametrize("selection", ["all", [10, 1, 3]])
def test_legacy_and_declared_loaders_preserve_molecular_values(selection):
    _run_case(
        f"""
        import molsysmt as msm
        import molsysmt.form as forms
        from depdigest import LazyRegistry

        indexed_registry = forms._dict_modules
        indexed = msm.convert('molsysmt/data/pdb/181l.pdb',
                              to_form='molsysmt.MolSys', selection={selection!r},
                              get_missing_bonds=False)
        try:
            forms._dict_modules = LazyRegistry(
                'molsysmt.form', forms.current_dir, attr_name='form_name')
            legacy = msm.convert('molsysmt/data/pdb/181l.pdb',
                                 to_form='molsysmt.MolSys', selection={selection!r},
                                 get_missing_bonds=False)
        finally:
            forms._dict_modules = indexed_registry
        attributes = dict.fromkeys(
            ['atom_index', 'atom_id', 'atom_name', 'atom_type',
             'group_index', 'group_id', 'group_name', 'bonded_atom_pairs',
             'bond_order', 'formal_charge', 'coordinates', 'box', 'time'], True)
        assert msm.compare(indexed, legacy, include_none=True, **attributes)
        expected = 1441 if {selection!r} == 'all' else 3
        assert msm.get(indexed, n_atoms=True) == expected
        """
    )
