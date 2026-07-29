# Course Module Renumbering and Stable-Identifier Scheme

**Status:** resolved and archived on 2026-07-29. F1 implemented the recommended
20-module Common Core and four Paths numbered 21–54, with stable semantic labels,
a manifest, complete toctrees, and executable structural validation.
**Relates to:** `devguide/pending_bugs/course_module_numbering_overlaps.md` (Confirmed),
`devguide/documentation_sync.md` (lifecycle contract), audit finding **B2** in
`devguide/archive/release_1_0/release_1_0_independent_gate_audit.md`.

This is a concrete resolution scheme for the course-numbering defect. It proposes an
end state and a mechanical migration; it does not modify any file.

## 1. Problem — a three-layer inconsistency, not just an overlap

The curriculum lives in `docs/content/course/` as a Common Core plus four Paths. Three
layers disagree about how many core modules exist and what they are called:

| Layer | What it says | Evidence |
|---|---|---|
| Top course page | "50-module odyssey", "Common Core (Modules **1–16**)", "Choose Your Path (Modules **17–50**)" | `docs/content/course/index.md` lines 3, 20, 28 |
| Common-Core index toctree | **16** modules, with **stale filenames** (`01_Philosophy_and_Forms.ipynb`, `02_Visualizing_Anything.ipynb`, … `16_Semantic_Labeling.ipynb`) | `docs/content/course/00_Common_Core/index.md` toctree |
| Filesystem (source of truth for content) | **20** core notebooks with different, current names (`01_The_Form_Agnostic_Philosophy.ipynb` … `20_The_Specialized_Domains.ipynb`); each Path has **34** notebooks numbered **17–50** | `ls docs/content/course/00_Common_Core/*.ipynb` |

Two concrete failures follow:

1. **Number collision.** Because the core grew to 20 (01–20) while every Path still
   starts at 17, display numbers **17, 18, 19, 20 name two different notebooks**:

   | # | Common Core (disk) | Every Path (disk) |
   |---|---|---|
   | 17 | `Semantic_Labeling` | `Surgical_Extraction` |
   | 18 | `Merging_and_Growing_Systems` | `Structural_Auditing` |
   | 19 | `Surgical_Extraction_and_Removal` | `Structural_Repair` |
   | 20 | `The_Specialized_Domains` | `Peptide_Synthesis` |

2. **Toctree references nonexistent documents.** `00_Common_Core/index.md` lists 16
   filenames that **do not exist on disk** and omits the four real notebooks 17–20. The
   non-existence is confirmed statically (the referenced names are absent from the
   directory); the **exact effect on the Sphinx build is not yet verified** and must be
   established by an actual `sphinx-build` run before any categorical claim (Sphinx may
   error, warn-and-drop, or behave differently depending on configuration).

Real curriculum size (excluding `.ipynb_checkpoints/`): **156 notebooks** = 20 core +
4 × 34 path. The checkpoints (**18** files under `.ipynb_checkpoints/`) are **not
versioned content** — they are matched by `.gitignore` (`git check-ignore` confirms it) —
so they must be excluded from every count and validator. A raw `find` returns 174 only
because it counts those ignored checkpoint copies.

## 2. Recovered design intent

A learner completes the Common Core once, then picks **one** Path and continues to the
end. For the "continue" step to read as one journey, the first Path module must follow
the last core module. The original intent (`index.md`) was core = 16, Paths = 17–50
(a 50-module journey). The core was later expanded to 20 without renumbering the Paths
or updating either index. The four added core notebooks (Semantic Labeling, Merging &
Growing, Surgical Extraction & Removal, Specialized Domains) are **general** topics that
belong in the core, not in a single Path — so the expansion is legitimate and should be
kept.

## 3. Recommended end state

**Adopt two layers: a continuous display number (for the journey narrative) and a
stable canonical identifier (for links and lifecycle tooling).**

### 3a. Display numbering — Option A (recommended): core = 20, Paths = 21–54

Keep all 20 core notebooks as 01–20. Renumber every Path notebook **17–50 → 21–54**
(a uniform **+4** shift). The journey becomes 20 + 34 = **54 modules**; update
`index.md` wording from "50-module" / "Modules 1–16" / "Modules 17–50" to
"54-module" / "Modules 1–20" / "Modules 21–54".

