---
summary: Assign and validate AutoDock atom types under a named scheme
issue: uibcdf/molsysmt#222
status: resolved
opened: 2026-09-22
closed: 2026-10-04
verification: reproduced
area: [build, attribute]
guard: tests/physchem/test_get_autodock_atom_types.py
normative:
blocked_by: []
supersedes: []
---

# Assign and validate AutoDock atom types under a named scheme

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved for the documented experimental chemical_environment@1 profile.
Chemical classification, named attachment, provenance and bounded export are implemented
and contract-tested; consumer protocol acceptance remains separate.

## What

Provide chemically grounded AutoDock atom typing as an explicitly identified parameter scheme.

## How

Classify atoms using element, bonding, aromaticity and chemical context rather than names; validate full coverage and define how the scheme is stored alongside atom_ff_type.

## Why

PDBQT requires AutoDock types, while an unqualified atom_ff_type value does not identify its typing rules.

## What is measured and what is assumed

**Inspected:** Inspected native MolecularMechanics storage and DockingMT preparation. Meeko documents SMARTS-based AutoDock4 typing.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Inferring types from atom or residue names was rejected because names do not reliably encode chemical context.

## Scope and exclusions

Atom typing and scheme provenance; no partial-charge calculation or DockingMT scoring choice.

## Acceptance criteria

- Representative aromatic, donor, acceptor, halogen, and unsupported cases have explicit tested assignments or errors.
- Tests distinguish polar hydrogens that remain in the selected PDBQT profile from mergeable nonpolar hydrogens using chemical context rather than atom names.
- The selected scheme and its version are inspectable; PDBQT export can require compatible typing.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#5.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.



## Explicit label decoding checkpoint — 2026-10-03

`molsysmt.element.atom.get_atom_type_from_atom_ff_type` decodes an existing
label or one-dimensional label collection under `typing_scheme='autodock4'`.
Standard labels map to chemical element symbols, independently of atom names.
Custom, macrocycle glue and hydrated-ligand pseudoatom labels fail explicitly.
An empty collection still requires a supported named scheme. Tests are in
`tests/element/atom/test_get_atom_type_from_atom_ff_type.py` and the public
contract is documented in the atom-type tutorial and Master course.

A shared private scalar primitive supplies both the public value tool and
PDBQT parsing/writing. The PDBQT writer requires the scheme declaration and
checks each label against the stored chemical element. It performs no new
assignment, aromaticity perception or donor/acceptor classification. AutoDock
labels remain separate atom_ff_type assignments; no competing chemical store
or placeholder scheme attribute was introduced. General scheme provenance in
native storage and chemically justified label assignment remain outstanding.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.


## Named chemical profile checkpoint — 2026-10-04

**Implemented:** `physchem.get_autodock_atom_types` evaluates the full selected
chemical state before atom selection; `build.assign_autodock_atom_types` attaches
the full result to a detached single-state MolSys. The required vocabulary is
`autodock4`, descriptive method `chemical_environment`, rule version
`chemical_environment@1`. The exact precedence and supported charge environments
are normative in [the typing tutorial](../../../docs/content/user/tools/physchem/get_autodock_atom_types.md).

The classifier calls the reusable aromaticity and hydrogen-inventory tools.
Aromaticity remains a detached interpretation, not chemical-state repair.
Indexed H are mandatory and retained; polar/nonpolar classification does not
merge H or redistribute charges. Rule codes, overlap counts, original provider
versions, evaluated source scope, state, references and optional attribution are
inspectable. Meeko 0.8.0 at commit
`1eac18bd6d1111f35f9f1abaa8af502c2668d054` was inspected as a clean reference
checkout; it is not a runtime dependency or vendored rule table. RDKit 2025.09.5
is the actual aromaticity/valence provider in these local checks.

