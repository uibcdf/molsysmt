# Pre-1.0 source claims and work-order review — 11 November 2026

**Role:** dated operational review under uibcdf/molsysmt#334.
**Source basis:** `7b7cbc2f10f74870b9556f6e483c53c8293053f2`, followed by
the documentation-only delta recorded in the
[receiving receipt](../devtools/data/release_claims_receiving_334_20261111.json).
This completes the original phase-5 current-state/claim reconciliation at
source level. It does not close #334 or select a release candidate.

## What was inconsistent

Maintained public and developer explanations still described default H5MSM
0.5 writing and deferred all mechanical persistence until after 1.0. The
implemented native writers now default to 1.0 and retain bounded experimental
mechanics. The developer landing page's resume link also led to an October
candidate sequence rather than the current agreed joint 1.0 target.

These were current-claim defects, distinct from historical receipts. The
existing audit explicitly assigns their reconciliation to phase 5 under #334;
no new feature or release requirement is introduced here.

## Reviewed surfaces and evidence

| Surface | Corrected or confirmed scope | Evidence boundary |
| --- | --- | --- |
| README | Form-agnostic calls require available attributes/routes; native domain ownership and named analyses are explicit; preparation is limited to supported profiles; geometric quantities and index/category outputs differ. | Existing README preparation and analysis examples execute. No universal conversion, chemistry or performance claim follows. |
| H5MSM public narrative | Native conversion, `write` and `write_layers` default to 1.0; explicit 0.5 excludes stored mechanics, explicit 0.6 remains experimental. Migration preserves scientific producers separately from root writer metadata. | Existing default-writer, migration, independent-layer, original-report and older-target refusal controls; canonical [format contract](h5msm_format.md). |
| Foundations, Cookbook and bound addon | The native default is documented. The hydrophobic recipe explicitly requests its existing 0.5 example. Bound addon writers retain their own explicit 0.5 defaults; the native default is not silently imposed on them. | Native and addon signatures inspected; two small Cookbook notebooks reexecuted. No addon default/signature is changed. |
| Periodic interface | Row-vector bases, explicit origins, fractional primary cells and whole-component placement replace a universal Cartesian `[0, L)` rule. | Existing analytic wrapping, component and rotated-basis controls, plus small-origin/unit invariance cases. Old cross-provider percentages are not revalidated or promoted to current guarantees. |
| Release scope and navigation | The accepted pre-1.0 mechanical-persistence admission and H5MSM 1.0 target supersede the old deferral. One current resume entry points to remaining owners and qualification. | Maintainer decisions already recorded in #256/#334 and the [completion packet](pre_1_0_completion_handoffs_20261110.md); no new staging/publication authority. |
| Stability and science | Container/query/persistence contracts, experimental detector profiles and scientific evidence remain different claims. | [API stability](api_surface.md), [scientific validation](scientific_validation.md), [scalability](SCALABILITY.md) and [core ownership](CORE_SPECIFICATION.md) were checked for consistency; their classifications are unchanged. |
| Performance guide | The interaction benchmark's private 0.5 fixture and default public writer now have different version scope. | Executable call sites inspected. No timing campaign is repeated and no historical measurement is updated. |

The four unrelated human API-RST edits remain untouched. Source modules,
dependency floors, API stability/evidence registries and the native binary are
unchanged. This is a bounded reconciliation of maintained current claims,
not a new whole-library scientific audit or an assertion that every old page
has been rewritten. Explicit-version examples and dated evidence keep their
original meaning.

## Verification

The focused existing cohort passes **196 tests with no failures or skips**:
README examples, default writers, versioned refusal and migration, physical
origins/units and analytic periodic wrapping. Eight expected diagnostics remain
recorded: four structural-attribute-drop, two legacy-file and two unknown-atom
name warnings. The receptor's final phase stream and JUnit agree on exit zero;
its separately bounded extension channel reports dropped records explicitly.

Both Cookbook notebooks were forced through the maintained execution tool,
sequentially: **14 code cells** complete without errors. Five selected HTML
pages build and their revised text was inspected, with zero Sphinx warnings.
Typed overrides disable API-RST regeneration and notebook execution during the
HTML build. The existing **15/15 fast gates**, applicable notebook Ruff checks,
developer index and complete paginated board agreement pass. These are local
source checks, not a replacement complete suite or any hosted/candidate gate.

Tests use two workers with a 3-GiB cgroup cap; notebook/HTML/fast work is
sequential with one CPU and 2–3 GiB caps, no swap. The receipt records maximum
child RSS where measured; that value is not aggregate cgroup or host usage.
No native compilation, new environment or sibling edit is involved.

## Historical evidence and remaining decisions

The former resume sequence is retained under a dated historical heading in
the ledger. Its original producer, staged files, selected older counterpart,
campaign identifiers and publication receipts are not replaced. The previous
periodic prose is recoverable from the source basis above; its example
percentages are historical observations rather than a normative box rule.

Current source evidence supports the agreed work order:

1. Receive the H5MSM 1.0 default-specific client checks and decide the stable
   format under #256. Explicit-1.0 client receiving alone is not that decision.
2. Obtain a causal correction or evidenced bounded environmental disposition
   of #615. Instrumentation and one passing cold attempt do not resolve it.
3. Agree clean exact MolSysMT 1.0.0 / MolSysViewer 1.0.0 sources and builds,
   then qualify required source/native/scientific/docs and installed matrices.
   #524's public compatible-host floor and #250/#254 final-candidate acceptance
   remain pending.
4. Review failures and obtain the final publication decision. Preserve the
   existing files, hashes and release pause until resumption is agreed.

#473/#475 retain their bounded experimental disposition and primary-reference
follow-up. Completing this source documentation milestone neither closes them
nor certifies their unresolved scientific interpretation. Other deferred
capabilities keep their owners; none is silently promoted to a release gate.

The original scorecard gains only its existing `phase5/334-ledger` source leaf.
All weights, fifty graphical intents and composite acceptance requirements are
unchanged. New candidate selection must refresh this current-state review for
any subsequent source delta; it cannot reuse this document as exact-candidate
or installed-artifact qualification.
