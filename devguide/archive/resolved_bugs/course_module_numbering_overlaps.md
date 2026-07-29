# Course Module Numbering Overlaps

**Status:** resolved and archived on 2026-07-29. The mechanical migration
(Task M), editorial pass (Task E), course-structure validator, and full Sphinx
confirmation are complete. Release stage F1 closed the structural contract;
release stage F4 closed the two remaining narrative references.

## Problem

`docs/content/course/index.md` and `README.md` describe a common core containing
modules 1–16. The filesystem contains 20 common-core notebooks numbered 01–20,
while every specialized path contains modules 17–50. Modules 17–20 therefore
have two meanings in the same curriculum.

The course contains 174 notebooks rather than a simple common 16 plus four
non-overlapping continuations.

## Impact

- lifecycle instructions cannot identify a module unambiguously;
- links and progress tracking can refer to different content;
- renumbering proposals and actual files disagree;
- students can receive conflicting sequence expectations.

## Required resolution

Choose the intended common-core boundary, define stable module identifiers that
do not depend only on display numbers, migrate filenames/indexes/cross-links,
and add a course-structure validator. Preserve redirects or an explicit mapping
if published links already exist.

## Resolution log — 2026-07-22

Resolved design and scheme:
`devguide/archive/resolved_proposals/course_module_renumbering_scheme.md`.
Approved direction: **Option A** — keep the Common Core at 1–20 and shift every Path
17–50 → 21–54 (+4). All work below was done in the working tree; **no commit was made**.

### Count correction

The curriculum is **156 notebooks** (20 core + 4×34 path), not 174. The extra 18 are
`.ipynb_checkpoints/` copies, which are `.gitignore`d, non-versioned, and must be
excluded from every count/validator. (The "174" and "1–16" figures in the Problem
section above were the original diagnosis; 156 is the verified content count.)

### Task M — mechanical migration (DONE, verified)

1. **Renamed 136 Path notebooks** `17–50 → 21–54` via `git mv` (Core 1–20 unchanged).
2. **Regenerated all index toctrees from disk.** The Common-Core `index.md` toctree had
   referenced 16 stale filenames that no longer exist (e.g. `01_Philosophy_and_Forms.ipynb`
   while disk has `01_The_Form_Agnostic_Philosophy.ipynb`); it now lists the real 20
   files. Path indexes list 21–54.
3. **Reconciled narrative wording** in `docs/content/course/index.md` and
   `docs/content/course/README.md`: "50-module"→"54-module", "Modules 1-16"→"Modules
   1-20", "Modules 17-50"→"Modules 21-54". Path index headers → "Modules 21 to 54.";
   Common-Core header → "Modules 1 to 20.".
4. **Updated 136 Path notebook H1 titles** `+4` (e.g. `Path A - Module 17:` → `Module 21:`).
   Core H1 numbers were already correct (verified: 0 mismatches).
5. **Stable semantic identifiers.** Added a permanent MyST label to **all 156 notebooks**
   immediately before the top heading, of the form `(course-<section>-<topic>)=`
   (e.g. `(course-alzheimer-surgical-extraction)=`). The slug is derived from the
   subject, not the position, so future reordering does not change identity. Internal
   cross-references should use `` {ref}`slug` `` (renumber-proof).
6. **Manifest** `docs/content/course/course_manifest.yml` records `(id, path, section,
   display_number, title)` for all 156 modules — the machine-readable index for
   validators and lifecycle tooling. It is not the link-resolution mechanism (the
   in-notebook label + `{ref}` is).

Notebook edits were made surgically via the notebook JSON so diffs are minimal; all 156
notebooks remain valid `nbformat`.

**Verification (all green):** Core numbers = exactly 1..20; each Path = exactly 21..54;
a Core+Path journey = a contiguous 1..54 with no gaps/duplicates; every `index.md`
toctree entry resolves to an existing file and no disk notebook is missing from its
toctree; every notebook's declared label is unique and matches its manifest id (156/156,
0 missing, 0 mismatch, 0 duplicate); `devtools/scripts/validate_devguide.py` passes.

