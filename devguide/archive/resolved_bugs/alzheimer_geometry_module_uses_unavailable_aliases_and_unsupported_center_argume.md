---
summary: Alzheimer geometry module uses unavailable aliases and unsupported center arguments
issue: uibcdf/molsysmt#758
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: medium
verification: reproduced
area: [docs, structure]
guard: tests/documentation/test_alzheimer_geometry_examples.py
normative:
blocked_by: []
supersedes: []
---

# Alzheimer geometry module uses unavailable public calls

**Reported:** 2026-11-14 in the #334 geometry-example review, after finding
#757's independent endpoint-position reporting error.
**Status:** resolved; actual supported geometry, complete local execution and independent receiving are documented below.

## What

`docs/content/course/Path_Alzheimer/30_Geometrical_Measurements.ipynb`
calls `msm.get_distances`, `msm.get_minimum_distances` and `msm.get_angles`.
The current root lazy registry exports none of those aliases; their public
owner is `msm.structure`. The center-distance call also supplies
`center_of_selection=True`, which is absent from `get_distances`' signature;
its two endpoints use independent `center_of_atoms` flags.

The lesson assigns the minimum-distance tuple to one variable and calls it a
distance. Its narrative also suggests that geometry proves fit/affinity, even
though the setup simply merges a downloaded fibril and newly built peptide,
without an explicitly placed or qualified complex. Those explanatory claims
need correction, not a new docking or affinity algorithm.

## How

Read the actual nine cells against `molsysmt/__init__.py` and the public
structure signatures. The first obsolete call raises before the intended
measurement can occur. The setup requests live `pdb:2BEG`, so a full execution
has not been claimed from the current offline geometry cohort. Hard-coded
angle atoms and molecule-type selections also need checking against the actual
chosen system rather than being assumed to define the stated interface.

## Why

Readers cannot run the advertised measurement workflow on current MolSysMT.
Its scientific interpretation overstates what coordinate measurements establish.
This is admitted pre-1.0 documentation correctness work under #334, not the
post-1.0 missing micro-contract debt in #512.

## Proposed bounded correction

- Retain the fibril/peptide teaching context and all distance, closest-contact,
  angular and challenge scenarios; preserve existing anchors and figures.
- Use supported form-agnostic `msm.structure` tools with explicit independent
  endpoints, quantity handling and local-to-source index correspondence.
- Choose and document a deterministic input/placement strategy. Prefer suitable
  bundled data; if no faithful input exists, record the required bounded fixture
  and its provenance before adding it. Do not silently describe arbitrary merged
  coordinates as a docked or experimentally established complex.
- Explain that these are coordinate observables, without an affinity estimate,
  chemical-interaction assignment, binding proof or pose-quality validation.
- Execute the actual complete corrected lesson, inspect its numerical results
  independently and receive the rendered article.

## What is measured and what is assumed

The unavailable aliases and unsupported keyword are source-inspected. No live
PDB download, preparation, docking or full lesson execution has occurred in this
review. #757's separate 21-case geometry receiving and nine executed tool
notebooks do not qualify this course module.

## Acceptance criteria

The actual lesson runs on supported public calls, reports physically correct
quantities/axes/source indices, preserves its scientific scenarios and clearly
states the input and interpretation limits. A regression must exercise those
actual cells against independent coordinate/membership expectations; a token
rename or successful Sphinx build alone is insufficient.

## Provenance

Inspected on 6deb0200c plus the separate #757 documentation/test delta, on
2026-11-14. Runtime, providers, algorithms and the native binary are unchanged.

## Chosen input and placement plan — 2026-11-14

Retain 2BEG and KLVFF. RCSB identifies the entry as ten deposited NMR structures
of a five-chain fibril model (entry DOI 10.2210/pdb2BEG/pdb; original study
10.1073/pnas.0506723102). Bundle the unchanged compressed PDB download only as a
documentation resource, recording its download URL, raw/decompressed hashes and
retrieval date. Select structure index 0 explicitly; do not reconstruct missing
atoms or chemistry and do not classify it as a complete prepared simulation.

Build the same short peptide with the existing native builder. Place its
geometric center at an explicitly declared offset from the target center for
teaching only. Keep target/candidate memberships as explicit arrays after the
ordered merge; their classification as protein or peptide does not distinguish
those two populations. Use the central target chain only for the stated
center/angle examples. The minimum uses all deposited target atoms and maps
both returned endpoint positions. Select angle atoms by actual CA names and
explain the middle vertex. Receive independent Cartesian distances, centers,
angle and membership checks under ordinary and pm/fs unit policies, actual
fresh-kernel outputs and the rendered page. No docking, affinity calculation,
protonation protocol, minimization or new molecular API is added.

## Resolution — 2026-11-14

The original three calculation cells fail six controls on unavailable root
aliases. Their replacements use the validated public structure tools, two
independent center flags, an unpacked minimum result and separately mapped
source populations. The angle uses actual CA atoms and a declared middle
vertex. The group matrix first obtains atom-to-group membership because numeric
`get(element='group')` selections address groups, not atoms.

The unchanged RCSB compressed snapshot is 308,428 bytes, representing ten
structures and 18,550 ATOM records. Its adjacent record retains the exact URL,
compressed/decompressed hashes and original-study/entry DOIs. The lesson
selects structure index 0 (1,855 deposited atoms) and preserves those Cartesian
fields exactly. The added native KLVFF has 97 atoms and a declared 4-nm center
offset. It is an illustrative placement, not a docked/optimized complex or
chemical/affinity validation. The uneven atom_ff_type merge diagnostic remains
visible and is explained.

The final complete selected command passes **31 cases, zero skips**. Ten new
controls check independent Cartesian centers/minima, actual source pair/CA
memberships, the middle-vertex angle, unchanged deposited coordinates, complete
populations, the actual 5-by-26 matrix sent to Matplotlib and ordinary versus
pm/fs policies. One actual fresh Jupyter kernel executes all five code cells
and retains its figure. A strict complete Sphinx build produces 1,400 pages
without warnings. The actual article, six anchors, next-module link, identical
PNG payload and both unchanged downloadable fixture/provenance files are received.
The [receipt](../../../devtools/data/alzheimer_geometry_receiving_758_20261114.json)
retains original failures, full JUnit/receptor agreement, runtime hashes and
resource limits. All source/science acceptance claims keep that finite scope.

Initial authored corrections fail on a relative path, incorrect oracle element
and atom indices supplied on a group axis. They remain unsuccessful evidence;
these are not new library calculation defects. The final output adoption retains
all authored code/Markdown and cell IDs. The three original teaching scenarios,
challenge and existing top anchor remain, with precise interpretation and links.
The reviewed companion contract is specific to this lesson, not boilerplate for
#512's remaining authoring debt.

No public runtime API, scientific method, dependency, native binary, environment,
hosted matrix, package or tag changes. Existing public validation/dependency,
quantity/diagnostic and optional construction-attribution boundaries remain.
One-CPU/two-GiB services monitor a 6.5-GiB host reserve, with at most two own jobs
at once. Full-corpus, browser, installed/platform and exact-final-pair gates
remain separate. #759 owns the newly identified neighboring synthesis lesson;
#256/#615 and the publication pause are unchanged.
