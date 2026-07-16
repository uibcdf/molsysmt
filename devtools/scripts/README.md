# Developer Validation Scripts

Run scripts from the repository root.

- `validate_dependencies.py` checks hard/soft dependency boundaries.
- `validate_form_adapters.py` checks adapter structure, the explicit tier
  registry, and declared-attribute delivery. Existing delivery debt is tracked
  by a monotonic baseline in `devtools/data/`; new unreachable declarations
  fail validation.
- `validate_devguide.py` checks developer-guide links and retired document
  references.
- `validate_resources.py` checks project resource metadata.
