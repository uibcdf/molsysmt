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
