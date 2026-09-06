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


# Three forms cannot satisfy the contract without a decision that is not this test's to
# make: the two mechanics forms have no element axis, and the sequence form indexes by
# group everywhere in its module, not by atom. They raise TypeError through `msm.extract`
# today. Listed rather than skipped, so the debt is visible and any *new* breach fails.
EXTRACT_CONTRACT_DEBT = {
    'molsysmt_MolecularMechanics',
    'molsysmt_MolecularMechanicsDict',
    'string_amino_acids_3',
}


def test_every_form_extract_accepts_the_dispatch_contract():
    """`basic.extract` calls every form the same way, so every form must accept it.

    `molsysmt/basic/extract.py` dispatches with `atom_indices`, `structure_indices`,
    `copy_if_all` and `skip_digestion`. A form whose `extract` declares anything else
    raises `TypeError` for every call, including the default one -- which is what
    `molsysviewer.MolSysView` did with the public signature instead of the form-level
    one, and `molsysmt.StructuresDict` did without `skip_digestion`.
    See uibcdf/molsysmt#204.
    """

    import ast

    required = {'item', 'atom_indices', 'structure_indices', 'copy_if_all', 'skip_digestion'}

    offenders = {}
    for path in sorted(FORM_ROOT.glob('*/extract.py')):
        form = path.parent.name
        if form in EXTRACT_CONTRACT_DEBT:
            continue
        for node in ast.parse(path.read_text()).body:
            if isinstance(node, ast.FunctionDef) and node.name == 'extract':
                missing = required - {argument.arg for argument in node.args.args}
                if missing:
                    offenders[form] = sorted(missing)

    assert offenders == {}
