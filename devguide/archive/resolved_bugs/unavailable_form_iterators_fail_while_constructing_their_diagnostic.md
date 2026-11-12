---
summary: Unavailable form iterators fail while constructing their diagnostic
issue: uibcdf/molsysmt#717
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [form, diagnostics]
guard: tests/form/test_unavailable_iterator_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Supplying form identity when refusing unavailable iteration

## What

The #716 GRO receiving calls the advertised iterator and gets TypeError because
NotImplementedIteratorError requires a form argument. Unsupported iteration
should retain its structured refusal, not fail while building that exception.

## How

Source inspection finds 103 unconditional bare-raise branches in 60 iterator
modules, covering 59 registered forms and the unregistered generic template.
Some reject construction; others reject their first next call. All reviewed
branches contain only the refusal after any docstring. Do not touch supported
iteration, wrappers, signatures, dependency routes or scientific computations.

## Why

Clients need the documented diagnostic and actual form identity to distinguish
unsupported capability from a broken parser, provider or computation. The
existing SMonitor exception owns this boundary; no provider change or new error
class is needed. ArgDigest remains responsible for existing public wrappers;
isolated refusal tests deliberately unwrap those wrappers without claiming
input-validation or optional-engine receiving.

## Scope and acceptance

Supply the actual registered form string at each reviewed refusal. Identify
the generic template explicitly as unregistered rather than guessing a source
form. Retain all available iterators, code outside those raise expressions and
exception definitions. A reviewed explicit 103-route regression inventory must
execute the actual methods and check the structured exception and form identity;
it must not auto-discover away a missing route. Preserve baseline failures.

Run the overlapping GRO documentation/bridge contracts and existing public
iterator controls, with bounded memory and unchanged native/client/support
composition. No optional engine computation is certified by importing its
adapter. Update the iteration contract and release/polishing queue. Full source,
installed and final-candidate qualification remain separate.

## Provenance

2026-11-11, shared Linux/Python 3.14 development source. One actual GRO refusal
is reproduced while auditing #716; the remaining inventory is initially source
inspection pending its direct-branch cohort. Use existing reviewed support
sources and unchanged qualified native binary, no environment changes.

## Bounded source receiving

All 103 reviewed refusal branches fail with the missing-form TypeError before
correction. The explicit inventory spans 60 modules, including the unregistered
template. Replacing only the exception expression supplies the actual form;
a normalized AST comparison proves every other statement, signature and wrapper
is unchanged. The existing SMonitor constructor and qualified native binary
are untouched. No dependency is made eager and no iterator becomes available.

The combined cohort passes 166 cases with zero skips: the 103 exact branches,
eight GRO documentation/example cases, four GRO record contracts, 34 GRO bridge
cases and 17 public iterator controls. Expected legacy-deprecation and explicit
off-axis warnings remain visible. The single-CPU 1.5-GiB/no-own-swap service peaks
below 0.82 GiB, keeps more than 13.46 GiB host memory available and records no
own memory-high/max/OOM event or reserve stop. A transient global pressure pulse
is retained; available memory is not a resource reservation.

All 15 fast release gates, applicable Ruff and queue checks pass. Complete HTML
is received below; publication/closure follow its final checks. This is diagnostic/contract receiving,
not a complete source suite, optional-engine execution or installed qualification.

## Resolution — 2026-11-11

Implementation 9adad50d1 supplies the existing SMonitor exception's required form
in all 103 reviewed refusals across 60 modules. The explicit 103-route guard
executes each actual refusal, including decorated constructors deliberately
unwrapped only to isolate the branch, and checks exception type and form text.
It fails at every original missing-form expression. A normalized AST comparison
proves signatures, wrappers and all other statements unchanged. The generic
unregistered template identifies that scope explicitly.

The 166-case combined source cohort, fifteen fast gates and applicable Ruff/
index checks pass. Complete strict HTML on clean bc2db775d has zero warnings;
two GRO articles and their actual references are inspected. The [shared receipt](../../../devtools/data/gro_iterator_receiving_716_717_20261111.json)
retains original failures, warnings, input hashes, native exits and shared-host
telemetry. No phase changes its checked inputs, reaches an own memory limit or
stops for the host reserve. Temporary global pressure is retained explicitly.

These are later executable changes outside complete-source checkpoint 6acad4f35;
their focused receiving does not clear the next deliberate complete-source or
hosted nightly backlog. #718, #713/#615 uncertainty and final artifact/installed
qualification remain open. The publication pause is unchanged.
