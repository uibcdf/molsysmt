---
summary: Execute every declared conversion edge in the test suite, not only audit it statically.
issue: uibcdf/molsysmt#181
status: partial
opened: 2026-08-19
closed:
verification: measured
area: [form, convert, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Run the conversion graph, do not only describe it

**Reported:** 2026-08-19, from the post-mortem of
[`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180): seven public
conversion routes were broken for eleven days with every audit green.
**Status:** partial. The resident-native execution profile is implemented;
external/file/network profiles remain coverage debt.

## What

Generate one smoke case per declared conversion edge, over a small shipped system,
asserting only that the conversion completes and returns an object of the declared form.

Not fidelity. Not shapes, units, indexing or `None` semantics — those are the subject of
[Conversion Fidelity and MolSysDict v1](conversion_fidelity_and_molsysdict_v1.md) and are
a much larger claim. This proposal asserts the weakest useful property: **the route
runs**.

## How

The graph is already discoverable. `audit_conversion_fidelity.py` builds it from each
adapter's `_convert_to` map, and the same traversal can emit parametrised cases instead
of a coverage report.

The hard parts are not the traversal:

- **Which system to use per source form.** A `file:prmtop` case needs a prmtop; an
  `openmm.Topology` case needs coordinates supplied, as
  [`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180) showed. Some
  forms have no small shipped instance.
- **Soft dependencies.** Edges into `pdbfixer`, `parmed`, `MDAnalysis` and the rest must
  skip cleanly, not fail, when the dependency is absent.
- **Runtime.** `tests/form` already runs 6 772 tests in roughly 270 s on 14 workers.
  Adding up to 561 cases is not free, and some edges download or write files.

## Why

Measured on 2026-08-19:

| | |
|---|---|
| declared conversion edges | **561** |
| adapters declaring them | 92 |
| median edges per adapter | 5 |
| largest | `molsysmt_MolSys` 34, `file_pdb` 23, `string_pdb_id` 20 |
| `convert(` calls in `tests/` | 956 |
| distinct target forms named in `tests/` | 55 |

Coverage exists and is substantial. What does not exist is any statement about *which*
of the 561 edges it touches, so the answer to "is this route exercised?" is unknown
rather than yes or no.

**Both audits over this graph are static, and both say so.**
`audit_conversion_fidelity.py`: *"The compact baseline records accepted non-exhaustive
coverage debt; it is not a claim that those routes are fully verified."*
`validate_form_adapters.py`: *"This static reachability check does not prove correct
values, shapes, units, indexing, `None` semantics, conversion fidelity, decorator
correctness, or iterator output behavior."*

Neither is wrong. The gap is not a defect in either tool; it is that nothing closes it.

**What that cost.** In `e6b20c77c` (2026-08-08, 214 files, *"make a plugin's converters
lazy, and unambiguous to import"*), seven adapters acquired an import of the target
form's identity converter instead of their own. Seven public routes — `nglview.NGLWidget
-> openmm.Topology`, four out of `openmm.Topology`, two out of `string:alphafold_id` —
raised on every call. Both audits stayed green for eleven days.

A smoke case per edge would have failed on the introducing commit. It would also have
caught the two further defects found while fixing #180, neither of which needs fidelity
to detect: a `StringIO().read(text)` misuse raising `TypeError`, and an unguarded
`coordinates.shape[0]`.

## What is measured and what is assumed

Measured: every figure in the table above, by parsing the `_convert_to` dictionaries and
grepping `tests/`.

Assumed, explicitly: that most edges can be exercised from a shipped system. Not
checked — some forms may have no small instance, and that is precisely what a first
measurement pass should establish before any estimate is offered.

Not estimated: the effort. The 2026-08-19 conversation put a figure on a related idea
without measuring it and had to withdraw it; no figure is offered here.

## What was refuted

**A static check in `validate_form_adapters.py`, proposed as the guard for #180 and
withdrawn.** Two rules were tried. Flagging any absolute import of a converter that
shadows a local module produced 52 hits, most legitimate — `MDAnalysis_AtomGroup`
delegating to `MDAnalysis_Universe` is by design. Narrowing to *identity* converters
looked sharper and still flagged `file_h5msm` and `file_pdb`, whose target converters
deliberately accept a path; those routes were run and all succeed.

What separates the defect from the legitimate cases is whether the imported converter
tolerates a foreign item, which is behavioural and invisible to a static rule. That
failure is the argument for this proposal: the property in question only exists at run
time, so the check has to run.

## Scope and exclusions

In scope: one executable case per declared edge, asserting completion and returned form.

Out of scope:

- Fidelity of the converted content — [Conversion Fidelity and MolSysDict
  v1](conversion_fidelity_and_molsysdict_v1.md).
- Replacing either static audit. They answer a different question, cheaply, and should
  stay.
- Transitive routes. Only edges declared in a `_convert_to` map.

## Acceptance criteria

- Every declared edge is either exercised or explicitly listed as not exercisable, with
  the reason.
- The list may only shrink, in the idiom already used by
  `form_attribute_delivery_baseline.json` and `tier1_conversion_fidelity_baseline.json`.
- Missing soft dependencies skip; they do not fail.
- Introducing #180's defect again fails the suite.

## Provenance

MolSysMT at `bc42b2eaa`, 2026-08-19. Edge counts from the `_convert_to` dictionaries in
`molsysmt/form/*/__init__.py`; test counts from `tests/`; timing from
`pytest tests/form -n 14 --dist loadfile`.


## First executable profile — 2026-10-22

At baseline cdf7808e1, discovery reports 96 forms and 596 declared direct edges.
The new resident-native-v1 profile selects 41 edges among thirteen native and
dictionary forms. Each case executes the declared adapter with digestion enabled
and its public conversion route on fresh inputs. The two harness controls
reject callable exceptions and wrong output forms. The inventory audit is
explicitly non-executing and independent of capability visibility settings.

The other 555 edges are individually listed as accepted unexecuted debt for
this profile, with fixture/profile reasons. This is not a claim that no existing
adapter test exercises them, nor that they are impossible to execute. New routes
must be covered or explicitly accounted for; retired/newly covered debt fails
the audit until removed. The inventory has no automatic baseline rewrite route.

The first run found two genuine digest metadata defects, tracked and repaired
under uibcdf/molsysmt#418. Neither failing edge was skipped or removed from the
profile. Mirrored adapter regressions fail before the repair (four failed, two
passed) and preserve copy policy and foreign-form rejection after it.

```bash
python -m pytest tests/conversion_truth tests/form/molsysmt_MolecularMechanics tests/form/molsysmt_MolecularMechanicsDict devtools/tests/test_audit_conversion_execution.py --receptor=llm -n 12
```

Result: 194 passed, no skips, 17.77 seconds; four expected legacy H5MSM warnings.
Linux x86_64, Python 3.14.7, NumPy 2.4.6, pytest 9.1.1. Source development evidence,
not installed release qualification. The [operational guide](../conversion_execution.md)
records current commands, scope and expansion obligations. No fidelity or
scientific-accuracy guarantee follows from output-form smoke coverage.

Remaining work: source fixtures and executable profiles for external objects,
file/string formats and separately marked network identifiers, with honest
optional-dependency handling. #181 stays partial; #334 release coordination is
unchanged. The bounded block does not satisfy whole-graph execution acceptance.

Final combined regression on 2026-10-22 executes the scientific suite and registry
controls, conversion truth, mechanics adapters, inventory audit and real-takeaway
rendering controls: **587 passed**, zero skips/failures, 54.75 seconds, with twelve
workers and Pytest Receptor. Seven expected legacy H5MSM warnings remain. Command:

```bash
python -m pytest devtools/tests/test_validate_scientific_evidence.py devtools/tests/test_execute_scientific_evidence.py devtools/tests/test_audit_conversion_execution.py devtools/tests/test_course_takeaway_rendering.py tests/scientific_truth tests/conversion_truth tests/form/molsysmt_MolecularMechanics tests/form/molsysmt_MolecularMechanicsDict --receptor=llm -n 12
```

All fourteen fast release gates, full-package Ruff check and format verification
also pass. No new release matrix, artifact production or publication is implied.


## Resident MDTraj/OpenMM expansion — 2026-10-22

The next bounded profile extends both graph axes with `mdtraj.Topology`,
`mdtraj.Trajectory`, `openmm.Topology` and `openmm.Modeller`. The profile is now
`resident-native-engines-v2`: 70 declared edges (29 additional) and 526 explicitly
unexecuted edges, still within the 596-edge graph. Only newly covered edges were
removed from the debt inventory; no new exception or accepted failure was added.

External water inputs use each provider's own topology API and literal
three-atom coordinate arrays. Native inputs remain fresh four-atom systems.
Topology-only sources receive explicit unit-bearing coordinates for targets
that require geometry. Setup skips a provider-specific case only if the needed
optional package is genuinely unavailable; conversion exceptions propagate.
The direct/public reachability assertion is unchanged and does not certify
fidelity. The original thirteen-form native subset remains covered.

Execution found two broken cross-engine container routes and a nested topology
selection route, recorded under uibcdf/molsysmt#419. Investigating the otherwise
passing topology-to-trajectory route's unit-stripping warnings exposed silent
tenfold coordinate scaling for angstrom input, ignored atom selection and a
lost explicit cell, recorded under uibcdf/molsysmt#420. Neither defect was hidden
by excluding its edge. Mirrored conversion guards add physical values, selected
coordinates, source-order duplicate selection and box checks beyond the smoke
profile's weaker output-form promise.

The focused updated selection passes 100 cases without warnings. The independent
original #420 guards first produce six failures and two passing nanometer
controls; the original cross-engine guards produce eight failures. Nested subset
controls additionally reproduce two failures before correcting the source-form
import. These negative runs distinguish repaired runtime defects from broader
scientific or format-fidelity claims.

The conversion tutorial and Native Forms course module now explain full-source
coordinate axes, explicit units and the single-structure Modeller boundary.
Only Markdown source text changes: executable cells, saved outputs, execution
counts, notebook/cell metadata and cell IDs are identical to the baseline.
No full notebook re-execution is claimed for prose changes. The operational guide
is updated; #181 remains partial pending external/file/string/network profiles.

### Expanded qualification

The full relevant regression command and environment are retained in the
[receipt](../../devtools/data/conversion_execution_engines_20261022.json):
2,178 passed, zero skips/failures, 123.67 seconds. Ten existing dummy-PDB-cell
warnings and five legacy H5MSM notices remain. A separate final doctest passes.
The full documentation build exits 0 with 711 warnings and no errors, without
new warning families or a whole-site cleanup claim. All fourteen fast gates
and applicable Ruff check/format controls pass. MDTraj 1.11.1 and OpenMM 8.6.1
were already installed; no dependency version or installed environment changes.

The repaired defects are archived under their own issue identities. This
profile is a more useful execution baseline, not whole-graph completion:
526 edges still require profiles and fixtures, so #181 remains partial.
