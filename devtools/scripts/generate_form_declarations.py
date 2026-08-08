#!/usr/bin/env python
"""
generate_form_declarations.py

Writes `form.json` into every `molsysmt/form/<plugin>/` directory.

A form's identity -- its name, its category, and the class of the items it holds -- lives
inside the plugin module today, so learning it means importing the plugin, and the
registry needs all of them to exist at all. Asking anything about forms therefore imports
89 plugins and the third-party libraries behind them: measured at 3.9 s and 1123 modules
for a single `get_form` call on a string.

`form.json` puts the same facts where they can be read without executing anything:
`os.scandir` plus 89 small reads, measured at 2 ms. The declaration stays in the form's own
directory, next to the code it describes.

This script imports the plugins once, offline, to write those files. Nothing at runtime
does. `tests/test_form_plugin_conventions.py` fails if a declaration stops matching its
module, so the two cannot drift apart.

Usage:
    python devtools/scripts/generate_form_declarations.py --write
    python devtools/scripts/generate_form_declarations.py --check
"""
import argparse
import json
import os
import sys
import warnings

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

FORM_ROOT = os.path.join(REPO_ROOT, "molsysmt", "form")


def item_class_key(form_name):
    """The `(top-level module, class name)` an item of this form is expected to have.

    Form names encode the class they hold -- `openmm.Topology` is an
    `openmm.app.topology.Topology`, `mdtraj.Trajectory` is a
    `mdtraj.core.trajectory.Trajectory`. Deriving the key from the name rather than from a
    hand-written class path keeps it from drifting, and the key is compared as *strings*,
    so recognising an item never imports the library that defines its class.

    None when the form is not identified by a class: a file, a string, or a form whose
    name is not a dotted class path.
    """

    if form_name.startswith(('file:', 'string:')) or '.' not in form_name:
        return None
    parts = form_name.split('.')
    return [parts[0], parts[-1]]


def declaration(module, form_name):
    entry = {
        'form_name': form_name,
        'form_type': module.form_type,
    }
    if module.form_type == 'file':
        entry['extension'] = form_name.split(':', 1)[1]
    key = item_class_key(form_name)
    if key is not None:
        entry['item_class_key'] = key
    return entry


def collect():
    from molsysmt.form import _dict_modules

    declarations = {}
    for form_name, module in _dict_modules.items():
        directory = module.__name__.rsplit('.', 1)[-1]
        declarations[directory] = declaration(module, form_name)
    return declarations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the declarations")
    parser.add_argument("--check", action="store_true", help="fail if any drifted")
    args = parser.parse_args()

    warnings.filterwarnings("ignore")
    declarations = collect()

    drifted = []
    for directory, entry in sorted(declarations.items()):
        path = os.path.join(FORM_ROOT, directory, "form.json")
        rendered = json.dumps(entry, indent=4, sort_keys=True) + "\n"
        try:
            with open(path) as handler:
                current = handler.read()
        except FileNotFoundError:
            current = None
        if current != rendered:
            drifted.append(directory)
            if args.write:
                with open(path, "w") as handler:
                    handler.write(rendered)

    if args.write:
        print(f"Declarations written: {len(drifted)} changed, {len(declarations)} total")
        return 0

    if args.check and drifted:
        print(f"FAILED: {len(drifted)} declarations no longer match their module:")
        for directory in drifted:
            print(f"  {directory}")
        print("Run: python devtools/scripts/generate_form_declarations.py --write")
        return 1

    print(f"OK: {len(declarations)} declarations match their modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
