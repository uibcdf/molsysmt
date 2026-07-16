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

### Tier 3 functions (decorated with `@support_tier(3)`)

- `molsysmt.molecular_dynamics.run_NPT_equilibration`
- `molsysmt.molecular_dynamics.run_NVT_equilibration`

The entire `molecular_dynamics` module is outside the contractual 1.0.0 core.
Individual functions are decorated rather than the module to keep the signal granular.

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

## Pending design questions

- **Function-level Tier 2**: no MolSysMT functions are currently classified Tier 2, but
  `@support_tier(2)` is available if needed.
- **`molecular_dynamics` module expansion**: if more functions are added to this module,
  apply `@support_tier(3)` to each.
- **Tier 1 function audit**: explicitly classify public API functions. Silence
  currently does not distinguish an approved Tier 1 function from an
  unclassified function.
- **`support_tier` as a module-level decorator**: for marking entire sub-packages (e.g.,
  `molecular_dynamics`) as Tier 3 without decorating every function individually.
- **CLI / session report**: a `smonitor report` section listing Tier 2/3 items used in
  a session would help QA and support workflows.
