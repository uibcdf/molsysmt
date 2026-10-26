---
summary: The documentation build carries a large accepted warning population that hides new warnings.
issue: uibcdf/molsysmt#144
status: partial
opened: 2026-07-29
closed:
severity: low
verification: measured
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Sphinx Warning Baseline and API Reference Debt

**Status:** confirmed documentation debt; accepted as non-blocking for the 1.0
source release after the F4 structural repairs.
**Found:** 2026-07-29 during a forced full Sphinx build.
**Scope:** generated API reference, legacy User Guide pages, course markup style,
orphan pages, and notebook metadata.

## Evidence

The forced build

```bash
cd docs
sphinx-build -E -q -b html -w /tmp/molsysmt-sphinx-warnings.log . _build/html
```

completed with exit code 0 and generated the HTML site. Its warning log contained
1,223 `WARNING:` records before the bounded F4 repairs. The largest tagged
families were:

| Family | Count | Meaning |
| --- | ---: | --- |
| `myst.header` | 423 | non-consecutive heading levels; 369 are in the course |
| `toc.no_title` | 350 | notebook targets without a usable title, often repeated |
| `toc.not_included` | 114 | source pages absent from every toctree |
| `myst.xref_missing` | 78 | unresolved legacy MyST links |
| `autodoc.import_object` | 50 | stale API objects |
| `myst.directive_unknown` | 32 | unsupported directives; 13 course occurrences use `key-takeaway` |
| `docutils` | 22 | malformed or inconsistent reStructuredText |
| `toc.not_readable` | 11 | references to source documents that did not exist |
| `ref.ref` | 4 | unresolved Sphinx labels |

Autosummary also reported 42 initial import failures and 49 generation-time
failures, dominated by form pages that still name a module-level `get` adapter
which the current form does not expose.

The full log is deliberately not committed: it contains absolute environment
paths and is reproducible from the command above.

## What F4 fixed

All 11 `toc.not_readable` cases found by the forced build were corrected:

- obsolete API entries for molecular dynamics, `thirds`, and oligosaccharides;
- a removed showcase membrane page;
- stale amino-acid, hydrogen-bond, structure, NGLView, and OpenMM-reporter
  notebook names.

An incremental Sphinx build after those repairs exited 0 and reported zero
`toc.not_readable` warnings. It also reported no unresolved course cross-reference
and no warning involving either of the semantic targets introduced in Common Core
12 and 17.

The Sphinx build regenerated ten checked-in autosummary pages for native and H5MSM
forms. Those changes expose current chemical-state, bond-metadata, and
thermodynamic getters/setters instead of preserving the stale generated lists.

## The published build was worse than this baseline, until 2026-08-08

Everything above measures the build produced by the command in **Evidence**, run by
hand. Until 2026-08-08 that was not the build being published.

`uibcdf/action-sphinx-docs-to-gh-pages` ran `sphinx-apidoc -o . ../` by default, and
the documentation workflow never disabled it. Reproduced against a scratch output
directory, that step generates **153 `.rst` files** — `modules.rst`, `conftest.rst`,
and one per subpackage — into `docs/`. None of them is in any toctree, so each was an
orphan page, built, published and counted as a warning the local baseline never saw;
autodoc also imported every module in the tree to render them. The published site
carried the result: `modules.html` and `molsysmt.basic.html` were reachable on
`www.uibcdf.org/molsysmt/`, a second API reference beside the curated one under
`docs/api/`, which nobody maintained.

The workflow now passes `sphinx-apidoc: false`, and version 3.0.0 of the action also
makes it the default. `modules.html` returns 404 on the published site as of
2026-08-08.

**Consequence for this report:** the local command and the CI build now measure the
same thing, so the inventory above is finally the inventory of what readers get. Any
ratchet built per the remediation plan should be measured once more before being
frozen — the `toc.not_included` and `autodoc.import_object` families are the two this
change touches, and neither has been re-counted since.