- Pure mechanical shift; no content is written, merged, or deleted.
- Preserves the continuous-journey feel (core 1–20 → path 21–54).

Rejected alternative — **Option B (core = 16)**: shrink the core back to 16 by folding
notebooks 17–20 into earlier modules. This honors the current `index.md` numbers but
**destroys or merges four deliberately-written notebooks** and needs editorial judgment
per notebook. Higher risk, content loss; not recommended.

### 3b. Canonical identifiers — required regardless of Option A/B

A section-scoped positional id (`core-01`, `alzheimer-01`) is **not** truly stable: its
numeric suffix is still a position, so reordering modules within a section changes it and
it stops identifying the same content. The canonical id must be **semantic and
permanent** — derived from the module's subject, not its position:

```
course-core-form-agnostic-philosophy
course-core-native-forms-and-the-trinity
course-core-semantic-labeling
course-alzheimer-surgical-extraction
course-alzheimer-structural-auditing
course-enzyme-structural-auditing
course-antiviral-pdb-frontier
course-biophysics-molecular-mechanics
```

Rules for the slug: `course-<section>-<topic>`, lowercase, hyphen-separated, derived from
the notebook's **title/subject** (not its filename number), unique across the whole
course, and **never changed once assigned** even if the title is later reworded (the slug
is an identity, not a display string). Reordering or renumbering a module does not change
its slug.

This identity layer has three parts, and **the manifest alone does not stabilize links**
— the label in the notebook is what `{ref}` resolves to:

1. **MyST/Sphinx target label in each notebook.** The first Markdown cell of every module
   declares a label immediately before its top heading, e.g.:

   ```markdown
   (course-alzheimer-surgical-extraction)=
   # Surgical Extraction
   ```

   (`myst_parser` with the `colon_fence`/heading-anchor setup already used by the course;
   the `(label)=` form is the portable MyST target syntax.)

2. **Internal cross-references use the label, never a number or filename.** Replace prose
   like "as in Module 17" and any direct relative link to a numbered notebook with a MyST
   role:

   ```markdown
   see {ref}`course-core-semantic-labeling`
   ```

   `{ref}` resolves through the label, so display renumbers and file renames never break
   the link. (`{doc}` by path is the fallback only where a whole-document link is needed;
   it must point at the current path and be updated on rename.)

3. **A manifest** recording, per module, the tuple **`(id, path, display_number,
   section, title)`** — see §4a. The manifest is the machine-readable index for lifecycle
   tooling and for validating that every declared label exists and is unique; it is
   **not** the link-resolution mechanism (that is the in-notebook label + `{ref}`).

## 4. Two distinct tasks

Correction from review: a uniform +4 shift is **not** the whole job. Two tasks with
**separate scope and closure criteria** must not be conflated. Task M (below) is the
mechanical migration this proposal authorizes for execution. Task E (§4c) is a
pre-existing editorial-correctness problem that a +4 shift does **not** fix and that must
be tracked and closed on its own.

### 4a. Task M — mechanical migration (Option A)

1. **Path files:** for each of the four Path directories, `git mv` `NN_Name.ipynb` →
   `(NN+4)_Name.ipynb` for `NN` in 17..50 (process in descending order to avoid transient
   collisions). Result: `17_Surgical_Extraction.ipynb` → `21_Surgical_Extraction.ipynb`,
   …, `50_Final_Project.ipynb` → `54_Final_Project.ipynb`.
2. **Path index toctrees** (`0X_Path_*/index.md`): update every entry to the new number.
3. **Common-Core index toctree** (`00_Common_Core/index.md`): **regenerate from disk** so
   it lists the actual 20 files with current names (it currently lists 16 stale names).
4. **Top course page** (`index.md`): "50-module" → "54-module"; "Modules 1–16" →
   "Modules 1–20"; "Modules 17–50" → "Modules 21–54". **README** course section: same.
5. **Path-internal display references affected by +4:** update literal "Module NN"
   mentions and path links inside Path notebooks that point to a *shifted Path module*.
   This is the mechanical half only; see Task E for references that are already wrong.
