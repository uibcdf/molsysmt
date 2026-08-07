# Presentation and citation surface: the remaining public-facing work

**Status:** partially resolved on 2026-08-07. The authorship question and the
duplicate landing page are decided and applied. Item 1c is decided but deliberately
not yet executed: `CITATION.cff` is a placeholder until 1.0, and the Zenodo record
and DOI are updated when the release closes — it is now a line in the
[release gate](../release_gate.md) sign-off so it cannot drift again. Item 3, the
installation-instruction sequencing, is still open.
**Raised:** 2026-07-29, during the positioning audit recorded in
[`readme_positioning_and_1_0_refresh.md`](readme_positioning_and_1_0_refresh.md).
**Scope:** `CITATION.cff`, `.zenodo.json`, `docs/index_v2.ipynb`, and the Conda
installation instructions across `README.md` and the documentation landing page.

## Why these are separated from the positioning work

The positioning pass rewrote how MolSysMT presents itself and corrected every
factual error it could verify from the repository. These three items could not be
finished the same way: two of them turn on facts only the maintainers hold, and
one turns on release timing. Recording them here keeps them from being lost
between "already fixed" and "nobody owns it".

They are also the surface that the forthcoming methods paper will point at. A
reader arriving from the paper meets the citation record, the landing page and the
installation instructions before anything else.

## Item 1 — the citation record is stale, inconsistent, and misattributes an ORCID

Three separate problems, in decreasing order of seriousness. **1a and 1b were
resolved on 2026-08-07**: the maintainer's decision is that Daniel Ibarrola-Sánchez
is not an author, so he was removed from `CITATION.cff`. That settles the
misattributed ORCID by removing the entry that carried it, and it makes the three
records agree — `CITATION.cff` and `.zenodo.json` now list the same two authors with
the same ORCIDs, and the README acknowledges his contributions to MolSysMT's early
development. **1c remains open.**

**1a. A real person is listed with someone else's ORCID.** `CITATION.cff`
records:

```yaml
- family-names: "Ibarrola-Sánchez"
  given-names: "Daniel"
  orcid: "https://orcid.org/0000-0003-3375-870X"
```

That identifier is Diego Prada-Gracia's, which appears immediately above in the
same file. An ORCID is a persistent identifier tied to an individual researcher,
so this is not a typo in a version string: it attaches one person's scholarly
identity to another's contribution record. It should be corrected with Daniel
Ibarrola-Sánchez's own ORCID, or the field removed if he does not have one.

**1b. The two citation records disagree about authorship.** `CITATION.cff` lists
three creators (Prada-Gracia, Ibarrola-Sánchez, Moreno-Vargas). `.zenodo.json`
lists two (Prada-Gracia, Moreno-Vargas), and `README.md` credits Daniel Ibarrola
Sánchez under Acknowledgments rather than as an author. Two of these three
positions can be right; not all three. The distinction between authorship and
acknowledgment is the maintainers' call, and once made it should be identical in
both machine-readable records.

**1c. The version and DOI are stale, and the DOI is malformed.**

| Field | `CITATION.cff` | Reality |
| --- | --- | --- |
| `title` | `uibcdf/MolSysMT: 0.8.1` | current version is 0.21.0 |
| `version` | `0.8.1` | 0.21.0 |
| `date-released` | `2023-06-28` | over two years stale |
| `doi` | `10.5281/8092688` | malformed — a Zenodo DOI is `10.5281/zenodo.<id>`; the README badge uses `10.5281/zenodo.2530946` |

`.zenodo.json` carries no version or DOI at all, which is correct for a
concept-level record, and its description is already well framed. It does not
need the same treatment.

**Decisions required:** Daniel Ibarrola-Sánchez's ORCID; whether he is an author
or an acknowledged contributor; and which DOI is canonical — the concept DOI that
resolves to every release, or a version DOI updated at each tag.

