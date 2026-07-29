# Function Support-Tier Classification (derive from stability, do not add a second registry)

**Status:** Implemented and validated (closes audit risk **R1** in
`../release_1_0/release_1_0_independent_gate_audit.md`; addresses the "Tier 1 function audit" pending
question in `support_tier_protocol.md`)

## Problem

Forms have an explicit tier registry (`molsysmt/_private/form_tier.py`), but **public
functions do not**. Only two functions carry a tier — `molecular_dynamics.run_NPT_equilibration`
and `run_NVT_equilibration` (`@support_tier(3)`). `support_tier_protocol.md` records the
gap: *"Silence currently does not distinguish an approved Tier 1 function from an
unclassified function."* For a 1.0 contract, the support tier of every public function
must be knowable and mechanically checkable.

## Decision — tier is a documented function of API stability

`devtools/data/public_api_stability.json` already classifies every public symbol
(190 entries: 125 stable, 57 experimental, 8 outside-contract) and is enforced by
`devtools/scripts/validate_api_stability.py`. Adding a **separate** per-function tier
registry would create a second source of truth that can contradict the first — exactly
what `support_tier_protocol.md` forbids for forms ("it would become a second and
potentially contradictory registry"). Instead, **derive the support tier from the
stability classification**:

| API stability | Support tier | Meaning |
|---|---|---|
| `stable` | **Tier 1** — contractual | regressions are patch-priority; stable for 1.x |
| `experimental` | **Tier 3** — experimental / niche | available, outside the contractual 1.0 core |
| `outside-contract` | **outside the core contract** | e.g. `molecular_mechanics.*`; no core tier guarantee |

Notes:

- **Tier 2 (best-effort)** currently maps to no function: `support_tier_protocol.md`
  already states *"no MolSysMT functions are currently classified Tier 2."* If a function
  ever needs Tier 2, it gets an explicit `@support_tier(2)` decorator (below), which
  overrides the derived value.
- **Explicit `@support_tier(N)` decorators override** the derived tier. This is how
  `molecular_dynamics` is Tier 3 today.
- Scope-root submodule entries (`molsysmt.basic`, `molsysmt.structure`, …) carry a
  stability but are containers, not functions; the tier applies to their leaf symbols.

## `molecular_dynamics`: deferred post-1.0, not classified (decided 2026-07-22)

`molecular_dynamics` is **not part of the public 1.0 surface**: it is not exported (absent
from the lazy registry in `molsysmt/__init__.py` and from the stability registry), and
`run_NPT_equilibration` / `run_NVT_equilibration` are stubs that raise
`NotImplementedMethodError`. A support tier classifies the public contract surface, and
this module is not on it, so it carries **no tier**. Its former `@support_tier(3)`
decorators were **removed** (they advertised a public Tier 3 that does not exist). This
leaves the tier system covering exactly the real public surface, with no phantom Tier 3
and no special-case exception in the validator. When the module is implemented and
exported, classify it then (its functions would enter as `experimental` ⇒ Tier 3).

## Enforcement

`devtools/scripts/validate_function_tiers.py` (added with this proposal):

- derives the tier for every leaf symbol from the stability registry;
- scans the code for `@support_tier(N)` decorators and checks each is **consistent** with
  its stability-derived tier (there are none today; the check guards future decorations);
- fails if any decorated function contradicts its derived tier or has no matching public
  symbol in the registry;
- prints the tier distribution so the contractual surface is visible at a glance.

Completeness (no silently-unclassified public function) is already guaranteed by
`validate_api_stability.py`, which fails when a discovered export is missing from the
registry. This proposal adds the tier *view* and the decorator-consistency *check* on top.

## Acceptance criteria

- `validate_function_tiers.py` exits 0 and reports the tier counts.
- Every `@support_tier`-decorated function is consistent with its stability-derived tier
  (currently there are none; the check guards future decorations).
- The stable⇒Tier 1 mapping is documented here and in `support_tier_protocol.md`
  (updated 2026-07-22).

## Cost, independence, regression risk

- **Cost:** low — one validator plus this decision record; no library code changes.
- **Independent?** Yes — data and tooling only; no dependence on the current WIP.
- **Regression risk:** none for runtime (no code path changes). The only risk is a
  policy disagreement over `experimental⇒Tier 3` vs `⇒Tier 2`; current reality has no
  Tier 2 functions, so the mapping is safe today and adjustable per-function via the
  decorator.
