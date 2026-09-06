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
