---
summary: Evaluate AAindex, modlAMP and Peptides for additional physicochemical observables
issue: uibcdf/molsysmt#485
status: partial
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
**Status:** Preliminary inventory and ranking completed. The first selected
Zimmerman bulkiness reader is implemented under uibcdf/molsysmt#487;
wider candidate, original-source, licensing and client-priority reviews remain
partial.

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

## Preliminary inventory — 2026-10-26

Static inspection at source 8cf8b0107b4772c48d220416dc9a4e1f36b38679 identifies
30 direct exports in `physchem/__init__.py` and 49 literal group dictionaries
containing all twenty standard amino-acid keys. Forty-seven have numeric values
for those keys; the count includes historical tables and placeholders and is
not a count of supported observables. Twenty-three dictionaries match at least
one AAindex1 record over all twenty values, without rescaling, at absolute
tolerance 1e-9. The snapshot contains 566 records; its hash is in the receipt.

The public toolbox already exposes hydrophobicity (fifteen named scales),
polarity (two), transmembrane tendency, tabulated surface/volume/burial values,
mass/charge and coordinate-based SASA. Additional chemical-site and chemical-state
tools must not be confused with sequence reference scales. A public export does
not itself establish a complete scientific or unit contract.

The existing bulkiness, flexibility, refractivity, mutability, composition,
accessible-fraction and secondary-structure-propensity tables have no identified
direct public reader in the inspected exports or explicit group-module imports.
This is a bounded source search, not proof that dynamic access is impossible.
In particular:

- Zimmerman bulkiness agrees with AAindex1 ZIMJ680102 at all twenty entries.
- Nine of thirteen secondary-structure-propensity tables match AAindex1 records
  exactly. These are population reference propensities, not predictions or
  assignments of the input's observed secondary structure.
- The Bhaskaran flexibility table differs at nineteen entries from BHAR880101;
  the differences are consistent in magnitude with rounding to two decimals.
  The intended precision/source needs review before exposing it. No values are
  corrected based solely on this comparison.
- The table named `refractivity.jones` matches MCMT640101, whose curated citation
  identifies McMeekin data cited by Jones. Preserve the distinction between the
  original data source and the secondary table source during attribution.
- `aminoacid_composition` stores published reference-population frequencies;
  it does not calculate the composition of the user's selected system.
- `groups/template.py` is a placeholder, not a second bulkiness implementation.

The [inventory receipt](../../devtools/data/physchem_observable_inventory_20261026.json)
records every literal-table/accession match and hashes of inspected local files.
The standard-library-only
[research runner](../../devtools/scripts/audit_physchem_reference_inventory.py)
can reproduce the inventory from an explicitly supplied AAindex1 snapshot:

```bash
python devtools/scripts/audit_physchem_reference_inventory.py \
  --aaindex1 /tmp/aaindex1 \
  --output /tmp/physchem_observable_inventory.json
```

Download the official snapshot separately and compare its SHA-256 with the
receipt when reproducing this checkpoint. The runner does not download data,
import scientific providers or act as a release/scientific-validation gate.
Its controls distinguish the two halves of the AAindex paired header, reject
ambiguous axes and prevent missing values or partial matches being certified.
Numeric matches do not establish units, additivity or redistribution rights.

## Provisional candidate ranking

This ranking weighs reuse, clarity of the scientific contract and likely general
utility. Client demand is still a hypothesis, not an endorsement by another
component. Costs are algorithmic estimates, not measured performance.

| Rank | Candidate | Existing pieces / source | Proposed contract and adoption condition |
| --- | --- | --- | --- |
| 1 | A small set of validated reference readers | Existing Zimmerman bulkiness, Bhaskaran flexibility and secondary-structure propensity tables; AAindex1 | Group-aligned scalar or labelled multi-component outputs; explicit definition, original data source and precision. Start with one or two well-supported scales after units/normalization and licensing review; do not expose all stored tables merely because they exist. |
| 2 | Sequence hydrophobic moment | Existing hydrophobicity readers; Eisenberg method; modlAMP `calculate_moment` and Peptides `hmoment` | Explicit ordered peptide groups, scalar scale, angular increment, window and reduction. Profile versus global/max/mean must be explicit; no window across chain breaks or an unordered/repeated selection. Validate analytic constant/alternating controls and separately compare equivalent provider parameters. |
| 3 | Actual selected-sequence composition | Existing group/sequence information; Peptides `aacomp` | Counts and fractions with explicit denominator, sequence/chain boundaries and unknown/modified-group handling. Keep observed composition separate from stored population frequencies. Counts are integers; fraction and percentage representations must be declared. |
| 4 | Sequence-model charge and isoelectric point | Existing charge stores and fixed-pH reference lookup; modlAMP and Peptides pH/pKa models | Explicit pH, pKa parameter set, ionizable groups and free/capped termini. Predicted mean charge is in elementary charge; pI is a pH coordinate. No implicit replacement of stored formal/force-field charges or enumeration of ChemicalStates. Environment-dependent pKa remains the separate provider work in uibcdf/molsysmt#177. |
| 5 | Selected QSAR descriptor vectors | Peptides Kidera, Z, VHSE and MS-WHIM families | Labelled group-by-component arrays with exact ordering, scaling, version and allowed domain. Standardized coordinates are not independent physical quantities; sum/mean is not a scientific default. Require a concrete modeling client before adding a family. |
| Deferred | Broad scale catalogue, autocorrelation/covariance families and generic downloading | AAindex1 catalogue; modlAMP/Peptides sequence descriptors | Too broad for a first tranche. Establish supported sequence ordering, finite-window semantics, normalization, missing-data policy and real client demand first. AAindex2 substitution matrices and AAindex3 contact potentials are distinct domains, not additional scalar observables. |

