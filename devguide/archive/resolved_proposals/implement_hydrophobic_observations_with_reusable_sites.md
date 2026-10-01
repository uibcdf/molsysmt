---
summary: Implement hydrophobic observations with reusable sites
issue: uibcdf/molsysmt#278
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api, docs, structure, tests]
guard: tests/interactions/hydrophobic/test_get_hydrophobic_interactions.py
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Hydrophobic observations with reusable sites

**Reported:** 2026-10-01, continuation of the approved interaction-family roadmap.
**Status:** Resolved; the first reference profile is implemented and remains experimental.

## What

Add independent atomic hydrophobic-site recognition in physchem and an
experimental atom-pair detector returning sparse Interactions analyses.

## How

Use the exact ProLIF 2.2.2 Hydrophobic SMARTS with full-source declared chemistry,
then the descriptive atom_pair_distance/smarts_hydrophobic_atoms criterion with
inclusive 0.45 nm default. Store distinct unordered atom pairs (ascending source
indices) once per frame, with roles hydrophobic_1 and hydrophobic_2. Equal-type
roles do not imply ligand/protein direction. Internal, incident and between
scopes must preserve this identity. Exclude same-atom self observations only;
no additional covalent or intramolecular exclusions are inferred from the core.
Recommend disjoint ligand/environment selections for an interfacial analysis.

Reuse general topology SMARTS, compiled bounded spatial candidates, the PBC
chain MIC helper and the projected coordinate executor. Canonical pair imaging
must remain identical across scope/search orientation. Preserve known-empty
coverage, units, source axes, producer versions and optional Ackredit bibliography
through typed and named H5MSM 0.5 persistence. No automatic attachment.

## Why

Residue hydrophobicity scales are not atom typing. The general chemical tool
belongs in physchem and may serve PharmacophoreMT or other consumers independently.
The profile is a chemically interpreted proximity definition, not an energy model
or measurement of the solvent-mediated hydrophobic effect.

## What is measured and what is assumed

**Inspected:** ProLIF commit 19f1800218387c49536eb9d3e8cd3044fdb337ee,
Hydrophobic and Distance classes, exact SMARTS and inclusive distance comparison.
Its source explicitly links constituent patterns to RDKit chemical features.
Terminal methyl carbons are not all eligible; neutral aromatic atoms, eligible
chain carbons, Br/I and particular sulfur atoms match this version. Do not
substitute a generic carbon mask, residue scale or guessed authorship.

Mol* uses carbon bonded only to C/H plus fluorine, excludes F-F contacts and uses
a 0.40 nm default. This different method/profile is not an alias of the first.
**Scientifically validated, bounded scope:** unmodified ProLIF 2.2.2 generated
seven chemical controls / 21 synthetic structures / 119 distinct unordered
observations, with actual source hashes in the offline JSON. Twenty-one
RDKit/native/H5MSM form guards compare recognized sites and pair identities
exactly and distances within 1e-12, including reversed disjoint atom partitions.
The oracle includes indexed hydrogens and avoids simultaneous exact distance
boundaries; separate analytical tests guard inclusive cutoff membership.

**Contract-tested:** the final affected run passes 585 tests in 135.54 seconds:

```bash
python -m pytest tests/interactions tests/physchem/test_get_hbond_sites.py \
  tests/physchem/test_get_halogen_bond_sites.py \
  tests/physchem/test_get_hydrophobic_sites.py \
  tests/scientific_truth/curated/test_attributed_interaction_methods.py \
  tests/scientific_truth/curated/test_halogen_bonds.py \
  tests/scientific_truth/curated/test_hydrophobic_interactions.py --receptor=llm
```

Seventeen warnings are explicit low-RAM controls (12) and legacy H5MSM 0.4
fixture reads (5). Native/RDKit/composite/H5MSM input parity, all scopes,
unordered/self identity, coincident distinct atoms, repeated/nonconsecutive
structure indices, empty queries, units, named/typed round trips, remapping,
MIC images and ties, bounded file projection, invalid inputs and candidate/RAM
failures are exercised. Existing interaction regressions also pass.

