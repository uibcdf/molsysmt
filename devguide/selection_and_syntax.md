"""
MolSysMT Developer Guide — Selection and Syntax
"""

# Selection and Syntax

## Purpose
Selections are a core feature for addressing subsets of a molecular system.
This document defines selection rules and syntax responsibilities.

## Standard Parameters
- `selection`
- `syntax` (default `MolSysMT`)

## Invariants
- Selection indices are 0-based.
- `'all'` selects every element.

## Engines and Compatibility
Selection parsing must be consistent across forms and engines. If a syntax is
not supported, raise a `NotSupportedSyntaxError` through SMonitor.

## Documentation
User-facing selection syntax is documented under `docs/content/user/intro/`.
Developer rules should be synced with that content.
