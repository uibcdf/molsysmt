# Developer Validation Scripts

Run scripts from the repository root.

- `validate_dependencies.py` checks hard/soft dependency boundaries.
- `validate_form_adapters.py` checks adapter structure, the explicit tier
  registry, and declared-attribute delivery. Existing delivery debt is tracked
  by a monotonic baseline in `devtools/data/`; new unreachable declarations
  fail validation.
- `validate_devguide.py` checks developer-guide links, retired document
  references, and the work-queue front matter defined by
  `devguide/reporting_protocol.md`.
- `devguide_reports.py` is not a command: it holds the work-queue schema that
  `validate_devguide.py`, `devguide_index.py` and `devguide_issue.py` share, so
  the protocol is described in one place.
- `devguide_index.py` renders the generated index of each work queue from that
  front matter. `--check` fails instead of writing.
- `devguide_issue.py` keeps the GitHub issue board in step with the queues:
  `open` creates an issue and scaffolds its document, `sync` pushes the derived
  labels and state, `close` closes an issue behind an archived document. It
  needs the network and an authenticated `gh`, so it stays out of the release
  gate.
- `validate_api_stability.py` checks the AST-discovered public API against the
  normative stability registry and verifies its generated developer-guide view.
  Pass `--baseline <previous-registry.json>` to reject stable demotions or
  removals across a proposed change.
- `validate_scientific_evidence.py` assembles the domain-split Scientific Truth
  evidence registry, checks it against the Stable API registry and real pytest
  nodes, validates tolerance governance, and verifies the generated evidence
  matrix.
- `validate_resources.py` checks project resource metadata.
