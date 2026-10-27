---
summary: Implement state-aware Wildman-Crippen molecular lipophilicity descriptors
issue: uibcdf/molsysmt#496
status: resolved
opened: 2026-10-27
closed: 2026-10-27
verification: measured
area: [physchem, api, chemical-states]
guard: tests/physchem/test_get_lipophilicity.py::test_equivalent_forms_preserve_supplied_state_and_provider_score
normative:
blocked_by: []
supersedes: []
---

# State-preserving molecular lipophilicity descriptors

**Requested:** 2026-10-27; the maintainer accepted the model-descriptor boundary
reviewed under uibcdf/molsysmt#485.
**Status:** Implemented and locally qualified; API remains experimental and
scientific evidence partial.

## What

Expose experimental `physchem.get_lipophilicity(method='wildman_crippen')` for
complete molecules in their supplied chemical state. Return dimensionless
float64 scores or a score/report pair with original producer versions, source
maps, charges and scientific attribution. Supported charged graphs are evaluated
without pretending the score certifies a physical logP or computes logD.

## How

The public tool is form agnostic, ArgDigest-validated, SMonitor-instrumented and
lazily requires the existing optional RDKit provider. It reuses the same molecule
membership, state resolution, declared-H, aromaticity and covalent-boundary
checks as TPSA through private `physchem._molecular_descriptors`. Existing general
chemistry/conversion tools remain the owners of graph interpretation; no new
chemical store, molecular partition or public implementation-detail API is added.
TPSA's public signature, units and report schema are retained.

The calculation invokes compiled `CalcCrippenDescriptors(includeHs=True,
force=True)` on a detached working graph. Materialized H atoms correspond to
declared inventory; this is not molecular preparation. Repeated molecule indices
reuse a calculation within the call; the source atom correspondence is retained
in the repeated output rows. Selected covalent boundaries are checked in one
pass over source bonds, and source coordinate series are not copied.

The report uses `molsysmt.lipophilicity@1`, a dimensionless model-score value kind,
source molecule indices and ragged atom indices, state index/label/digest, net
formal charges in elementary-charge units, and ragged charged source atom indices.
Charged indices describe the graph, not a resonance/zwitterion classification.
Parameters declare no chemical preparation and inclusion of hydrogen
contributions. Original Wildman–Crippen bibliography and executed MolSysMT/RDKit
versions are detached into the result; optional Ackredit uses the enclosing
application session and records actual aromaticity child work. Empty results
retain method provenance without claiming aromaticity was calculated.

## Why

The earlier neutral-only proposal had an insufficient interpretation gate:
net-neutral nitro groups, zwitterions and disconnected salts are different
scientific cases. A single supplied-graph model tool provides useful calculations
without a heuristic neutralizer or duplicate strict/broad APIs. The report and
documentation expose the limits. This is a design judgment accepted by the
maintainer, not evidence that ionic partition predictions are accurate.

## What is measured and what is assumed

- Contract-tested initial new scope: 60 tests passed in 11.82 seconds, including
  provider parity across RDKit/native/H5MSM/explicit-valence SDF, charged/nitro/
  zwitterionic inputs, state selection, source preservation, reports and Ackredit.
- TPSA regression after extraction: 70 tests passed in 11.79 seconds.
- Independent primary atomic-sum controls cover methane, ethane and benzene:
  C1=0.1441, C18=0.1581 and H1=0.1230 from Wildman–Crippen Table 1.
  These are versioned-reference controls, not experimental prediction benchmarks.
- Expanded local qualification: 2,218 tests passed in 93.06 seconds, followed by
  61 final focused tests in 10.72 seconds including fresh-process lazy imports
  and genuine Ackredit absence. Existing Viewer TPSA receiving tests: 53 passed
  in 11.87 seconds; no new Viewer lipophilicity wrapper is claimed.
- Both public doctests pass. All 14 fast gates pass. The new tutorial executed
  in 10.4 seconds, the paired-descriptor recipe executed with value/index
  assertions, and all five edited course notebooks retain code and saved outputs.
  Final incremental HTML exits zero with 17 existing header/orphan warnings
  outside the new tool/recipe; no warning-debt reduction is claimed.
- Exact commands, environment, scope and source hashes are in the
  [qualification receipt](../../../devtools/data/molecular_lipophilicity_implementation_20261027.json).
- No runtime/memory improvement or general partition accuracy is benchmarked.

## What was refuted

A blanket charged-atom rejection wrongly excludes net-neutral nitro representations.
A net-charge-zero gate admits zwitterions and salts and does not certify physical
applicability. Silent neutralization would change the requested chemical state.
A separate `get_logp` alias, duplicate atom-type coefficients, new dependency and
new Rust implementation are unnecessary for this first compiled-provider tool.

## Scope and exclusions

Only complete connected molecules with declared supported closed-shell chemistry
are accepted. Numeric molecule selection preserves order/repetitions; string
selection identifies whole molecules. Output shape is `(n_selected_molecules,)`,
including typed `(0,)` results. There is no coordinate/structure output axis;
structures only supply spatial-selection or chemical-state context. Requests
resolving to several states fail instead of averaging.

No logD, pH/pKa model, species-population inference, tautomer generation,
neutralization, counterion removal, capping, fragment/system summation, automatic
MolSys/H5MSM descriptor attachment or new persistence codec is included. Metals,
radicals, dummy/query atoms, dative bonds and missing H evidence remain excluded.
Scientific evidence is partial and the API experimental. This change does not
publish a package or add a new 1.0 release gate.

## Acceptance criteria

- Preserve both public descriptor contracts through the shared private boundary.
- Test chemical states, molecules, maps, charges, empty/repeated selections,
  unsupported chemistry, H-presentation parity and unchanged sources/caches.
- Separate independent primary sums from provider/form parity and acknowledge
  the original method separately from executed software through optional Ackredit.
- Complete docstring/doctest, executed Tools tutorial, Foundations, Cookbook,
  four-path course and API/evidence registry lifecycle.
- Run relevant regression, static and documentation checks and retain their scope.

## Provenance

Scientific method: Wildman, S. A. and Crippen, G. M. (1999), Prediction of
Physicochemical Parameters by Atomic Contributions, JCICS 39, 868–873,
[doi:10.1021/ci990307l](https://doi.org/10.1021/ci990307l).
The [author-uploaded primary text](https://www.researchgate.net/publication/220524632_Prediction_of_Physicochemical_Parameters_by_Atomic_Contributions)
was inspected for the bounded Table 1 controls. The model, RDKit's implementation
and installed producer version are separate evidence identities. See the
[prior source/probe receipt](../../../devtools/data/tpsa_logp_contract_review_20261026.json)
and the [scope analysis](../../pending_proposals/evaluate_aaindex_modlamp_and_peptides_for_additional_physicochemical_observables.md).
Qualification uses the existing shared Linux/Python 3.14 development environment,
not a clean installed-pair or release environment.