6. **Declare the MyST label** (§3b.1) in each of the 156 notebooks and **switch the
   references touched in steps 4–5 to `{ref}`** (§3b.2), so the migration lands the
   stable-identity layer rather than merely re-shifting fragile numbers.
7. **Create the manifest** (§4b) covering all 156 modules.

Steps 1 are `git mv`; steps 2–5 are bounded text edits; step 6 adds one label line per
notebook and converts the touched links; step 7 generates one file. No module content is
rewritten.

**Checkpoints are not part of this task.** The 18 `.ipynb_checkpoints/` files are
`.gitignore`d, non-versioned local artifacts. They may optionally be removed as local
cleanup (`git clean`-style), but this is **not** a substantial part of the change and
must never appear in the commit. Every counter, toctree generator, and validator in this
proposal must exclude `*/.ipynb_checkpoints/*` explicitly.

### 4b. Manifest schema

One machine-readable file, e.g. `docs/content/course/course_manifest.yml`, one entry per
module:

```yaml
- id: course-alzheimer-surgical-extraction   # semantic, permanent (§3b)
  path: 01_Path_Alzheimer/21_Surgical_Extraction.ipynb
  section: alzheimer                          # core | alzheimer | enzyme | antiviral | biophysics
  display_number: 21                          # presentation only; may change on future renumbers
  title: "Surgical Extraction"
```

The manifest records the tuple `(id, path, display_number, section, title)`. It is the
validation index and the lifecycle-tooling key (it feeds the future
`documentation_lifecycle_manifest.md`); per §3b it is **not** the link-resolution
mechanism — the notebook label plus `{ref}` is.

### 4c. Task E — editorial reference review (separate, pre-existing)

A superficial audit already shows internal references that are wrong **independently of
the +4 shift**, because the Common Core was renamed/expanded (16→20) without updating its
prose. Example: the stale index called the visualization notebook module 02, but on disk
it is `04_Visualizing_Anything.ipynb`; any prose that says "as in Module 2" for
visualization is already incorrect and a +4 Path shift does not touch it. Core notebooks
also carry "Module NN" prose (`grep -oE "Module [0-9]+"` across `00_Common_Core/*.ipynb`)
whose correctness predates this migration.

- **Scope:** all internal cross-references in the **Common Core** and any Path reference
  that was wrong *before* the migration (not merely off by +4).
- **Method:** resolve each reference to a module **by semantic id** (§3b) and rewrite it
  as `{ref}`; do not re-encode a corrected number.
- **Closure criterion:** no notebook contains a bare "Module NN"/filename cross-reference;
  every internal reference is a `{ref}` to an existing label; a link-check (or
  `sphinx-build -b linkcheck` for internal targets) reports zero unresolved course refs.
- **Tracking:** this is its own work item and must not be reported as done by completing
  Task M. Recommended: a checkbox/section in
  `course_module_numbering_overlaps.md`'s resolution, or a dedicated follow-up note.

## 5. Acceptance criteria (verifiable)

Correction from review: "every number maps to exactly one notebook across the whole
course" is **impossible and wrong** — display numbers 21–54 exist once *in each* of the
four Paths by design. The correct numeric contract is:

- **1–20 appear exactly once globally** (the Common Core);
- **21–54 appear exactly once per Path** (four occurrences each, one per Path);
- **each journey = Common Core + one Path = exactly 54 modules**, numbered continuously
  1..54 with no duplicate and no gap;
- **within any single section there are no repeated numbers and no gaps** (core is 1..20;
  each Path is 21..54).

Verification command (structural check, checkpoints excluded):

```bash
cd docs/content/course
NB() { find "$1" -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' \
        | sed -E 's|.*/0*([0-9]+)_.*|\1|' | sort -n; }

# Core must be exactly 1..20, no repeats, no gaps
diff <(NB 00_Common_Core) <(seq 1 20) && echo "core 1..20 OK"

# Each Path must be exactly 21..54, no repeats, no gaps
for p in 01_Path_Alzheimer 02_Path_Enzyme 03_Path_Antiviral 04_Path_Biophysics; do
  diff <(NB "$p") <(seq 21 54) && echo "$p 21..54 OK"
done

# A journey (core + one Path) must be a contiguous 1..54
diff <(cat <(NB 00_Common_Core) <(NB 01_Path_Alzheimer) | sort -n) <(seq 1 54) \
  && echo "journey 1..54 contiguous OK"
```

