---
summary: Setuptools build minimum does not establish support for declared license metadata.
issue: uibcdf/molsysmt#541
status: open
opened: 2026-11-03
closed:
severity: medium
verification: inspected
area: [packaging, deps]
guard:
normative:
blocked_by: []
supersedes: []
---

# Qualifying the backend minimum for existing license metadata

**Reported:** DockingMT's packaging review in uibcdf/molsysmt#541, coordinated
through uibcdf/molsyssuite#162.
**Status:** intake recorded; minimum-backend reproduction and owner decision pending.

## What and how

Current `pyproject.toml` permits setuptools>=68.0 while declaring a string
SPDX license and license-files. Static source inspection confirms those fields.
The reporter points to Setuptools's PEP 639 support boundary; an exact compatible
patch minimum still needs primary-documentation review and build qualification.
No old-backend failure has been reproduced in this intake, and successful builds
with a newer backend do not certify the declared minimum.

## Why

The declared build contract should cover its actual metadata syntax. This is a
build dependency question, separate from #524's runtime floors. It matters
before the next public source/wheel publication; there is no evidence here that
an existing public artifact is broken or omits its license.

## Proposed work and acceptance

Choose and justify a supported Setuptools minimum, align applicable build inputs
and test actual wheel/sdist metadata plus license inclusion in that minimum
context. Preserve runtime Python support and scientific code. Do not downgrade
the shared development environment to investigate an old backend. Retain exact
context, artifact names/digests and exclusions in the final receiving record.
No license change, release, package replacement or sibling pin update is implied.
