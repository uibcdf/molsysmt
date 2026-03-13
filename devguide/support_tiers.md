# Support Tiers for Molecular System Forms

This document defines the support contract for molecular-system forms in the `1.x` line of MolSysMT.

Its purpose is not to list every implemented adapter. Its purpose is to make explicit:

- which forms are part of the contractual support surface;
- what kind of guarantee each tier provides;
- which forms are backed by contract verification;
- which forms are parity-verified;
- which forms are relevant to the future heavy-trajectory roadmap;
- and which areas remain outside the `1.0.0` support contract.

## How to read this document

This document separates four ideas that should not be conflated.

### 1. Support tier

The support tier tells users how strongly MolSysMT stands behind a form in the `1.x` line.

### 2. Contract verification

Contract verification means that the form is exercised by tests that validate the expected observable contract for its supported scope.

This is stronger than "the adapter exists", but different from full cross-form parity.

### 3. Parity verification

Parity verification means that equivalent molecular content represented in different supported forms is explicitly tested for equivalent results where such equivalence is part of the supported contract.

This is stronger than ordinary form support.

### 4. Heavy-mode status

Heavy-mode status indicates whether the form participates in the committed pre-`1.0.0` chunked-execution contract, is only a candidate for it, or is outside that scope.

Heavy-mode readiness must not be inferred from ordinary form support.

## Tier definitions

### Tier 1 — Contractual Forms

Tier 1 forms are part of the supported `1.x` contract.

For Tier 1 forms:

- regressions are patch-priority;
- supported semantics are expected to remain stable across the `1.x` line except for documented bug fixes and explicit support-contract revisions;
- contract support is based on implemented tests and documented scope, not only on adapter presence.

Tier 1 does not mean that every conceivable capability is guaranteed. It means that the documented supported scope of the form is part of the contractual product surface.

### Tier 2 — Supported Best-Effort Forms

Tier 2 forms are supported, maintained, and recommended where their scope is useful, but they are not part of the strongest contractual surface.

They may be:

- lossy by design;
- partially supported;
- stable in daily use without carrying full Tier 1 parity guarantees;
- likely candidates for promotion once their scope and verification harden further.

### Tier 3 — Experimental, Transitional, or Niche Forms

Tier 3 forms are available but outside the contractual core of the `1.0.0` line.

They may be:

- experimental;
- specialized;
- legacy;
- transitional;
- or insufficiently verified for contractual support.

Tier 3 forms are useful to retain, but they should not be presented as part of the guaranteed production-grade core.

## Tier 1 forms

These forms are currently considered part of the contractual `1.x` support surface, within the scope stated in the notes.

| Form | Category | Scope | Contract verified | Parity verified | Heavy-mode status | Notes |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `molsysmt.MolSys` | Native | Full native system object | Yes | Yes | Tier 1 target | Canonical reference form |
| `molsysmt.Topology` | Native | Native topology object | Yes | Yes | Tier 1 target | Canonical topology contract |
| `molsysmt.Structures` | Native | Native structures object | Yes | Yes | Tier 1 target | Canonical structures contract |
| `molsysmt.MolSysBuilder` | Native editable | Declared-state editable molecular system | Yes | Not applicable | Outside current heavy contract | Canonical explicit editing path |
| `molsysmt.MolSysDict` | Native declarative | Declarative in-memory molecular-system form | Yes | Partial | Outside current heavy contract | First declarative full-system form |
| `molsysmt.TopologyDict` | Native declarative | Declarative in-memory topology form | Yes | Partial | Outside current heavy contract | Declarative topology form |
| `molsysmt.StructuresDict` | Native declarative / native helper | Declarative or helper structures payload, as documented | Yes | Partial | Outside current heavy contract | Treated as part of the declarative family |
| `file:molsys_yaml` | File | Declarative YAML molecular-system file form | Yes | Partial | Outside current heavy contract | Detected by content, not by typed extension |
| `file:topology_yaml` | File | Declarative YAML topology file form | Yes | Partial | Outside current heavy contract | Detected by content, not by typed extension |
| `file:structures_yaml` | File | Declarative YAML structures file form | Yes | Partial | Outside current heavy contract | Detected by content, not by typed extension |
| `file:h5msm` | File | Native persisted molecular system | Yes | Yes | Tier 1 heavy candidate | Canonical persisted native form |
| `file:bcif` | File | BinaryCIF structural input, within documented scope | Yes | Partial | Outside current heavy contract | High-value structural form and future heavy-read candidate for structure-centric workflows |
| `file:bcif_gz` | File | Compressed BinaryCIF structural input, within documented scope | Yes | Partial | Outside current heavy contract | High-value compressed structural form and future heavy-read candidate for structure-centric workflows |
| `openmm.Topology` | Class | Topological interoperability | Yes | Yes | Outside current heavy contract | Strongly validated interop form |
| `mdtraj.Trajectory` | Class | Supported current eager-path trajectory interoperability | Yes | Yes | Tier 1 heavy target | Primary trajectory interoperability target for the first committed heavy slice |
| `mdtraj.Topology` | Class | Topological interoperability | Partial | Partial | Outside current heavy contract | Candidate for stronger parity hardening |
| `file:pdb` | File | PDB file interoperability, lossy where the format is lossy | Yes | Yes within documented scope | Outside current heavy contract | Round-trip semantics explicitly constrained by PDB limitations |
| `file:xtc` | File | Supported current eager-path trajectory input | Yes | Partial | Tier 1 heavy target | Primary local trajectory file target for the first committed heavy slice |