### Shared public-contract requirements

All proposed readers remain form agnostic: query the needed group/connectivity
information through existing tools or convert once to a native domain. A
sequence-derived operation must establish chemical sequence order from topology
or a genuine sequence form; sorting group indices is not a substitute. A broken
or disconnected selection cannot silently become a new peptide with artificial
termini. An atom selection cannot silently redefine a complete group descriptor.

Reference lookups need no coordinates or structures. Scalar group readers should
retain established selection order and repetitions, while sequence-window tools
must explicitly define or reject noncontiguous/repeated selections. Unknown,
modified, terminal and dummy groups require a declared policy for each method;
generic zero filling is not a universal scientific rule. Quantity outputs use
PyUnitWizard when physical dimensions are established, with typed empty axes.
Index/vector outputs retain metadata instead of inventing a physical unit.

Bounded lookup and fixed-window sequence calculations need O(n_groups) storage;
a sliding hydrophobic moment admits rolling sine/cosine sums rather than a dense
all-window matrix. These estimates justify starting with existing NumPy tools;
Rust is a later measured-workload decision. No runtime dependency on AAindex,
modlAMP or R is required merely to provide a curated, permitted fixed table.

Scientific criteria stay in `physchem`; reusable connectivity and geometric
operations retain their owning modules. An assumed periodic sequence angle is
not an observed 3-D angle and must not acquire box/PBC semantics. ChemicalStates
continues to own actual chemical assignments. Ackredit should identify the
original method/data and any faithful provider implementation separately; it
must not imply that a table lookup executed the original generation method.

### Source comparison boundaries and remaining decisions

modlAMP defaults to a 100-degree increment and a large/global window; its docstring
suggests 180 degrees for beta strands. Peptides defaults to 100 degrees, an
eleven-group window and maximum reduction, suggesting 160 degrees in its example.
These are different parameter choices, so default-output disagreement would not
demonstrate a faulty implementation. A MolSysMT method must expose these choices
rather than hide them behind a software-name alias. The cited method is
Eisenberg, Weiss and Terwilliger (1984), DOI 10.1073/pnas.81.1.140; the complete
primary method and adopted scale still require bounded verification before coding.

The reviewed Peptides charge/pI functions offer named pKa sets and sequence-level
models. Their values are useful comparison cases, not independent measurements
of charge in an explicit molecular environment. In particular, neither source
settles the physical ECI question under uibcdf/molsysmt#475.

Licensing is not cleared by public access or by matching an existing table.
Review each source's license and the underlying data redistribution terms,
retaining attribution and source pins before copying data/code. No new external
code or table is incorporated by this study. No new observable is implemented.
The next maintainer decision is the first bounded candidate set and whether its
implementation belongs before or after 1.0. Original-source/units review,
license clearance and client priorities keep this proposal partial and open.

## Local qualification of the research tooling

On Linux/Python 3.14.7, the six synthetic inventory controls pass in 4.00 seconds
with `python -m pytest devtools/tests/test_physchem_reference_inventory.py
--receptor=llm -n 12`. The runner also reads the pinned 566-record snapshot and
reproduces the 30/49/47/23 inventory counts above. Selected Ruff check/format,
developer-guide validation and generated-index checks pass. No molecular
runtime implementation, table entry, dependency or public signature changes.
These are research-tool controls, not validation of any proposed observable.

## First-candidate review: Zimmerman bulkiness — 2026-10-26

