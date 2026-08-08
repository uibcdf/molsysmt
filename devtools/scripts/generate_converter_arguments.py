#!/usr/bin/env python
"""
generate_converter_arguments.py

Writes the table `convert` is held to: the extra keywords each target form accepts.

`msm.convert(molsys, to_form=...)` forwards anything it does not recognise to the
converter it resolves, so the admissible set is whatever that converter accepts. There are
561 conversion edges, which is too many to keep by hand -- but the table itself is data,
committed and reviewable in a diff, not something computed while the library runs. This
script is what writes it.

Keyed by the target form only. The exact set depends on the pair (from_form, to_form), but
`from_form` is not an argument -- it has to be derived from the molecular system -- so the
table admits the union across origins. A keyword valid for a different origin is caught by
the converter itself a moment later, where the origin is known.

Usage:
    python devtools/scripts/generate_converter_arguments.py --write   # rewrite the table
    python devtools/scripts/generate_converter_arguments.py --check   # fail if it drifted
    python devtools/scripts/generate_converter_arguments.py --show    # print it
"""
import argparse
import inspect
import os
import sys
import textwrap
import warnings
from importlib import import_module

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

TABLE_PATH = os.path.join(
    REPO_ROOT, "molsysmt", "_private", "argdigest", "domain", "converter_arguments.py")

#: Accepted for every target: read by `convert` itself rather than by the converter.
ALWAYS = (
    'compression', 'compression_opts', 'float_precision', 'get_missing_bonds',
    'int_precision',
)

HEADER = '''"""The extra keywords `convert` forwards to the converter it resolves.

`msm.convert(molsys, to_form=...)` hands anything it does not recognise to the converter,
so what is admissible depends on the target form. This table says which keywords each
target accepts.

**Generated. Do not edit by hand.** Rewrite it with

    python devtools/scripts/generate_converter_arguments.py --write

and review the diff. `tests/test_argument_contract.py` fails if the file stops matching
the converters it was derived from, so a signature change shows up as a failing test with
a diff to apply, never as a silently wrong contract.

**Keyed by the target form only, deliberately.** The exact set depends on the pair
`(from_form, to_form)` -- for `file:pdb` alone there are six different sets depending on
where the conversion starts. But `from_form` is not an argument: deriving it from the
molecular system costs a significant fraction of the conversion itself, on every call.
Keying on the target admits the union across origins: 4.9 names on average where the exact
set averages 3.3. The comparison that matters is not 4.9 against 3.3, it is 4.9 against
*anything at all*. A mistyped keyword belongs to no union and is refused either way; what
gets through is a keyword valid for a different origin form, which the converter itself
rejects a moment later, where the origin is known.
"""

from argdigest import Domain

#: to_form -> the keywords some converter into that form accepts.
CONVERTER_ARGUMENTS = {
'''

FOOTER = '''}


domain = Domain(
    name='converter_arguments',
    depends_on='to_form',
    by_value=CONVERTER_ARGUMENTS,
    description='keywords the converters into a given target form accept',
)
'''


def derive():
    """Read the admissible keywords out of the converters' own signatures.

    A converter whose signature cannot be read is reported rather than skipped: every name
    it declares would leave the table, and `convert` would start refusing calls that are
    valid, blaming the caller for it.
    """

    from molsysmt.form import _dict_modules

    targets = {
        target
        for module in _dict_modules.values()
        for target in getattr(module, '_convert_to', {})
    }

    table = {}
    unreadable = []
    for to_form in sorted(targets):
        names = set(ALWAYS)
        for from_form, module in _dict_modules.items():
            converter = getattr(module, '_convert_to', {}).get(to_form)
            if converter is None:
                continue
            try:
                if isinstance(converter, str):
                    converter = getattr(
                        import_module(f'{module.__name__}.{converter}'), converter)
                names |= set(
                    inspect.signature(
                        getattr(converter, '__wrapped__', converter)).parameters)
            except Exception as error:                     # noqa: BLE001 - reported below
                unreadable.append((from_form, to_form, type(error).__name__, str(error)))
                continue
            names |= set(getattr(module, '_conversion_opt_kwargs', {}).get(to_form, ()))
        table[to_form] = tuple(sorted(names - {'item'}))

    return table, unreadable


def render(table):
    lines = [HEADER]
    for to_form, names in table.items():
        body = ', '.join(repr(name) for name in names)
        wrapped = textwrap.fill(
            body, width=92, initial_indent=' ' * 8, subsequent_indent=' ' * 8)
        lines.append(f"    {to_form!r}: (\n{wrapped}\n    ),\n")
    lines.append(FOOTER)
    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite the table")
    parser.add_argument("--check", action="store_true", help="fail if the table drifted")
    parser.add_argument("--show", action="store_true", help="print the table")
    args = parser.parse_args()

    warnings.filterwarnings("ignore")
    table, unreadable = derive()

    if unreadable:
        print(f"FAILED: {len(unreadable)} conversion edges have an unreadable signature.")
        for from_form, to_form, kind, message in unreadable:
            print(f"  {from_form} -> {to_form}: {kind}: {message[:80]}")
        return 1

    rendered = render(table)

    if args.show:
        for to_form, names in table.items():
            print(f"{to_form}\n    {', '.join(names)}")

    if args.write:
        with open(TABLE_PATH, "w") as handler:
            handler.write(rendered)
        print(f"Written: {os.path.relpath(TABLE_PATH, REPO_ROOT)}")

    if args.check:
        with open(TABLE_PATH) as handler:
            current = handler.read()
        if current != rendered:
            print("FAILED: the committed table no longer matches the converters.")
            print("Run: python devtools/scripts/generate_converter_arguments.py --write")
            return 1
        print("OK: the committed table matches the converters.")

    sizes = [len(names) for names in table.values()]
    print(f"Target forms: {len(table)} | keywords per target: min {min(sizes)}, "
          f"max {max(sizes)}, mean {sum(sizes) / len(sizes):.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
