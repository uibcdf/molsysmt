# Deprecation Policy for the 1.x Line

> **Status (updated 2026-03-23)**
>
> This document defines the official deprecation policy for MolSysMT starting
> with the `1.0.0` release. It applies to all symbols classified as **Stable**
> in `devguide/api_surface.md`.

---

## 1. Why a deprecation policy is necessary

A `1.0.0` support contract is only meaningful if users know what to expect when
the library evolves. Without an explicit policy, any change to a public symbol
is ambiguous: users cannot tell whether it is a bug fix, a planned evolution,
or an accidental break.

The goal of this policy is not bureaucratic process. It is to give users a
reliable window to adapt their code before a breaking change takes effect.

---

## 2. Scope

This policy applies to symbols classified as **Stable** in `devguide/api_surface.md`:

- all functions in `msm.basic`;
- structural analysis and manipulation functions in `msm.structure` (Stable subset);
- `msm.pbc` (all);
- `msm.physchem` (Stable subset: `get_mass`, `get_charge`, `get_atomic_radius`);
- `msm.topology` (Stable subset);
- `MolSysBuilder`, `MolSysDict`, `TopologyDict`;
- public exception classes.

It does **not** apply to:

- symbols classified as **Experimental** — these may change in any `1.x` minor
  release without a formal deprecation cycle;
- symbols classified as **Outside contract** — no stability guarantee applies;
- anything under `molsysmt/_private` — always internal;
- `msm.molecular_dynamics` — explicitly outside the `1.0.0` contract.

---

## 3. What counts as a breaking change

A breaking change is any modification to a **Stable** symbol that can cause
previously correct user code to fail or silently produce different results:

- removing a public function, class, or module;
- renaming a public function, class, or module without an alias;
- removing or renaming a positional or keyword argument;
- changing the type or units of a return value;
- changing the semantics of an existing argument in a way that alters results
  for currently valid input.

The following are **not** breaking changes and do not require deprecation:

- adding new optional keyword arguments with default values that preserve
  existing behavior;
- adding new public functions or classes;
- fixing a bug where the previous behavior was demonstrably incorrect and
  documented as such;
- changes to **Experimental** or **Outside contract** symbols;
- internal implementation changes that do not affect the public contract.

---

## 4. Deprecation process

### 4.1 Minimum warning period

A **Stable** symbol must remain available and functional for **at least one
full minor release cycle** after the deprecation warning is introduced before
it can be removed or changed in a breaking way.

In practice this means:

- deprecation warning introduced in release `1.N.0`;
- breaking change may land no earlier than `1.(N+1).0`.

For changes with significant user impact (widely used functions, argument
renaming), the maintainers should prefer a two-minor-release warning period.

### 4.2 How to signal deprecation in code

Use the `msm.warn_once` mechanism (backed by SMonitor) to emit a one-time
structured deprecation warning on first use:

```python
msm.warn_once(
    "DeprecationWarning",
    message="msm.foo() is deprecated since 1.N.0 and will be removed in 1.(N+1).0. Use msm.bar() instead.",
    caller="msm.foo",
)
```

The old symbol must remain functional during the warning period. If the
replacement has a different signature, the deprecated wrapper should translate
arguments and delegate to the new implementation.

### 4.3 Documentation requirements

Every deprecation must be:

1. noted in the docstring of the deprecated symbol with the version it was
   deprecated and what replaces it;
2. listed in the release notes for the release that introduced the deprecation;
3. listed in the release notes for the release that removes the symbol.

### 4.4 Bug-fix exception

If a breaking change is required to fix a bug where the previous behavior was
incorrect and the correct behavior is clearly defined by the documentation or
scientific intent, the change may land without a deprecation cycle. In this
case:

- the fix must be explicitly described as a bug fix in the release notes;
- the previous incorrect behavior must be documented as the reason for the
  change;
- the fix must be covered by a regression test.

This exception is narrow. It does not apply to design changes or API
reorganization.

---

## 5. Experimental symbols

Symbols classified as **Experimental** in `devguide/api_surface.md` are not
subject to this deprecation policy. They may change in any `1.x` minor release.

However, the maintainers should still:

- prefer additive changes over breaking ones where possible;
- note significant changes to Experimental symbols in release notes;
- promote an Experimental symbol to Stable (with the associated stability
  guarantees) before it is relied upon in critical workflows.

Promotion from Experimental to Stable is a one-way operation within a `1.x`
line. Demotion from Stable to Experimental is itself a breaking change and
requires the full deprecation cycle.

---

## 6. Version numbering convention

MolSysMT follows semantic versioning (`MAJOR.MINOR.PATCH`):

- `PATCH` releases (`1.x.N → 1.x.N+1`): bug fixes, no breaking changes, no
  new deprecations that affect Stable symbols;
- `MINOR` releases (`1.N.x → 1.N+1.0`): new features, new deprecations
  introduced, previously deprecated symbols may be removed;
- `MAJOR` releases (`1.x.x → 2.0.0`): reserved for changes that cannot fit
  within the `1.x` compatibility contract; subject to a separate policy when
  that time comes.

---

## 7. Relationship with the support tiers

The deprecation policy is tied to the stability classification in
`devguide/api_surface.md`, not to the form support tiers in
`devguide/support_tiers.ipynb`.

A Tier 1 form being reclassified (e.g., demoted from Tier 1 to Tier 2) is a
breaking change for users who depend on that form's contractual guarantees and
follows the same deprecation process.
