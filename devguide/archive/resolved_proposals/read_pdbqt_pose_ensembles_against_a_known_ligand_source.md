---
summary: Read PDBQT pose ensembles against a known ligand source
issue: uibcdf/molsysmt#226
status: resolved
opened: 2026-09-22
closed: 2026-10-22
verification: measured
area: [form, convert]
guard: tests/form/file_pdbqt/test_known_source_poses.py
normative:
blocked_by: []
supersedes: []
---

# Read PDBQT pose ensembles against a known ligand source

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved for the documented experimental known-source profile; brought forward before 1.0 by the maintainer on 2026-10-22.

## What

Read multi-model docking PDBQT poses and place their coordinates on a known ligand molecular graph.

## How

Parse pose boundaries and atom records, require a source ligand plus explicit atom mapping or equivalent carried metadata, and reconstruct supported structures without guessing absent bond orders. Define how omitted hydrogen coordinates are represented: they remain explicitly unavailable, or a separate named reconstruction method generates them with provenance. Original input H coordinates must not be presented as if Vina returned them.

## Why

Docking output loses chemical information; a bare PDBQT pose cannot reliably regenerate the original ligand graph.

## What is measured and what is assumed

**Inspected:** Inspected the initial PDBQT proposal, which excludes multi-model output; Meeko export documentation describes preserved ligand metadata and mapping.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Inferring a complete chemical graph from each output PDBQT was rejected because bond orders and omitted carbon-bound hydrogens are absent.

## Scope and exclusions

Pose ensemble parsing and reconstruction against a known source; score/rank interpretation and experiment provenance belong to DockingMT.

## Acceptance criteria

- Representative multi-model outputs reconstruct atom-aligned ligand structures and preserve available pose coordinates.
- A missing or inconsistent source map produces a clear error; no unsupported chemistry is claimed as recovered.
- A pose with omitted hydrogens has an explicit, tested missing-coordinate or named-reconstruction outcome; no stale or invented H positions are silently reported as docked coordinates.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#8.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Provider prerequisite delivered — 2026-10-22

#223 now provides a public typed nonpolar-H transform and opt-in completed
PDBQT writer maps. Maps distinguish retained/merged/excluded source atoms and
actual written atom order/serials, including rooted traversal and full-input
selection axes. This is the prepared-source/export boundary needed here; it
does not implement a MODEL reader or recover omitted H coordinates. The next
reader must validate these declared axes against each model rather than infer
identity from positions or names. Earlier preparation-generated H keep their
separate source-history mapping.


## Implemented profile — 2026-10-22

`molsysmt.form.read_pdbqt_poses` owns specialized known-source pose I/O. Generic
PDBQT `convert`/`get` retain their existing single-system profile. The new public
boundary uses ArgDigest, accepts file/prefixed-text input and a form-agnostic
known source, and requires a completed `molsysmt.atom_export@1` writer map from
#223. No optional engine is required for a ready native source.

The reader validates balanced MODEL/ENDMDL boundaries, positive unique MODEL
labels, every supported single-body ROOT/BRANCH tree, finite fields and all
poses before returning a result. MODEL labels become string structure IDs,
never structure indices. Nonconsecutive selections, requested order/repetitions
and an empty structure selection are supported. Only selected coordinates are
retained; parsing/validation still visits all poses. This is a resident reader,
not a streamed trajectory execution contract.

Map validation checks source counts, inverse unique atom maps, ordered source
IDs/names/elements, a single complete state and its chemical digest. Every pose
must match written serials/names/elements, charges in explicitly declared
`elementary_charge`, available AutoDock labels and the exported tree. The writer
now also records `output_atom_ff_types`; older maps can use labels supplied by
the source. Atom identity/type fields cannot change between poses. The declared
map is not authenticated correspondence or a spatial matching algorithm.

