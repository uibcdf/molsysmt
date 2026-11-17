---
summary: paper/main.tex is an unfilled template and the manuscript argument is unrecorded.
issue: uibcdf/molsysmt#191
status: partial
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
**Status:** partial. A proposed author-facing argument/evidence packet and the
maintainer-selected venue are recorded in the dated section below; final claims,
comparisons and manuscript writing remain author work.

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
view, offered as input and not as a decision, and revised once during the same session.

*First reading:* the defensible contribution is *conversions that declare what they lose*.
`msm.convert(..., return_report=True)` returns `outcome='lossy'` with a per-attribute
account of what the destination form cannot represent, and the audit found no equivalent
in the tools MolSysMT interoperates with. That is a methodological claim about how
heterogeneous molecular representations should interoperate, and the 89 forms are its
demonstration surface rather than the claim itself.

*Revised reading, after the maintainer stated the ecosystem context the repository does
not carry* ([#192](https://github.com/uibcdf/molsysmt/issues/192)): the fidelity contract
is the mechanism, not the thesis. The thesis is that **a common molecular-system
substrate is what lets a family of tools interoperate at all, and declared-loss
conversion is the condition that makes such a substrate possible.** MolSysViewer,
MolSys-AI, TopoMT, PharmacophoreMT and ElasNetMT are the demonstration that the
abstraction carries weight beyond one library.

This framing is more ambitious and better supported by what exists, and it comes with a
cost the manuscript must pay openly: **no third party outside UIBCDF is known to build on
MolSysMT.** ASE and RDKit are substrates because outsiders adopted them. A suite by the
same authors demonstrates that the abstraction serves its authors, which is evidence of
design soundness and not of adoption. A reviewer will find this in one search, so the
paper states it rather than being asked.

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

If the substrate thesis is chosen, the peers change with it: not Biotite and ProDy but
**ASE**, **RDKit**, **OpenMM** and the **MDAnalysis MDAKits** ecosystem, where the
criterion is whether third parties build on the abstraction. The five classes and the
tools in each are recorded in
[`../competitive_landscape_and_vision.md`](../competitive_landscape_and_vision.md).

Whichever is chosen, the related-work section must still name **Biotite** and **ProDy**. They
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
   excludes them; if the substrate thesis is chosen, it also names the substrate peers
   and states the absence of external adopters.

## Dependencies and risks

[#190](https://github.com/uibcdf/molsysmt/issues/190) depends on this for its scope,
though its registry mechanism does not.
[#192](https://github.com/uibcdf/molsysmt/issues/192) is the repository-side half of the
same question: this entry decides what the paper argues, that one decides whether the
public surfaces argue it too. They should be settled together, and the paper should not
claim a role the README does not state. The risk of writing this down is that it fixes an
argument early; the risk of not writing it is that four documents keep serving a referee
nobody has specified.

## Provenance

Inspected 2026-08-19 at repository commit `dc0e06014`. `paper/main.tex` was last modified
in the working tree on 2026-04-22 and its `\copyrightyear` is 2020.

## Proposed manuscript inputs — 2026-11-17

**Owner:** #191, with #378's bounded reader/discoverability work and #334 B4.
**Status:** proposed author-facing evidence packet; not an approved abstract,
finished manuscript, new scientific certification or software release gate.
The maintainer selected a **JCIM Application Note** in the session. The old
Bioinformatics template does not determine the venue or current journal rules.
No claim about current submission limits is made here.

### Proposed contribution and comparison

**Working contribution:** MolSysMT provides a form-agnostic, unit-aware molecular
system toolbox with separate native domains and explicit conversion, persistence
and provenance contracts for reusable computational workflows.

The native representation, reusable tools and fidelity contracts support this
claim together. A form count, a wrapper list or the existence of suite clients
alone does not establish novelty, scientific accuracy, usability or adoption.
The authors still decide the final emphasis and scientific claims.

Compare supported tasks and contracts, rather than ranking whole libraries.
Biotite, ProDy, MDAnalysis and MDTraj are proposed structural-workflow comparison
subjects; RDKit, OpenMM and ASE provide additional chemistry/model-substrate
context. This packet supplies no new head-to-head result and does not establish
that any feature is absent from those tools. A novelty or performance comparison
requires version-pinned primary-source review and equivalent executed workloads.
MolSysSuite receiving demonstrates internal reuse; independent external adoption
has not been established by this packet.

### Claim-to-evidence table

These labels qualify the cited scope only. The
[scientific evidence matrix](../scientific_evidence_matrix.md) and its underlying
registry remain authoritative for governed scientific scopes and gaps; this
manuscript table cannot promote a symbol or replace exact-candidate execution.

| Proposed statement | Evidence and reproducible entry point | Classification and practical limit |
| --- | --- | --- |
| Separate stable inventory, chemical state, geometry, mechanics and named interaction analyses can travel in a native molecular system. | [Core specification](../CORE_SPECIFICATION.md), [native queries](../native_queries.md), native partial-domain tests and `tests/basic/test_permute_atoms.py`. | Implemented and contract-tested for supported native domains. Topology has no chemical facade; chemical changes do not redefine declared stable molecule membership. MolecularMechanics remains experimental. |
| Supported forms share public operations with explicit capabilities and conversion-loss reports. | [Forms/conversions](../forms_and_conversions.md), `tests/conversion_truth/test_declared_docking_edges.py` and the #181 conversion-execution inventory. | Contract-tested for received edges/witnesses. A discoverable adapter is not proof of every conversion; non-exhaustive reports are not complete chemical validation. |
| H5MSM 1.0 persists supported native domains, histories, maps, original producer metadata and named analyses. | [Default-write receiving](../../devtools/data/h5msm_default_10_receiving_256_20261110.json), #256's BindingMT receiving and `tests/interactions/test_public_molsys_h5msm_workflow.py`. | Provider and bounded real-client source receiving. A stable wire decision and source result are separate from the still-unqualified final installed pair. Original source files must remain intact. |
| Sparse interaction results support composite participants, roles, parallel observations, explicit coverage and combined bounded queries. | [Interaction contract](../interactions_api.md), `tests/interactions/test_occurrence_pages.py`, `test_query_candidates.py`, `test_frame_replacement.py` and the received query/persistence corpus. | Implemented and contract-tested. Evaluated-empty differs from unevaluated; occurrence handles are analysis-version scoped. Independent-file correspondence remains a caller declaration. |
| Geometric interaction criteria and executed/reference software can be recorded without guessing scientific authorship. | Detector docstrings, `tests/scientific_truth/curated/test_attributed_interaction_methods.py`, `tests/interactions/test_scientific_attribution.py` and #292's public-reader guards. | Bounded reference/parity and provenance evidence. Experimental profiles are not blanket physical-interaction, binding-energy or biological-absence validation. No Buch paper is invented. |
| Saved interaction bibliography can be rendered independently of the original producer. | `tests/interactions/test_portable_attribution.py`: original versions, two reused/empty results, public Ackredit reader, typed/H5MSM persistence and fresh producer-blocked reading. | Contract-tested with source Ackredit and exact public 0.9.0 payload. Optional result-bibliography projection is distinct from observed workflow capture; installed release/Python matrices remain separate. |
| Native geometry and periodic tools preserve explicit source axes and physical units on their supported workloads. | [Scientific matrix](../scientific_evidence_matrix.md), governed analytic/external structure and PBC selectors, and `tests/form/XYZ/test_public_coordinate_delivery.py`. | Scientifically validated only within each registered fixture/tolerance. Indices are not labels; boxes use row vectors. No universal precision, periodic chemistry or all-form guarantee follows. |
| Explicit templates, fixed-state H generation and controlled native reconstruction can preserve observed coordinates and historical correspondence. | `tests/physchem/test_chemical_template.py`, `tests/build/add_missing_hydrogens/test_fixed_state.py`, pinned template manifests and the prepared-template Cookbook. | Contract/parity tested with bounded independent chemical/pose controls. This is not arbitrary ligand protonation, validated rotamer repair or environment-refined H geometry; uibcdf/molsysmt#323 and uibcdf/praxis#3 own further protocol work. |
| Physicochemical tools expose explicit reference/model definitions and units rather than treating every descriptor as an observed property. | Governed reference-property, TPSA, lipophilicity and SASA entries in the [scientific matrix](../scientific_evidence_matrix.md), plus their executed examples. | Bounded reference/analytic/parity evidence, with the matrix's partial/gap labels retained. Tabulated area is not conformational SASA; model logP is not logD or experimental predictive accuracy. |
| Native access and sparse storage avoid specific unnecessary reconstruction/materialization work. | [Native-query study](native_query_shortcuts.md), [dictionary baseline](../../benchmarks/baselines/dictionary_queries_20261021.json), [bounded HDF5 receipt](../../devtools/data/interactions_bounded_hdf5_writing_20261002.json), [scalability contract](../SCALABILITY.md). | Benchmarked only on each recorded workload/environment; additional mechanism guards protect bounded operations. No universal speedup, outperformance of third parties, or negligible peak RAM is claimed. |
| Real suite consumers can use received source contracts. | Published MolSysViewer/BindingMT handoffs and the live [release ledger](../release_1_0_status.md), with each exact source/binary/composition identified. | Bounded internal consumer receiving. This is not an independent adoption study, final installed acceptance, visible-human review or authorization to publish. |

### Reproducible examples and proposed figures

1. **Domain/ownership diagram:** derive it from the current core specification;
   distinguish stable topology, stored chemistry, coordinate structures,
   experimental mechanics and named sparse analyses. No unimplemented relation
   or automatic scientific recalculation should appear.
2. **Explicit chemical-input workflow:** use the five-atom independent SDF
   fixture in `tests/basic/test_chemical_workflow_composition.py`, through known
   permutation, H5MSM, export and selected coordinate edit. It gives numeric,
   isotope/charge/bond, map and evaluated-empty ownership oracles without docking.
3. **Sparse scientific analysis:** choose a documented detector/profile and its
   original/reference method, then show nonconsecutive structures, participant
   selection, original provenance and named persistence. Use a curated detector
   control for science; the synthetic container recipe is not detector validation.
4. **Native access/storage measurement:** select a dated reproducible baseline
   only if it supports a manuscript claim. Retain source, input hashes, hardware,
   dependency origins, warm-up, statistic, memory scope and uncertainty. Correct
   but slower implementations remain available; efficiency warnings/improvement
   issues follow #567 rather than blocking correct science.

The frozen B1 eight-article cohort and B2 composition receiving add bounded
examples; they do not substitute for the original scientific registry. Existing
I0–I5 native examples retain their separate source/execution receipts. No new
benchmark, broad receptor preparation or simulation is commissioned by this packet.

### Reproducibility and author decisions still required

- Freeze final claimed APIs and comparisons before making novelty or numerical
  accuracy claims. Check every proposed sentence against the scope/limit column.
- Bind the eventual figures/examples to exact MolSysMT/MolSysViewer sources,
  native binary, package filenames/builds/SHA-256, dependency versions/origins,
  inputs, units and deterministic parameters. Those final artifacts are not fixed.
- Keep source tests, stored rendering, actual Jupyter/browser receiving, installed
  pair/platform qualification and the maintainer's scientific/editorial review
  distinct. Existing failed/incomplete controls remain part of the record.
- Use the canonical citation lifecycle in [release and citation](../release_and_citation.md).
  The project concept DOI stays stable; verify an exact release DOI only after
  actual archival. No release metadata or DOI is manufactured for this proposal.
- The manuscript may be written and submitted on its own timetable; manuscript
  acceptance is not an engineering completion criterion. Final wording, venue
  requirements, authorship and external-reader review remain author decisions.

### Preserving the original 2020 argument notes

The original source is retained in Git at
`c9b9b2055d5ebfbc43336e56bc2575384bbf67b7:paper/main.tex`, blob
`e681c246f8a7eacf267dafb4c4083466786984cd`. The file is unchanged by this packet.
The seven argument notes are preserved here in English before future rewriting:

1. Make Python workflows involving third-party libraries easier to assemble.
2. Lower the entry barrier for non-experts by providing workflow support.
3. Facilitate reproducibility.
4. Supply in-house routines for computationally demanding work.
5. Illustrate forms and elementary functions through a workflow diagram.
6. Provide native molecular-system forms containing topology, structures and
   other appropriate domains.
7. Use the familiar pandas topology representation; the original note envisaged
   a future alternative dataframe/query engine. That substitution is a design
   possibility, not an implemented compatibility or performance claim.

The old future-work note also asks for a description broad enough to accommodate
new forms/tools and support other libraries. This is motivation, not a promise
that every future feature has already been implemented or scientifically validated.
