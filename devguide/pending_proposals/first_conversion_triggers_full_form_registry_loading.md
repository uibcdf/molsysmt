---
summary: Avoid loading the complete form registry on first conversion.
issue: uibcdf/molsysmt#382
status: blocked
opened: 2026-10-10
closed:
verification: measured
area: [form, performance, deps]
guard:
normative: devguide/forms_and_conversions.md
blocked_by: [uibcdf/depdigest#34]
supersedes: []
---

# First conversion triggers complete form-registry loading

**Reported:** 2026-10-10 by ElastNetMT, consumer uibcdf/elastnetmt#26.
**Status:** Reproduced; reusable provider capability requested under
uibcdf/depdigest#34. Runtime adoption is pending that public interface.

## What

An ordinary first conversion to `molsysmt.MolSys` initializes all eligible form
adapters. Metadata-based detection already avoids that cost, but target validation
and conversion dispatch still use the generic scan-on-first-access registry.
Reduce this cold cost without changing scientific conversion behavior, dependency
visibility or supported registrations.

## How

`digest_to_form` imports `_dict_forms_lowercase`, constructed by iterating
`molsysmt.form._dict_modules.keys()`. DepDigest's `LazyRegistry` initializes by
importing every eligible plugin. A direct `_dict_modules[form]` lookup also starts
that scan; changing only the lowercase-name dictionary moves the cost rather than
removing it.

MolSysMT already owns adapter-local `form.json` declarations and
`form.catalogue`. Detection uses declared class/extension keys and confirms the
candidate with its real detector. Converter modules are independently lazy strings
resolved by `form.load_converter`. Reuse these pieces.

DepDigest owns generic discovery, configuration/dependency filtering, plugin
loading, caches and load diagnostics. Its current public `LazyRegistry` interface
does not accept an identity-to-plugin declaration index or provide an indexed
lookup without whole-registry initialization. Request that additive capability
from its owner, then make MolSysMT supply declarations and consume it. Preserve
the existing legacy route for unindexed extensions where appropriate, with an
explicit contract. Do not implement a competing registry in MolSysMT.

## Why

Cold startup dominates small client workloads such as local PDB preparation for
ElastNetMT. The incoming consumer record independently separates first/repeated
file preparation from prepared input and retains exact contact/node parity.
Its 1TCD workload and its consumer-level times are not interchangeable with the
provider-only 181L conversion measured here.

## What is measured and what is assumed

Three initial diagnostic workers on source
`3347a108a19177482dcab4bd73a02374c960cd5e` validate only
`to_form='molsysmt.MolSys'` after importing the form helpers. This adds **1,156
form package/submodule entries** in each worker, taking **3.258–3.408 seconds**.
The observed whole-registry scan takes **3.255–3.405 seconds**, nested inside that
validation. Do not sum these overlapping times or describe this isolated probe as
an unprofiled complete client workflow. It instruments the scan with a small
timer wrapper and provides diagnostic attribution, not an optimization result.

The maintained measurement tool separates two workloads:

```bash
python devtools/scripts/benchmark_form_registry_startup.py --mode conversion --trials 3
python devtools/scripts/benchmark_form_registry_startup.py --mode validation --trials 3
```

Conversion mode times root import, the first public PDB conversion, repeated PDB
conversion and conversion of the prepared public MolSys separately. Validation
mode instruments the scan and validates the target first; its subsequent file
conversion is already warmed and is explicitly named accordingly. Each trial is
a new interpreter. Timings exclude later parity checks and provenance collection.
Neither mode computes contacts or measures a complete ANM workflow.

The tool checks 13 molecular attributes through public `compare` outside timed
regions, including atom IDs/order, groups, connectivity/orders, formal charges,
coordinates, box and time. It verifies unchanged fixture bytes and records all
raw samples, the input/tool/native hashes, host/Python and actual editable source
identities independently of distribution versions. PID values are informative;
PID namespaces can reuse their visible numbers for independent workers.

No optimization, universal speedup, memory saving or installed-candidate
qualification has been measured. Public comparison on one PDB does not qualify
every form or scientific consumer.

The [retained receipt](../../devtools/data/form_registry_startup_20261010.json)
contains the initial diagnostic and three samples per maintained mode. On this
host, conversion-mode medians are **3.793 s** for the cold public conversion,
**0.514 s** for repeated file conversion and **0.0316 s** for prepared conversion;
the separately timed root import is **0.508 s**. Prepared conversion presupposes
the original conversion and retains normal public validation. It is not a PDB
workflow completed in 0.0316 s.

Maintained validation mode has a **3.342 s** target-validation median and **0.443 s**
subsequent warmed conversion median. It adds 1,163 form module entries during
validation and 1,166 by conversion, starting the counter before the form helpers
are imported. The initial isolated diagnostic imported those helpers first and
counted 1,156; these counters have different boundaries, not different results.
The receipt retains the complete raw scan traces; cumulative/nested durations
must not be added. No concurrent local pytest run was used during retained
maintained-tool measurement; other host load was not controlled.

## What was refuted

- Metadata does not need a new MolSysMT catalog: `form.json` and `catalogue`
  already provide it, with declaration-consistency guards.
- Changing only `digest_to_form` cannot eliminate cold startup because the first
  module lookup independently triggers the same scan.
- Calling `catalogue.module_of` everywhere without reconciling availability and
  registry registrations would create divergent loading/registration paths.
- Manipulating DepDigest's private `_initialized` flag or using base-dict access
  to bypass discovery could silently lose forms and diagnostics.
- Skipping public digestion or dropping PDB bond inference changes the workflow
  rather than solving the measured startup mechanism. PDB inference is #304's
  separate scientific theme.

## Scope and exclusions

MolSysMT owns form declarations, alias validation, converter dispatch and
scientific parity. DepDigest owns the reusable loader extension. This work does
not authorize a new default conversion engine, copied dependency tables, a new
public MolSysMT registry API, provider publication or a changed release artifact.
The existing dependency floor and frozen candidates stay unchanged until an
admitted provider version and qualified consumer adoption exist. An open
performance proposal is not by itself a demonstrated functional release blocker.

## Acceptance criteria

1. Agree a public DepDigest interface that supports declared identity lookup and
   loads only the requested plugin, retaining its default/legacy behavior.
2. Define declared versus available versus successfully loaded identities,
   dependency visibility, configuration freshness, registration/override/removal,
   deterministic ordering and uncatalogued-plugin fallback. Handle conflicting
   identities, mismatched declarations and failed loads with truthful diagnostics.
3. Add a provider sentinel guard whose unrelated plugin fails on import; indexed
   lookup and metadata discovery must never touch it.
4. Adopt the owner interface in MolSysMT's validation and dispatch, without losing
   case normalization, tolerance aliases, optional-dependency checks, dynamic
   registrations or explicit form enumeration.
5. Verify cold public conversions avoid unrelated adapter imports, while full
   discovery still reaches every declared/registered form. Exercise failures and
   configuration overrides rather than only positive counts.
6. Compare raw first/repeated/prepared measurements on identical bytes and sources,
   then qualify form enumeration/converters and scientific consumers across the
   required interpreters. Record evidence separately from speed estimates.

## Dependencies and risks

Blocked by uibcdf/depdigest#34. The extension must have a public version/admission
contract before changing MolSysMT requirements. Reconcile the existing catalog's
module cache with provider registrations; do not assume that clearing a registry
unloads Python modules. Configuration overrides are public through DepDigest,
and current compatibility guards explicitly exercise filtered discovery.
Follow-up adoption may affect many dispatchers; its scope must be measured before
admission during stabilization.

## Provenance

Linux x86_64, Python 3.14.7, 2026-10-10, existing shared Suite development
environment. Input: bundled `molsysmt/data/pdb/181l.pdb`, 1,441 atoms,
SHA-256 `77018feaaa65bb22dea47c784e8c059b0ccc09cd6dc7442b79cce83f3170985f`.
DepDigest actual source `ba670098a5b773e7f1570adc47b890d063bd5627`, clean;
distribution metadata `0.12.0+13.g104661a`. Other exact versions and sources are
retained in the benchmark receipt. Editable distribution metadata is not evidence
that a published package has those source changes.

The host exposes 20 logical CPUs. Retained native SHA-256:
`76f5dd6c8ee8c97428d6727bd80df5468fcf3e8f68838d9798c7e3ccd150a79c`.
The runtime source remained unchanged; its recorded dirty state consists of this
measurement tool, tests and documentation. The receipt retains the final tool hash.

## Preparation checkpoint — 2026-10-10

Three tool guards pass on Linux/Python 3.14.7: actual fresh workers and untouched
fixture bytes for both measurement modes, distinct cold/warmed field names and
public molecular parity, and invalid-input rejection without a success record.
The initial tool check found and corrected aggregation of list-valued diagnostic
scan traces as scalar timing medians. These guards protect measurement integrity;
they do not assert that the outstanding registry optimization is implemented.
No MolSysMT or DepDigest runtime source, public signature or dependency floor has
changed. The provider request and adoption criteria remain open.

Ruff checks/formatting, whitespace validation and all fourteen fast development
gates pass for this preparation checkpoint. The runtime scientific-evidence and
installed-package matrices are neither executed nor replaced by these checks.
