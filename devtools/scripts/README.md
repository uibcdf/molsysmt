# Developer Validation Scripts

Run scripts from the repository root.

- `validate_dependencies.py` checks hard/soft dependency boundaries.
- `validate_form_adapters.py` checks adapter structure, the explicit tier
  registry, and declared-attribute delivery. Existing delivery debt is tracked
  by a monotonic baseline in `devtools/data/`; new unreachable declarations
  fail validation.
- `validate_devguide.py` checks developer-guide links and retired document
  references.
- `validate_api_stability.py` checks the AST-discovered public API against the
  normative stability registry and verifies its generated developer-guide view.
  Pass `--baseline <previous-registry.json>` to reject stable demotions or
  removals across a proposed change.
- `validate_scientific_evidence.py` assembles the domain-split Scientific Truth
  evidence registry, checks it against the Stable API registry and real pytest
  nodes, validates tolerance governance, and verifies the generated evidence
  matrix.
- `validate_resources.py` checks project resource metadata.
