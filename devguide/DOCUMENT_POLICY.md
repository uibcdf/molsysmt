# Developer Documentation Policy

This policy keeps `devguide/` useful as the repository evolves.

## Document roles

Every developer document must have one clear role.

### Normative

Normative documents define current behavior, invariants, or contribution rules.
Write them in the present tense. A normative claim must agree with the current
code and tests. Future work belongs in the roadmap or a proposal, not inside a
normative section disguised as current behavior.

### Operational

Operational documents explain how to test, benchmark, release, diagnose, or
maintain the project. Commands and paths must be executable from the repository
root unless the document states otherwise.

### Pending

Pending bug reports and proposals describe unresolved work. They must state:

- the problem or opportunity;
- the evidence currently available;
- the intended outcome and exclusions;
- validation or acceptance criteria;
- dependencies and risks when relevant.

A proposal must not describe itself as implemented. When accepted and completed,
move durable rules into the appropriate normative document and archive or remove
the proposal.

### Archived

Archived documents are immutable historical evidence except for corrections to
their archive banner or broken navigation. Their status statements and benchmark
numbers apply only to the date and environment they record.

## Authority and evidence

Current code and executable tests take precedence over prose when determining
what is implemented. A disagreement is a documentation defect or a software
defect and must be recorded explicitly; it must not be resolved by silently
choosing the more favorable claim.

Use these evidence labels when a status claim needs qualification:

- **Implemented:** the code path exists.
- **Contract-tested:** tests exercise the documented user-visible behavior.
- **Parity-tested:** equivalent supported forms or execution paths are compared.
- **Scientifically validated:** results are compared with an independent oracle,
  reference dataset, or analytical truth.
- **Benchmarked:** a reproducible benchmark records environment and methodology.

These labels are not interchangeable. In particular, an adapter existing does
not prove contract coverage, and parity between two implementations does not by
itself prove scientific correctness.

## Single-source rules

- Runtime form tiers are defined by
  `molsysmt/_private/form_tier.py`. The support notebook reports that registry.
- Public exports define discoverability. `api_surface.md` defines the stability
  process; a complete symbol-level stability registry is still pending.
- Diagnostic codes and templates are defined by the SMonitor catalog in code.
- Dependency classification is defined by `molsysmt/_depdigest.py`.
- Heavy-execution behavior is defined by current code and contract tests, with
  `SCALABILITY.md` as the maintained explanatory contract.

Derived tables must identify their source and should be generated where
practical. Never maintain two manually independent authoritative lists.

## Links and paths

- Use repository-relative Markdown links.
- Do not commit local-file URI links or absolute developer-machine paths.
- Link to the current filename, not an obsolete alias.
- A renamed document requires updating all repository references in the same
  change.

## Benchmark and release claims

Benchmark results must identify at least the dataset, hardware or execution
environment, dependency versions, warm-up policy, statistic, and date or commit.
Do not call a result "current" unless an automated process keeps it current.

Statements such as "all tests pass", coverage percentages, adapter counts, or
"release ready" are checkpoint observations. Put them in a dated report or
generated artifact, not in the developer-guide landing page.

## Review checklist

Before merging a developer-documentation change:

1. Confirm the document role and location.
2. Check claims against code and tests.
3. Separate implemented behavior from planned behavior.
4. Use the evidence labels consistently.
5. Update affected API, User Guide, Cookbook, and course material when lifecycle
   integrity requires it.
6. Run `python devtools/scripts/validate_devguide.py`.
