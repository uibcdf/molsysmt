---
summary: The MolSysSuite positioning is absent from every public surface.
issue: uibcdf/molsysmt#192
status: open
opened: 2026-08-19
closed:
severity: medium
verification: measured
area: [docs, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: the repository does not say the thing that makes it make sense

**Reported:** 2026-08-19, at the end of the external audit recorded in
[`../../archive/assessments/external_audit_august_2026.md`](../../archive/assessments/external_audit_august_2026.md).
It was not found by reading the repository. It was found by the maintainer stating it in
conversation after the audit had been written and filed.
**Status:** open.

## What

MolSysMT is the substrate of a multi-tool ecosystem: MolSysViewer coordinates with it,
MolSys-AI is being built on it as an assistant and later as an agent, and TopoMT,
PharmacophoreMT and ElasNetMT are queued as downstream consumers. That fact reframes most
of the project's design decisions. It appears almost nowhere a reader can reach.

```bash
$ for f in README.md AGENTS.md docs/index.ipynb; do
      printf '%-20s %s\n' "$f" "$(grep -ci 'molsyssuite\|topomt\|pharmacophoremt\|elasnetmt\|molsys-ai' $f)"; done
README.md            0
AGENTS.md            0
docs/index.ipynb     0
```

Two mentions exist in total on user-facing surfaces:

- `docs/content/about/what.md:12` — one subordinate clause: *"It is the core of the
  MolSysSuite ecosystem."*
- `CITATION.cff:22` — *"...within the MolSysSuite ecosystem"*, inside the abstract.

`pyproject.toml`, which supplies the PyPI and Conda storefront description, says
*"Molecular Systems Multi-Toolkit: build, prepare, query, transform, analyse and
visualise molecular systems and trajectories through one uniform API"* — a capable
library, described as a capable library.

Within `devguide/`, the sibling tools appear only in `release_1_0_status.md`, which is by
its own declaration an operational ledger of transient execution state, and in
`release_and_citation.md`. Until 2026-08-19,
[`../../competitive_landscape_and_vision.md`](../../competitive_landscape_and_vision.md)
— the document whose role is to define what MolSysMT is competing with and why — did not
mention the ecosystem at all.

## How

Not a code path. A consequence of every public surface having been written to describe
the library accurately, one surface at a time, with no surface owning the question *what
is this for*.

The audit is the evidence that the gap is real rather than theoretical. It read
`README.md`, `AGENTS.md`, the whole of `devguide/`, the stability registry, the evidence
matrix and the form registry; it produced an assessment, eight entries and a competitive
comparison; and it did all of that treating MolSysMT as a standalone library, because
nothing it read said otherwise. Several of its judgements were wrong in the same
direction as a result:

- **The 89 forms were described as an inflated headline.** As a standalone library the
  framing is arguable. As the ingestion surface of a suite through which four downstream
  tools and an agent must accept whatever a user brings, breadth is the product.
- **The governance apparatus was described as unusually rigorous.** For one library a
  stability registry, support tiers, a shared reporting protocol, cross-repository issue
  references and a shared unit policy are disproportionate. For six repositories with
  cross-dependencies they are the minimum that works. The currently failing cross-repo
  unit-policy tests are that coordination problem appearing, not a fragile test.
- **The comparison classes named the wrong peers.** Biotite and ProDy are the right
  analogues for a library. For a substrate the analogues are ASE, RDKit, OpenMM and the
  MDAnalysis MDAKits ecosystem, where the criterion is whether third parties build on it.

An audit that reads everything and still reaches the wrong frame is a measurement of the
surfaces, not of the auditor.

## Why

**A referee will make the same mistake.** Evaluated as a library, MolSysMT is good and
substitutable — the reader has Biotite and ProDy and MDAnalysis. Evaluated as the
substrate of an ecosystem with an agent above it, it is a different contribution with a
different bar. The manuscript decision is
[#191](https://github.com/uibcdf/molsysmt/issues/191); this entry is about the
repository, which a referee reads first and which currently argues the weaker case.

**It changes what a user is deciding.** Adopting a library is a reversible choice about
one task. Adopting the substrate of a suite is a different commitment, and a reader is
entitled to know which one is on offer before they find out from a sibling repository.

**It is the same defect as [#186](https://github.com/uibcdf/molsysmt/issues/186), one
level up.** There the README omits the project's own stability classification; here every
public surface omits the project's own purpose. Both are cases of the repository knowing
something true about itself and not saying it.

Severity is `medium` for the same reason as #186: nothing is false, and what is missing
sits on the surface that determines how everything else is read.

## What is measured and what is assumed

Measured: the three zero counts; the two existing mentions and their locations; the
`pyproject.toml` description; the absence from `competitive_landscape_and_vision.md`
before 2026-08-19; the confinement within `devguide/` to the release ledger and the
citation document.

Assumed, and stated by the maintainer rather than derived from the repository: that
MolSys-AI is moving from assistant to agent, and that TopoMT, PharmacophoreMT and
ElasNetMT are queued rather than hypothetical. This entry records the positioning gap, not
the roadmap; the roadmap is the maintainers' to state.

Not established: whether the omission is deliberate. Leading with an ecosystem that is
not yet publicly released is a defensible editorial choice, and if it is the choice, this
entry closes by recording it rather than by changing the pages.

## What was refuted

*The ecosystem is documented and the audit missed it.* Checked and refuted by the counts
above. Two subordinate clauses, one of them inside a citation abstract.

*`release_1_0_status.md` covers it.* It does not, and it should not.
[`../../DOCUMENT_POLICY.md`](../../DOCUMENT_POLICY.md) makes that file an operational
ledger of current execution state; positioning is not execution state, and a reader
looking for what MolSysMT is for will not open a release ledger.

## Scope and exclusions

Covers the public surfaces: `README.md`, `pyproject.toml`, the documentation landing
page, and `competitive_landscape_and_vision.md` — the last already partly addressed on
2026-08-19 by the comparison-classes section, which now names the substrate class
explicitly.

Excludes the manuscript, [#191](https://github.com/uibcdf/molsysmt/issues/191). Excludes
any claim about the sibling tools' status, capabilities or release dates: this repository
should state its own role, not advertise software it does not contain. Excludes
`AGENTS.md`, which governs contribution and is the wrong place for positioning.

## Acceptance criteria

1. `README.md` states MolSysMT's role in MolSysSuite where a reader meets it, not in a
   later section.
2. The `pyproject.toml` description, which is the PyPI and Conda storefront, agrees.
3. The documentation landing page agrees.
4. A test asserts that the three surfaces above and `CITATION.cff` carry a consistent
   one-line statement of role, so they cannot drift apart again. This is the `guard`, and
   it is the same mechanism #186 needs for its capability bullets.
5. Or: a recorded decision that the ecosystem is deliberately not led with until the
   sibling tools are released, in which case this closes as `withdrawn` with that reason.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64 at repository commit `c26de0c31`.
Counts refer to that commit; the `competitive_landscape_and_vision.md` figure is stated
against `ae6a6b8a6`, its last revision before the comparison-classes section landed.
