"""
Every relative import inside `molsysmt/form/**` must name a module that exists.

Conversion functions are registered in `_convert_to` as function objects imported when
the form package is imported, so the catalogue only proves that the `to_*.py` module
itself imports. The imports those functions perform are function-local, so they are
resolved at call time. A `to_*.py` whose body imports a nonexistent sibling is
therefore indistinguishable from a working one until somebody calls it, and nothing
calls every registered edge.

The sweep below closes that gap statically. It is the acceptance test proposed in
`devguide/pending_bugs/form_conversions_importing_nonexistent_modules.md`.
"""

import pathlib
import re

import molsysmt as msm

FORM_ROOT = pathlib.Path(msm.__file__).parent / 'form'

RELATIVE_IMPORT = re.compile(r'^\s*from\s+\.(\w+)\s+import', re.MULTILINE)

# Conversions that are still broken, each one an advertised edge that raises
# ModuleNotFoundError when called. They are listed so that a new occurrence fails this
# test while the known ones stay visible; both need a converter written or the route
# changed, which are separate decisions recorded in the report named above.
KNOWN_BROKEN = {
    ('mdtraj_HDF5TrajectoryFile/extract.py', 'to_mdtraj_Trajectory'),
    ('molsysmt_Topology/to_nglview_NGLWidget.py', 'to_molsysmt_MolSys'),
}


def _unresolved_relative_imports():
    unresolved = set()
    for path in FORM_ROOT.rglob('*.py'):
        for match in RELATIVE_IMPORT.finditer(path.read_text()):
            name = match.group(1)
            if (path.parent / f'{name}.py').exists() or (path.parent / name).is_dir():
                continue
            unresolved.add((path.relative_to(FORM_ROOT).as_posix(), name))
    return unresolved


def test_no_new_relative_import_names_a_missing_module():
    new = _unresolved_relative_imports() - KNOWN_BROKEN
    assert not new, (
        'these modules import a sibling that does not exist, so the conversions '
        f'reaching them raise ModuleNotFoundError when called: {sorted(new)}')


def test_the_known_broken_baseline_has_not_been_fixed_silently():
    # The baseline is debt, not a permission. When one of these is repaired its entry
    # must be removed here, or the sweep stops guarding that file.
    fixed = KNOWN_BROKEN - _unresolved_relative_imports()
    assert not fixed, (
        'these entries of KNOWN_BROKEN now resolve and must be removed from the '
        f'baseline: {sorted(fixed)}')
