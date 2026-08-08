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

## A wider pattern behind these, found 2026-08-08

Fixing `molsysmt.MolSys -> openmm.System` (see
`convert_molsys_to_openmm_system_passes_the_wrong_topology.md`) exposed a defect of the
same family but a different mechanism, and looking for more of it found these cases again
from another angle.

A converter in `molsysmt/form/<plugin>/to_<target>.py` receives an `item` of **its own**
form. When it needs an intermediate it must call the sibling in its own directory -- the
converter that goes *from this form*. Reaching instead for the identically named converter
in the target's plugin passes the item to a function written for a different form. The
names match, so the mistake reads as correct.

`devtools/scripts/audit_converter_routing.py` searches for it statically: it resolves where
each imported name came from and reports a call whose first argument is literally `item`
when the callee came from another plugin. A converted `tmp_item` handed to another plugin
is normal and is not reported.

It currently reports **69 candidates**, of which **4 import from a plugin directory that
does not exist** -- the cases this report is about, plus one more:

```
file_psf/to_molsysmt_MolSysOld.py:14        to_molsysmt_TopologyOld   <- molsysmt_TopologyOld
openmm_PDBFile/to_molsysmt_MolSys.py:11     to_molsysmt_Topology      <- molsysmt_TopologyOld
openmm_PDBFile/to_molsysmt_MolSys.py:12     to_molsysmt_Structures    <- molsysmt_StructuresOld
pdbfixer_PDBFixer/to_biopython_Seq.py:9     to_string_aminoacids1     <- string_aminoacids1
```

**A candidate is not a verdict.** Two forms can be compatible enough that reusing a
converter is deliberate, so the remaining 65 need reading before anything is changed. That
is why this is a devtools script and not a test yet: turning it into one now would leave
the suite red with 69 failures and no way to tell the real ones from the deliberate ones.

The end state is a fourth entry in `tests/test_form_plugin_conventions.py`, with whatever
survives triage carried as an explicit baseline -- the same shape as
`test_converter_imports_resolve.py` already uses here.

### A static triage was tried and does not work

The obvious way to turn the 69 candidates into verdicts is to compare the callee's
`@arg_digest(form=...)` against the calling plugin's form: if the callee declares it takes
an `openmm.Topology` and the caller's `item` is a `molsysmt.MolSys`, that is a defect
without needing to run anything.

It was implemented and it fails. The check calls **all 69** inconsistent -- including
conversions that demonstrably work:

```
string:pdb_text -> molsysmt.MolSys     works, and is flagged
string:pdb_text -> openmm.Topology     works, and is flagged
string:pdb_text -> molsysmt.Topology   works, and is flagged
```

Zero consistent out of 69, against code that passes its tests, means the premise is wrong:
`form=` in the decorator does not declare the form of the converter's `item`. It appears to
name the plugin's own form, for resolving digesters. Whatever it means, it cannot
discriminate here.

**So there is no static verdict available with what the code currently declares.** The one
real defect of this family found so far -- `MolSys -> openmm.System` -- was found by
*running* a conversion, not by reading imports. That is the honest lesson: the audit script
generates leads, and the way to confirm a lead is to attempt the conversion.

Which points at the cheaper path: the 29 forms still in `UNREACHED` in
`tests/basic/test_get_form_battery.py` are exactly the conversions nobody exercises.
Closing those is likely to surface the remaining defects of this family the same way the
first one surfaced, with a real diagnosis instead of a suspicion.
