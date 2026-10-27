---
summary: Evaluate AAindex, modlAMP and Peptides for additional physicochemical observables
issue: uibcdf/molsysmt#485
status: open
opened: 2026-10-26
closed:
verification: inspected
area: [physchem, attribute, api, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluating external sources for physicochemical observables

**Requested:** 2026-10-26 by the maintainer during the Collantes review.
**Status:** Open exploration proposal; no new observable or implementation adopted.

## What

Assess whether AAindex, modlAMP and Peptides R can support useful additions to
MolSysMT's public physicochemical tools and reference datasets. Inventory current
coverage first, identify actual client needs and produce a ranked implementation
proposal. Distinguish direct molecular observables, sequence-derived descriptors,
reference scales and learned statistical embeddings.

## Why

The Collantes review exposed both the value and limits of third-party sources:
modlAMP agrees with the current twenty ISA and twenty ECI entries, but supplies
no explicit physical unit for that table. The current 566-record AAindex1 text
contains no identified Collantes/ISA/ECI record under the searched references.
Peptides R exposes multiple other descriptor families and pH-dependent charge
calculations. The same audit could reveal reusable capabilities for suite clients,
provided numeric compatibility is not mistaken for scientific validation.

Related work: uibcdf/molsysmt#473 (ISA units), uibcdf/molsysmt#475 (ECI dimension
and aggregation), uibcdf/molsysmt#177 (environment-dependent PROPKA integration),
uibcdf/molsysmt#27 (optional attribution) and uibcdf/molsysmt#334 (release scope).

## Sources inspected and reproducibility

- Official AAindex1: https://www.genome.jp/ftp/db/community/aaindex/aaindex1
- modlAMP source: https://github.com/alexarnimueller/modlAMP/tree/458c4dbb4c7888208ce3d9326484906b95324801
- Peptides R source: https://github.com/dosorio/Peptides/tree/a1a91be11bd6ba183541008cd038e328b4c33868
- Source inventory, hashes, bounded searches and Collantes comparison:
  [audit receipt](../../devtools/data/collantes_external_sources_20261026.json).

These pins identify inspected sources, not scientific endorsement or permission
to redistribute every underlying table. This is not a full original-paper audit.

## How

### Inventory and useful candidates

Compare current MolSysMT mass, charges, radius, hydrophobicity, polarity,
transmembrane tendency, surface/volume descriptors and geometric SASA against
source capabilities. Candidate directions for assessment include:

- Additional curated group/amino-acid reference scales, such as flexibility,
  bulkiness and supported conformational propensities, with explicit scope.
- Sequence-composition indices and hydrophobic moments where clients need them.
- pH-dependent sequence charge and isoelectric-point models, distinguished from
  environment-dependent pKa and actual stored formal/force-field charges.
- QSAR descriptor families such as Kidera, Z-scales, VHSE and MS-WHIM, correctly
  identified as descriptor vectors rather than assigned physical quantities.

These are exploration categories, not promised API names or a claim that each
is absent today. Determine which are independently useful and which belong in
another owning provider or scientific workflow.

### Required candidate matrix

For every proposed capability, record:

1. Existing equivalent and owning module/provider; concrete client use.
2. Input information and supported element axes, using groups rather than a
   generic residue axis; source-index and chemical-state interpretation.
3. Scientific definition, original reference, method name and provider algorithm.
4. Physical dimension, units, normalization and legal aggregation operations;
   mark unknown values explicitly rather than deriving units from magnitude.
5. Applicability and missing/unsupported-group behavior; whether structures,
   periodic geometry, sequence, stored chemistry or parameterization are needed.
6. Independent validation examples and justified numerical tolerances, alongside
   separate implementation-parity and compatibility controls.
7. Runtime/dependency, memory and scalability costs, plus reusable suboperations.
8. Data/code license and redistribution constraints, source version, citation and
   optional Ackredit integration requirements.
9. Expected API/doc/course impact, priority and adopted/deferred decision.

### Implementation principles if accepted

Keep public tools form agnostic, ArgDigest-validated and consistent with current
selection, index and skip_digestion conventions. Use PyUnitWizard for physical
quantities; preserve explicit descriptor semantics for normalized/index outputs.
Do not classify an index as net charge or infer additivity from the existence
of a generic sum/mean operation. Keep chemical assignments in ChemicalStates.

Reusable chemical-property tools belong in physchem; connectivity, geometry and
periodic helpers remain in topology, structure and pbc. Reuse existing primitives
and compose workflows from them. Scientific criteria and source assumptions must
remain explicit. Do not add a runtime network dependency merely to read a fixed
reference table. Curated distributed data must retain exact provenance and an
appropriate update policy. Optional attribution must distinguish table lookup
from execution of the original descriptor-generation method.

## Acceptance and deliverables

Deliver a reviewed inventory/ranking, an explicit rejected/deferred list with
reasons, scientific/data provenance, proposed public contracts and a bounded
first implementation tranche with meaningful validation plans. Actual adopted
APIs require the normal User Guide, Cookbook, course, docstring and test lifecycle.

The proposal can be studied during the current research window. Adding new
observables is a separate maintainer decision and does not automatically extend
the MolSysMT 1.0 gate or authorize a new dependency, release or publication.