Returned atoms follow sorted retained source indices. Only known chemical
inventory/state domains are detached and extracted; original coordinates and
analysis tables are not materialized or copied. New pose positions are converted
from angstroms to native nm through PyUnitWizard. Source boxes, time, observables,
interactions and MolecularMechanics are not inherited. Parsed written types and
charges remain explicit data in the optional report, not a newly certified
force-field assignment. No new scientific calculation is performed, so Ackredit
calculation tracking is inapplicable; the source writer/reader producer versions
are retained as provenance.

`missing_atoms='error'` is the default. Explicit `missing_atoms='omit'` returns
the retained known-source subsystem with no coordinate row for absent atoms.
The report identifies omissions with -1 forward-map entries and an omitted
index list. Native extraction removes incident bonds; virtual-H counts are not
silently increased. This is not a representation of the original full ligand.
For prepared nonpolar-H reduction, call the #223 transform before export and
keep that separate projection map. Neither policy substitutes old or parent
positions for H absent from docking output. H reconstruction remains outside
this reader.

The detached `molsysmt.pdbqt_pose_read@1` report includes both atom axes, the
PDBQT-to-output axis, input structure indices and MODEL labels, selected opaque
remarks, written types/charges with units, the input SHA-256 and a copy of the
export map/producer provenance. Scores, rank and experiment protocols remain
consumer-owned. The returned chemical/structure system can persist in H5MSM
0.5; the sidecar report is not a new H5MSM domain.

## Verification scope

`tests/form/file_pdbqt/test_known_source_poses.py` tests independently displaced
fixed-column poses, reordered/nonconsecutive atom serials, branched trees,
nonconsecutive/repeated/empty structure selections, inconsistent maps and models,
unselected corruption, missing-H rejection/explicit subsystem semantics, JSON
map lists, non-default pm session policy, source immutability, no materialization
of source coordinates, native/Topology source parity, H5MSM 0.5 round trip and
execution of the User Guide examples. A fresh-process loader guard rejects
actual RDKit/Meeko/OpenMM/MDAnalysis/MDTraj/Vina loads for ready native input.

An optional integration case uses the hash-verified original Vina 1IEP SDF and
receptor, prepares a known source with named typing/charges and nonpolar-H
projection, writes a deliberately reordered all-rigid ligand and invokes Vina
with one CPU, fixed seed and bounded evaluations. It compares every imported
written-axis coordinate with Vina's numeric pose array, allowing only the
PDBQT 0.001-angstrom quantization (0.00051 angstrom tolerance). This tests real
engine syntax and coordinate correspondence, not chemical-preparation coverage,
docking accuracy, ranking or a flexible docking protocol. Consumer adoption is
tracked separately by uibcdf/dockingmt#8 and uibcdf/dockingmt#49.

The User Guide, prepared-PDBQT Cookbook and course Module 19 are synchronized.
The final focused source run passed **838 tests**, zero failures/skips, in 50.30 s
with 12 pytest workers and Pytest Receptor. Its 37 unsuppressed warnings are 28
legacy H5MSM 0.4, six MDAnalysis mass deprecations, two declared structural
attribute drops and one previously recorded optional NumPy ABI-size warning.
One meaningful doctest passed; course Module 19 executed in 11.3 s. All 14 fast
gates passed, as did Ruff and the public-signature/docstring guards.

The exact commands, environment, Vina version/settings and tested executable
SHA-256 values are recorded in
[the source receipt](../../../devtools/data/pdbqt_pose_read_20261022.json).
This is source-level contract and engine-format/coordinate evidence, not
installed-package, complete scientific or release-candidate qualification.

## Resolution

Accepted and implemented the bounded reader. The guard module fails if reordered
written positions stop mapping to their declared source indices, MODEL labels
replace structure indices, any missing H receives an invented/stale coordinate,
invalid models/maps are accepted, original geometry is read, or persisted pose
chemistry/coordinates are lost. Its real-engine case adds actual Vina output
syntax and numeric-coordinate comparison when that optional test engine exists.
The reader remains experimental under the public form namespace; flexible
receptors, multiple source chemical states, source-free chemistry recovery and
streaming were not part of this delivered profile.
