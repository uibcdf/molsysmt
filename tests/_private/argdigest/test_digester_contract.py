"""
Structural contract of the argument digesters.

A digester has exactly two outcomes: it returns the digested value, or it raises. These
tests hold the whole `argument/` tree to that shape, rather than one module at a time,
because both defects they guard against were single modules that broke a rule the other
390 kept.
"""

import ast
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "molsysmt"
DIGESTION_ROOT = PACKAGE_ROOT / "_private" / "argdigest"


def _returned_call_name(node):
    if not isinstance(node, ast.Call):
        return ""
    if isinstance(node.func, ast.Name):
        return node.func.id
    return getattr(node.func, "attr", "")


def test_no_digester_returns_the_error_it_should_raise():
    """An error that is returned is not raised.

    It becomes the digested value of the argument and reaches the function body as if
    the user had passed it, which is how `digest_method` accepted every value for as
    long as it existed. See uibcdf/molsysmt#209.
    """
    offenders = []

    for source_file in sorted(DIGESTION_ROOT.rglob("*.py")):
        tree = ast.parse(source_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Return) or node.value is None:
                continue
            if _returned_call_name(node.value).endswith("Error"):
                relative = source_file.relative_to(PACKAGE_ROOT)
                offenders.append(f"{relative}:{node.lineno}")

    assert offenders == []


def test_every_attribute_has_a_digester():
    """An attribute with no digester module is not validated at all: it is accepted
    whatever its type, answered as if it were a flag, and warned about on every
    legitimate call. See uibcdf/molsysmt#208.

    Module presence plus a callable of the expected name is the floor this can check
    structurally; whether a given digester refuses the right values stays with the
    behavioural tests for that digester.
    """
    from importlib import import_module

    from molsysmt.attribute import attributes

    missing = []
    for attribute in sorted(attributes):
        try:
            module = import_module(f'molsysmt._private.argdigest.argument.{attribute}')
        except ModuleNotFoundError:
            missing.append(attribute)
            continue
        if not callable(getattr(module, f'digest_{attribute}', None)):
            missing.append(attribute)

    assert missing == []


def test_a_string_that_is_not_a_quantity_is_refused_as_an_argument():
    """The unit registry's own exception must not reach the caller.

    An unparseable string used to leave these digesters as pint's `UndefinedUnitError`,
    while a bare number left them as `ArgumentError`: the same class of bad input arrived
    as two different exception types, and the one that escaped named pint rather than the
    argument. See uibcdf/molsysmt#203.

    The set is discovered from the source, so a digester that starts parsing quantity
    strings is covered the day it is written.
    """
    from importlib import import_module

    from molsysmt._private.smonitor import ArgumentError

    argument_root = DIGESTION_ROOT / "argument"
    parsers = [
        path.stem
        for path in sorted(argument_root.glob("*.py"))
        if path.stem != "_quantity_parsing"
        and ("parse_quantity_string(" in path.read_text(encoding="utf-8")
             or "puw.parse.parse(" in path.read_text(encoding="utf-8"))
    ]
    assert parsers, "no quantity-parsing digester was discovered"

    escapes = {}
    for name in parsers:
        digester = getattr(import_module(f"molsysmt._private.argdigest.argument.{name}"),
                           f"digest_{name}")
        try:
            digester("definitely-not-a-unit", caller=None)
        except ArgumentError:
            continue
        except Exception as error:  # noqa: BLE001 - the point is which type escapes
            escapes[name] = type(error).__name__
        else:
            escapes[name] = "returned instead of raising"

    assert escapes == {}
