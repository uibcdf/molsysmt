# Support Tier Protocol — MolSysMT Integration

## Scope

MolSysMT uses the SMonitor support-tier protocol to communicate which parts of
the API carry a formal support guarantee at runtime. This document defines the
MolSysMT integration; implementation details must be confirmed against the
referenced code and tests.

The SMonitor integration guide defines the generic protocol. This document
covers MolSysMT-specific choices visible in this repository.

---

## Tier semantics (recap)

| Tier | Meaning | Runtime signal |
|------|---------|----------------|
| **1** — Contractual | Regressions are patch-priority; API is stable for 1.x | None |
| **2** — Best-effort | Supported and maintained but not contractually guaranteed | `WARNING` once per form/function per session |
| **3** — Experimental / niche | Available but outside the contractual 1.0.0 core | `INFO` once per form/function per session |

---

## Form classification

Forms are classified only in `molsysmt/_private/form_tier.py`. Every discovered
form, including Tier 1 forms, has an explicit entry. Unknown forms are registry
integrity failures and are never interpreted as Tier 1.

Run `devguide/support_tiers.ipynb` to display the live classification. Do not add
a manually maintained form list to this document: it would become a second and
potentially contradictory registry.

The form-adapter validator and focused registry tests require exact agreement
between adapter `form_name` declarations and `FORM_TIERS`. Adding or renaming an
adapter therefore requires an explicit support decision.

---

## Function classification

Public-function tiers are derived from the normative API stability registry in
`devtools/data/public_api_stability.json`; MolSysMT does not maintain a second
function-tier registry:

| API stability | Function support tier |
| --- | --- |
| `stable` | Tier 1 — contractual |
| `experimental` | Tier 3 — outside the contractual 1.0 core |
| `outside-contract` | outside the core support-tier contract |

An explicit `@support_tier(N)` decorator may override the derived value only
when the API stability classification permits that tier. The release validator
`devtools/scripts/validate_function_tiers.py` fails if a public function is
unclassified or if a decorator contradicts the stability registry.

At the F3 closure checkpoint, the public surface contains 117 Tier 1 functions,
56 Tier 3 functions, and seven outside-contract functions. No public function
uses an explicit decorator. The unfinished `molecular_dynamics` module is not
exported and therefore has no public support tier; classify its functions if
and when they enter the public API.

---

## How the hook works

`molsysmt/basic/get_form.py` is the hook point for form tier signals. Public
operations that resolve an input through `get_form()` trigger the check. Public
utilities without a molecular-system form do not necessarily pass this hook.

```python
# get_form.py (simplified)
from molsysmt._private.form_tier import check_form_tier

def get_form(molecular_system):
    ...
    check_form_tier(output)   # emits WARNING/INFO at most once per session
    return output
```

`check_form_tier()` lazily registers the form with the bundle's `SupportTierRegistry`
and calls `registry.check()`, which deduplicates via `DiagnosticBundle._tier_dedup_cache`.

---

## SMonitor catalog entries

Two new entries were added to `molsysmt/_private/smonitor/catalog.py`:

| Catalog key | Code | Level | Purpose |
|---|---|---|---|
| `SupportTier2Warning` | `MSM-WARN-TIER-002` | WARNING | Tier 2 form/function used |
| `SupportTier3Info` | `MSM-INFO-TIER-003` | INFO | Tier 3 form/function used |

The CODES dict provides multi-profile messages (developer, user, debug) for both codes,
plus a revised `MSM-INFO-EXP-001` entry for the legacy `ExperimentalPath` catalog key.

---

## How to use `support_tier` in MolSysMT modules

```python
from molsysmt._private.smonitor import support_tier

@support_tier(3)
def my_experimental_function(...):
    ...
```

`support_tier` is exported from `molsysmt._private.smonitor` alongside `experimental`
(which is now an alias for `support_tier(3)`).

---

## Possible future extensions

- **Function-level Tier 2**: no MolSysMT functions are currently classified Tier 2, but
  `@support_tier(2)` is available if needed.
- **`support_tier` as a module-level decorator**: for marking entire sub-packages (e.g.,
  `molecular_dynamics`) as Tier 3 without decorating every function individually.
- **CLI / session report**: a `smonitor report` section listing Tier 2/3 items used in
  a session would help QA and support workflows.
