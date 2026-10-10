---
summary: Freeze 1.0 scope and complete bounded stabilization
issue: uibcdf/molsysmt#334
status: active
opened: 2026-10-05
closed:
verification: measured
area: [docs, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Freeze 1.0 scope and complete bounded stabilization

**Accepted:** 2026-10-05, following the maintainer's request to stop capability expansion and preserve deferred work in issues.

## Source delta for coordination resumption — 2026-10-10

**Role of this checkpoint:** plan the affected review scope during the publication
pause. It neither selects a replacement source/version/build nor executes a new
qualification campaign. The [execution ledger](../release_1_0_status.md#release-coordination-paused--2026-10-08)
owns the pause and retained qualification; the [release gate](../release_gate.md)
continues to own mandatory admission/publication requirements.

### Reproducible source inventory

The [dated delta snapshot](../evidence/release_resume_source_delta_20261010.json)
compares frozen producer `6dc80725ea506f977fb5e52dfd701c2227875fa5` with reviewed
main `c3e78e5afa42dbf96b0e581ccac1184759034602`. Reproduce its path inventory with:

```bash
git diff --name-status --no-renames 6dc80725ea506f977fb5e52dfd701c2227875fa5 c3e78e5afa42dbf96b0e581ccac1184759034602
```

This records **269 changed paths** with their old/new Git object identities,
including **68 under `molsysmt/`** and **28 removed legacy-addon paths**. The
no-renames convention counts both sides of a move independently. Among the 68
package paths, 41 have different Python ASTs after removing docstrings, 17 are
added/removed Python files, nine retain that AST and one is non-Python metadata.
These are source-review counts, not measured behavior changes or performance.
Import reordering can change an AST; AST equality does not certify compatibility
or identical public documentation.

No changed path is under `molsysmt/physchem/` or the H5MSM form adapter, and no
Rust source changes. The `Interactions` implementation and its codecs are
unchanged; the two changed hydrogen-bond source files differ only in docstrings
under this AST inspection. Native composition, selection, conversion and
packaging still changed and require their applicable qualification. This is
not an argument for waiving an exact-candidate gate.

Read-only remote observations confirm the candidate branches still identify
the original provider and Viewer sources. The snapshot records the current
frozen receipt's Git identity and SHA-256, without reading/downloading package
files or changing any frozen ref/receipt. Preserve original files and historical
verdicts; evidence of those bytes cannot qualify a future package.

### Affected review map

This table identifies retained regression nodes and additional consumer checks;
it does not claim that they ran on a replacement candidate. The owning resolved
records and the ledger retain each earlier execution scope/outcome.

| Change and owning issues | Existing addressable provider guards | Required check when coordination resumes |
|---|---|---|
| Native composition, atom-aligned mechanics, chain labels and boolean validation (#352/#353/#356) | `tests/basic/merge/test_merge_prepared_mechanics.py`; `tests/basic/add/test_chain_identifiers.py`; `tests/native/test_native_add_digestion.py` | Preserve supported domain associations and maps through client edits/composition. H5MSM 0.5 still excludes nonempty mechanics. |
| Empty bonded selections and hydrogen-free Buch coverage (#355) | `tests/basic/select/test_empty_bonded_to.py` | The installed consumer calculates and stores a named evaluated-empty analysis; no inferred H or scientific-profile change. |
| Retirement of the separate Viewer addon (#354) | `devtools/tests/test_native_viewer_integration.py` | The built sdist/wheel/Conda install contains the native backend and no obsolete addon package/entry point; real Viewer flows must use its native path. Source inspection cannot establish installed contents. |
| Adapter delivery, sequence identity/subsets and file metadata (#139/#359/#360/#362/#363/#364) | `devtools/tests/test_validate_form_adapters.py`; `tests/form/biopython_Seq/test_group_queries.py`; `tests/form/biopython_Seq/test_copy_and_identity_conversion.py`; `tests/form/file_inpcrd/test_getters.py`; `tests/form/file_fasta/test_positional_queries.py`; `tests/form/file_crd/test_get_file_crd.py` | Retain truthful support tiers, source indices/string IDs, units and explicit unsupported routes. Do not infer universal conversion coverage from the delivery audit. |
| TRJPK subsets and output dispatch (#365/#370) | `tests/form/file_trjpk/test_queries_and_roundtrip.py` | Verify both selected axes, nm/ps encoding and legacy call compatibility. The keyword-only signature addition has an explicit existing registry waiver, not a general API waiver. |
| Underdetermined translated fit anchors (#367) | `tests/structure/fit/test_degenerate_anchors.py` | Reject before mutation; retain the established numerical-rank policy and independent fit controls. No new physical near-collinearity threshold. |
| Owned storage/LEaP failure lifecycle (#372/#373) | `tests/heavy/test_persistent_result.py`; `tests/third_party/tleap/test_tleap.py`; `tests/build/build_peptide/test_leap_resource_lifecycle.py`; `devtools/tests/test_tleap_check.py` | Protect caller files and retire only owned scratch across the covered failure stages. Keep optional-engine, concurrency and #374 exception boundaries explicit. |
| Public unit/rendering claims (#357/#358/#361), course/guide updates | `tests/structure/get_dihedral_angles/test_angle_policy.py`; `devtools/tests/test_public_api_docs.py` | Run applicable documentation/citation/course gates on the actual candidate; preserve active PyUnitWizard output policies. |

### Remaining decisions and execution

1. Viewer owns the design round and its open regressions
   uibcdf/molsysviewer#189 and uibcdf/molsysviewer#198. Their issue bodies do not
   currently request a new detector or provider implementation change. Confirm
   the consumer direction and any provider requirement before selecting sources.
2. Agree exact replacement source SHAs, versions, build coordinates and package
   identities. Changed files need new immutable artifact coordinates; never
   overwrite the frozen build or move its references. A different version/build
   is an owner decision, not supplied by this inventory.
3. Execute mandatory provider source/native/scientific/documentation gates and
   the exact installed pair under the existing release contract. Retain original
   hashes/import origins and inspect genuine failures/skips. The delta map helps
   target regressions; it does not reduce the mandatory matrix.
4. Reconcile the actual Viewer canvas/session/edit workflows and its own
   regressions using those installed identities, separately from provider source
   tests and clean-install smoke. The accepted experimental scientific profiles
   do not become stable through packaging or visual acceptance.
5. Close #250/#254 only at their final-candidate acceptance conditions and #334
   only with the required final evidence/sign-off. Public publication and
   archival actions remain subject to separate authorization.

The read-only board review finds only #250/#254/#334 in the provider's 1.0
milestone; bugs #144/#368 and new proposals #366/#369/#375 remain explicitly
post-1.0. No new current-profile defect was demonstrated in this review.
Source-count provenance: 2026-10-10, Linux, Python 3.14.7; the snapshot records
the Git version and UTC timestamp. No replacement tests, heavy matrix, browser
run, package construction/upload or scientific comparison executes here.
Local developer-guide validation, generated-index verification and the dependency
contract audit pass. These administrative checks validate the planning record
and declared routes; they do not qualify a replacement package.

## What

Freeze feature scope at `d609187ae17af089ef976116252e5a64b6331210` and complete a finite stabilization queue. The normative [scope decision](../release_1_0_scope.md) owns the admission rule, included profiles, six exit packages and full issue classification. This record tracks its execution; it does not duplicate that inventory.

## How

Review the current public contracts and board, separate correctness/qualification from extensions, retain current experimental profiles, and place unimplemented editing/storage/scientific extensions in #335–#338. Use the existing `1.0.0` milestone for remaining release reviews and a dedicated `Post-1.0` milestone for extensions and accepted debt. Update the roadmap, execution plan and ledger to route future work to this boundary.

## Why

The recent #304 reader checkpoint delivers explicit engine selection and inspectable evidence but still has chemical/performance extensions. Continuing all of them before publication would keep moving the endpoint. The same distinction applies to already implemented interaction replacement/compaction versus arbitrary editors and streaming.

## What is inspected and what remains unknown

The 2026-10-05 board query returned 75 open issues:

```bash
gh issue list --repo uibcdf/molsysmt --state open --limit 200 \
    --json number,title,body,labels,milestone,url
```

The initial scope review inspected their requests, current active queues, native/H5MSM/interaction public code, existing qualification records and the release gate. It did not reproduce #25/#30/#112, execute a new full suite, certify published dependency closure or obtain new Viewer canvas feedback. S1 is now qualified as recorded below; the other unknowns remain explicit queue items. Historical receipts and the prior weighted 99% figure are not current release certification.

The resulting board classification was read back and checked against the entire
snapshot: 15 issues in `1.0.0` (the 14 review/qualification owners plus this
tracking issue), and 65 in `Post-1.0` (61 original issues plus four extensions).
No issue was closed. Existing lifecycle-label drift in #215/#250/#252/#254/#271
was corrected to their actual partial reports; #286's existing area metadata
was synchronized, including its missing `coverage` label. Milestone scheduling
does not replace those lifecycle states or turn the reviews into proven defects.

## What was refuted

Closing every open issue is not the release criterion: most are additional capabilities, older delivered requests awaiting reconciliation, or explicit accepted debt. Conversely, labelling a current-profile correctness failure experimental is not sufficient to defer it. Installed-source parity or an old green campaign cannot qualify a different candidate.

## Scope and exclusions

This accepts the local scope rule and tracking changes, without changing runtime methods, signatures, scientific tolerances, dependencies, format versions or platform obligations. Other client integrations remain outside the initial required Viewer integration. No tag, package upload or GitHub Release is authorized by this record.

## Acceptance criteria

- The normative scope owns a finite stabilization queue and an exhaustive classification of the inspected open issues.
- Previously discussed deferred work has an owning issue; no issue is closed solely for deferral.
- Board milestones, proposal cross-links, roadmap, plan and ledger agree.
- S1–S5 reach their documented exit conditions; S6 follows the unchanged exact-candidate publication/sign-off policy.
- Close this operational tracking issue only with the final candidate/evidence and normative scope/release references. Creating this document alone does not close qualification.

## Dependencies and risks

Provider lifecycle and result qualification remain #250/#251/#252/#254; Python/dependency review remains #237/#244/#245. Viewer-owned feedback and product gates stay in uibcdf/molsysviewer#114/#112. Do not create a second scientific or release-gate checklist.

## Provenance

2026-10-05; read-only GitHub board and source inspection at `d609187ae`. Repository-facing changes in this checkpoint are documentation and issue tracking only.

## Documentation and board checkpoint

`validate_devguide.py`, `devguide_index.py --check`, the 263-symbol API registry
check and `git diff --check` pass. The read-only `devguide_issue.py sync --check`
also confirms that the open board agrees with the queues after label alignment.
No runtime code or notebook executable cell changed; no new scientific/full
suite was run or release gate declared complete.

## S1 checkpoint

The [execution ledger](../release_1_0_status.md) records the complete S1 triage:
#30's supported conversion now reuses native inference, #112's existing absence
behavior has an additional public guard, and #25's external-enrichment remainder
is a post-1.0 proposal. The scoped Python 3.14 selection passes 819 tests and
converter doctests; this is not the full release suite. The source fix, user
documentation and unchanged executable notebook cells are recorded in the
owning reports rather than a second acceptance list.

The previous head's devguide and policy runs did not acquire hosted runners;
they failed without executing steps. Applicable hosted evidence is still
required at the next checkpoint. Sphinx builds in the existing 3.13 documentation
environment; completing 3.14 documentation tooling remains #237. Continue
with S2, retaining S3–S6 and final publication approval.

## S3 current-profile checkpoint — 2026-10-05

The [execution ledger](../release_1_0_status.md#s3-preparationform-qualification--2026-10-05)
records the bounded profile review at `fe0b813d7267f4c5a0728264094441e62c910e1b`.
The preparation/form selection passes 1,094 cases without skips; the separate
native pipeline, reinsertion, public mechanics-exclusion and doctest selection
passes 80 without skips. Source, fixture and environment identities are retained
in the [artifact](../../devtools/data/preparation_profiles_20261005.json).

The native SDF/PDBQT, mapped template/context, fixed-state H, named parameter,
torsion and bounded inference contracts retain their conservative exclusions.
No current-profile runtime defect is reproduced. Stale conversion/preparation
claims and the PDBQT recipe are corrected against existing guards. Native history
persists with original axes; H5MSM rejects nonempty mechanics. The wider parser,
chemical and geometry/performance work remains in #214/#215/#304 and the scoped
post-1.0 owners. Their partial issues are not closed by this review.

S3 local stabilization is complete; S4 claims, S5 environment/dependency review,
updated Viewer feedback and S6 exact-artifact gates remain. The scientific run's
single NumPy size-change warning and Python 3.14 documentation qualification are
explicit S5/#237 follow-ups. Source tests and an incremental Python 3.13 HTML
build do not certify the installed release matrix.
