# Residue chemical coverage contract

Preserve `Tutorial_Residue_Chemical_Coverage`, exact template identity, group-index
selection, whole-group string selection and source indices. Distinguish unassessed
inventories from empty missing lists, unknown edges/orders from explicit conflicts,
and candidate H inventories from environmental protonation. Keep MSE/SEP/TPO/MLY
heavy-only coverage and absent terminal-context limits explicit. Never imply
chemical validity, automatic repair or docking readiness. Regression evidence:
`tests/build/test_get_residue_chemical_coverage.py`.

Keep naming-scoped caches, missing-context unassessed entries and the limited
Meeko-derived heavy connectivity/H-count verification in template provenance.
No full chemical-state certification follows from that reference comparison.

Keep candidate variant_sources and actual content identities, preserving raw
indices and explicitly identifying additional construction layouts. Multiple H
name sets remain ambiguous; do not turn one exact match into unique chemical
assessment.
