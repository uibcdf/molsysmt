"""Conventions a form plugin must follow, enforced so they cannot quietly erode."""

import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FORM_ROOT = REPO_ROOT / 'molsysmt' / 'form'

_PACKAGE_ATTRIBUTE_IMPORT = re.compile(
    r'^\s*from (?:molsysmt\.form\.[A-Za-z0-9_]+|\.\.[A-Za-z0-9_]+) import to_[A-Za-z0-9_]+',
    re.M)


def test_converters_are_imported_from_their_own_submodule():
    """`from molsysmt.form.<form> import to_x` is ambiguous, so it is not allowed.

    A form declares its converters lazily, by submodule name, so that importing the form
    does not import every conversion it can perform. Importing `<form>.to_x` binds the
    *submodule* as an attribute of the form package, shadowing the function of the same
    name -- so `from <form> import to_x` yields the function or the module depending on
    whether some earlier conversion happened to load it. That is a bug that appears far
    from its cause.

    `from molsysmt.form.<form>.to_x import to_x` always means the function.
    """

    offenders = {}
    searched = [p for root in ('molsysmt', 'tests')
                for p in (REPO_ROOT / root).rglob('*.py')]
    for path in searched:
        found = _PACKAGE_ATTRIBUTE_IMPORT.findall(path.read_text())
        if found:
            offenders[str(path.relative_to(REPO_ROOT))] = found

    assert not offenders, (
        'these import a converter as a package attribute, which may hand back the '
        f'submodule instead of the function: {offenders}')


def test_no_plugin_imports_its_converters_eagerly():
    """A form's `__init__` must not import the converters it declares.

    Importing one form used to pull in the third-party libraries behind every conversion
    it can perform. The converters are named as strings in `_convert_to` and resolved by
    `molsysmt.form.load_converter` when a conversion actually happens.
    """

    eager = re.compile(r'^from \.(to_[A-Za-z0-9_]+) import \1\s*$', re.M)

    offenders = {}
    for path in sorted(FORM_ROOT.glob('*/__init__.py')):
        found = eager.findall(path.read_text())
        if found:
            offenders[path.parent.name] = found

    assert not offenders, f'form plugins importing converters eagerly: {offenders}'


def test_declared_converters_can_be_resolved():
    """Every name in a `_convert_to` table resolves to something callable."""

    from molsysmt.form import _dict_modules, load_converter

    broken = []
    for form, module in _dict_modules.items():
        for target, converter in getattr(module, '_convert_to', {}).items():
            try:
                resolved = load_converter(module, converter)
            except Exception as error:                     # noqa: BLE001 - reported below
                broken.append(f'{form} -> {target}: {type(error).__name__}: {error}')
                continue
            if not callable(resolved):
                broken.append(f'{form} -> {target}: resolved to {type(resolved).__name__}')

    assert not broken, 'unresolvable conversions:\n' + '\n'.join(broken)
