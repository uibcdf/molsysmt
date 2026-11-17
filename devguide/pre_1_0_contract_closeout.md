# Finite contract closeout before the 1.0 documentation review

**Role:** operational receiving packet under uibcdf/molsysmt#334, #256, #250,
#254, #421 and #524. **Reviewed:** 2026-11-17.
**State:** provider source offer; final consumer/candidate acceptance pending.

This packet collects the already required decisions. It adds no detector,
format revision, client workflow, performance promise or release gate.
[The handoff plan](technical_handoff_for_1_0_documentation_review.md) owns the
destination; [the live ledger](release_1_0_status.md) owns progress. Normative
API and schema documents linked below own behavior. This checklist does not
replace their rules or promote Experimental APIs to Stable.

## Source continuity and evidence

The reviewed provider reference is `ea9d4ef16`. Relative to
`96988b6ea42fb02a662fa3dda5eb2f7659f28c56`, received by MolSysViewer profile
897, the only production-source changes are the two mmCIF reader files in
`b8c798474`. Interactions, ChemicalStates, H5MSM and the bound addon retain
identical implementation bytes. This is a Git-tree comparison, not new runtime
or installed compatibility evidence. The mmCIF correction has its own original-
file guards and client profile 949 (114 passing cases). Its immutable public
report is received and Git-blob verified; private raw JUnit/input manifests
are not replayed. The later public receipt
5f6fc2a5 receives 952's two complete-file msv.new_view loads: 53,592 atoms /
51,770 canonical bonds for 3WU2 and 98,986 atoms / 102,708 bonds for 5XNL.
Both original input digests match the owner manifest. These are reported
headless data-integration outcomes, not rendered or installed qualification;
private raw JUnit and custody files are not replayed here.

The [contract receipt](../devtools/data/pre_1_0_contract_closeout_334_20261115.json)
records that comparison, current scoped smoke/quality checks and exact source
identities. The earlier [client source review](../devtools/data/viewer_current_source_client_review_256_524_20261115.json)
retains the independently inspected public guards, reported execution and its
limits. Earlier full-source, browser, installed and scientific results keep
their original source/runtime identities. No full matrix is repeated here.

The current public smoke selection passes **19 cases without skips**: all
12 prescribed original-packet policy/route combinations plus public named-
analysis round trips, source-map preservation, explicit state association,
bounded paging and real controlled geometry/chemistry invalidation. This is
provider execution, not BindingMT's independent acceptance or final-pair
qualification. It requires no preparation/docking, new engine, environment
installation or native rebuild. The one-CPU/two-GiB process family peaks at
about 223 MiB and retires; source inputs remain unchanged.

## Current provider guarantees offered for consumer review