## Tier 2 forms

These forms are supported and useful, but they remain best-effort compared with the contractual Tier 1 core.

| Form | Category | Scope | Contract verified | Parity verified | Heavy-mode status | Notes |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `MDAnalysis.Universe` | Class | General MDAnalysis interoperability | Yes | Partial | Outside current heavy contract | Hardened adapter, not contractual Tier 1 yet |
| `MDAnalysis.AtomGroup` | Class | Selected-group interoperability | Yes | Partial | Outside current heavy contract | Hardened recently, still best-effort compared with Tier 1 |
| `openmm.Modeller` | Class | Editable topology-plus-positions interoperability | Partial | Partial | Outside current heavy contract | Important OpenMM object, but not yet contractual at the same level as `openmm.Topology` |
| `openmm.Context` | Class | State extraction and interoperability within documented scope | Partial | Partial | Outside current heavy contract | Supported where explicitly documented, but not a Tier 1 parity reference object |
| `openmm.Simulation` | Class | State-bearing interoperability within documented scope | Partial | Partial | Outside current heavy contract | Important operational object, but outside the strongest contractual surface |
| `rdkit.Mol` | Class | Chemical graph / small-molecule interoperability | Partial | Partial | Outside current heavy contract | Useful but narrower than core molecular-system forms |
| `biopython.PDBStructure` | Class | Structural biology interoperability | Partial | Partial | Outside current heavy contract | Useful and supported, but not Tier 1 contractual |
| `parmed.Structure` | Class | ParmEd interoperability | Partial | Partial | Outside current heavy contract | Stable enough for use, not Tier 1 |
| `molsysviewer.MolSysView` | Viewer | Viewer-oriented inspection and interaction | Yes | Not applicable | Outside current heavy contract | Viewer workflow support, not a parity reference form |
| `nglview.NGLWidget` | Viewer | Viewer-oriented inspection and interaction | Yes | Partial | Outside current heavy contract | Lossy visual round-trips are documented where applicable |
| `string:pdb_id` | Remote | Remote retrieval entry point | Partial | Partial | Outside current heavy contract | Useful and important, but network-dependent by nature |
| `string:alphafold_id` | Remote | Remote retrieval entry point | Partial | Partial | Outside current heavy contract | Candidate for Tier 1 promotion once contract tests and parity coverage are hardened |

## Tier 3 forms

These forms are available but remain outside the contractual `1.0.0` core.

| Form | Category | Scope | Contract verified | Parity verified | Heavy-mode status | Notes |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| `networkx.Graph` | Class | Topology graph only | Limited | No | Outside current heavy contract | Specialized topology-only adapter |
| `pytraj.Trajectory` | Class | Legacy / optional trajectory interoperability | Limited | No | Outside current heavy contract | Useful but not contractual |
| `biopython.Seq` | Class | Sequence-only workflows | Limited | No | Outside current heavy contract | Not a full molecular-system form |
| `XYZ` and related simple formats | Format | Narrow coordinate-file use cases | Limited | No | Outside current heavy contract | Specialized and intentionally non-core |
| Obscure or low-use file forms | File | Narrow or low-maturity workflows | Limited | No | Outside current heavy contract | Retained without contractual guarantee |

## Explicitly outside the `1.0.0` support contract

The following area is explicitly outside the `1.0.0` support contract, even if code remains in the repository:

- `molsysmt.molecular_dynamics/**`

This means:

- it is not part of the contractual `1.0.0` product surface;
- it does not define the release baseline;
- and it is excluded from the stabilization-oriented coverage target.

## Contract verification status

Contract verification for this document should be interpreted conservatively.

The relevant question is not whether a form can be imported or whether some conversion exists. The relevant question is whether the supported scope of the form is exercised by tests that validate the expected user-visible behavior.

The contract-verification program should keep hardening:

- native forms;
- declarative forms;
- canonical persisted forms;
- and the strongest interoperability forms that are part of Tier 1.

## Parity verification

Parity verification is narrower than general support.

The expected parity matrix should be derived from the support contract, not guessed informally. In practice, this means:

- Tier 1 forms should carry the strongest parity obligations where equivalent semantics are meaningful;
- Tier 2 forms may be parity-verified only for their documented scope;
- viewer and remote forms may remain lossy or best-effort where that is intrinsic to their role.

Two parity axes should remain explicit:

1. **form parity**
   - equivalent molecular content represented in different forms should produce equivalent observable results where the contract says so;
2. **execution parity**
   - eager and heavy execution paths should produce equivalent results for operations that officially support both.

## Heavy-mode status

Heavy-mode support should not be inferred from ordinary form support.

This document therefore uses the following heavy-mode states informally:

- `Tier 1 heavy target`
  - forms that are expected to matter directly for the committed pre-`1.0.0` heavy slice;
- `heavy candidate`
  - forms that are plausible heavy inputs but are not yet committed in the support contract;
- `outside current heavy contract`
  - forms that may still be fully supported for ordinary workflows while not participating in the first heavy slice.

The authoritative design for heavy trajectories is tracked in:

- `devguide/scalability_and_heavy_trajectories_v2.md`

The support contract and the heavy roadmap must remain aligned, but they are not the same document.

## Contractual capability matrix

This matrix summarizes the expected capability envelope of each support tier. It is intentionally high-level: the authoritative form-by-form scope remains the tier tables above, but this section provides the product-level view that users need when deciding whether a form is suitable for production work.

| Capability | Tier 1 (Contractual forms) | Tier 2 (Supported best-effort forms) | Tier 3 (Experimental / niche forms) |
| :--- | :--- | :--- | :--- |
| **Basic introspection** (`get`, `info`, documented `compare`) | Full, within documented form scope | Full or near-full within documented scope | Limited and form-dependent |
| **Selection semantics** (`select`) | Full where selection is part of the form contract | Partial to full, depending on form scope | Best-effort |
| **Structural analysis** (`distances`, `RMSD`, related structure operations) | Full on the native/core surface; heavy support only where explicitly declared | Eager-path support where documented; heavy not implied | Best-effort |
| **Topology editing** | Full through `MolSysBuilder` / `build.editable(...)` on the native editing path | Partial where the ecosystem form can be converted and edited safely | Not contractual |
| **Coordinate updates** (`set`) | Full within documented structural scope | Partial to full within documented scope | Limited |
| **Format conversion** (`convert`) | Expected to preserve the documented supported scope; lossless where the form pair is contractually lossless | Supported but may be lossy or partial by design | Experimental or transitional |
| **Visualization workflows** (`view`, viewer-oriented adapters) | Verified where viewing is part of the documented workflow | Supported where explicitly documented | Limited |
| **Heavy / chunked execution** | Only for forms explicitly marked as Tier 1 heavy targets in this document | Not contractual unless promoted explicitly | Outside current heavy contract |

Notes:

- "Full" never means "all imaginable semantics". It means full support for the documented contractual scope of that tier.
- Lossy formats remain Tier 1 when the lossy boundary is intrinsic to the format and explicitly documented, as in the case of PDB-based workflows.
- Heavy-mode support must be read from the form-specific heavy-status column, not inferred from the general support tier alone.
- The goal of this matrix is expectation management and testing focus. The detailed contractual source of truth remains the per-form tables above.

## Tier 1 guarantee summary

Tier 1 forms are the forms that MolSysMT is prepared to defend as part of its supported `1.x` line.

This means, in practical terms:

- regressions are patch-priority;
- Tier 1 regressions block the release of new minor versions until resolved or explicitly reclassified;
- regressions discovered in the wild should trigger an immediate patch-release decision path;
- semantics are expected to remain stable across `1.x` except for documented bug corrections and explicit contract revisions;
- support claims must be backed by tests, not only by adapters;
- any future heavy-mode commitments for Tier 1 forms must be reflected explicitly in this document rather than inferred informally.