## Why this does not block 1.0

The release contract requires the course structure to be free of references to
nonexistent documents. That condition is now satisfied dynamically by Sphinx and
statically by `validate_course.py`. The remaining warnings are real quality debt,
but they do not change runtime correctness, API availability, scientific results,
or the resolved course navigation.

Making all 156 course notebooks warning-free, rebuilding the old form reference,
and deciding which orphan pages belong in the published navigation are separate,
potentially large editorial projects. Folding them into the release candidate
would delay the source release behind pre-existing documentation cleanup without
improving its scientific contract.

This is accepted debt, not a claim that the documentation is warning-clean.

## Remediation plan

Work by family and keep a ratcheted warning inventory:

1. generate form API pages from the discovered module surface, never from stale
   hand-maintained operation lists;
2. add a documentation validator that fails on a new warning family or count
   increase while allowing the recorded baseline to decrease;
3. repair unresolved public API labels and remove duplicate source identities;
4. decide whether each orphan User Guide page belongs in a toctree or should be
   archived;
5. add titles and stable semantic labels to published notebooks;
6. replace or register `key-takeaway`, then normalize course heading levels;
7. normalize notebook cell IDs before a future `nbformat` release makes their
   absence an error.

Each step should update the baseline by category. Do not solve the problem by
globally suppressing warnings.

## Closure criteria

- a forced clean Sphinx build emits no warnings;
- generated API pages name only importable current objects;
- every published page has an intentional navigation status;
- course directives and heading levels follow the documented MyST conventions;
- notebooks validate without missing-cell-ID compatibility warnings;
- CI rejects any reintroduced warning.

## Fresh shared Python 3.14 build — 2026-10-06

At source `5e2721691`, the shared development environment runs
`python -m sphinx -b html -q -j 12 docs <fresh-output-directory>` with Sphinx
9.1.0 and the actual configured extensions. It exits 0 and reports 781
`WARNING:` lines, five Docutils `ERROR:` lines and no missing course toctree
documents. Notebook execution remains disabled. Three generated autosummary
formatting rewrites were restored; executable notebook cells and saved outputs
were unchanged. The [receipt](../../devtools/data/stabilization_s5_shared_20261006.json)
records effective extension versions, the log hash and the error locations.

The five error lines arise from an unknown `yyy` target in the NGLView
`set_color_by_value` docstring, three undefined vector substitutions in the
`get_lengths_and_angles_from_box` docstring, and an invalid grid argument in the
legacy `content/user/tools/index_v2.md` draft. They are existing rendering debt
under this issue. Exit zero permits these Docutils errors and must not be
reported as error-free documentation. Counts from fresh and incremental builds
or different installed extensions are checkpoint observations, not a ratchet
comparison. This checkpoint satisfies the missing-course-document condition;
the broader closure criteria above remain unmet.

## Bounded box API repair — 2026-10-09

The three vector-substitution errors and associated definition-list warning in
`get_lengths_and_angles_from_box` are repaired under uibcdf/molsysmt#358. Its
[resolution record](../archive/resolved_bugs/box_geometry_documentation_misstates_units_and_fails_rendering.md)
retains a real one-page Sphinx HTML guard: original prose fails, corrected prose
renders without page diagnostics. Nondefault length/angle policy controls and
the public doctest also pass. This is a bounded API repair, not a fresh full-site
warning inventory; it does not close the other errors or the broader criteria
above. The initial checkpoint's counts remain historical evidence.

## Bounded NGLView API repair — 2026-10-09

Under uibcdf/molsysmt#361 the unknown `yyy` target is removed and the obsolete,
invalid public example is replaced by a local example using explicit NGLView.
The [resolution record](../archive/resolved_bugs/nglview_color_example_uses_obsolete_apis_and_fails_rendering.md)
retains an actual page-rendering and example-execution guard, existing color
regressions and one re-executed Toolbox notebook. The API page has no diagnostics;
this is not a new whole-site warning inventory. The legacy `index_v2.md` grid
error and broader warning/navigation debt remain under this issue.

