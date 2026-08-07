# Advertised conversions that raise `ModuleNotFoundError`

**Reported:** 2026-08-06, from MolSysViewer, while verifying which input objects
a viewer can accept.

**Status:** case 1 fixed on 2026-08-07; cases 2 and 3 remain open. The static sweep
proposed below landed with the fix as
`tests/form/test_converter_imports_resolve.py`, carrying the two remaining cases as
an explicit baseline: a new occurrence fails the suite, and repairing one of the two
requires removing its baseline entry.

## Summary

Three conversions are advertised as available by `msm.supported.conversions` and
raise `ModuleNotFoundError` when called. Each one is a `to_*.py` module that
imports a sibling module which does not exist in its form package.

One of the three was a **dead import**: the name it bound was never used, and
deleting the line was the whole fix. `file:prmtop → molsysmt.MolSys` now returns a
MolSys with 5207 atoms and zero structures, guarded by
`tests/form/file_prmtop/test_to_molsysmt_MolSys.py`.

The other two genuinely call the missing module, so they need the converter written
or the route changed, and each turns on a semantic decision this report does not
make. `molsysmt.Topology → nglview.NGLWidget` receives `coordinates` and `box` as
arguments and has to decide what showing a topology without coordinates means;
`extract` on an `mdtraj.HDF5TrajectoryFile` without an output filename has to decide
whether returning an in-memory `mdtraj.Trajectory` from a file-handle form is the
intended contract.

## Reproduction

Each line raises; the environment is the current working tree, Python 3.13.

```python
import molsysmt as msm

prm = msm.systems['pentalanine']['pentalanine.prmtop']
h5  = msm.systems['pentalanine']['traj_pentalanine.h5']

# 1
msm.convert(prm, to_form='molsysmt.MolSys')
# ModuleNotFoundError: No module named 'molsysmt.form.file_prmtop.to_molsysmt_Structures'

# 2
msm.extract(msm.convert(h5, to_form='mdtraj.HDF5TrajectoryFile'), selection=list(range(10)))
# ModuleNotFoundError: No module named
#     'molsysmt.form.mdtraj_HDF5TrajectoryFile.to_mdtraj_Trajectory'

# 3
msm.convert(msm.convert(prm, to_form='molsysmt.Topology'), to_form='nglview.NGLWidget')
# ModuleNotFoundError: No module named 'molsysmt.form.molsysmt_Topology.to_molsysmt_MolSys'
```

All three are declared available:

```python
from molsysmt.supported import conversions
conversions(from_form='file:prmtop',       to_form='molsysmt.MolSys').data      # True
conversions(from_form='molsysmt.Topology', to_form='nglview.NGLWidget').data    # True
```

## Affected public behavior

- **`file:prmtop` → `molsysmt.MolSys` is unreachable.** Any user handed a
  `.prmtop` cannot reach the library's central form. Downstream, MolSysViewer's
  `msv.new_view('…/pentalanine.prmtop')` fails with the same traceback, which is
  how this was found.
- **`extract` on `mdtraj.HDF5TrajectoryFile` fails whenever a selection is
  requested and no `output_filename` is given** — the in-memory branch, i.e. the
  interactive one.
- **`molsysmt.Topology` cannot be shown in NGLView.**

## Severity

Reachable from the public API with default arguments, on forms the catalogue
advertises. No data corruption and no silent wrong answer: the failure is loud
and immediate. Case 1 costs one deleted line; the other two are real gaps.

## Likely cause

Two conventions combine, and neither is wrong on its own:

1. Conversion functions are registered in `_convert_to` as **function objects**
   imported at form-package import time, so the catalogue only proves the
   `to_*.py` module itself imports.
2. Inner imports inside those functions are **function-local**, so module
   resolution is deferred to call time.

The result is that a `to_*.py` file whose body imports a nonexistent sibling is
indistinguishable, from the catalogue's point of view, from a working one. Only
calling it reveals the difference, and nothing calls all of them.

`molsysmt/form/file_prmtop/to_molsysmt_MolSys.py` also shows the dead-import
variant: line 8 imports `to_molsysmt_Structures`, the name is never used —
the body builds an empty `Structures()`, with a comment explaining that a prmtop
carries topology only — and `git log` shows the module never existed in that
package. Executing the body without that line returns a correct MolSys: 5207
atoms, 0 structures.

## Acceptance tests

1. **A static check, which finds all three in under a second.** Every relative
   import inside `molsysmt/form/**` must resolve to a module or package that
   exists:

   ```python
   import pathlib, re

   root = pathlib.Path("molsysmt/form")
   broken = []
   for path in root.rglob("*.py"):
       for match in re.finditer(r"^\s*from\s+\.(\w+)\s+import", path.read_text(), re.M):
           sibling = path.parent / f"{match.group(1)}.py"
           if not sibling.exists() and not (path.parent / match.group(1)).is_dir():
               broken.append((str(path.relative_to(root)), match.group(1)))
   assert not broken, broken
   ```

   Today it returns exactly the three cases above. As a test it is cheap enough
   to run always, and it covers every future `to_*.py` without enumerating them.

2. **Regression tests calling the three conversions**, since the static check
   proves importability and not correctness: `file:prmtop → molsysmt.MolSys`
   should yield a MolSys with the prmtop's atom count and zero structures;
   `extract` on an `HDF5TrajectoryFile` with a selection and no output filename
   should return the filtered trajectory; `molsysmt.Topology →
   nglview.NGLWidget` should build a widget.

3. Optionally, the stronger form of the same idea: a test that walks every entry
   of every `_convert_to` and asserts the target is callable *and* that its
   inner imports resolve. That closes the gap between "the catalogue says True"
   and "calling it works", which is the actual defect class here.

## Notes

Fixing case 1 alone restores a whole input format and unblocks MolSysViewer for
Amber users; it does not depend on the other two. Cases 2 and 3 are separable
and may deserve their own decisions — in particular, case 3 may be better solved
by routing `molsysmt.Topology → nglview.NGLWidget` through an existing path than
by adding a new `to_molsysmt_MolSys` to that package.
