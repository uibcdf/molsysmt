# Risk-Based Catalog Diagnostics Migration

**Status:** Proposed

## Why

SMonitor is the intended diagnostics layer, but current code still contains
direct `print`, bare `NotImplementedError`/`RuntimeError`, hardcoded warnings,
and broad exception suppression. These paths have unequal risk: a debug print
in a developer tool is not equivalent to a swallowed scientific error in a
public analysis.

## Proposal

Create an enforceable, risk-ranked migration rather than claiming complete
catalog adoption.

## How

1. Build an AST inventory for public package paths, excluding data-generation
   scripts and intentionally interactive reporters.
2. Classify findings as scientific-integrity, public UX, optional-backend,
   internal, or developer-tool debt.
3. Fix scientific-integrity and public API paths first, preserving causes and
   adding behavioral tests.
4. Add a narrow CI baseline so new direct prints, bare public exceptions, and
   `except Exception: pass` findings cannot increase.
5. Ratchet the baseline down as existing findings are migrated.
6. Validate catalog keys, required extras, warning categories, and hint URLs.

## Acceptance criteria

- No maintained public scientific path reports a failure only through `print`.
- Unsupported public behavior uses typed domain exceptions.
- Broad exception suppression is justified and allowlisted or removed.
- Fallback tests assert diagnostics and scientific output parity.
- CI prevents new violations without blocking intentional CLI/report output.
