---
summary: Jupyter receiving launcher leaves runtime settings after fixture preparation fails.
issue: uibcdf/molsysmt#688
status: resolved
opened: 2026-11-10
closed: 2026-11-10
severity: medium
verification: reproduced
area: [tests]
guard: tests/molsysviewer_molsysmt/test_jupyter_runtime_files.py
normative:
blocked_by: []
supersedes: []
---

# Jupyter runtime settings outlive failed fixture preparation

## What

The real-Jupyter launcher creates settings and server configuration before
preparing its notebook. A controlled `_notebook` failure reproduces retained
runtime credentials before any server starts. The initial one-case guard fails
on unchanged 075cd4a40; its synthetic remnants are hashed privately and retired
by the guard, without publishing contents. No running service, exposed secret
or product authentication failure is established.

## How

A small private `_runtime_files` context now owns file creation after all
fixture/notebook preparation. Exclusive create-only writes use restrictive
POSIX permissions from creation, without a permissive create/chmod interval.
Partial setup and body failures retire already-created entries. Cleanup checks
file identity, leaving preexisting destinations and foreign replacements intact.
It attempts every owned entry and reports cleanup errors alongside any body
error. The existing server shutdown remains inside this lifetime.

## Why

A failed receiving setup must not retain unused authentication material or
silently overwrite a destination. This is development-tool correctness, not a
new runtime library API or scientific capability. Other teams' private artifacts
remain theirs; permission to fix this launcher does not authorize inspecting or
retiring their files.

## Receiving and scope

Eight real-filesystem guards pass, including the actual launcher preparation
failure, normal/body exit, partial creation/write failure, preexisting files,
foreign replacement and cleanup-error reporting. One actual Jupyter/Mol*
workflow also passes six browser/kernel checks, including both independent
popups, exactly two managed edits and credential retirement. Clean source
e0bf27ca3 uses frozen Viewer 9b8662cf and the existing Python 3.14.7 environment;
no new package, platform, human or release qualification is inferred.

The earlier six-case control passes before the two cleanup-error guards are
added. Original failed preparation remains failed. The original reporter's
unused runtime files and diagnostic retention have not been inspected here:
only the controlled synthetic reproduction is retired. Their owner must confirm
hash-only retirement of those original remnants before administrative closeout.

## Acceptance criteria

Keep the addressable filesystem guard, scoped create-only ownership and actual
server/popup receiving. Publish the verified source and notify #688/#687 without
claiming the latter integrated. Confirm the original reporter's private-remnant
retirement without disclosing credentials, then close and archive this record.

## Reporter-owned handoff — 2026-11-10

The reporter has now verified completed owned-process cleanup and retired the
unused settings/configuration from the original preparation failure and the
subsequent controlled OOM/resource-stop campaigns (127, 130, 134 and 136).
Only file names, sizes and pre-retirement SHA-256 are retained in the private
evidence; no credentials are disclosed. Original diagnostic logs and outcomes
remain preserved under uibcdf/molsysviewer#315. This is the requested reporter
handoff; owner review, archival and administrative closure remain separate.
The new continuous-session scenario reuses the native `_runtime_files` owner
and its stronger foreign-replacement/partial-write/error-reporting guards,
rather than retaining the independently proposed duplicate context. The legacy
unconditional unlink after server shutdown is removed so that this call site
retains the context's documented foreign-file identity protection.

## Owner combined acceptance — 2026-11-10

Clean **81b4fc86644994a24f7ee65fa7414beda0aa0c67** receives the reporter's
handoff and removes the old call site's unconditional unlink. The addressable
guard now has **nine cases**. Its added actual-entrypoint test replaces both
owned files before a synthetic startup failure and requires preservation of
those foreign identities. Direct invocation against the unchanged published
3bcd573da launcher fails by deleting them; the corrected entrypoint passes.
The first added fixture intercepted the unrelated Node version subprocess and
fails independently (80 pass / one fail); it is corrected to stub only that
version query, preserving the original failed attempt.

The complete affected addon/inventory/native-boundary collection passes
**5,923 cases without omissions**, with **116 scientific cases / 74 nodes**,
fourteen fast gates and the inspected HTML build. Two actual Jupyter workflows
pass **13 browser checks**, including both popup boundaries, native scientific
session close/recovery/continuation, and retirement of both owned runtime files.
A representative native Qt workflow passes four checks. The reporter confirms
retirement of their own unused private remnants in #691; this owner neither
reads nor removes those private files. See the [combined receiving record](../../../devtools/data/combined_session_receiving_687_688_691_20261110.json).

This closes development-launcher lifetime/ownership, not abrupt-scope cleanup,
all Qt sessions, human/installed/platform or release acceptance. #615 remains
causally unresolved, and the old-host graphical failures under #690 remain
failed on their actual source cohorts.