## Bounded legacy Toolbox grid repair — 2026-10-09

The retained `content/user/tools/index_v2.md` draft supplies three grid-size
arguments, which Sphinx Design rejects: the directive requires one or four.
The actual card section fails its strict Sphinx/MyST rendering guard before the
repair. Four breakpoint values now retain one column on small displays, two on
medium and three on large displays. The guard
`devtools/tests/test_public_api_docs.py::test_legacy_toolbox_cards_render_without_directive_errors`
renders the source card content, rejects all page diagnostics and verifies the
responsive grid and endpoint cards in HTML. Its separate legacy navigation is
outside this bounded test; the draft is not newly admitted to published navigation.

All four API/documentation guard cases pass. Rendering applications now use
Sphinx's test application cleanup to avoid leaking global directive/node
registrations between serial tests. Six Python warnings remain separate
(Sphinx 11 deprecations and expected legacy H5MSM notices); they are not page
diagnostics. The five error locations named in the earlier checkpoint have
received bounded repairs, but no fresh full-site build or warning inventory is
claimed. Broader warning, navigation and API-reference debt remains open here.

## Notebook-schema checkpoint — 2026-10-13

The #385 HTML build exits 0 but prints twelve repeated JSON schema errors from
six untouched notebooks: Common Core 08/10/19, Biophysics 39 and basic get/set
tutorials. Their nbformat minor is 4 while cells contain IDs introduced for minor
5. The gzip tutorial and modified Module 01 are valid. A zero Sphinx exit does not
prove a clean build. This bounded schema repair remains pending within #144; it
is separate from gzip input correctness and requires preserving existing outputs.

## Bounded notebook-schema repair — 2026-10-13

The six notebooks in the preceding checkpoint declared nbformat 4.4 but contained
cell IDs, which that schema rejects. They now declare 4.5, retain their existing
IDs and assign missing IDs once. New IDs use the first sixteen hexadecimal digits
of SHA-256 over documentation-relative path, cell position and cell type; stored
IDs remain attached to their cells during subsequent edits. IDs are unique within
each notebook. No random identifiers, content rewrites or execution are involved.

The [receipt](../../devtools/data/notebook_schema_repair_20261013.json) records the
six paths, file hashes, schema versions, preserved/added ID counts and a hash of
the complete JSON payload excluding only nbformat_minor and per-cell id. A direct
comparison with the original files confirms that all other JSON values are
identical: source text and list/string representation, outputs, execution counts,
cell/notebook metadata and attachments. Existing code execution fingerprints and
saved outputs therefore remain applicable; this repair does not qualify the
legacy scientific examples afresh.

The guard `devtools/tests/test_documentation_notebook_schema.py` validates raw
stored JSON with nbformat, before any reader can normalize or repair it, and checks
that validation leaves the input unchanged. All six cases fail on the original
files and pass after repair. The schema cases plus the five notebook-executor
controls pass 11/11 using Python 3.14.7, twelve workers and pytest-receptor.

A focused Sphinx HTML project copies the actual six notebooks, uses MyST-NB and
the same notebook reader options, disables execution as in the site configuration,
and renders each page with its stored outputs. It exits 0 with no ERROR lines or
Notebook JSON is invalid diagnostics. Its 102 warnings include references to
pages absent from that isolated project and legacy course directives; this is
neither a full-site build nor a warning-baseline comparison. Sphinx 9.1.0,
MyST-NB 1.4.0 and nbformat 5.11.1 are recorded in the receipt. Course structure,
Ruff and developer-guide checks pass. The broader #144 closure criteria remain
open, with partial status unchanged.

## Bounded API-to-tutorial link repair — 2026-10-13

