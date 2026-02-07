"""
MolSysMT Developer Guide — IO and File Registry
"""

# IO and File Registry

## Scope
Defines how MolSysMT handles file-based inputs, caching, and internal
registries for file-backed forms.

## Rules
- File-backed forms must not load full data eagerly unless requested.
- File registry should prevent double-registration of the same file.
- IO errors must emit SMonitor diagnostics.
