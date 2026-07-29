# F3 Support-Tier and Proposal-Lifecycle Checkpoint

**Date:** 2026-07-29
**Stage:** F3 — function support-tier and pending-guide hygiene
**Status:** `DONE`
**Base commit:** `fd19f9196`

## Function Support-Tier Contract

MolSysMT has one normative public-symbol classification:
`devtools/data/public_api_stability.json`. Function support tiers are derived
from it rather than copied into a second registry:

| API stability | Derived support tier |
| --- | --- |
| `stable` | Tier 1 |
| `experimental` | Tier 3 |
| `outside-contract` | outside the core tier contract |

`devtools/scripts/validate_function_tiers.py` reports 117 Tier 1 functions,
56 Tier 3 functions, and seven outside-contract functions. No public symbol is
unclassified and no explicit `@support_tier` decorator contradicts the
stability registry.

The stale pending question in `support_tier_protocol.md` was removed. That
normative guide now states the derived mapping, the override rule, the
validator, and the fact that unfinished non-exported modules do not acquire a
phantom public tier.

## Proposal-Lifecycle Reconciliation

The following completed or superseded records moved from
`pending_proposals/` to `archive/resolved_proposals/`:

- explicit form support registry;
- course module renumbering and stable identifiers;
- Rust packaging backend design;
- Rust linear-algebra backend selection;
- chemical-graph execution checkpoint;
- Chemical State v1 executable contract;
- chemical-state adapter fidelity audit;
- neighbour-list consumer migration;
- original heavy-computation Rust exploration.

The independent 1.0 gate audit moved to `archive/release_1_0/`: it is an
historical assessment whose actionable findings are now resolved or routed to
later release stages, not a pending design proposal.

Archiving does not erase design provenance. Each moved document carries a
resolution banner, and references were updated. Durable present-day rules
remain in normative or executable sources:

- `support_tier_protocol.md`, `molsysmt/_private/form_tier.py`, and the API
  stability/function-tier validators;
- the Four Paths manifest, toctrees, stable labels, and
  `validate_course.py`;
- `forms_and_conversions.md`, the attribute policy, conversion-fidelity gate,
  and chemical-state implementation tests;
- `rust_kernel_optimization_guide.md`, packaging artifacts, Rust source, and
  wheel/runtime validators.

Partially implemented, deliberately deferred, or post-1.0 proposals remain
pending. F3 does not promote Tier 2/3 adapter expansion, a lifecycle manifest,
GPU redesign, native format parsers, optional columns, or other expensive work
into the 1.0 critical path.

## Evidence

- `python devtools/scripts/validate_function_tiers.py`: pass;
- `python devtools/scripts/validate_devguide.py`: pass;
- `git diff --check`: pass;
- the F2-closing fast release gate immediately before this documentation-only
  stage: 12/12 pass.

F3 is complete. The next lifecycle stage is F4: reconcile the remaining User
Guide, Cookbook, API, demos, and course obligations without reopening closed
architecture or accepted post-1.0 debt.