The earlier import-failure counts are historical observations. A fresh inventory
checks the 246 explicit autodoc declarations in current `docs/api/**/*.rst`
through Sphinx's `import_by_name`, honoring each page's `currentmodule`:
all resolve. This does not inventory every API role in notebooks or establish
full-site warning counts.

Three public docstrings still link to removed tutorial labels. They now point to
the actual stored notebook targets:

| Public function | Tutorial target |
|---|---|
| `molsysmt.form.get_attributes` | `Tutorial_Form_Get_attributes` |
| `molsysmt.form.has_attribute` | `Tutorial_Form_Has_attribute` |
| `molsysmt.build.solve_atoms_with_alternate_location` | `Tutorial_Solve_atoms_with_alternate_locations` |

The alternate-location tutorial also contained three Markdown API roles using
the nonexistent plural function name. Those roles now use the singular public
name, matching the existing executable examples. Its paired instructions record
that name while retaining the plural tutorial filename, title and stable label.
A complete JSON comparison confirms that only these three Markdown names change;
code, saved outputs, execution counts, cell IDs and metadata are preserved.
Common Core 12 and the affected PDB Frontier course examples already use the
singular API and need no changes for this repair.

The guard
`devtools/tests/test_public_api_docs.py::test_api_tutorial_links_resolve_to_actual_notebook_targets`
builds each real public docstring together with the introduction read from its
actual tutorial notebook and the actual Forms introduction. It does not inject
a replacement target. It checks the generated API-to-tutorial hyperlink and the
tutorial-to-API hyperlink; removing either real target or changing the public
function name fails. All three cases fail on the original docstrings with their
undefined labels and pass after repair, with empty Sphinx warning streams.

The complete public-API rendering selection passes **29 cases**, and all three
changed-module doctests pass, on Python 3.14.7 with twelve workers and
pytest-receptor. The wider selection retains Python-level Sphinx Napoleon
deprecations and three existing legacy H5MSM warnings. Focused Ruff and
developer-guide checks pass. The
[receipt](../../devtools/data/api_tutorial_links_repair_20261013.json) retains
versions, before/after outcomes and notebook hashes.

This is a repair of three API/tutorial boundaries, not a reexecution of the full
notebooks or a fresh full-site warning baseline. Runtime behavior and signatures
are unchanged; #144 remains partial and release coordination under #334 remains
paused. Remaining work follows the family-by-family remediation plan above.

## Bounded Common Core navigation repair — 2026-10-14

All twenty Common Core notebooks now link to the real Foundations target
`user-foundations-index`, replacing 26 references to the undefined
`user-foundations` target. The course template and contributor examples use the
same current target. Eleven links to removed notebook names are replaced with
semantic module references and accurate display names:

- Module 02 proceeds to Module 03, Molecular Elements; its transition now
  describes the atom/group/molecule hierarchy rather than Native Forms.
- Module 06 points to Module 08's attribute extraction, without promising a
  nonexistent Interactive Selection module.
- Modules 11, 13 and 17 use the actual Module 12, 14 and 18 identities.
- Module 15 points forward to composition in Module 17 in its narrative, while
  its sequential Next Module link correctly reaches Module 16.

The README and course instructions locate the Native Forms reference model in
Module 04 rather than a missing Module 02 file. Paired module instructions retain
their protected topics and use the current navigation identities.

The guard
`devtools/tests/test_validate_course.py::test_common_core_navigation_links_reach_real_module_and_foundations_targets`
renders actual stored module headings and navigation lines through MyST-NB,
with the real Common Core index and actual Foundations/selection-syntax headings.
The resulting HTML must contain a Foundations hyperlink in every Core module
and a Next Module hyperlink to the following notebook in the current order.
It uses no invented replacement labels. Replaying the final guard against the
original Git notebook content, without modifying the checkout, rejects 26
undefined Foundations references and eleven missing-module references: 37
Sphinx warning lines. The corrected project has an empty Sphinx warning stream.