Remaining criteria:

- **Toctree ↔ disk agreement:** every entry in each section's `index.md` toctree resolves
  to an existing on-disk notebook, and no on-disk course notebook (checkpoints excluded)
  is missing from its section toctree.
- **Narrative agreement:** `index.md`, `00_Common_Core/index.md`, the four path indexes,
  and `README` agree on the ranges and totals (54-module journey; 20 core + 4×34 = 156
  notebooks; checkpoints excluded).
- **Sphinx:** an actual `sphinx-build` of the course reports **no "toctree contains
  reference to nonexisting document"** for the course tree. (This criterion presupposes a
  real build run; it is the point at which the currently *unverified* build effect is
  established.)
- **Identity layer:** every module declares its semantic MyST label (§3b.1); the manifest
  (§4b) lists all 156 with unique ids; every internal cross-reference touched by Task M
  is a `{ref}` (Task E closes the remainder).
- **Archival:** `devguide/pending_bugs/course_module_numbering_overlaps.md` moved to
  `devguide/archive/resolved_bugs/` **only after Task M is done and Task E has its own
  tracked closure** (Task M alone does not resolve the bug).

## 6. Cost, independence, regression risk

- **Cost:** low–medium for Task M (≈136 `git mv`, a few index regenerations, one label
  line per notebook, one manifest); Task E is a separate bounded editorial pass. No module
  content is rewritten in Task M.
- **Independence — not currently full.** Correction from review: the migration touches only
  `docs/content/course/` and `README` (no library code, no other subsystem), **but course
  notebooks are already modified in the working tree**. `git status --short
  docs/content/course` currently lists several changed notebooks. A `git mv` preserves
  those working-tree modifications, so a naive execution would **mix unrelated content
  edits into the renumbering commit**. Execution must therefore be done **either**:
  1. **after landing the WIP** that touches those course notebooks (clean tree for the
     course subtree), **or**
  2. with an **explicit, audited change selection** (e.g. stage only the renames and the
     index/label edits, review `git diff --staged` per file) that guarantees the commit
     absorbs no unrelated modification.

  Until one of those holds, the migration is **not** independent of the current WIP.
- **Regression risk:** none for code (untouched). The real risk is **stale links**: any
  external bookmark or reference to an old Path number breaks. Mitigation: land the
  semantic-label + `{ref}` layer (§3b) in the same change so internal links are
  renumber-proof, and add a short redirect note in each Path index for one release. Also
  ensure every validator/counter excludes `*/.ipynb_checkpoints/*` so cleanup state never
  affects results.

## 7. Scope note

This document is a proposal. It renames nothing and edits no course file; it specifies the
end state, the mechanical migration (Task M, §4a), the separate editorial-correctness work
(Task E, §4c), the semantic-identity layer (§3b), the manifest (§4b), and verifiable
acceptance (§5). Two things are **not** yet established and must not be asserted as done:

- the **exact Sphinx build effect** of the current stale toctree (statically confirmed
  nonexistent references; build behavior pending a real `sphinx-build` run);
- **Task E** — pre-existing incorrect internal references that a +4 shift does not fix.

Executing Task M closes the *numbering* half of audit finding B2 and the mechanical part
of `course_module_numbering_overlaps.md`; the bug is fully resolved only when Task E also
has a tracked closure. The other half of B2 — an actual executed pass over the Tier-1 core
notebooks to satisfy the `documentation_sync.md` lifecycle contract — remains separate and
is not part of this renumbering.

Execution readiness (per review): Option A is conceptually approved; the identity scheme,
manifest, MyST labels, and corrected acceptance are specified above. Before executing,
resolve the WIP-independence condition in §6 (the working tree currently has modified
course notebooks, including Path notebooks that Task M would rename).