Mechanical assignment provenance stays in MolecularMechanics. Copy/pickle
preserve original producer versions. Atom extraction projects parent labels and
per-atom rule evidence, retaining original evaluated scope and source maps.
The source binding is checked before projection so stale assignments cannot be
reauthenticated by extraction. Manual property replacement clears the report;
strict joins reject incompatible original provenance and intersection joins
warn and clear reports while retaining compatible values. PDBQT export checks
state/chemistry/ordered labels and emits a bounded original-version summary.
Native PDBQT reading does not reconstruct the complete report. H5MSM 0.5 still
excludes this experimental mechanical domain (uibcdf/molsysmt#256).

**Contract-tested:** The initial combined calculation, attachment, charge,
aromaticity and doctest run had 80 passing cases and one test-regex mismatch
against the correctly rejected mechanical 0.5 export. The test expectation was
corrected without weakening the format boundary. Additional regression and
real-input results are recorded below when complete. The local runtime is
Python 3.13.14 under the bounded development exception uibcdf/molsysmt#237,
with the released ArgDigest 0.13 source snapshot at commit
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`. This does not qualify a public release,
installed package or full Linux/platform matrix.

**Inspected and exercised:** Four byte-verified Vina ligand SDF/PDBQT pairs from
`tests/form/data/vina_examples/manifest.json` were compared by unique heavy-atom
coordinate correspondence, without trusting equal atom counts or serial order.
Native SDF version/valence/stereo restrictions remain unchanged; the exploratory
comparison explicitly read the original SDF through RDKit, then converted the
declared graph. Fixed-state H materialization was separate when needed.
Heavy-atom labels matched in 1IEP and both 5X72 cases. 1S63 atom index 0 is a
neutral tertiary aliphatic amine (three saturated carbon neighbors): the local
profile produces NA, while the supplied prepared PDBQT declares N. The
comparison does not establish protonation truth, docking-score equivalence or
universal reference correctness. The difference is retained explicitly in a
regression rather than modifying source chemistry to force parity.

**Scope:** Metals/pseudoatoms, macrocycle glue, arbitrary open-shell chemistry,
protonation selection, charge models, H merging, active torsion/ROOT policy and
complete parameterization remain separate. An ordinary receptor PDB lacking
formal/radical/bond-order evidence must fail this classifier, rather than being
typed from residue/atom names. Complete receptor chemical assignments require
their own explicit preparation and consumer acceptance. No Rust routine was
added: this rule pass visits graph adjacency, not all possible atom pairs, and
no workload measurement yet justifies another backend.

The User Guide Foundations, Toolbox, Cookbook and Master module 12 are updated.
Public docstring validation reports 237 structurally consistent supported
functions. The maintained `devtools/scripts/validate_course.py` passes all 156
course structures; the old `docs/content/course/devtools/validate_course.py`
was also tried and rejects their historical layout (0/156), so it is not treated
as equivalent or passing evidence. Notebook changes are narrative only; this
check does not claim that every course code cell was rerun. Documentation HTML
build succeeded with existing unrelated reference/toctree warnings.


## Resolution — 2026-10-04

The public classifier and detached builder meet the bounded acceptance criteria,
with typed empty outputs, full-source context before selections, explicit polar
versus nonpolar H indices, unsupported-case refusals and inspectable versioned
scheme provenance. No arbitrary-ligand, receptor, docking-score or Meeko-wide
parity claim is made. Classification and attachment guards protect their
respective contracts; the named real-file cases retain the 1S63 difference.

- 545 affected chemistry/native/charge/SDF/PDBQT cases passed in 167.68 seconds,
  with nine existing structural/provider/binary warnings.
- Four original ligand graph comparisons and all-H-preserving exports passed
  in 7.53 seconds, after explicit positive-integer PDBQT serial preparation.
  The earlier refusals of source index-like IDs were correct format enforcement,
  not a reason to silently renumber inside the scientific classifier.
- 74 focused typing, attachment, manual mechanical setters and signature-guard
  cases passed in 25.20 seconds after the newly found setter defect was repaired.
  These overlap earlier cases and are not summed as unique coverage.
- uibcdf/molsysmt#315 fixes the false public-signature classification of a local
  private helper; uibcdf/molsysmt#316 fixes native mechanical setter dispatch
  and missing label-vector validation. Both have their own returning-failure guards.
- The public stability registry now classifies the five new named-charge,
  aromaticity and chemical-typing exports as experimental, with owning modules,
  documentation and regression routes. This also closes the missed registry
  bookkeeping for the earlier charge/aromaticity additions; it does not change
  their previously executed scientific evidence.
- Ruff, soft-dependency validation, public docstring/registry/signature checks,
  the maintained course-structure gate and documentation HTML build pass.
  Form adapter delivery retains the accepted 78-declaration debt in nine forms;
  this change introduces no new delivery debt.

Next consumer step: review the named profile against its declared prepared
chemistry in uibcdf/dockingmt#33, replace local element/name approximations,
and preserve the scheme/report explicitly. General rotatable-bond eligibility
remains uibcdf/molsysmt#224; H projection/accounting remains uibcdf/molsysmt#223.


Final local administration: the returning-failure guards for #315/#316 passed
28 cases in 4.39 seconds, including genuine public parameter removals and
invalid label vectors without mutation. The generated stability view classifies
257 symbols; final public docstring validation covers 237 functions. A second
HTML build after the setter documentation changes also succeeded, retaining
course heading/directive and reference warnings. These observations are bounded
local evidence, not an exact-commit hosted CI result or scientific release gate.


## Post-publication CI observation — 2026-10-04

At `68c924d842870536857b409aa7eabe6c368962b0`, hosted CI smoke, developer-guide
integrity and Conda publication governance passed. Ruff correctness also passed
inside its run, but its formatting step rejected 24 files: two from this
checkpoint and inherited formatting debt. The subsequent maintenance change
formats exactly these files, with identical parsed ASTs before/after; no new
scientific behavior or broadened test claim is inferred from formatting.

The MolSysSuite conformance run failed on an intentional historical development
archive tag, not scientific code. The preserved object and required archival
migration review are tracked by uibcdf/molsysmt#317. Hosted smoke and local
contract evidence do not establish a full Linux/platform matrix or clear its
backlog. GH Run Receptor summaries were inspected first; native failed-step logs
supplied the concrete formatter/tag diagnostics absent from those summaries.