The course/API/schema selection passes **37 tests** in 8.64 seconds on Python
3.14.7 with twelve workers and pytest-receptor. Python-level MyST/Sphinx
deprecations and existing H5MSM migration warnings remain visible in that
selection. The 156-notebook course validator, whole-repository Ruff lint and
format checks, and developer-guide validation pass. The
[receipt](../../devtools/data/course_navigation_repair_20261014.json) records
versions, the negative control, per-notebook hashes and preservation evidence.

Only Markdown source fields change in twenty Core notebooks and the template.
All other JSON, including code, saved outputs, execution counts, metadata,
cell IDs and attachments, is identical to the original. Semantic anchors and
filenames remain unchanged. This does not reexecute scientific examples or
certify complete notebook rendering or a warning-clean site. Generic portal
links for deeper topics in Native Forms still need semantic review; the guard
does not claim to verify those topic descriptions. The broader #144 closure
criteria remain unmet and release coordination under #334 remains paused.


## Bounded native links and course directive repair — 2026-10-22

A forced full-site HTML build on the development source based on cdf7808e1
reports 739 `WARNING:` records, zero `ERROR:` records and exit 0. This supersedes
neither the historical measurements nor their environment: it is a new baseline.

The repair redirects six nonexistent per-form reference paths in the native
Foundations pages to actual native-query and conversion/form API targets.
Paired instructions retain their protected topics and require real API targets.
It preserves all other page sections. The configured local `key_takeaway`
extension registers the course's existing directive as a standard Docutils
admonition with a default title. No notebook, stored output or heading changes;
no warning suppression. Its guard renders the actual twenty Common Core blocks,
the course template and Foundations block, comparing the parsed body and inline
content against standard admonitions. Without registration the negative control
reports the unknown directive and produces no admonition nodes. Both cases pass.

Developer testing docs also use the existing distance-test directory and current
Python 3.11–3.14 matrices, distinguish PR/push/scheduled checks and correct the
release/manual documentation deployment trigger. Maintainer CI-skip policy is
linked rather than reduced to general advice to skip prose commits. The generated
`get_vectors` API page is retained because the current structure autosummary
already declares it; unrelated generated formatting rewrites are restored.

```bash
python -m pytest devtools/tests/test_course_takeaway_rendering.py --receptor=llm -n 12
python -m sphinx -E -q -j 12 -b html -w /tmp/molsysmt-144-warnings-after.log docs /tmp/molsysmt-144-html
```

The clean full-site rebuild exits 0 with **711 warnings and zero errors**:

| Family | Before | After |
|---|---:|---:|
| myst.header | 411 | 411 |
| myst.directive_parse | 270 | 270 |
| myst.directive_unknown | 24 | 2 |
| toc.not_included | 17 | 17 |
| ref.doc | 6 | 0 |
| myst.xref_missing | 5 | 5 |
| misc.highlighting_failure | 4 | 4 |
| docutils | 1 | 1 |
| ref.ref | 1 | 1 |

The remaining unknown directives are `tabs` in the citation page and `info` in
Common Core 01. No broad course/header rewrite or global warning ratchet is
claimed. The proposed complete-warning closure criteria remain unmet, so #144
stays partial. Notebook execution is disabled in this build; rendering a block
is not a new scientific qualification of the notebook's executable examples.

Linux x86_64, Python 3.14.7, Sphinx 9.1.0, MyST-NB 1.4.0 and the current development
Viewer source; local source evidence, not installed release qualification.
The [receipt](../../devtools/data/documentation_warning_repair_20261022.json)
records sanitized counts, warning-log digests, versions and the rendering guard.


## Additional notebook-schema checkpoint — 2026-10-26