| Boundary | Offered behavior and owning contract | Existing receiving route |
| --- | --- | --- |
| Named analyses | A validated name maps to a full Interactions analysis in MolSys.interactions. Computation returns a result; attachment is explicit. A query view is not silently installed as a complete analysis. [Result contract](interactions_api.md#associating-analyses-with-a-system). | tests/native/test_molsys_interactions.py |
| Sparse observations | Typed relations and role-bearing compound participants are separate from occurrences. No dense atom-pair tensor or maximum-count padding is promised. Occurrence indices distinguish parallel observations within one analysis version and survive views/persistence; editing/remapping can create a new version. [Result contract](interactions_api.md). | tests/interactions/test_result.py; tests/interactions/test_public_molsys_h5msm_workflow.py |
| Queries and coverage | Nonconsecutive atom/structure lists and the canonical involving_selection, within_selection, across_selection_boundary and between_selections operations retain their defined semantics. Every constituent participant atom counts. Evaluated-empty differs from unevaluated, within the declared searched universe. [Query contract](interactions_query_semantics.md). | tests/interactions/test_public_molsys_h5msm_workflow.py; tests/interactions/test_query_candidates.py |
| Bounded inspection | to_page bounds occurrence and participant copies after query construction. It does not promise constant-memory whole-trajectory query construction or a complete serialization codec. [Paging contract](interactions_api.md#selected-structure-queries-and-bounded-inspection). | tests/interactions/test_occurrence_pages.py |
| Images and units | Image vectors are integer shifts applied as image_vector @ box with lattice vectors in rows, relative to the first participant for relative geometry. All atoms of a compound participant share its shift; internal ring unwrapping is separate. Missing images are unknown. Geometry and thresholds retain explicit physical units. [Image contract](interactions_api.md). | tests/interactions/test_result.py; tests/interactions/hbonds/test_buch_results.py; tests/interactions/disulfides/test_get_disulfide_candidates.py |
| Evidence and attribution | Original producing software, method/profile, parameters, units, evidence and evaluated scope survive transport. Loading/querying does not claim another scientific calculation. Optional Ackredit attribution and reference implementation are distinct from executed software. [Attribution contract](interactions_api.md#scientific-method-names-and-attribution). | tests/interactions/test_software_provenance.py; tests/interactions/test_execution_provenance.py; tests/interactions/test_scientific_attribution.py |
| Controlled edits | Supported geometry setters invalidate affected structure coverage, including previous empty observations, without automatic detection. Chemical edits follow their documented conservative or state-association scope. Raw-array alias edits require explicit user invalidation. Previous result snapshots are not proof about the edited system. [Lifecycle contract](interactions_api.md). | tests/form/molsysmt_MolSys/test_geometry_edit_interactions.py; tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py |
| Chemical authority | Topology owns stable inventory and chains, with no bond/component facade. ChemicalStates owns state-local chemistry/components. Missing, empty and unknown chemistry are distinct; state resolution cannot guess ambiguous associations. [Migration contract](chemical_states_migration.md). | tests/native/test_chemical_states_owner.py; tests/native/test_molsys_chemical_state_association.py |
| Projection and association | Supported coordinated extraction/permutation remaps present domains. Standalone imports require declared local-axis correspondence; matching sizes/source_id are not authentication. remap is extraction/reordering, not arbitrary embedding in a larger target. [Association contract](interactions_api.md#associating-analyses-with-a-system). | tests/native/test_molsys_interactions.py; tests/form/file_h5msm/test_public_h5msm_v05.py |
| H5MSM persistence | Development defaults are 1.0, with independent optional domains and typed associations. Structures-only and interactions-only files remain representable. A selective read validates the decoded scope; unknown assignment-report content can be transported without certifying export/parameter usability. [Format contract](h5msm_format.md). | tests/form/file_h5msm/test_public_mechanics_v06.py; tests/form/file_h5msm/test_public_migration_v10.py |
| Default migration | Existing original complete/projected/merged 0.6 files use omitted-version public save and whole-file conversion under ordinary and pm/fs policies. Root 1.0, original scientific producers, data/maps/coverage, source hashes and migration history retain their distinct meanings. [Client prescription](pre_1_0_completion_handoffs_20261110.md#finite-default-write-and-migration-receiving). | tests/form/file_h5msm/test_original_packet_default_migration.py |

The source APIs Interactions, ChemicalStates, h5msm and interaction detectors
remain Experimental as classified by
[the authoritative registry](../devtools/data/public_api_stability.json).
A stable file-format decision concerns the represented wire contract; it does
not certify every detector, aromaticity rule, protonation assumption or stored
mechanical model. Scientific classifications remain owned by the maintained
[evidence matrix](scientific_evidence_matrix.md). No stability label changes here.

## Exact returns needed from each owner

BindingMT's finite #73 return is now accepted in the
[owner review](../devtools/data/binding_default_h5msm_acceptance_256_20261115.json).
All twelve omitted-version operations pass on the original packet; the owner
also verifies the 92 published archived members and actual HDF5 data. #256's
source/wire decision is complete in the [format contract](h5msm_format.md#first-stable-schema-decision--2026-11-15).
The remaining returns below concern the final consumer/candidate composition;
do not ask BindingMT to repeat this storage profile.

| Owner / issue | Return required | Work not being requested |
| --- | --- | --- |
| BindingMT #73 / MolSysMT #256 | Received and accepted: immutable 2b761a84, twelve default operations, original data/maps/provenance and hashes. Preserve earlier P5/P6 acceptance and the bounded old-native decision. | No repeat receiving, preparation, minimization, docking, C1/resolve_region, new model, package or new matrix. |
| MolSysViewer / #250, #254, #421 | Confirm these current consumption semantics or name the concrete remaining incompatibility; retain Experimental scientific/API scope. Identify remaining work before selecting the final host source. Existing source evidence need not be rerun just to acknowledge the contract. | No new detector, lazy-file API, broad matrix, candidate build or promotion. Current owner-authorized UI diagnosis remains separate. |
| Both maintainers / #524, #334 | Agree exact clean producer commits, versions, unused builds, artifact coordinates and applicable runtime composition. Review the already prepared compatible minimum-host metadata before freezing. | A future version label is not an already qualified/public compatible package; no floor changes or release authorization by this packet. |
| MolSysMT / #256 | Completed: client return reviewed, no exercised-scope discrepancy found, first-stable 1.0 source/wire contract recorded with admitted schema revisions and explicit limits. | No publication, general scientific/ABI certification or final installed-pair acceptance. |
| Both release owners / #334 | After agreed resumption, qualify the exact same artifacts and sources under existing source/native/scientific/documentation and installed-pair gates, including the retained #671 lane. Then hand off the review packet. | Historical or scoped source passes do not replace final installed/platform qualification. |

## Publication order and completion boundary

### Independent offline preflight — 2026-11-17

The [finite local receipt](../devtools/data/independent_native_work_334_20261116.json)
records the I0–I5 scope and current execution. The original offline preflight
exposed two stale positive dependency fixtures under #771. Corrected controls
now distinguish satisfied direct requirements from a transitive refusal;
159 selected native/documentation, staging identity, runtime closure,
dependency-audit and citation cases pass without skips. This exercises guards
with simulated records; it does not install or qualify a candidate.

The seven-surface metadata draft remains unapplied. Its existing patch digest is
`52b5e5bb7ddc18940c00102ad17d8840a76f121e6f705b7e3e7c3b5e466a3057`.
All seven current inputs match the reviewed basis and the read-only apply check
passes. The reciprocal >=1.0.0 minimum agreement remains a future coordinated
producer change. Preserve the declared ipykernel >=7.4.0 notebook-host baseline;
do not mistake the version in an administrative/headless process for receiving
of a selected graphical kernel. Main runtime floors and citation date are not
changed here. Refresh the provisional date and audit the complete actual root
only when producer preparation resumes.

| Required identity or action | Owner and existing route | Present disposition |
| --- | --- | --- |
| Final clean MolSysMT/MolSysViewer source commits and exact build numbers | Both maintainers under #334/#524 | Target 1.0.0/1.0.0 agreed; producer SHAs, unused builds and triggerable refs still unselected. Historical files/refs are preserved. |
| Coherent dependency/citation metadata and source pins | Both producer owners; `prepare_release.py`, complete-root dependency/citation audit | Draft only. Do not substitute a future package label for the real untagged source version. |
| Four native ABI3 files and MolSysViewer's noarch file, channels, original URLs and SHA-256 | Existing `build_and_upload_conda_packages.yaml` and consumer producer | No new producer dispatch or artifact is authorized by this preflight. Verify original producer and artifact custody. |
| Source/native/scientific/documentation qualification at that exact composition | Existing release gate and source/native workflows | Required final receiving, including #671's original matrix lane; earlier scoped passes retain their original identities. |
| Sixteen installed-pair cells | `validate_conda_staging.yaml`: explicit versions/builds, `python_max=3.14`, `target=all`, staging | Pending exact artifact selection and agreed resumption. Capture actual paths, URLs and hashes outside checkouts. |
| Independent verification of that completed installed run | `verify_installed_conda_pair.yaml`: existing `run_id`, exact `candidate_sha`, title and profile | This route inspects existing evidence; it does not execute the installed matrix. A receipt is not a new run. |
| Current consumer capture gate and final consumer source | MolSysViewer, including reopened #344 | Its remaining work-file capture diagnosis and covering source gates are external. Do not infer a provider scientific defect or a complete pass from earlier successful capture cases. |

The final stop conditions remain those of the owning release/resource rules:
missing identities, wrong bytes/import origins, failed or incomplete gates and
unsafe resource admission cannot become a pass. No extra matrix, new detector,
candidate reservation or publication permission is added by this table.

The already inspected manifests depend on each other: MolSysMT consumes
MolSysViewer and MolSysViewer consumes MolSysMT. Compatible floors and actual
files determine a jointly qualified staging/promotion order. Stage and test the
candidate artifacts before release authorization; verify public solver closure
after authorized promotion when both required counterparts exist. Do not demand
that an unbuilt future pair already be public before testing that pair.

New candidate construction, hosted qualification, tags, promotions and
publication remain paused. The packet selects no producer or build. The target
is unchanged: a technically qualified pair for which only Diego's substantive
documentation review remains. No percentage is added for this preparation.
