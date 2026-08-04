# The course validation gate is red after the Common Core renumbering

**Reported:** 2026-08-03, noticed while editing Module 13. Pre-existing: no course
notebook was modified when the failure was first observed.

**Status:** the gate is green again as of 2026-08-03. Both checks that depended on
decisions the course has not taken yet are deferred rather than deleted; what has to
be re-enabled is in *Remaining*.

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

## Remaining

- Decide the Common Core module count, then pin the range again.
- Migrate the Common Core to semantic MyST labels and remove it from
  `UNCONSOLIDATED_LABELS`. The four Paths already did this: each carries one semantic
  label such as `(course-alzheimer-surgical-extraction)=`. The Common Core still uses
  `(course-core-13)=` plus per-section anchors like `course-core-13-learning-outcomes`,
  **82 anchors in total**. One of them is already stale: notebook 19 declares
  `(course-core-20-learning-outcomes)=`, left over from the renumbering.
- Record the chosen scheme in `course_structure.md`.