**Lifecycle-tested:** both public docstrings pass 11 doctest examples. All three
new notebooks execute with saved outputs; the four Module 38 conceptual
extensions are updated while their existing biological code/outputs remain
unchanged and were not rerun. Course validation passes 156 notebooks; the API
registry passes 232 symbols. Ruff, dependency validation and public signature
checks pass. The docstring inventory omission surfaced during this validation
and is independently fixed under uibcdf/molsysmt#279: corrected discovery checks
216 functions, including all exported interaction families. Nineteen validator
regressions demonstrate missing/wrong documentation fails the gate.

Sphinx renders the new API, two tutorials and recipe with their internal links.
The new pages have no parser diagnostics. Existing unrelated documentation
warnings remain; this is not a clean full release-documentation gate.

**Estimate:** numerical coordinate blocks reserve one quarter of configured RAM,
bounded candidates one eighth and resident sparse accumulation/packing one half.
Graphs, Python overhead and RSS are outside these estimates. No new comparative
performance benchmark or biological accuracy claim is made.

## What was refuted

- Residue hydrophobicity cannot provide this atom-level SMARTS classification.
- All-carbon or carbon/sulfur element masks change the pinned chemical rule.
- A directed Cartesian result would duplicate symmetric pairs and introduce
  self observations absent from a proper distinct ligand/environment comparison.
- Filtering covalent neighbors silently would add an unreferenced criterion.
- Merely reversing stored images can make MIC tie choices scope-dependent;
  image canonical pairs through the shared periodic tool.

## Scope and exclusions

The first profile supports complete declared chemical states, every selected
structure and two singleton participants. It does not promise reference residue
fingerprint pruning, arbitrary chemical-state switching, attractive energy,
Mol* parity, automatic component assignment or renderer qualification.
Hydrophobicity residue scales keep their independent meaning and API.
No ProLIF production dependency or new Rust kernel is introduced. Accepted sparse
output and full source chemistry remain resident; numerical budgets are not RSS.
Metal coordination and water-mediated hydrogen bonds remain separate pending work
under uibcdf/molsysmt#250. No family is added as a new mandatory release gate.

## Acceptance criteria

- Digested form-agnostic recognition and detector APIs, lazy RDKit, explicit units.
- Independent pinned chemical/distance controls across native/RDKit/H5MSM inputs.
- Deterministic unordered identities, all scopes, zero results, repeated and
  nonconsecutive structure indices, periodic images and stable occurrence metadata.
- Bounded coordinate projection, match/candidate/resident-output failures,
  H5MSM/typed round trips and original attribution without a ProLIF dependency.
- Executed tutorials/recipe, foundations/course updates, API registry and local gates.

## Provenance and references

- https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/interactions.py
- https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/base.py
- https://doi.org/10.1186/s13321-021-00548-6
- uibcdf/pharmacophoremt#11 records the independent consumer reference review.

## Resolution

General atomic site recognition is independently public in physchem and delegates
topology SMARTS. The consumer reuses compiled sparse spatial candidates, general
PBC MIC chains and the projected executor. It owns the distance/profile criterion,
canonical pair identity, role-aware scope and sparse accumulation. The result
uses the existing Interactions, MolSys named storage and H5MSM 0.5 contracts; no
new schema or chemical store is introduced. ProLIF is absent from production
dependencies. The preserved residue-scale API keeps its independent meaning.

Metal coordination and water-mediated hydrogen bonds remain pending under #250.
Mol* chemistry and its pair/exclusion policy require an independent future
profile. Renderer qualification and broader Ackredit adoption keep their existing
separate scopes. Experimental completion does not stabilize those consumers or
claim original authorship, interaction energy or optimal performance.

## Validation provenance

Measured 2026-10-01 on Linux x86_64, Python 3.13.14 and RDKit 2025.09.5 in the
shared MolSysSuite development environment. The source patch is based on published
review commit 6bb5357a3; the closing issue names the implementation commit. The
runtime MolSysMT version string observed by the calculations was
0.22.4+60.g7a8350f76.dirty; installed runtime metadata is not proof of this source
revision. The reference installation stayed isolated under /tmp and no production
dependency or shared environment was changed. Recorded source hashes and runtime
versions are in devtools/data/hydrophobic_validation_systems.json.
