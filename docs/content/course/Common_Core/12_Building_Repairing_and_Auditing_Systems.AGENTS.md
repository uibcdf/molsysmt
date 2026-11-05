# Module 12 Content Governance (`12_Building_Repairing_and_Auditing_Systems.AGENTS.md`)

This document defines the **non-negotiable content contract** for `12_Building_Repairing_and_Auditing_Systems.ipynb`. 
Global course layout and editorial style rules are inherited from [`docs/content/course/AGENTS.md`](../AGENTS.md). 

Contributors modifying this notebook must strictly preserve all sections and core topics detailed below.

---

## 🎯 Module Core Domain & Inviolable Content Rules

This module introduces the **`msm.build`** specialized function module, focusing on auditing structural anomalies, repairing missing hydrogens and covalent bonds, and synthesizing peptides from sequence.

Any future revision or enhancement of this notebook **MUST preserve** the following sections and essential explanations:

### 1. Introductory Block
* Must introduce `msm.build` functions (`add_missing_hydrogens`, `add_missing_bonds`, `build_peptide`).
* Must feature the **Glossary: MolSysMT modules** custom admonition (````{admonition} Glossary: MolSysMT modules\n:class: dropdown info`).
* Must feature the **Learning Outcomes** collapsible custom admonition (````{admonition} Learning Outcomes\n:class: dropdown learning-outcomes`).

### 2. Section 1: Auditing Anomalies
* Must demonstrate auditing non-standard groups with `msm.build.get_non_standard_residues()` and checking hydrogen status with `msm.build.has_hydrogens()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.get_non_standard_residues`.

### 3. Section 2: Repairing Missing Atoms
* Must demonstrate repairing incomplete structures by adding missing hydrogens with `msm.build.add_missing_hydrogens()`.

### 4. Section 3: Reconstructing Covalent Bonds
* Must demonstrate auditing missing covalent connectivity with `msm.build.get_missing_bonds()` and reconstructing bonds with `msm.build.add_missing_bonds()`.

### 5. Section 4: Building Peptides from Sequence
* Must demonstrate synthesizing a 3D peptide structure from sequence using `msm.build.build_peptide()`.
* Must include a `:::{hint}` dropdown box for `{func}`molsysmt.build.build_peptide`.

### 6. Challenge & See Also
* Must include **Challenge 12: The Quality Auditor** using T4 Lysozyme (`181L`), and the Key Takeaway box (````{key-takeaway}`).
* Must include the **See Also** block (`(course-core-system-auditing-and-curing-see-also)=` / `:::{seealso}\n:class: dropdown`) with hyperlinked cross-references to Module 11 and Module 13.


Preserve the additive expert-addon construction guidance: assemblies and explicit
AutoDock4 nonpolar-H projection return independent current-primary results,
without automatic chemistry preparation or view adoption. Retain declared
chain/operator/structure scope, typed charge/inventory prerequisites and distinct
direct/merged identity. Keep all original biological scenarios, code, saved
outputs, cell IDs and notebook metadata unchanged in prose-only receiving.


Keep the independent addon atom-expansion routes distinct from hydrogen/pH
preparation: terminal attachment consumes declared parents and all-structure
coordinates with original-axis history; heavy repair uses bounded templates and
can reorder atoms or leave gaps unassessed. Both preserve the source scene and
apply declared loss/invalidation policies to their output, with no implicit
adoption. Preserve all existing code, outputs, IDs and biological scenarios.


Preserve the independent addon H/terminal routes: explicit fixed-state RDKit
materialization and historical evidence are distinct from approximate legacy
pH rules. A selector does not implicitly extract the required single source
structure/state/component. Terminal preparation can complete the opposite free
end. Keep source/scene preservation and native provider/chemistry limits, without
changing original course code, outputs, metadata or biological scenarios.


Keep detached builder and conditional overlap-filter ownership explicit, including
builder domain losses, candidate/reference selection and one-structure decisions.
A no-removal result aliases the primary; neither route implicitly adopts an output.
Preserve original code, saved outputs, IDs and notebook metadata.


Preserve independent peptide construction/substitution guidance, distinguishing
fresh sequence-based geometry from observed coordinates and complete chemistry
from an unassessed target name. Retain native mask/naming/provider/H limits and
all original notebook code, outputs, metadata, IDs and biological scenarios.


Preserve the managed add_missing_bonds guidance: native in-place default,
retained identities, reference-state components/coverage effects and true
no-op behavior. Deferred projection and its retry never repeat science;
independent results remain caller-owned. Preserve original code and outputs.


Preserve the addon alternate-site guidance and native #569/#570/#571 limits.
Distinguish retained indices from changed labels, deferred scene projection
from partial native writes, and projection retry from scientific replay.
All original course code, outputs, IDs and metadata remain unchanged.


Preserve the independent addon solvate route and its one-structure engine-ready
input, explicit molecular preparation, native model/identifier/count limits and
absence of automatic scene adoption. Keep source copying/parity and geometric
receiving separate from simulation-equilibration claims; retain all original
course code, outputs, IDs and metadata.

Preserve independent addon protonation reconciliation with explicit reference-rule
limits and no implicit adoption. Managed in-place removal remains unavailable
until native correspondence is qualified; neither private rules nor identity
matching is a substitute. Keep original course code, outputs, IDs and metadata.

Preserve native mutation-selection repair receiving: masks address source atoms
and enable groups for every request form, with independent no-op copies and
pre-write ID/target validation. Forward native skip_digestion without a consumer
selector translation. Retain all owner course code, outputs, IDs and metadata.
