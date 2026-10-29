---
summary: Provide reusable molecular identity and scaffold overlap annotations for leakage audits.
issue: uibcdf/molsysmt#447
status: open
opened: 2026-10-24
closed:
verification: measured
area: [topology, chemistry, api]
guard:
normative:
blocked_by: [uibcdf/molsysmt#255]
supersedes: []
---

# Molecular identity and scaffold overlap annotations

**Reported:** uibcdf/pharmacophoremt#64/#66; provider uibcdf/molsysmt#447.
**Status:** Proposed contract for maintainer review. No public functions are added,
no scientific profile is admitted, and no release boundary is changed by this document.
The maintainer subsequently selects chemical_states as the target namespace;
its implementation follows the separately accepted #255 domain migration.

## What

Provide read-only, form-agnostic molecular identity and scaffold annotations, plus
compact evidence of shared identities/scaffolds between explicit collections.
An annotation describes a selected chemical graph under a declared profile,
not external identifier equality, chemical-series independence or a valid study
split. Preserve unresolved inputs, their original positions, selected chemical
states and source atom correspondence.

## Why

The consumer can exclude known CIDs but cannot interpret different database IDs
as different molecules. Its reported exposure ledger also includes rows without
CIDs; blank identities must never become one equivalent molecule or independently
novel observations. The consumer's later source-population failure is independent
of provider delivery. This proposal does not claim to unblock those source gates.

Sharing an exact scaffold is useful overlap evidence. Different scaffold keys do
not establish different medicinal-chemistry series or absence of leakage. Study
sampling, split optimization, labels and scientific interpretation remain owned
by PharmacophoreMT. Molecular graph interpretation stays in MolSysMT.

## Existing reusable pieces

Inspected provider: `5bcd2b76086b1fc4af9d1ab595cfb2866fad7d41`.

| Piece | Reuse | Boundary |
| --- | --- | --- |
| `physchem.get_chemical_readiness` | Inspect available assignments and missing evidence. | Not a universal chemical-validity certificate. |
| `topology.get_atom_correspondences` | Existing declared-state chemistry checks and optional exact witnesses. | Its strict profile requires one complete covalent context and matching H encodings; do not enumerate mappings just to obtain a key. |
| `topology._chemical_graph` | State resolution, detached chemistry and source-axis checks. | Its ordered consistency digest is not a canonical molecular identity. |
| `topology.get_rings`, `get_substructure_matches` | Existing graph tools and selection conventions. | A cycle basis is not itself a molecular scaffold definition. |
| `physchem.get_cip_stereochemistry` and shared stereo helpers | Supported assigned stereo and conversion verification. | Do not infer missing stereo from coordinates. |
| Existing `rdkit.Mol`/SMILES adapters | Optional compiled canonicalization backend. | The existing converter exposes no complete identity-policy or overlap contract. |
| `physchem.normalize_aromatic_bond_orders` | An explicitly requested transformation when appropriate. | No automatic normalization by the proposed readers. |

Factor shared graph-validation/projection internals where needed; keep the
existing correspondence profile unchanged and guarded. Do not duplicate its
chemistry checks in a scaffold adapter. No new chemical-assignment store is needed.

## Proposed public tools

Names and arguments below are proposals, not existing or approved API.

| Proposed function | Responsibility |
| --- | --- |
| `chemical_states.get_molecular_identity` | Return a canonical, policy-qualified key and inspectable canonical payload for one selected molecular composition. |
| `chemical_states.get_molecular_scaffold` | Return a named framework descriptor, its key and retained source atom indices. |
| `chemical_states.get_molecular_overlap` | Annotate two explicit input collections using those tools and return compact shared-key membership. |

The maintainer selects `chemical_states` as the target namespace on 2026-10-28:
identity and frameworks describe a selected chemical graph. The
[accepted #255 migration](retire_topology_bonds_after_1_0_in_favor_of_chemicalstates.md)
first establishes the native/functional owner and relocates existing graph tools.
The current-source paths in the reusable-pieces table above are inspected
pre-migration paths, not the target public layout. Physical-property perception
remains in `physchem`; stable elements and hierarchy stay in Topology and
assignments in ChemicalStates. The initial supported chemistry may be bounded
to ordinary small-molecule graphs without a new element container.

Single-system tools follow `molecular_system`, `selection`, `structure_indices`,
`chemical_state`, `syntax` and `skip_digestion` conventions, with `@arg_digest`.
Coordinates are unnecessary; structures only resolve an explicitly requested
structure-associated state. A mixed-state structure selection must not choose
an arbitrary state. Unsupported or incomplete chemistry is explicit.

An identity describes the complete composition selected by the caller. Do not
silently choose the largest fragment or one molecule from a complex. Initially
require complete covalent components, with clear errors for a selection cutting
heavy-atom connectivity; define any ordinary-H support projection explicitly.
Existing per-component/molecule queries can help callers choose the scope.

The collection operation uses plural `molecular_systems` and
`reference_molecular_systems`. This boundary must be explicit because a list of
providers in singular `molecular_system` already means a composed system. Each
collection entry can itself use a supported singular form/composition. Retain
entry positions and repetitions; external IDs are optional labels, never keys.

## Identity profile proposed for the first delivery

Suggested separation: `method='canonical_isomeric_graph'`, `engine='RDKit'`,
with independently recorded policies rather than a software name pretending to
be a scientific definition.

- Preserve selected charge/protonation, isotope labels, radicals, bond chemistry
  and supported assigned tetrahedral/double-bond stereo. No tautomer collapse,
  neutralization, resonance equivalence or chemical completion is implicit.
- Ignore source atom/group/molecule IDs, coordinate structures, atom order,
  database IDs and nonchemical atom-map labels when computing the chemical key.
  Keep all original labels and source indices in correspondence/provenance.
- Recommend `hydrogen_policy='collapse_ordinary'`: ordinary indexed/virtual H
  encodings can share an identity, while isotope-labeled H and chemically or
  stereochemically significant H remain distinct. This is an explicit descriptor
  projection on a detached graph, not modification of the source. Validate
  formula, total H/charge and stereo preservation. An optional encoding-sensitive
  profile may preserve indexed-H distinctions, but cannot masquerade as broader
  molecular independence.
- Recommend `fragment_policy='all'`: disconnected components form an unordered
  multiset with multiplicity. Fragment order is irrelevant, salts and component
  counts are retained. Parent-compound policies belong to separately requested
  transformations under uibcdf/molsysmt#366.
- Potentially stereogenic but unassigned structures receive an unresolved strict
  identity, not an arbitrary stereoisomer or a wildcard equated with an assigned
  isomer. Any later connectivity-only annotation needs its own explicit profile.
- Initially reject unsupported enhanced/non-tetrahedral stereo, query atoms,
  unqualified polymer/S-group semantics and unsupported coordination rather than
  dropping them during conversion. A form must expose required information;
  source metadata that cannot survive the native boundary must be detected.

The output retains canonical payload, key/profile identifier, producer and
backend versions, selected state, source scope, statuses and attribution. The
payload must remain inspectable; a digest is only an index accelerator and must
not replace comparison of compatible canonical payloads. Do not compare keys
from different methods, policies or unqualified backend versions as ordinary
matches/nonmatches. Return an explicit incompatible-profile outcome.

Unknown inputs and native sequence inventories without atomic chemistry do not
receive an empty chemical identity. Equal `None` values never establish equality.
No universal, cross-backend or cross-version chemical identifier is promised.

## Scaffold definitions and attribution

Start with `method='bemis_murcko'`, an explicitly named RDKit variant and
`scaffold_type='chemical'`. Add the RDKit generic projection only after separately
checking its atom/bond abstraction. RDKit's variant preserves certain degree-one
atoms double-bonded to the framework; its generic projection then converts atom
and bond types. It must not be labeled a faithful reproduction of the original
Bemis-Murcko pruning definition.

Keep method, variant, engine and any stereo/isotope abstraction separate in the
result. Framework stereo policy should be explicit; a connectivity-oriented
framework can ignore stereo without weakening the separate strict identity.
All abstraction occurs on detached derived data. Retained original atom indices
must come from verified transport through extraction, not an arbitrary match of
a symmetric scaffold back onto its parent. Do not promise a unique canonical
atom ordering for symmetric graphs.

A valid acyclic input has `no_cyclic_scaffold`, not an invalid molecule and not
a common empty-scaffold group. An empty input, unavailable atom inventory and
unsupported chemistry have different statuses. With several fragments, report
which contribute cyclic framework and retain correspondence for the others;
scaffold abstraction does not discard counterions from source identity.

Ackredit is optional and observes completed scientific work. Cite Bemis and
Murcko as the conceptual source, RDKit as the executed implementation/variant,
and the actual canonicalization/stereo algorithms where executed. Distinguish
faithful implementation, variant and inspiration in documentation and result
metadata; never claim full-paper reproduction from an abstract alone.

## Collection output and computational behavior

Return a detached, versioned dictionary with numeric columns and explicit schema,
not one persistent Python object for every possible cross-collection pair:

- original input positions, status codes, selected states and packed source atom
  memberships; preserve failed/unresolved rows in the input axis;
- deduplicated canonical payload/key tables plus aligned per-input indices;
- shared identity and scaffold groups, encoded as key plus left/right member
  indices and offsets, and unassessed/incompatible scopes;
- methods, policies, exact software versions and detached bibliography.

Do not create dense `N x M` matrices. If every entry shares a scaffold, retain
its two member lists instead of expanding their Cartesian product. A later
pair iterator needs a bounded-output contract. After molecular annotation,
hash-indexed grouping should have expected linear cost in input counts plus
stored memberships; canonicalization has its own workload-dependent cost.
Cache keys include graph consistency and the complete profile, not coordinates.

Single-system calls should raise actionable errors by default. Collection
`on_error='record'` can retain diagnosed scientific input failures; it must not
swallow programming/backend failures or label unavailable dependencies as invalid
molecules. Unknown group indices are sentinels, not an equivalence class.

Define an explicit typed serialization boundary for these derived dictionaries;
JSON transport converts numeric columns explicitly. This proposal does not add
an H5MSM layer, an `Interactions` analysis, or automatic attachment to MolSys.
Reuse RDKit's compiled backend first. Measure before introducing a Rust routine
or a new dependency; the indexing/grouping layer alone does not justify one.

## What is measured and what is assumed

**Executed reference probes:** installed RDKit 2025.09.5, without changes to
MolSysMT source. These establish observed backend behavior, not the proposed API
or universal chemical/scientific validity.

| Input/control | Observation |
| --- | --- |
| `CCO` versus `OCC` | Both canonicalize to `CCO`. |
| Mapped ethanol `[CH3:7][CH2:8][OH:9]` | Plain canonical SMILES retains map labels; descriptor projection must handle nonchemical labels explicitly. |
| `CO` and `Chem.AddHs(CO)` | Plain outputs differ; an explicit ordinary-H removal projection recovers `CO`. |
| Opposite assigned tetrahedral configurations of `CC(O)F` | Canonical outputs differ; the unspecified configuration is a third encoding, not a wildcard. |
| Acetic acid / acetate / sodium acetate | Distinct canonical outputs; reversing sodium-acetate fragment order preserves the output. |
| Acetone / its enol | Distinct outputs despite equal reported formula. |
| Toluene / phenol | Both RDKit frameworks are benzene, while source identities differ. |
| Pyridine / benzene | Chemical frameworks differ; their generic projections coincide. |
| Cyclohexanone / cyclohexane | RDKit retains exocyclic O; generic projections are respectively `CC1CCCCC1` and `C1CCCCC1`. |
| Ethanol | Empty cyclic framework; requires an acyclic-specific result status. |
| Atom index property transported through scaffold extraction | Original indices survived in these probes; this is not yet a qualified invariant for all supported graphs. |

Minimal reproduction of the key scaffold distinction:

```bash
python - <<'PY'
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
for text in ('O=C1CCCCC1', 'C1CCCCC1', 'CCO'):
    mol = Chem.MolFromSmiles(text)
    scaffold = MurckoScaffold.GetScaffoldForMol(mol)
    print(text, Chem.MolToSmiles(scaffold),
          Chem.MolToSmiles(MurckoScaffold.MakeScaffoldGeneric(scaffold)))
PY
```

**Assumed/proposed:** safe ordinary-H invariance across the whole admitted
chemistry, source-property transport, profile compatibility, performance and
consumer usefulness require the acceptance work below. No benchmark or
installed-consumer qualification has been performed for this proposal.

## What was refuted

- External identifier equality/inequality and ordered graph consistency digests
  do not establish the requested chemical grouping.
- The existing canonical SMILES converter is useful but insufficient by itself:
  atom maps, H encodings, unsupported chemistry and profile compatibility matter.
- RDKit `RegistrationHash` is worth studying, but adopting its default layered
  policy would also adopt representation/stereo/tautomer conventions. Do not
  relabel that output as an exact MolSysMT declared-state contract without review.
- A cycle basis is not a framework extraction algorithm. Generic RDKit scaffolds
  do not automatically equal the original untyped Bemis-Murcko framework.
- Different scaffolds do not certify different chemical series. Fingerprints or
  a similarity threshold would introduce a separate approximate criterion.

## Acceptance criteria and implementation order

1. Approve the scope, names, owner and policies. Keep this record proposed until
   the maintainer does so; do not silently add a 1.0 blocker.
2. Implement identity using shared state/graph/stereo preparation. Test atom,
   bond and fragment permutations, duplicate external IDs, distinct external IDs
   for one molecule, H representation, isotope/stereo/charge variants, tautomers,
   unknown assignments and immutable sources across supported forms.
3. Implement chemical scaffold extraction and source maps with hand-specified
   atom-set controls for rings/linkers/side chains and exocyclic bonds; separately
   qualify any generic projection, acyclic inputs and salts. Backend parity is
   useful but does not replace independent definition-based controls.
4. Implement collection overlap by composing the public molecular tools. Preserve
   repeated/failed rows, profile incompatibilities and fully shared-key groups
   without quadratic pair materialization. Distinguish an assessed nonmatch from
   an unassessed input.
5. Measure 1,000, 10,000 and, if practical, 100,000 input occurrences with both
   repeated and changing graphs. Record cold/warm annotation, grouping, peak RAM,
   serialized size and source/backend identities. These are proposed workloads,
   not measured performance promises.
6. Complete ArgDigest, lazy DepDigest, SMonitor diagnostics, optional Ackredit,
   truthful form/state boundaries, NumPy docstrings/doctests, User Guide/Cookbook
   and course examples. Test collection label changes cannot affect science.
7. Request consumer feedback against known toy controls before real-study claims.
   Scaffold/fingerprint/series expansions and explicit normalization retain their
   separate admission and scientific validation; no activity labels enter here.

## References and provenance

Review date: 2026-10-28, Linux, Python 3.14.7, installed RDKit 2025.09.5.
Provider source is identified above. Inspected external RDKit checkout:
`cbfb37abddcd5b5feeac97d53530ae6be83cac0d`, including
`rdkit/Chem/Scaffolds/MurckoScaffold.py`, its unit tests and
`rdkit/Chem/RegistrationHash.py`. Live documentation identifies RDKit 2026.09.1;
that documentation is not a claim to have executed that version.

- [Bemis and Murcko (1996), DOI 10.1021/jm9602928](https://doi.org/10.1021/jm9602928).
  Bibliographic record/abstract inspected; full paper not reproduced.
- [RDKit scaffold API](https://www.rdkit.org/docs/source/rdkit.Chem.Scaffolds.MurckoScaffold.html).
- [RDKit RegistrationHash API](https://www.rdkit.org/docs/source/rdkit.Chem.RegistrationHash.html).
- [RDKit maintainer discussion of scaffold definitions and split limits](https://greglandrum.github.io/rdkit-blog/posts/2024-05-31-scaffold-splits-and-murcko-scaffolds1.html).

Existing normalization proposal: uibcdf/molsysmt#366. Consumer molecular
annotation and study ownership: uibcdf/pharmacophoremt#64/#66. No source data,
activity table, external identifier service or molecular registry is queried.
