# Documentation Lifecycle Manifest

**Status:** Proposed

## Why

The repository requires every public API change to update docstrings, User
Guide, Cookbook, and the Four Paths course. Today there is no executable mapping
from a symbol to those consumers, so compliance depends on text search and
memory across 156 course notebooks.

## Proposal

Maintain a machine-readable manifest keyed by public symbol or capability. Each
entry should reference its API page, User Guide/Tools pages, Cookbook workflows,
course modules, stability level, and optional dependencies.

## How

1. Define a small YAML or TOML schema with local document targets.
2. Populate it first for Tier 1 core functions and native forms.
3. Validate that targets exist and symbols are public.
4. Add notebook/static scans that flag use of deprecated aliases and stale
   signatures.
5. Execute a representative environment matrix for notebooks requiring soft
   dependencies; mark network/GPU/viewer requirements explicitly.
6. Use changed-symbol detection in CI to report affected documentation surfaces.

## Acceptance criteria

- A public API diff produces an actionable list of documentation consumers.
- Broken local references and deprecated symbol use fail validation.
- Course verification records environment and execution result per module.
- Exceptions to lifecycle coverage are explicit, owned, and time-bounded.