The bounded first candidate is an explicit public reader of the existing
`groups/bulkiness.py` table. Its twenty entries agree exactly with both
AAindex1 ZIMJ680102 and the official
[ProtScale bulkiness page](https://web.expasy.org/protscale/pscale/Bulkiness.html).
No new table is needed. Agreement with a curated table is implementation/data
parity, not verification of physical dimensions or the original derivation.

### Definition and units: distinguish the evidence sources

The original reference is Zimmerman, Eliezer and Simha (1968), *Journal of
Theoretical Biology* 21, 170–201, DOI
[10.1016/0022-5193(68)90069-6](https://doi.org/10.1016/0022-5193(68)90069-6),
PMID 5700434. The accessible publisher abstract confirms the work's use of
bulkiness among six reference scales for sequence statistics. The complete
original table and normalization were not accessed; they are not claimed as
verified. AAindex and ProtScale identify the reference and all twenty numbers
but neither inspected entry explicitly specifies the physical unit.

There is additional, directly inspectable evidence for an area interpretation.
Proust et al. (2019), DOI
[10.3389/fmicb.2019.00906](https://doi.org/10.3389/fmicb.2019.00906), define the
Zimmerman bulkiness used in their original research as average side-chain
section in angstrom squared (Table 1). Their reported approximate mean across
the twenty standard amino acids is 15.4 angstrom squared. The unchanged local
table gives 15.3675, which rounds to that value. This supports the later
published area convention; it does not independently certify every original
1968 entry or reconstruct its molecular measurements.

Descriptions of a side-chain volume/length ratio are useful leads for the
original derivation, not a formula verified from the original full text in this
review. Do not turn the bare word "index" into a dimensionless declaration.
Conversely, do not assert that a reference lookup measures the actual selected
system's steric cross-section or coordinate-dependent surface area.

### Reviewed public boundary (adopted under #487)

The candidate signature follows the adjacent reference readers:

```python
msm.physchem.get_bulkiness(
    molecular_system,
    element='group',
    selection='all',
    definition='zimmerman',
    syntax='MolSysMT',
    skip_digestion=False,
)
```

This boundary is implemented under uibcdf/molsysmt#487. The return is a
PyUnitWizard area quantity with shape `(n_groups,)`, standardized to the active
unit policy. Explicit angstrom-squared extraction retains the unchanged table
scale: ALA 11.5 angstrom squared corresponds to 0.115 nm squared. No per-system
sum or peptide average is inferred by the group reader.

The supported population is the twenty named standard amino-acid groups. The
reader requires group identities, not coordinates, explicit hydrogens, a force
field, a particular chemical state or a structure axis. Inputs with that
information remain form agnostic, including native MolSys/Topology, MolSysDict
and suitable files. Structures alone cannot supply group identities. String
selections use the requested syntax; numeric group indices preserve order and
repetitions; an empty selection retains a floating zero-length quantity axis.
Unsupported population levels should fail before selection resolution.

Unknown or modified names must not silently acquire parent-amino-acid values.
Terminal caps and dummy groups also need explicit treatment. For this new
physical descriptor, the recommendation is an error for unsupported groups,
including DUM/X, rather than assigning an invented zero area. The existing
private group-table helper currently returns zero for dummy groups in legacy
readers. Reuse it only after a small general extension permits strict lookup
without changing those existing callers; do not duplicate the table-lookup
mechanism or silently change all legacy property semantics.

A peptide-average workflow can later perform an explicitly documented reduction
of the selected quantities. A tabulated amino-acid bulkiness sum is not the
physical area of a whole molecule; the reader therefore should not advertise
system/molecule/chain output axes merely because they can be added numerically.

### Attribution and implementation boundary

Use the existing lazy optional Ackredit boundary once per successful lookup,
including evaluated-empty lookups. Identify the original reference scale and
the later published unit interpretation separately. Cite AAindex/ProtScale as
curation/validation evidence without claiming to execute their software or
assuming that numeric agreement establishes the historical source of MolSysMT's
table. An absent/failing attribution provider must not alter completed values.
The docstring and maintained reference documentation remain usable without it.

The public reader belongs in `physchem`; its reusable strict table-lookup policy
belongs in the existing group helper. No new chemical store, sequence object,
network access, optional scientific runtime dependency or Rust kernel is needed
for this O(n_groups) lookup. This is a workload estimate, not a benchmark claim.

### Qualification requirements adopted under #487

- Compare all twenty outputs against the independently inspected curation,
  retaining explicit source identifiers, precision and unit interpretation.
- Assert values, shape and dimensionality under nm/angstrom/pm standard-length
  policies, including typed empty outputs and selected order/repetitions.
- Exercise native and file/dictionary routes and alternate selection syntax;
  verify detached outputs and unchanged source domains.
- Check explicit unsupported-group and unsupported-element diagnostics,
  including terminal caps, modified names and dummy groups.
- Check optional attribution absence, active-session reuse and provider failure
  without presenting those controls as scientific validation.
- Complete docstring, Toolbox, Foundations, Cookbook and shared/four-path course
  coverage, stability classification and scoped scientific-evidence accounting.
  The original paper's uninspected derivation must not be promoted to verified.

### Provenance and remaining boundary

The [candidate receipt](../../devtools/data/zimmerman_bulkiness_review_20261026.json)
records inspected references, curation snapshot hashes, the unchanged local-table
hash, the twenty-value comparisons and the proposed unit/scope contract.
The SIB portal's terms defer to each resource's own conditions; portal access is
not blanket permission to copy arbitrary underlying code or data. The 2019
research article explicitly declares CC BY. This review imports no external code
or table and does not assert a new license for the existing historical table.

No public reader, runtime behavior, dependency or scientific-evidence promotion
is implemented by this review. The candidate now has a concrete contract for
maintainer selection; original-derivation access and any further data-rights
question stay explicit rather than being hidden behind numeric agreement.

The existing six research-runner controls pass again (3.93 seconds) and the
unchanged local-table hash is rechecked. Developer-guide schema/link/index
validation passes. These controls do not test a new molecular observable or
replace the pending scientific/adoption decisions.

## First implementation received

The reviewed reader is now implemented as experimental `physchem.get_bulkiness`
under uibcdf/molsysmt#487. The proposed quantity/selection/strict-lookup contract
and optional attribution are covered by public tests and the documentation/course
lifecycle. The implementation uses existing data and general helpers. See
[its qualification receipt](../../devtools/data/zimmerman_bulkiness_implementation_20261026.json).
This proposal remains partial for the remaining candidate inventory and choices;
the original 1968 derivation is still outside the audited scientific claim.

## Second-candidate review: secondary-structure propensities — 2026-10-26

**Inspected and data-parity checked; proposed, not implemented.** The thirteen
existing dictionaries in `groups/secondary_structure_propensity.py` agree with
all 260 named values on the corresponding official ProtScale pages. Nine also
match complete AAindex1 vectors in the pinned 566-record snapshot. The four
Deleage/Roux vectors have no exact AAindex1 match under this comparison; their
complete agreement with ProtScale is separate positive evidence. A missing
AAindex match alone does not establish an error.

The [review receipt](../../devtools/data/secondary_structure_propensity_review_20261026.json)
records the source commit and local-file hash, all thirteen URLs and capture
hashes, the accession matches and the independent primary-paper transcription.
The comparison parses twenty named values per page and compares by group name;
it neither rescales data nor treats a partial match as complete. No runtime
constant or public API is changed by this review.

| Existing family | Complete ProtScale comparisons | Matching AAindex1 accessions | Source boundary |
| --- | --- | --- | --- |
| Levitt: helix, sheet, turn | 60/60 | LEVM780101, LEVM780102, LEVM780103; helix/sheet also PRAM900102/103 | Weighted relative frequencies; original detailed Tables III–V checked visually |
| Chou/Fasman: helix, sheet, turn | 60/60 | CHOP780201, CHOP780202, CHOP780101 respectively | Helix/sheet match 1978b, but the stored turn vector matches 1978a |
| Deleage/Roux: helix, sheet, turn, coil | 80/80 | No exact match in this snapshot | Curated values confirmed; original derivation not fully audited here |
| Lifson/Sander: total, antiparallel, parallel strand | 60/60 | LIFS790101, LIFS790103, LIFS790102 respectively | Distinct strand categories; no generic three-class predictor inferred |

### Primary-paper check and variant distinctions

Levitt (1978), DOI [10.1021/bi00613a026](https://doi.org/10.1021/bi00613a026),
defines relative frequencies against a reference population. The weighted
`P_ij` columns of detailed Tables III, IV and V match all sixty existing values.
These ratios are dimensionless, may exceed one and are not per-group class
probabilities. They must not be clipped, normalized to sum to one or interpreted
as an observed secondary-structure assignment.

The original was inspected using the
[institutional reprint](https://web.stanford.edu/class/sbio228/public/readings/Structure_Prediction_I_Lecture8/Levitt_BIOC_78_Conformational_prefs.pdf).
The receipt pins its SHA-256. Several turn entries in summary Table II differ
from detailed Table V; the existing vector matches the latter. This review does
not infer the reason or correct either table. The AAindex weighted/unweighted
variants are also distinct: LEVM780104–106 must not replace LEVM780101–103
merely because they share an author and year.

The current source comment attributes the Chou/Fasman family to the 1978b
reference, but its stored turn vector matches CHOP780101 (1978a), DOI
[10.1146/annurev.bi.47.070178.001343](https://doi.org/10.1146/annurev.bi.47.070178.001343).
It differs at fourteen entries from CHOP780203 (1978b, PMID 364941).
This establishes numeric variant identity, not the historical origin of the
local data. A future reader must name the adopted variant explicitly rather
than publish a silently mixed `chou_1978` family. No existing values or comments
are rewritten in this research checkpoint.

Deleage/Roux (1987), DOI
[10.1093/protein/1.4.289](https://doi.org/10.1093/protein/1.4.289), describes a
prediction algorithm as well as compositional parameters. Reading the existing
tables would not reproduce that algorithm. Lifson/Sander (1979), DOI
[10.1038/282109a0](https://doi.org/10.1038/282109a0), distinguishes parallel and
antiparallel strands; a future API must preserve that distinction. Full original
method/table checks for these families remain pending before adopting them.

### Recommended first public boundary

Start with the primary-checked Levitt vectors, reusing existing data and the
strict group-table helper introduced for bulkiness. Proposed signature:

```python
msm.physchem.get_secondary_structure_propensity(
    molecular_system,
    conformation,
    element='group',
    selection='all',
    definition='levitt_1978_weighted',
    syntax='MolSysMT',
    skip_digestion=False,
)
```

`conformation` is required and accepts `alpha_helix`, `beta_sheet` or
`reverse_turn`. This name avoids confusing the requested reference category
with MolSysMT's coordinate structures axis. One requested category produces
one group-aligned float64 array with shape `(n_groups,)`, including `(0,)` for
an empty selection. The proposed bare-array contract explicitly denotes a
dimensionless frequency ratio; no physical unit is invented. PyUnitWizard
continues to handle actual physical quantities in adjacent readers. A later
quantity/labelled-output extension must be explicit rather than depend on the
selected definition.

Group names are obtained through the form-agnostic public query path. Numeric
selection order and repetitions are preserved. Only the twenty supported
standard amino-acid identities are accepted initially; unknown, modified,
terminal-cap and dummy groups fail explicitly without zero filling or implicit
parent substitution. No coordinates, structure indices, force field, chemical
state assignment or sequence window are needed. An atom subset must not silently
redefine the full-group descriptor.

This tool belongs in `physchem`. Observed coordinate-based assignment remains
separate in `structure.get_secondary_structure`; this reader must not claim to
execute DSSP, a sequence predictor or the original table-generation procedure.
No average, argmax class, artificial coil remainder or peptide-level reduction
is a default. Future definitions must reject unsupported conformation/definition
combinations rather than mix source families silently.

Use ArgDigest and the established `skip_digestion` contract. Optional Ackredit
should credit Levitt's reference data and separately identify curated validation
sources; attribution must not suggest execution of those providers. The lookup
needs O(n_groups) output and no new dependency, runtime HTTP request or compiled
kernel. This is a complexity estimate, not a performance measurement. A Rust
implementation would require a demonstrated workload benefit.

### Adoption and qualification still required

Before coding, accept this public boundary and the bounded first definition.
Implementation must complete docstrings, User Guide, Cookbook and all course
paths, public API stability classification and appropriately bounded scientific
evidence. Tests should independently compare all sixty primary-checked entries,
assert dimensionless non-probability semantics and preserve native/file/dict
parity, selection order/repetitions, empty shape and detached outputs. Exercise
unsupported populations/categories, optional attribution and unchanged source
objects. Table parity does not validate secondary-structure prediction accuracy.

No external runtime table or code is copied. The institutional reprint's access
does not grant blanket redistribution rights; source attribution and any data
rights questions remain explicit before expanding the catalogue. The existing
lookup data are unchanged. This research extends uibcdf/molsysmt#485, which stays
partial and open; it does not expand the release gate or authorize publication.

Checkpoint controls on Linux/Python 3.14.7: the six existing inventory-parser
controls pass in 3.90 seconds with Pytest Receptor and twelve workers. The new
receipt also passes JSON parsing, thirteen-table/260-entry completeness and
zero-mismatch assertions. Developer-guide validation, generated-index checks
and `git diff --check` pass. These are research/data-parity controls; no new
molecular runtime behavior or prediction benchmark is claimed.


## Second implementation received

The bounded Levitt reader is implemented as experimental
`physchem.get_secondary_structure_propensity` under uibcdf/molsysmt#489, with
explicit category selection, dimensionless float64 outputs, strict supported
group identities and optional original-source attribution. The original sixty
values remain unchanged. The complete reference-table claim has independent
primary-table controls; no sequence-prediction or observed-assignment accuracy
is implied. See [its implementation receipt](../../devtools/data/secondary_structure_propensity_implementation_20261026.json).
The wider catalogue and remaining variant/source decisions keep #485 open.

## Broader physicochemical priorities — 2026-10-26

**Requested:** the maintainer asked whether further reference tables risk making
`physchem` an outdated property catalogue. This is an inspected capability review
and a recommendation for discussion, not implementation authorization or an
accuracy benchmark. The earlier ranking compared a bounded set of reference and
sequence readers; it must not be interpreted as the priority of the entire module.

A classic scale remains useful for reproducing a published descriptor. Its age
alone does not invalidate it, but a name-based amino-acid lookup cannot represent
the actual molecule's protonation, conformation, solvent exposure or local
field. Adding more such lookups has diminishing value after the two bounded
readers already delivered. Conversely, a recent learned method is not inherently
more accurate, physically interpretable or appropriate outside its training domain.
The useful distinction is reference data versus explicit molecular models and
coordinate-dependent observables, with declared applicability and evidence.

### Inspected existing foundation

At source 5681f5e78, `physchem` already exposes coordinate-based SASA, chemical
readiness, aromaticity/CIP interpretation, charge centers, site recognition and
partial-charge tools in addition to reference scales. These must be reused.
`get_partial_charges` currently supports Gasteiger–Marsili through RDKit and
force-field template charges through OpenMM, with explicit chemical admission
and charge conservation. It does not currently expose AM1-BCC, NAGL or general
quantum-derived charges. A bounded search found no public TPSA/logP, dipole,
electrostatic-potential or general electronic-property reader in the inspected
physchem exports. This is a source inventory, not proof of missing capability
in every external adapter.

### Recommended capability priorities

| Priority | Capability and concrete use | Existing pieces / candidate reference | Boundary to settle before coding |
| --- | --- | --- | --- |
| First bounded tranche | State-aware molecular TPSA and predicted logP, useful to DockingMT and PharmacophoreMT | Complete chemical graph and RDKit conversion; official RDKit `CalcTPSA` and Wildman–Crippen `MolLogP` | Whole-molecule population; declared protonation/tautomer and hydrogen treatment; model definition, contributions and units. A selected fragment must not become a silently capped molecule. TPSA is a topological area descriptor, not geometric SASA; predicted logP is not pH-dependent logD. Client usefulness is a hypothesis pending feedback. |
| High scientific value, larger contract | Environment-dependent pKa and state populations | Existing ChemicalStates, chemical preparation and uibcdf/molsysmt#177; PROPKA | Protein/complex applicability, index maps, required coordinates and protonation model. pKa, site occupancy and coupled microstate probabilities are distinct. A collection of predicted pKa values is not automatically a validated microstate ensemble. |
| Extend an existing tool | Additional partial-charge models for small molecules | Existing public charge calculation/assignment split; OpenFF Toolkit AM1-BCC and OpenFF NAGL | Explicit provider/model and model-file identity, chemical domain, conformer generation policy, total charge, original atom maps and force-field compatibility. Do not silently change charge methods based on installed software. |
| Structure-dependent descriptors | Polar/nonpolar solvent exposure and interface burial; dipole from declared point charges | Existing SASA, charge retrieval, coordinate/geometry/PBC tools | Explicit atom classification and radii/probe; complex versus separated reference state for burial. Charge-based dipoles require a declared origin for charged systems, compact molecular reconstruction under PBC, charge model and units. A point-charge dipole is not an electronic-structure calculation. Geometric shape primitives remain in `structure`. |
| Later provider integration | Electrostatic potentials and continuum-solvation properties | APBS; existing charges, radii and structural forms | Explicit dielectric/ionic-strength/temperature, boundary conditions, grid and units. Input preparation and iterative workflows may belong in Praxis; do not reimplement a mature solver or equate Coulomb and screened Poisson–Boltzmann models. |
| Research/client-driven | Electronic properties and local atomistic descriptors | xTB electronic-property interfaces; DScribe SOAP/MBTR | Separate approximate electronic observables from representation vectors. Require charge/spin, geometry, method and model domain. SOAP vectors have an explicit basis/species/cutoff and are not direct physical measurements. No indiscriminate learned-descriptor catalogue or hard dependency is proposed. |

### Sources and limits

Official documentation inspected on 2026-10-26:

- [RDKit molecular descriptors](https://www.rdkit.org/docs/source/rdkit.Chem.rdMolDescriptors.html)
  and [Crippen](https://www.rdkit.org/docs/source/rdkit.Chem.Crippen.html)
  document TPSA and atom-based logP/MR. These established models are not recent
  inventions; their value here is chemical-graph-based molecular scope and
  integration into current workflows. Original formulas/units still require
  bounded verification before implementation.
- [OpenFF charge assignment](https://docs.openforcefield.org/projects/toolkit/en/stable/api/generated/openff.toolkit.topology.Molecule.html)
  distinguishes charge methods, conformer use and provider requirements.
  In particular AM1-BCC-ELF10 is not interchangeable with single-conformer AM1-BCC.
- [NAGL AM1-BCC GNN model](https://docs.openforcefield.org/projects/nagl-models/en/stable/models/openff-gnn-am1bcc-1.0.0/)
  targets charges resembling an ELF10 implementation, with a specified element
  domain and molecular charge constraint. This does not establish universal
  electrostatic accuracy or justify replacing force-field charges.
- [PROPKA](https://propka.readthedocs.io/en/stable/command.html)
  predicts ionizable-group pKa from protein/complex structures; the existing #177
  owns integration decisions. That source is not evidence of a universal
  arbitrary-ligand pKa model.
- [APBS](https://apbs.readthedocs.io/en/latest/)
  supplies continuum electrostatics. Solver outputs depend on the declared
  physical model and preparation; no solver or package qualification was run.
- [xTB properties](https://xtb-docs.readthedocs.io/en/latest/properties.html)
  expose dipoles, population charges, orbital information and bond-order
  analysis. This inspection does not establish their accuracy for MolSysMT clients.
- [DScribe SOAP](https://singroup.github.io/dscribe/latest/tutorials/descriptors/soap.html)
  specifies local geometric representations with configurable species, cutoff,
  basis, periodicity and output size. Fingerprint quality requires a downstream
  task and benchmark, not a declaration of generic physical superiority.

Method and implementation names must remain distinct. Use named original
criteria/models where known, credit faithful/adapted implementations separately
and retain method parameters, units, producer versions and optional Ackredit
attribution. Python form-agnostic validation, explicit chemical-state admission,
source maps and lazy providers are more valuable than copying a provider's entire
API. Calculations need bounded execution for large structure sets; no performance
or memory claim is made without workload measurements.

### Proposed direction; maintainer decision pending

Pause automatic expansion of the reference-scale catalogue. Keep the completed
bulkiness/Levitt readers for reproducibility and record the remaining variants.
The next new bounded molecular-property design should compare TPSA and logP
contracts; pursue environment-sensitive pKa under its existing owner in parallel
only when its larger mapping/preparation contract is accepted. Evaluate charge
model extensions against actual force-field/client needs.

Simple graph counts belong in `topology` when reusable independently; chemistry
interpretation remains in `physchem`, HB-specific definitions in
`interactions.hbonds`, observed interactions in `interactions`, construction and
stored assignment in `build`/ChemicalStates, geometric operations in `structure`
and periodic reconstruction in `pbc`. Small-molecule-specific wrappers may use
`element.molecule.small_molecule`, but the model and generally useful operations
must not be hidden in client pipelines. Scientific workflow orchestration and
compound scores such as drug-likeness may belong in the consuming component or
Praxis rather than becoming universal physical attributes.

This recommendation does not remove existing APIs, add a dependency, adopt a
new predictor, or move the 1.0 publication boundary. Original-source, license,
provider compatibility, client feedback and benchmark reviews are still needed
for each adopted capability. No extra implementation is included in #490.

## TPSA/logP public-contract study — 2026-10-26

**Reviewed proposal:** TPSA was subsequently implemented under #492; logP remains
a proposal. The maintainer accepted studying the first
molecular-descriptor contract. The [review receipt](../../devtools/data/tpsa_logp_contract_review_20261026.json)
records thirteen RDKit characterization cases, five bounded original-table TPSA
sums, unchanged provider inputs and explicit/implicit hydrogen parity. These
checks do not qualify a public MolSysMT implementation or establish experimental
partition/transport accuracy. The installed RDKit 2025.9.5 and inspected clean
RDKit checkout cbfb37abddcd5b5feeac97d53530ae6be83cac0d are identified separately.

### Scientific definitions and method variants

TPSA uses Ertl, Rohde and Selzer (2000), doi:10.1021/jm000942e. The
[author-hosted paper](https://www.peter-ertl.com/reprints/Ertl-JMC-43-3714-2000.pdf)
explicitly labels Table 1 contributions in angstrom squared. Five simple fragment
sums agree with the executed provider. This is a fitted topological descriptor,
not an observed geometric surface or a guarantee of permeability.

The [RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html#implementation-of-the-tpsa-descriptor)
explains that its default N/O-only variant follows the reference implementation
and comparison table, while the paper's fragment table also includes S/P.
The proposed default is N/O-only for reproducible conventional behavior, with
explicit `include_sulfur_phosphorus=True` enabling the other supported subset.
Neither option is claimed universally superior. In the characterized foscarnet
example they give 94.83 and 104.64 angstrom squared respectively. Keep this
choice in metadata and tests; never silently change it with software versions.

LogP uses Wildman–Crippen (1999), doi:10.1021/ci990307l, through the executed
RDKit implementation. It is a dimensionless predicted octanol/water partition
logarithm, not logD at a specified pH. The original publisher full text returned
403 in this review; the exact original typing/derivation remains unaudited.
RDKit's documented implementation and local C++ source were inspected. Any
initial implementation must retain that distinction in its experimental evidence.
The provider's ability to return a number for an ion or disconnected salt does
not establish a physical whole-salt partition coefficient.

### Recommended public signatures

Use short established descriptor names, consistent with `get_sasa`, without
reusing `get_surface_area` or changing its historical reference-table contract:

```python
# Reviewed interfaces: get_tpsa is implemented under #492; get_logp remains proposed.
msm.physchem.get_tpsa(
    molecular_system,
    element='molecule',
    selection='all',
    structure_indices='all',
    chemical_state='reference',
    method='ertl_rohde_selzer',
    include_sulfur_phosphorus=False,
    return_report=False,
    syntax='MolSysMT',
    skip_digestion=False,
)
msm.physchem.get_logp(
    molecular_system,
    element='molecule',
    selection='all',
    structure_indices='all',
    chemical_state='reference',
    method='wildman_crippen',
    return_report=False,
    syntax='MolSysMT',
    skip_digestion=False,
)
```

Initially support only the molecule element. Numeric selections are molecule
indices, preserving requested order and repetitions. String selections use the
ordinary molecule-level selection contract; an atom-based expression may identify
whole molecules but must never truncate their graphs. The report must make the
complete source atom membership explicit. Do not introduce an undocumented
atom-index interpretation or silently calculate a selected capped fragment.

Each selected molecule must be a complete connected covalent graph in the
chosen chemical state, with no bonds crossing its boundary. A molecular label
containing disconnected salt components fails this first contract. A source
containing several separately selected valid molecules returns one value for
each; values are not summed as a system-level logP. Preserve source molecule
indices rather than replacing them with ad hoc component labels.

TPSA may evaluate supported charged graphs. For the first `get_logp` contract,
recommend rejecting molecules with nonzero net formal charge, without automatic
neutralization, counterion removal or tautomer selection. This is a proposed
scientific scope decision, not a limitation of RDKit's numerical API. Net-zero
graphs can contain formal atomic charges (nitro groups and zwitterions); do not
reject every graph with a nonzero atomic charge. A net-zero admission check is
not evidence that the prediction is accurate for all zwitterions. Broader ionic
model scores need a separately named and reviewed contract, not a claim of logD.

TPSA returns a PyUnitWizard area quantity of shape `(n_selected_molecules,)`,
standardized to the active policy. LogP returns a float64 array of the same shape,
explicitly dimensionless. Retain `(0,)` for empty selections. There is no
structure axis: coordinates are needed only for a spatial selection, and
structure indices also resolve structure-associated chemistry. Requests resolving
to different chemical states must fail initially rather than silently average.

With `return_report=True`, return `{'tpsa': quantity, 'report': ...}` or
`{'logp': array, 'report': ...}`. The detached report should retain source
molecule indices and ragged source atom membership, chemical-state index/digest,
net formal charges, exact method/options, hydrogen treatment, atom inventory,
producer versions and original bibliography. Default scalar-column returns are
not persistent records; callers needing provenance should request the report.

### Reuse and implementation boundary

Reuse chemical_graph_context, validate_chemical_frames, native chemical-state
storage and general conversion/selection. Use full-source covalent membership
from topology tools to establish boundary completeness, then construct only the
selected intact molecular graphs. get_covalent_blocks computes an induced
selected graph; invoking it only after cutting away external atoms would not
prove boundary completeness. Generic graph/molecule admission belongs in the
existing topology/native owners, with a new public tool only if its independent
contract warrants one. Do not hide competing molecular inference in physchem.

The exploratory molecule-axis check uncovered uibcdf/molsysmt#491: a group-free
RDKit graph converts with valid covalent components but zero molecule inventory,
and public molecule queries raise. That general defect must be addressed before
claiming the molecule-level boundary works across supported forms. It must not
be worked around with a TPSA-only partition or fabricated biological groups.

Require declared complete connectivity, valid elements/orders/charges and a
supported closed-shell concrete graph. Reject query/dummy atoms, unsupported
metals, radicals and dative relationships in the first bounded profile. Sanitize
on detached working graphs, retaining source correspondence and detecting known
chemical contradictions. Honor declared indexed and nonindexed hydrogen counts.
Any provider materialization of those hydrogens occurs only on a temporary graph,
never as scientific preparation or a change to the source atom axis. Undeclared
missing hydrogen inventory must not be silently guessed to obtain a value.

RDKit calculates descriptor caches on molecules, and Crippen's provider path can
add hydrogens. Copy the working molecule and request force=True with explicit
options, so user caches and hydrogen-presentation choices cannot leak across
calculations. Both providers already use compiled kernels; start without a new
Rust implementation or duplicate coefficient table. Use lazy DepDigest,
ArgDigest, explicit units and the existing optional Ackredit boundary. Credit
original models separately from actual RDKit execution. No package or predictor
is added by this study, and no timing/memory advantage has been benchmarked.

### Implementation sequence and acceptance

1. Resolve and regression-test the general molecule-inventory/query defect #491.
2. Confirm this boundary, especially N/O versus N/O/S/P and neutral-only logP.
3. Implement TPSA first, with full unit-policy, chemical-state and molecule-axis
   coverage; then share only genuinely general admission/reporting pieces with
   logP. Do not expose atom contributions until their source/H mapping is designed.
4. Check primary simple-fragment TPSA oracles separately from equivalent-provider
   parity. Keep original logP derivation and experimental prediction evidence
   explicitly partial until independently reviewed.
5. Cover implicit/indexed H parity, stale provider caches, source immutability,
   salts, mixtures, ionic/neutral pairs, nitro/zwitterion controls, malformed
   chemistry, molecules crossed by state-specific bonds, all supported form
   routes and rich/default/explicit-state selections. Test pm/angstrom/nm area
   policies and typed empty results; no artificial coordinate-axis expansion.
6. Complete optional attribution absence/failure/enclosing-session checks,
   detached report persistence through a reviewed typed unit boundary, public API
   classification, docstrings, User Guide, Cookbook and course lifecycle.

This study establishes a concrete proposal, not new functions or an expanded
1.0 release gate. #485 remains partial; #491 owns the independently reusable
prerequisite fix. Whether to adopt the two new functions before 1.0 is a separate
maintainer decision after this contract review.


## Molecular TPSA implementation received

Experimental `physchem.get_tpsa` is implemented under uibcdf/molsysmt#492,
following the reviewed molecule/chemical-state/unit boundary. General group-free
molecule membership is repaired under uibcdf/molsysmt#491 without inventing groups.
The implementation reuses general graph/aromaticity/conversion tools and the
compiled RDKit descriptor, preserving actual scientific references and producer
versions through optional Ackredit. Initial native SDF scope requires explicit
valence/H evidence; absent hydrogen inventory fails rather than being guessed.
LogP is not implemented: its charged-state scope remains a separate decision.
See [qualification](../../devtools/data/molecular_tpsa_implementation_20261026.json).
The wider capability review remains partial and open.
