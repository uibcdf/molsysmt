---
summary: The course validation gate disagrees with the manifest after the Common Core renumbering.
issue: uibcdf/molsysmt#142
status: resolved
opened: 2026-08-03
closed: 2026-08-12
severity: medium
verification: reproduced
area: [docs, ci]
guard: devtools/tests/test_validate_course.py::test_common_core_identity_and_numbering_are_fully_consolidated
normative: course_structure.md
blocked_by: []
supersedes: []
---

# The course validation gate is red after the Common Core renumbering

**Reported:** 2026-08-03, noticed while editing Module 13. Pre-existing: no course
notebook was modified when the failure was first observed.

**Status:** resolved on 2026-08-12. The Common Core is fixed at 20 modules, every
notebook uses its semantic manifest identifier as its MyST identity, and the gate
contains no exception for unconsolidated labels.

**Severity:** a release gate reports failure, so it can no longer detect a real
regression. The course content itself looks consistent; the checker and the
manifest are the parts that disagree with it.

## Symptom

```
$ python devtools/scripts/validate_course.py
Course structure validation FAILED:
  - 00_Common_Core: numbering [1, 2, 3]..[17, 18, 19] != expected 1..20 (gaps/dups/wrong range)
  - 00_Common_Core/01_The_Form_Agnostic_Philosophy.ipynb: label (course-core-01) != manifest id (course-core-the-form-agnostic-philosophy)
  ... 18 more of the same shape
```

20 errors, exit status 1.

## Two independent disagreements

**1. The expected module count was not updated.** `validate_course.py:28` declares

```python
"00_Common_Core": ("core", range(1, 21)),
```

but commit `c2520eba5`, *"merge Module 11 into Module 08 and renumber Common Core
to 19 modules total"*, left 19 notebooks on disk and 19 entries in
`docs/content/course/course_manifest.yml`. The manifest and the files agree with
each other; only the checker still expects 20.

**2. Labels and manifest ids use different schemes.** Every Common Core notebook
carries a numeric MyST label, `(course-core-13)`, while the manifest lists semantic
ids, `course-core-covalent-connectivity`. The checker compares the two directly, so
all 19 fail. Which scheme is intended has to be decided: the semantic ids were
introduced precisely so that renumbering would stop breaking cross-references, which
argues for the labels following the manifest.

## Why this matters beyond the noise

[`archive/resolved_bugs/course_module_numbering_overlaps.md`](../archive/resolved_bugs/course_module_numbering_overlaps.md)
was archived on 2026-07-29 recording that "the 156-notebook structural contract
remains guarded by `devtools/scripts/validate_course.py`". It is not being guarded
while the gate is red: a genuine numbering regression would be indistinguishable
from the current 20 errors.

## What was done

The Common Core module **count** is not settled — that is a decision about the course,
not a defect — so the gate no longer asserts one. Its numbering is still required to
run 1, 2, 3, ... with no gap and no duplicate; only the total is now whatever is on
disk. `SECTIONS["00_Common_Core"]` carries `None` instead of `range(1, 21)`, and the
four Paths remain pinned at 21..54.

The label check is deferred for the Common Core alone, through the explicit
`UNCONSOLIDATED_LABELS` set. Deferred, not dropped: the labels are still required to
exist and are now also checked for **uniqueness**, which the script did not do before
for labels at all.

`validate_course.py` now exits zero and reports 155 notebooks, 19 core plus 4x34
paths. The Paths, the toctrees, the manifest coverage and the id uniqueness are
checked exactly as before, so the gate can again detect a regression there.

## Resolution

The later course expansion restored the Common Core to 20 notebooks. The
resolution therefore pins `range(1, 21)` rather than preserving the temporary
variable-length rule.

All Common Core module, learning-outcome, and see-also labels now derive from the
semantic `id` already stored in `course_manifest.yml`. For example, Module 13 uses
`course-core-covalent-connectivity` rather than `course-core-13`. The matching
micro-governance files use the same permanent labels.

`UNCONSOLIDATED_LABELS` has been removed. The validator now requires exact label
agreement for every course section, in addition to the existing numbering,
toctree, manifest-coverage, and uniqueness checks. The durable identity and
numbering rules live in `course_structure.md`, and the regression test executes
the complete 156-notebook contract.
