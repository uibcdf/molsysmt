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

The Linux Python 3.14 development environment now uses official
conda-forge PySide6/Qt 6.11.2 rather than the local UIBCDF Qt family
(`uibcdf/molsyssuite#52`). This is a development baseline, not a final
1.0 Qt release gate. Viewer will reassess the newest compatible
conda-forge family during pre-1.0 dogfooding
(`uibcdf/molsysviewer#112`); the version may remain 6.11.2 if a newer
family does not pass.

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

The priorities below are continuing quality themes, not a second 1.0 gate
list. The execution ledger is authoritative for what remains before 1.0.

## Completed foundations

- Form support tiers and the machine-readable public API stability registry
  now define the claimed contract; see [the support-tier protocol](support_tier_protocol.md)
  and [public API surface](api_surface.md).
- The Rust extension is packaged and the transitional Numba CPU/CUDA runtime
  has been removed; see [the 1.0 execution ledger](release_1_0_status.md).

## Priority 0: scientific integrity

- propagate scientific failures instead of returning partial heavy results;
- correct attribute declarations that cannot be delivered;
- remove silent broad-exception fallbacks from high-risk paths;
- establish independent scientific reference tests for builders and analyses.

## Priority 1: support and API truth

- validate public attribute delivery and conversion fidelity;
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

### Current SDF/PDBQT and chemical-preparation sequence — 2026-10-03

The maintainer requested real-input validation and chemical preparation as the
next connected work. Native SDF/PDBQT serialization is implemented within a
bounded experimental profile; general chemical preparation is still pending.
This ordering brings bounded preparation work into current development without
making every chemical-state horizon a new 1.0 release gate. Keep the execution
ledger authoritative for release scope.