**Acceptance criteria:** no ORCID appears against more than one person; the author
list is identical in `CITATION.cff` and `.zenodo.json` and consistent with the
README; the DOI is well formed and resolves; and the release metadata either
matches the tagged version or is deliberately concept-level, stated as such.

**Worth considering:** version and date in `CITATION.cff` drifted for two years
because nothing updates them. If the canonical choice is a version DOI, this
should be part of the release procedure in `release_gate.md` rather than a manual
step that will drift again.

**Decided 2026-08-07.** `CITATION.cff` is treated as a placeholder until 1.0. The
new Zenodo record, its DOI, and the version, title and date fields are all updated
as part of closing the release rather than now, so the file is expected to read
`0.8.1` until then. To keep it from drifting a second time, the release gate's
sign-off checklist now carries the step explicitly.

## Item 2 — an unreferenced duplicate landing page — **resolved 2026-08-07**

The maintainer's decision is to delete it, and
`docs/content/user/index_v2.ipynb` was removed with its two `nbconvert` artifacts.

Three orphans of the same abandoned `_v2` experiment are still tracked and still
have no inbound reference from any page: `docs/api/index_v2.md`,
`docs/content/user/tools/index_v2.md`, and `docs/temp/index_v2.ipynb`. They carry
the same risk described below and feed the `toc.not_included` warning family
measured in `pending_bugs/sphinx_warning_baseline_and_api_reference_debt.md`.
Removing them is the same decision, not a new one, and is left pending only because
it was not part of the instruction.

The original finding, for the record: `docs/index_v2.ipynb` was last modified on
2026-05-26 (`00e13b27b`) and nothing linked to it — it appeared in no `toctree`, in
`docs/conf.py`, or in any other document.

It carries the superseded content the positioning pass has just corrected in
`docs/index.ipynb` — the "One API. 60+ molecular formats and libraries" tagline,
the "50-module journey", and "60+ molecular formats" in the ecosystem card.

The risk is not that it renders — it does not. The risk is that it is the second
file a contributor finds when searching for the landing page, and it now contradicts
the live one on every claim that was just fixed.

**Decision required:** delete it, or promote it and retire `docs/index.ipynb`. If
it represents an intended redesign, it should say so in its first cell and be
tracked as documentation work rather than left as an orphan.

## Item 3 — installation instructions describe a state that is not yet reachable

`README.md` and the documentation landing page both lead with:

```bash
conda install -c uibcdf -c conda-forge molsysmt
```

That is the intended 1.0 instruction and the official distribution channel. It is
not currently satisfiable: the Conda delivery track is open, and the blocking
findings are recorded in
[`molsysmt_1_0_conda_release_coordination.md`](molsysmt_1_0_conda_release_coordination.md)
— required sibling tags that exist only on local clones, a publishing workflow
that triggers on a GitHub Release rather than a tag, and a missing `molsysviewer`
build for Python 3.13.

This is a sequencing question, not a defect. The options:

1. **Publish the documentation with the README as written, once the Conda track
   closes.** Cleanest, and the instruction is never wrong. Ties the documentation
   release to a track that is explicitly off the technical critical path.
2. **Keep the instruction and add a short availability note** until the channel is
   live. Honest, slightly awkward on a front page.
3. **Lead with the source install** until the channel is live, then swap. Correct
   at every moment, but presents the harder path first and understates the product.

**Recommendation:** option 2 while the track is open, moving to option 1 on the day
the channel resolves. A reader who cannot install is better served by one sentence
than by an error message.

**Acceptance criterion:** at no point does a published page carry an installation
command that fails, without a note saying so.

## Out of scope

- The framing and factual corrections already applied; see
  [`readme_positioning_and_1_0_refresh.md`](readme_positioning_and_1_0_refresh.md).
- The methods paper itself. These items are the surface a paper reader lands on,
  not the paper's content.
- The Conda delivery track, which is tracked in its own coordination report.
