---
summary: paper/main.tex is an unfilled template and the manuscript argument is unrecorded.
issue: uibcdf/molsysmt#191
status: open
opened: 2026-08-19
closed:
verification: inspected
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: record the manuscript's argument before writing it

**Raised:** 2026-08-19, during the external audit recorded in
[`../archive/assessments/external_audit_august_2026.md`](../archive/assessments/external_audit_august_2026.md).
It was the audit's first finding and the one that framed the rest.
**Status:** proposed. The release ledger schedules "manuscript work"; no entry says what
the manuscript argues.

## What

`paper/` contains a 2020 *Bioinformatics* template with its placeholders intact.
`paper/main.tex` is 118 lines:

```latex
\abstract{\textbf{Summary:} Bla, bla, bla.\\
...
\section{Introduction}
Text Text Text Text Text Text  Text Text Text Text Text Text Text
```

The Implementation and Conclusion sections are the same. The only real content is a
`\subsection{Arguments}` list of seven notes in Spanish, and it is the most valuable part
of the file — it records what the authors thought the paper was about in 2020.

Two consequences follow, and only the second is worth an entry.

The first is obvious: there is no manuscript. That does not need tracking; it needs
writing.

The second is that **nothing in the repository states what the paper claims**, and
several things now depend on knowing. `presentation_and_citation_surface.md` prepares the
surfaces "the forthcoming methods paper will point at".
`release_1_0_execution_plan.md` schedules work around "manuscript writing or review".
[#190](https://github.com/uibcdf/molsysmt/issues/190) cannot populate a claimed-API scope
without the list of claims. Three documents wait on a decision that has no home.

What is proposed is that home: a short, argued statement of the manuscript's
contribution, its claimed surfaces, and its venue, written before the LaTeX.

## How

The statement needs five things, none of which is prose about the software:

**1. The contribution, in one sentence that survives a hostile reading.** The audit's
view, offered as input and not as a decision: the defensible contribution is
*conversions that declare what they lose*. `msm.convert(..., return_report=True)` returns
`outcome='lossy'` with a per-attribute account of what the destination form cannot
represent, and the audit found no equivalent in the tools MolSysMT interoperates with.
That is a methodological claim about how heterogeneous molecular representations should
interoperate, and the 89 forms are its demonstration surface rather than the claim
itself.

The alternative framing — a unified API over many libraries — is the one
[`readme_positioning_and_1_0_refresh.md`](readme_positioning_and_1_0_refresh.md) already
identified as damaging, for the same reason it fails in review: it invites the reader to
classify the work as integration rather than method.

**2. The list of claimed APIs**, which is the input [#190](https://github.com/uibcdf/molsysmt/issues/190)
needs, and which determines what must be validated before submission rather than after.

**3. The venue.** The template implies a *Bioinformatics* Application Note. Two pages
cannot carry the fidelity argument plus a validation section. This is a decision to take
deliberately, not to inherit from a file copied in 2020.

**4. The comparison class, and the tools in it.** "How does it compare" has no answer
until the reference class is named, and the class chosen decides how the work is read. A
paper positioned as a unified API over many libraries is read against MDAnalysis, where
the comparison is adoption and MolSysMT loses it. One positioned on declared-loss
interoperability and native preparation is read against a much thinner field.

Whichever is chosen, the related-work section must name **Biotite** and **ProDy**. They
are the closest architectural analogues in structural biology — a native object model,
many formats, a selection language, analysis over the same abstraction — and until
2026-08-19 neither appeared in
[`../competitive_landscape_and_vision.md`](../competitive_landscape_and_vision.md), which
named only MDTraj, MDAnalysis and BioPython. A referee in this field knows both. A
related-work section that omits them invites the question in the first round, and answering
it then is worse than answering it in the submission. The classes and the tools in each
are now recorded in that document; no reproducible comparison against either has been run,
and one may be needed before submission depending on the class chosen.

**5. The reproducibility package.** Which release, which DOI, which environment, and
which figures regenerate from what. `release_and_citation.md` governs the citation
record; nothing governs the manuscript's computational artifacts.

## Why

**The repository is being prepared for a reader who does not exist yet on paper.** The
positioning pass, the citation lifecycle, the presentation surface work and this audit
were all conducted against an imagined referee. An imagined referee is a weak constraint
and every participant imagines a different one.

**The claims determine the remaining engineering.** Whether `get_secondary_structure`
needs an independent oracle before submission is not a testing question; it is a question
about whether the paper reports secondary structures. Right now that is unanswerable, so
the validation backlog cannot be prioritised.

**The 2020 notes are evidence and will be lost.** They are in Spanish, in a `.tex` that
will be overwritten by the first real draft, and they contain the original framing —
lowering the barrier for non-expert users, reproducibility, in-house libraries for the
heavy work, the pandas-backed topology as a substitutable engine. Whether or not the
final argument keeps them, they should not disappear in a `git checkout`.

## What is measured and what is assumed

Inspected, not measured: the contents of `paper/main.tex`, and the three documents that
reference manuscript work.

Assumed, and flagged as the audit's opinion rather than a finding: that the fidelity
report is the strongest available contribution, that an Application Note is too short,
and that Biotite and ProDy are the comparisons a referee will reach for. Both are judgements from one reading of one repository by one reviewer who is not
a domain referee. The maintainers' view supersedes them, and this entry is the place to
record that it did.

## What was refuted

*The paper is drafted and simply not committed.* Not established either way — the audit
can only observe the repository, and this entry records what is in it. If a draft exists
elsewhere, the useful part of this proposal is still items 2, 3 and 4.

## Scope and exclusions

Covers the argument, the claimed-API list, the venue, the comparison class, and the
reproducibility package.

Excludes writing the manuscript. Excludes the citation record and the Zenodo lifecycle,
which are governed by [`../release_and_citation.md`](../release_and_citation.md), and the
installation-sequencing item still open in
[`presentation_and_citation_surface.md`](presentation_and_citation_surface.md).

## Acceptance criteria

1. A document in `devguide/` states the contribution in one sentence, the claimed APIs,
   the venue, the comparison class, and the reproducibility package.
2. The Spanish notes currently in `paper/main.tex` are preserved somewhere that survives
   the first draft.
3. [#190](https://github.com/uibcdf/molsysmt/issues/190) can populate its claimed scope
   from item 1 without further decisions.
4. The chosen comparison class names Biotite and ProDy, or records why the manuscript
   excludes them.

## Dependencies and risks

[#190](https://github.com/uibcdf/molsysmt/issues/190) depends on this for its scope,
though its registry mechanism does not. The risk of writing this down is that it fixes an
argument early; the risk of not writing it is that four documents keep serving a referee
nobody has specified.

## Provenance

Inspected 2026-08-19 at repository commit `dc0e06014`. `paper/main.tex` was last modified
in the working tree on 2026-04-22 and its `\copyrightyear` is 2020.