1. **Validate prepared real inputs and agree the consumer profile.** Extend
   [PDBQT #214](pending_proposals/add_pdbqt_file_and_string_forms_with_molsys_conversion.md)
   and [SDF #215](pending_proposals/add_sdf_file_form_with_molsys_conversion.md)
   using pinned 1IEP, 1S63 and both 5X72 stereoisomers already curated by
   DockingMT, plus a real rigid receptor. Track checksums, source atom indices
   separately from serial IDs, geometry units/precision, supported stereo,
   charges/types, branch bonds and fragment memberships. Classify each actual
   encoding as supported, explicitly unsupported or defective. Consumer
   integration and profile feedback are requested in uibcdf/dockingmt#33;
   uibcdf/dockingmt#17 owns differing torsion policies. Existing published
   preparations are comparison inputs, not chemical ground truth.
   The first provider corpus is now committed in
   `tests/form/data/vina_examples`; dated execution evidence and remaining
   admission limits are in the two linked reports. PDBQT parser fidelity and
   explicit-fragment projection have bounded reference coverage. Native SDF
   still rejects 1IEP's valence override and 1S63's missing version marker;
   exact source copies preserve both unchanged. Consumer acceptance and
   chemical preparation remain separate pending work.
2. **Assess chemical readiness and coverage before transformations.**
   [Ligand readiness #217](archive/resolved_proposals/diagnose_ligand_chemical_readiness_for_a_selected_molecular_state.md)
   and [receptor coverage #218](archive/resolved_proposals/report_receptor_residue_chemistry_and_preparation_coverage.md)
   must distinguish declared, inferred, missing, conflicting and unassessed
   information. A successful conversion, an empty missing-atom list or the
   presence of hydrogens is insufficient. Start with one explicitly selected
   state/frame and report unsupported residues/cofactors. Inspect existing
   public predicates and reports before choosing or extending a public boundary.
   The experimental `physchem.get_chemical_readiness` now reports stored field
   coverage, declared edge evidence and limited conflicts without repair or a
   universal ready flag. The experimental `build.get_residue_chemical_coverage`
   now adds exact residue-template inventories and stored-graph comparisons,
   retaining unsupported groups and unresolved H/protonation dimensions. Scientific
   valence/protonation validation is not established by either assessment.
3. **Complete selected chemistry and missing H through reusable tools.**
   uibcdf/molsysmt#298 owns explicit template assessment/application with
   caller-declared atom correspondence; [Fixed-state hydrogen addition #300](archive/resolved_proposals/add_ligand_hydrogens_for_a_fixed_chemical_state.md)
   delivers the initial RDKit ligand placement route. Experimental template tools now
   provide the bounded same-graph, absent-field-only contract, copy semantics and
   a detached provenance report. Unsupported representation normalization,
   native report attachment and real consumer acceptance remain open under #298.
   Complete prepared inputs may
   bypass template application. Preserve existing atom identity and coordinates,
   reject conflicting assignments and retain preparation provenance. Template
   application cannot add absent atoms; local H placement cannot select a
   protomer or establish an energy-minimized orientation. Review native-domain
   reconstruction and metadata contracts before extending hydrogen placement.
   The experimental fixed-state RDKit route now reuses public hydrogen-inventory
   and terminal-attachment tools, preserving old indices/coordinates and checking
   declared chemistry/stereo. It rejects unsupported source scope, invalidates
   interactions only on the expanded output, and returns detached provenance.
   Local geometry is not an optimized receptor orientation; consumer acceptance
   and a [future native ligand engine #308](pending_proposals/add_a_native_general_ligand_hydrogen_engine_for_fixed_chemical_states.md)
   remain separate evidence. #308 does not block continuing with the explicit
   RDKit route.
4. **Assign charges and chemical AutoDock types explicitly.**
   [Named charges #221](archive/resolved_proposals/assign_partial_charges_with_an_explicit_named_model.md)
   are implemented with detached Gasteiger-Marsili and matched-force-field routes,
   original provenance, native projection and stale-binding checks. Mechanical
   persistence remains outside H5MSM 0.5.
   [AutoDock typing #222](pending_proposals/assign_and_validate_autodock_atom_types_under_a_named_scheme.md)
   still needs methods, original software versions, state association, coverage and
   independent chemical controls. Resolve their inspectable assignment/provenance
   contract without introducing competing stores. Chemical interpretation belongs
   in `physchem`; reconstruction belongs in `build`; chemical assignments remain
   in `ChemicalStates` and current mechanical values in `MolecularMechanics`.
   Test conventional receptors separately from small molecules. Charge-model
   fidelity is not proven by agreement with one prepared file; missing values
   must not become zeros. Label decoding is not chemical type assignment.
5. **Project a prepared state under an agreed docking profile.**
   [Atom projection #223](pending_proposals/preserve_atom_correspondence_through_lossy_molecular_exports.md)
   owns retained/omitted/merged/added atom correspondence and charge accounting;
   [torsions #224](pending_proposals/classify_rotatable_bonds_and_derive_rigid_molecular_fragments.md)
   owns general chemical eligibility and fragment output. Keep the current
   all-H-preserving writer distinct from a future nonpolar-H merging profile.
   Choose eligibility rules explicitly, explain exclusions and preserve source
   bond indices. Reuse the delivered explicit-cut fragment tool. DockingMT owns
   active torsion selection and ROOT policy. Serialization consumes prepared
   data and must not quietly perform any preceding step.
6. **Accept the composed workflow on real receptor/ligand cases.** Compare
   chemistry/coverage, atom maps, charge conservation, stereo, exact retention
   of existing coordinates, failure immutability and non-default session units;
   separately test Vina parser acceptance and downstream pose correspondence.
   Include 1S63's reference-only H and aryl–nitrile torsion, the 5X72 stereo
   pair, and ester/amide/ring controls. Remove consumer-side temporary molecular
   operations only after the shared tools pass equivalent contracts. Keep
   docstrings, User Guide and course material aligned with each delivered slice.

Preparation is a shared need: uibcdf/pharmacophoremt#22 motivates the explicit
template/H contracts, and uibcdf/dockingmt#4/#5/#6 motivate state, parameter and
torsion use. Preserve other components' concurrent work while coordinating
these owned issues. Do not require all enumeration (#220/#229/#230), new
heavy-atom conformers (#219), environmental pKa (#177), flexible receptors
(#225), pose ensembles (#226) or H5MSM mechanics persistence (#256) to accept
the first supported fixed-state workflow. Record any real dependency discovered
during implementation in its owning issue. H5MSM 0.5 continues to exclude
MolecularMechanics; this plan does not promise persistence of charge/type data
there.

Completed proposals should be moved to an archive or replaced by a concise
decision record. A checked box or dated prose is not completion evidence without
code, tests, and documentation.