The full HTML build for the ParmEd bridge repairs (uibcdf/molsysmt#463 and
uibcdf/molsysmt#464) exits 0 but emits ten repeated notebook-schema ERROR
diagnostics from five other course notebooks: the four paths'
`34_Comparison_Superposition.ipynb` and Common Core
`16_Structural_Operations.ipynb`. Their stored cells contain IDs while the
notebooks still declare schema 4.4. They are outside the six-file raw-JSON guard
added on 2026-10-13; that bounded repair did not cover these five.

The newly edited ParmEd/MDTraj/Modeller pages, conversion Cookbook and Common
Core Module 01 are not the source of these schema errors. Their public examples
execute successfully, but the full-site command must not be described as clean.
Extend the existing schema guard and apply the same metadata-only 4.5 repair,
preserving every source cell and executed output, before clearing this debt.
The [ParmEd receipt](../../devtools/data/conversion_execution_parmed_20261026.json)
retains the observed exit, diagnostic count and scope. #144 remains partial.


## Source-wide notebook-schema guard and repair — 2026-10-26

The follow-up inventory reads every documentation source notebook as raw JSON,
not through a reader that can normalize metadata. It finds ten invalid sources:
six declare schema 4.4 while containing IDs, and four declare 4.5 while lacking
a cell ID. The first inventory also includes 21 local editor checkpoints; these
are excluded from the source guard. The actual guarded inventory is 491 notebooks:
490 under `docs/content/` and the homepage, with generated builds outside its scope.
The expanded guard initially fails ten cases and passes 481 in 7.26 seconds.

The six 4.4 notebooks now declare 4.5. All 84 existing cell IDs are retained, and
37 missing IDs are assigned using the same deterministic path/position/type hash
as the earlier repair. The [receipt](../../devtools/data/notebook_schema_repair_20261026.json)
lists the ten paths, pre/post hashes and unchanged payload hashes. Direct comparison
against HEAD verifies that every other JSON value is identical, including source
text and its list/string representation, saved outputs, execution counts, all
metadata and attachments. There is no execution or scientific requalification
of the examples in this metadata-only repair.

`tests/documentation/test_notebook_schema.py` brings the shared raw-JSON guard
into ordinary pytest discovery; the developer-tool entry point remains valid.
The guard discovers source paths instead of maintaining a whitelist of previously
repaired notebooks, so future sources are included automatically. It also checks
that validation has not repaired its input and that 4.5 cell IDs are unique.
The schema and executor controls pass **496/496**, with no failures or skips, in
7.21 seconds using twelve workers and Pytest Receptor. The maintained
[compilation guide](../notebook_compilation_and_visualization.md) records the
normal test command and source scope.

A forced full-site HTML rebuild exits zero, renders all ten repaired pages, and
emits **zero errors and zero notebook-schema diagnostics**. It retains 731 warnings:
428 `myst.header`, 271 `myst.directive_parse`, two `myst.directive_unknown`,
17 `toc.not_included`, five `myst.xref_missing`, four `misc.highlighting_failure`,
one `ref.ref`, one `ref.footnote` and two untagged warnings. This is a new source
checkpoint, not a controlled warning-count reduction against the October 22
checkpoint. Ruff lint/format and the fourteen fast gates pass. #144 remains partial
for its broader markup/navigation/reference debt; no clean-warning site, installed
package pair or release qualification is claimed.

## Additional source-schema repair — 2026-10-26

The property-query documentation build encountered three path-39 notebooks
with newly introduced cell IDs under schema 4.4. The raw source guard failed
three cases with 488 controls passing; Sphinx also emitted invalid-notebook
ERROR messages despite a successful process status. That run is not a clean
HTML qualification.

The Alzheimer's, antiviral and enzyme path notebooks now declare schema 4.5
and have 31 deterministic missing IDs assigned. Existing IDs, cell payloads,
outputs and execution metadata are preserved exactly. The paired payload
comparison and before/after hashes are retained in
[the query receipt](../../devtools/data/physchem_queries_20261026.json).
The raw schema guard then passes all 491 source notebooks. The broader warning
and reference debt remains open; no complete course or warning-free build is
claimed by these metadata-only repairs.
