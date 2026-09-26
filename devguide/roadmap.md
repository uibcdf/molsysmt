# Developer Roadmap

This roadmap is a maintained ordering principle, not a mirror of a nonexistent
root `ROADMAP.md`. Concrete unresolved work lives under `pending_bugs/` and
`pending_proposals/`.

## Distribution milestone completed — 2026-09-25

MolSysMT 0.22.4 and MolSysViewer 0.23.4 are published as a compatible
pre-1.0 pair. The exact public Conda pair passed 20/20 clean installations
across five platforms and Python 3.11–3.14; see
[the paired-support checkpoint](python_3_14_checkpoint.md) for coordinates
and evidence. The mutual-dependency publication cycle is no longer the next
roadmap blocker. This does not certify every optional backend, the Viewer
visible-window/hosted-E2E gates, MolSysSuite-wide 3.14 admission, or either
project's 1.0 release. Both Zenodo version records are now independently
verified, with distinct version DOIs; see the paired-support checkpoint.

For the next 1.0 session, start with
[the 1.0 execution ledger](release_1_0_status.md) and
[the exact-commit release gate](release_gate.md). Recertify an actual 1.0
candidate against today's published dependency floors; do not reuse an old
0.22.x staging plan as a current blocker. The
[false-red Conda promotion verification](archive/resolved_bugs/five_public_abi3_promotions_succeed_but_final_verifiers_exit_one.md)
was replaced by a read-only checker and passed on GitHub without re-uploading
the already public files. The multi-hour Zenodo delay
and its false-red verifier are recorded under `uibcdf/molsyssuite#49` and
`uibcdf/molsysmt#247`; the paired-release procedure and lessons are in
[release and citation](release_and_citation.md).

## Priority 0: scientific integrity

- propagate scientific failures instead of returning partial heavy results;
- correct attribute declarations that cannot be delivered;
- remove silent broad-exception fallbacks from high-risk paths;
- establish independent scientific reference tests for builders and analyses.

## Priority 1: support and API truth

- make form tiers explicit rather than treating unknown forms as contractual;
- create a machine-readable public API stability registry;
- validate public attribute delivery and conversion fidelity;
- productize the Rust extension and remove the transitional Numba CPU/CUDA
  implementations before 1.0;
- keep Python-version metadata and release matrices aligned automatically.

## Priority 2: reproducibility and lifecycle

- make benchmark regression gates statistically and operationally robust;
- link public symbols to User Guide, Cookbook, and course consumers;
- resolve course numbering and execute the Four Paths in supported environments;
- migrate public diagnostics through a risk-ranked catalog program.

## Priority 3: capability expansion

Only after the preceding contracts are reliable:

- extend heavy execution to additional analyses and input forms;
- broaden native scientific builders with independent validation;
- improve device backends and transfer-aware execution;
- add integrations whose maintenance and fidelity can be sustained.

Completed proposals should be moved to an archive or replaced by a concise
decision record. A checked box or dated prose is not completion evidence without
code, tests, and documentation.
