---
summary: Adopt policy-v1.5.12 and review current common guidance
issue: uibcdf/molsysmt#764
status: resolved
opened: 2026-11-15
closed: 2026-11-15
verification: measured
area: [ci, docs]
guard:
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# Latest-policy adoption and common-guide review

**Reported:** central owner handoff in uibcdf/molsyssuite#201.
**Status:** source adoption received locally; published-head verification belongs to the owner closeout.

## What

MolSysMT's actual reusable policy caller selected policy-v1.5.9. Central's live
rule now requires the latest published policy or an accepted bounded exception;
compatibility with an older frozen policy does not establish current adoption.
The canonical common guide also contains later accepted instructions.

## How

The actual caller now selects policy-v1.5.12. Its immutable tag object is
7294f684dbaf3f0267c6e978937475d3deb8f633, peeled source
bb641488bc22b262549f795857d6ede529b14ca1. MolSysMT is already registered in that
frozen policy, so no separate admission_sha input is needed. Scientific/installed
SDK, artifact-verification, publication and Sphinx action pins are unchanged.

The official registered synchronizer delivers the common guide from published
central main f13e3fe18f2331252d67d6dd5a0c6035cc6c5958, SHA-256
0150f8bd618f9c1029af31b8b9171609ee1693b7c5dc431b223e6b00423b7b8a.
This is later than #201's initial guide handoff and includes accepted allostery
ownership and resource-aware instructions. No policy tag is moved. Because the
shared central checkout contains active unrelated edits, a clean owned checkout
of that exact published commit runs the official synchronizer; its remote-main
verification and clean canonical input requirements remain enabled.

## Why

A version-string change alone cannot establish conformance, semantic adoption
or scientific readiness. The common guide and versioned policy caller are
separate contracts and need separate receiving.

## What is measured and what is assumed

The official complete workspace inventory receives eighteen registered member
states. Every behind/ahead, dirty and missing checkout is explicitly preserved;
only this authorized component's source changes. The source-owner working tree
is also preserved. The native conformance check before adoption returns exactly
GUIDE_DRIFT and LATEST_POLICY; after synchronization/caller change it returns
an empty findings list with exit zero. The authoritative remote tag matches
the declared target, and the selected adoption inventory reports CURRENT.
The [receipt](../../../devtools/data/policy_notebook_adoption_764_765_20261115.json)
retains actual source/input identities and checks; published default-branch
receiving is separate from the initial dirty/local check.

## Semantic review and resource boundary

Root and nested instruction routes retain the common layer's scoped precedence,
English repository text, modular owners and local scientific criteria. Reviewed
actual callers and other reusable/SDK pins do not require new inputs or runtime
changes. Existing ArgDigest, DepDigest, SMonitor, PyUnitWizard, Ackredit and
receptor boundaries remain; copying a guide does not adopt newer runtime versions.

The accepted resource rule is read with its central workload guidance. The
active operator policy is the principal maintainer's session policy for this
shared host. Ordinary reads/edits remain lightweight. Current selected checks
use measured bounded source profiles, one CPU per process family, finite memory
and no own swap, at most two owned jobs and a monitored 6.5-GiB host reserve.
A cgroup budget bounds owned children; observed availability is not reservation
or aggregate protection. Unknown larger loads require a fresh estimate and
admission. Only owned work may be cancelled. No host configuration, shared
prefix, automatic scientific campaign or infrastructure adapter is introduced.

## What was refuted

Older-policy compatibility is not current adoption. A matching guide is not
scientific/installed conformance. Uncommitted canonical edits are not a valid
source for the synchronized consumer. The clean owned source route avoids
both altering another team's work and silently bypassing official preflights.

## Acceptance and exclusions

Receive the actual caller, exact published tag, current registered guide,
semantic review, local conformance and post-publication adoption. Preserve
all separately qualified scientific/operator pins. Hosted execution of the
new policy caller, full/nightly science, the exact coordinated installed pair,
public artifacts and publication retain their existing distinct gates and
pause. This administrative adoption adds no original weighted-plan credit.

## Provenance

2026-11-15, Linux and existing Python 3.14.7; source parent b8c798474. Central
published f13e3fe1 and the immutable policy are read without changing the
shared owner checkout. Detailed commands, input hashes, native exits and
bounded execution outcomes are retained in the receipt.
