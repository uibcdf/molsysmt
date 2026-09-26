# Release Citation and Zenodo Contract

This operational guide defines how MolSysMT publishes citable software releases. It is
also the template for MolSysViewer, PyUnitWizard, ArgDigest, SMonitor, and DepDigest.
The normative tag gate remains [`release_gate.md`](release_gate.md); this document
explains the citation and preservation part of that gate.

## The identifiers and their roles

MolSysMT already has a working Zenodo version family:

| Identifier | Role |
|---|---|
| `10.5281/zenodo.1298752` | stable concept DOI for MolSysMT as a project |
| `10.5281/zenodo.8092688` | historical DOI for release 0.8.1 |
| `10.5281/zenodo.17850104` | historical DOI for release 0.12.0 |

The concept DOI is stable across releases. Use it in `CITATION.cff`, README badges,
documentation landing pages, governance, and general project citations. Zenodo creates
a distinct version DOI after ingesting each GitHub Release. Use that version DOI when a
paper or workflow must identify the exact archived source used for reproducibility.

The old `10.5281/zenodo.2530946` identifier belongs to MolModMT, not MolSysMT. It must
not appear on a current MolSysMT citation surface.

## Metadata authority

The files have deliberately different consumers:

- `CITATION.cff` is the canonical user-facing citation record. GitHub reads it for
  **Cite this repository**. It owns the project title, authors, ORCIDs, release version,
  release date, concept DOI, license, and repository URL.
- `.zenodo.json` controls metadata used by Zenodo's GitHub ingestion whenever the file
  exists. Zenodo ignores `CITATION.cff` in that case. Keep it for Zenodo-specific fields
  such as communities, grants, contributor roles, and related identifiers.
- README and documentation citations are derived public surfaces. They must agree with
  `CITATION.cff`; they are not independent metadata authorities.

MolSysMT keeps `.zenodo.json` for 1.0 because this route has already archived releases
successfully. Shared fields in the two records must agree. A sibling that needs no
Zenodo-specific metadata may use `CITATION.cff` alone.

## What GitHub and Zenodo automate

Enabling a repository in the Zenodo GitHub integration is a one-time maintainer action.
After that, publishing a GitHub Release archives the snapshot for its tag and creates a
version DOI in the existing concept family. Pushing a Git tag without publishing a
GitHub Release does not request Zenodo ingestion.

Zenodo ingestion is asynchronous. Its DOI cannot be treated as present merely because
the GitHub Release exists. The post-release verifier polls the public records API and
checks the version, repository tag, concept DOI, publication state, and archived files.

No Zenodo access token belongs in the normal release path. Public verification needs no
credentials. Direct deposition, file upload, DOI pre-reservation, or publication through
the Zenodo REST API requires a token and is reserved for recovery or a deliberately
manual deposit. Do not run both direct deposition and GitHub ingestion for one release;
that can create duplicate records or DOI families.

Official references:

- [Enabling a GitHub repository in Zenodo](https://help.zenodo.org/docs/github/enable-repository/)
- [Archiving a GitHub Release](https://help.zenodo.org/docs/github/archive-software/github-upload/)
- [CITATION.cff precedence](https://help.zenodo.org/docs/github/describe-software/citation-file/)
- [.zenodo.json precedence](https://help.zenodo.org/docs/github/describe-software/zenodo-json/)
- [Zenodo REST API](https://developers.zenodo.org/)

## Preparing a release

Prepare metadata before the candidate commit is tagged:

```bash
python devtools/scripts/prepare_release.py 1.0.0
python devtools/scripts/validate_citation.py --expected-version 1.0.0
```

The preparation command updates release-specific fields in `CITATION.cff` and its
derived documentation/BibTeX surfaces. Review the resulting diff. It does not create a
tag, GitHub Release, Zenodo record, or network request.

The candidate then follows the exact-commit gates in [`release_gate.md`](release_gate.md).
Do not put `[skip ci]` on the candidate commit.

## Publishing and verifying a release

After the exact candidate passes every gate:

1. create and push the version tag on that exact commit;
2. publish the GitHub Release for that tag;
3. complete the selected Conda route: a staged version promotes the exact
   SHA-256-verified ABI3 files instead of rebuilding them, while a direct
   release is allowed only after an empty-version registry preflight;
   if post-promotion verification fails, inspect the promotion receipt and
   rerun `.github/workflows/verify_public_conda_package.yaml` with the exact
   version, platform, filename and SHA-256. This workflow checks the public
   `main` label and solver-visible index without credentials or another
   promotion; never rerun a mutating upload merely to change a red verifier;
4. allow the enabled Zenodo integration to ingest it and verify the new record:

   ```bash
   python devtools/scripts/verify_zenodo_release.py 1.0.0
   ```

The `verify-zenodo-release.yaml` workflow performs step 4 automatically for published
releases. A failed or delayed external ingestion does not change the tested software
commit, but the release is not fully signed off until the verifier passes. Retry the
verification before attempting any manual deposit.

## Citation policy for readers

Public pages should say both of the following without conflating them:

- cite the stable concept DOI for MolSysMT generally;
- cite the DOI of the exact Zenodo version when reproducing a particular calculation.

The methods paper can later become `preferred-citation` in `CITATION.cff`. The software
record and concept DOI remain present because citing a paper does not identify the
software snapshot.

## Applying the contract across MolSysSuite

For every sibling repository:

1. enable the repository once in the maintainer's Zenodo GitHub settings;
2. establish or identify its own concept DOI; never reuse MolSysMT's DOI;
3. adopt a repository-local `CITATION.cff` with that concept DOI;
4. keep `.zenodo.json` only when Zenodo-specific metadata is needed;
5. port the preparation, validation, and post-release verification tools;
6. add the validator to the repository's fast release gate;
7. publish GitHub Releases rather than relying on tags alone.

The workflow is shared; project identity, authorship, and concept DOI remain local to
each repository.

## Repeatable release practice learned from 0.22.4/0.23.4

The 2026-09-25 paired release is evidence for the following operational order,
not a rule that every later patch must use staging. The common staging and
promotion contract is proposed in `uibcdf/molsyssuite#27`; do not let two
component checklists become independent policy authorities.

1. Decide **paired versus independent** and **staged versus direct** before
   freezing a version. A hard dependency floor that has no public candidate,
   a mutual publication cycle, or a changed release recipe requires a
   coordinated staging plan. A compatible independent patch can use the
   guarded direct route after its registry preflight. Record the decision
   and the exact version, tag candidate, channel, build number and owner.
2. Preflight dependency resolution and source/package version identity before
   expensive native builds. For a paired candidate, preserve the source SHA,
   Conda build coordinates and SHA-256 receipts; a correction gets a new
   build number, never replacement bytes at a tested coordinate. Check the
   Viewer Python wheel's packaged JS runtime before tagging, not only the
   Conda/npm rebuilds (`uibcdf/molsysviewer#102`).
3. Run the **staged exact-pair** clean-install matrix before tags. Evaluate
   failures by layer (solver, package metadata, code, resources, hosted test
   infrastructure) and retain a narrow explicit exception only for evidence
   that the maintainers have accepted for a pre-1.0 release. The 0.22.4/0.23.4
   exception does not weaken either 1.0 gate (`uibcdf/molsysviewer#100`).
4. Publish immutable tags/Releases, promote only the verified staged files,
   then rerun the **public-channel** installed-pair matrix. A successful
   upload action and a green workflow conclusion are different observations:
   the 0.22.4/0.23.4 uploads succeeded while duplicated final verification
   steps made those jobs red (`uibcdf/molsyssuite#48`). Never re-upload a
   public artifact just to repair that diagnostic; use independent read-only
   package and installation checks.
5. Verify npm/CDN when Viewer is involved and treat Zenodo as a separate
   asynchronous archival gate. The 0.22.4/0.23.4 records arrived after the
   existing 900-second polling window; that timeout was not a failed
   ingestion (`uibcdf/molsyssuite#49`). Recheck public records before any
   account-side recovery. Validate the repository identity, exact version,
   concept/version DOIs, published state and source ZIP inventory. Do not
   require a `/tree/<tag>` related identifier when Zenodo supplies the exact
   repository and versioned archive instead (`uibcdf/molsysmt#247`).

Evergreen citation tests must compare derived surfaces with the current
`CITATION.cff`, not a hard-coded future release number. The exact candidate
gate is the place to assert its intended version (`uibcdf/molsysmt#248`).

The five-platform ABI3 build (one artifact per native platform) and Viewer
noarch build kept the expensive stage to six files, while both staging and
public installed-pair matrices exercised all 20 Python/platform cells. Reuse
those distinct evidence layers instead of rebuilding per Python minor or
repeating a mutation workflow to change its status. Use GH Run Receptor for
compact run triage, escalating to targeted native logs only when needed.

## Recovery rules

- If metadata validation fails before tagging, correct the candidate and rerun its
  exact-commit gates.
- If Zenodo rejects a release, inspect the repository entry under the Zenodo GitHub
  integration, correct the metadata in a new commit, and decide explicitly whether the
  release must be replaced. Do not silently retag a published release.
- If ingestion is only delayed, rerun the verifier. Do not create a manual duplicate.
- If an incorrect Zenodo record was published, preserve its history and use Zenodo's
  supported editing/versioning controls or contact Zenodo support; never repoint a DOI.