The numeric contract is **not** "each number is globally unique": display numbers 21–54
appear once *per Path* by design. The verified contract is: 1–20 once globally; 21–54
once per Path; every journey contiguous 1..54; no repeats or gaps within a section.

### Task E — editorial reference pass (DONE)

Prose "Module NN" cross-references were audited (86 total; there are no `.ipynb` file
links). Two kinds:

- **Path forward/backward navigation (DONE).** In Path notebooks, body references to the
  old Path range 17–50 were shifted `+4` (69 references across 59 notebooks), e.g.
  `21_Surgical_Extraction`'s "In **Module 18**, … Structural Audit" → "**Module 22**".
  References ≤16 (to the Common Core) were left unchanged.
- **Pre-existing Common-Core errors — the ones with a certain target were CORRECTED.**
  Several core references were already wrong *before* this migration (a +4 shift does not
  fix them). Where the sentence context made the target certain, the number was corrected:
  - `00_Common_Core/04_Visualizing_Anything`: "explore its full syntax in **Module 3**" →
    **Module 5** (selection syntax = `05_Selection_Basics`). **FIXED.**
  - `00_Common_Core/10_Discovery_and_Attributes`: "In **Module 8**, … combine different
    files" → **Module 3** (`03_Combined_Sources`). **FIXED.**
  - `00_Common_Core/16_Comparing_Systems`: "In **Module 14**, wrap up … Semantic Labeling"
    → **Module 17** (`17_Semantic_Labeling`). **FIXED.**
  - `01_Path_Alzheimer/37_Interaction_Networks`: "labeling skills (from **Module 16**)" →
    **Module 17**. **FIXED.**

  Verified already-correct (no change): `02` ("Module 3" = compose from multiple sources),
  `09` ("Module 10" = Discovery), `13` ("Module 14: System Auditing"), plus the ten
  title-bearing references that were self-consistent.

- **The final two narrative items were resolved in F4:**
  - `00_Common_Core/12_Navigating_Between_Levels`: "In **Module 11**, we will … look at the
    1D world: **Sequences**." There is **no "Sequences" module** among the current 20 core
    notebooks. The orphaned promise was removed and the closing paragraph now links to
    `{ref}``course-core-iterating-over-hierarchies``, the actual next module.
  - `00_Common_Core/17_Semantic_Labeling`: "Pick your folder and open **Module 17** to
    continue your quest." A narrative artifact from the old 16-module core (module 17 used
    to be the Path start). It now directs the student to
    `{ref}``course-core-merging-and-growing-systems`` before choosing a Path.

**Closure criterion for Task E:** the two open items resolved (ideally rewritten as
`` {ref}`slug` `` to the intended module); a link check reports zero unresolved course
references.

### Sphinx build

The stale-toctree defect is resolved: toctree ↔ disk agreement is verified statically
for all five sections. On 2026-07-29, `make html` under `docs/` completed successfully
with `nb_execution_mode = "off"` and generated all HTML pages. The build reported 1,146
warnings from broader historical documentation debt; none invalidated the course
structure or the two semantic references closed here. That warning baseline is not
misrepresented as a warning-free documentation gate.

### Course-structure validator (DONE)

`devtools/scripts/validate_course.py` was added and passes. It asserts the numeric
contract (core 1..20; each Path 21..54; no gaps/dups), toctree↔disk agreement, unique
manifest ids matching each notebook's MyST label, and excludes `.ipynb_checkpoints`. It
imports nothing from MolSysMT and exits non-zero on any violation, so the structure
cannot silently regress. Current run: *"Course structure valid: 156 notebooks …"*.

### Closure evidence

- `python devtools/scripts/validate_course.py` validates all 156 notebooks, their
  numbering, toctrees, semantic labels, and manifest.
- Both final narrative links use stable semantic `{ref}` targets.
- `make html` completes and resolves the course structure into generated HTML.
- The course-structure contract remains in the fast release gate.
