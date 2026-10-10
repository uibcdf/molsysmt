# MolSysMT Repository Agents Guide

This document defines global rules for automated agents and human contributors working on the MolSysMT repository.
More specific `AGENTS.md` files in subdirectories refine or override these rules within their scope.

Read `MOLSYSSUITE_GUIDE.md` before development. It is the synchronized, read-only
suite-governance guide owned by `uibcdf/molsyssuite` and routes shared policies,
cross-component feedback, and issue ownership.

## Scope

- This file applies to every file in the repository unless a more specific `AGENTS.md` in a subdirectory states otherwise.
- When rules conflict, the more local `AGENTS.md` wins; this root file remains the global baseline.

## Language and documentation

- All repository-facing text must be written in English: code comments, docstrings, error/warning messages, READMEs, guides, developer notes, notebooks, and all `AGENTS.md` files.
- User-facing conversations (issues, PR reviews, interactive assistant replies) may follow the user’s preferred language, but anything committed to the repo stays in English.
- Follow the documentation conventions in `devguide/`, `coding/coding_guide.md`, and the documentation-specific AGENTS under `docs/`.
- For web documentation (User Guide, Showcase, Cookbook, developer docs), use MyST and cross-linking patterns described in `docs/content/developer/documentation/web/` (notably `references.md`).
- **Lifecycle Integrity:** Any change or addition to the public API is considered incomplete until: (1) Docstrings are updated and pass doctests, (2) the **User Guide** (Foundations, Toolbox, and Cookbook) reflects the new behavior, and (3) the corresponding modules of **'The Four Paths of the MolSysMT's Master'** course are verified and updated. Documentation is treated as code; it must be accurate and functional.

## Public vs private API

- Public functions and methods (imported in package `__init__` modules or intended for users) should use the `@arg_digest` decorator from `molsysmt._private.argdigest` for argument validation.
- Private helpers, especially anything under `molsysmt/_private`, must **not** use `@arg_digest`. Keep them small, focused, and internal.
- Do not expose `_private` modules in public APIs.
- When adding new public functions, ensure they follow existing naming, argument, and return-value conventions in adjacent modules.

## Docstrings and style

- Use NumPy-style docstrings (see `coding/coding_guide.md` and `docs/content/developer/documentation/api/docstrings.md`) with a gerund one-line summary.
- Standard order: summary; optional extended description; Parameters; Returns (single section); Raises; Notes; See Also; Examples (doctest `>>>`); tutorial admonition; `.. versionadded::`.
- Types in lowercase; defaults in the description; reuse standard wording for `molecular_system`, `selection`, `structure_indices`, `syntax`, `skip_digestion`, `to_form`; document units (nm, ps, radians, elementary charge) where applicable.
- Examples must be minimal and deterministic, using bundled systems; avoid duplicating heavy test logic.
- Keep comments/docstrings meaningful; avoid restating obvious code behavior.

## Data conventions

- Use **structures** for MolSysMT's general coordinate axis in public API text and
  documentation. Reserve **frames** for molecular-dynamics-specific context or
  external APIs that explicitly use that term; structures also cover ensembles
  and independent conformations.
- Use **groups** for MolSysMT's general grouping element in code, public API text
  and documentation. A group can be an amino-acid residue, a nucleotide, a water
  molecule, an ion, a lipid or a small molecule. Do not use **residues** as a
  generic synonym for groups. Reserve residue terminology for an explicitly
  biological residue context or an external API/file format that uses that term.
- Use `structure_index` / `structure_indices` and `group_index` / `group_indices`
  for the corresponding MolSysMT axes. Indices are positions; IDs are labels.
  Preserve existing public identifiers and external field names rather than
  renaming them implicitly when applying these terminology rules.
- Coordinates: NumPy arrays with shape `(n_structures, n_atoms, 3)`, including iterator chunks; units: nanometers.
- Box: NumPy arrays with shape `(n_structures, 3, 3)`; lengths in nanometers, angles handled in radians when derived.
- Time: arrays in picoseconds.
- Charges: expressed in units of the elementary charge.
- Respect the invariants described in `dev_guide.md` for `Get`, `Iterator`, `Form`, and `Native` behavior.

## Dependency Management
- **Hard vs Soft Dependencies:** MolSysMT distinguishes between essential libraries (Hard) and optional feature-enabling ones (Soft). This status is centrally managed in `molsysmt/_depdigest.py`.
- **Lazy Imports:** Never import a soft dependency (e.g., `mdtraj`, `openmm`, `MDAnalysis`, `parmed`, `pytraj`, `nglview`, `pdbfixer`, `biopython`, `plotly`) at the module's top level. Always perform imports inside functions or methods.
- **Enforcement:** Use the `@dep_digest(library, when=None)` decorator from the `depdigest` package (configured by `molsysmt/_depdigest.py`) to enforce dependency availability and provide metadata for introspection.
- **Validation:** Run `devtools/scripts/validate_dependencies.py` to ensure no top-level imports of soft dependencies leak into the codebase. Exempt zones (tests, dev tools) are defined in the script and documented in `SPEC_DEPENDENCIES.md`.
- **Runtime-contract audit:** Treat `pyproject.toml` as the authority for public dependency floors. Run `python devtools/scripts/audit_dependency_contract.py` after changing dependencies or CI source pins; it checks the Conda recipes, runtime-bearing environments, and controlled-source routes without rewriting them. Follow `devguide/dependency_contract_audit.md` for ownership and release checks.

## Forms and conversions

- Form adapters live under `molsysmt/form`; see `molsysmt/form/AGENTS.md` for detailed guidance.
- Discovery and registration are lazy and dynamic. They rely on the central mapping in `molsysmt/_depdigest.py` (specifically `MAPPING`). Do not add dependency-related variables to the form's local `__init__.py`.
- Each form module should declare `form_name`, `form_type`, `form_info`, and populate `_convert_to` with callables.
- Respect `msm.configure.show_all_capabilities` which allows users to filter available forms based on their installed environment.


## Modular tool design

- Before adding a feature, inspect existing general tools and identify the
  owning module or MolSysSuite provider for each required capability.
- When an operation has meaningful standalone use or serves other workflows,
  implement or extend it as a documented general-purpose tool in that owner,
  with its own contract and tests. Have the new feature call that tool.
  Keep feature-specific scientific criteria and orchestration in the consumer.
- Chemical-property interpretation belongs in `physchem`, connectivity tools
  in `topology`, geometric operations in `structure`, and periodic reconstruction
  and image conventions in `pbc`. Stored chemical assignments remain owned by
  `ChemicalStates`; reusable tools must not create competing chemical stores.
- Hydrogen-bond-specific site definitions, local directional models and occurrence
  detection belong together in `interactions.hbonds`. Recognition and directions
  remain independent public tools: neither requires previously calculated hydrogen
  bonds. They reuse general chemistry, connectivity, geometry and periodic tools
  from their owning modules. Reusability alone does not determine module ownership.
- Report missing sibling capabilities to the provider and link the consumer
  requirement. Preserve dependency direction and lazy optional dependencies.
  Temporary duplication requires a tracked reason and removal condition.
- Reuse existing compiled primitives. Further heavy routines may use the
  bundled Rust backend when workload measurements justify them; preserve
  scientific behavior and explicit public validation, units, and provenance.
- Internal helpers can remain private behind a supported general tool. Export
  operations with meaningful user contracts rather than every implementation
  detail. Do not create placeholder APIs or speculative utility packages.

This is an accepted local maintainer instruction. Its suite-wide policy and
adoption are tracked by `uibcdf/molsyssuite#61`; the central rollout is pending.

## Performance Architecture

- **Validated Boundaries**: Normalize user input once at a clear public boundary. A
  controlled internal delegation may use `skip_digestion=True` only when every argument
  already satisfies the callee's contract; MolSysMT has no value-passport protocol.
- **Fast-Track Units**: Register canonical units (nm, ps, Da, K) in `puw.fast_track` within `molsysmt/_pyunitwizard.py` to enable instant unit bypass.
- **Chunked Execution**: Large trajectories must be processed via the `ChunkedExecutor` (see `devguide/SCALABILITY.md`).

## Testing and validation

- Use `pytest` for tests; follow the structure and conventions documented in `tests/AGENTS.md`.
- Place tests in the mirrored path under `tests/` corresponding to the package area you change.
- Keep tests deterministic and reasonably fast; rely on bundled systems in `molsysmt.systems` and small fixtures when possible.
- When changing behavior, update or add tests to capture the intended semantics instead of weakening existing expectations.
- **A gate must check intent, not form.** A validator, test or lint must be satisfiable
  only by the property it exists to protect, never by output shaped to match it.
  `validate_form_adapters.py` is the model: a declared attribute fails unless a real
  delivery route exists. `validate_docstrings.py` was the counterexample: it checked that
  every parameter appears with a matching default, and one generated sweep supplied 8,810
  descriptions that restate the parameter name and passed
  (see [`devguide/archive/resolved_bugs/validators_that_check_form_instead_of_intent_admit_conforming_emptiness.md`](devguide/archive/resolved_bugs/validators_that_check_form_instead_of_intent_admit_conforming_emptiness.md)).
  This rule matters more, not less, as contributions are machine-generated: generation
  scales exactly to the criterion and not one step past it. Review every new gate against
  the question *what conforming output would satisfy this without doing the work?*

## Reporting a defect or a proposal

**Read [`devguide/reporting_protocol.md`](devguide/reporting_protocol.md) before filing
or closing anything.** It is normative and enforced by `validate_devguide.py` in the
release gate. The short version:

- If it deserves a document in `devguide/`, it deserves a GitHub issue. One theme, one
  issue, one or more documents. We do not file documents for typos, so the document is
  already the significance filter.
- Open the issue first to get its number, then write the document from
  [`devguide/templates/report.md`](devguide/templates/report.md) with `issue:` filled
  in. `python devtools/scripts/devguide_issue.py open` does both.
- The document holds the analysis and changes continuously. The issue holds state and
  the settled facts an outside reader needs, and is written at two moments only — at
  open and at close. Never put analysis in an issue.
- Closing requires naming either the test that fails if the defect returns (`guard`) or
  the normative document that absorbed the durable rules (`normative`). The validator
  checks that the file exists.
- Cross-repository references use `uibcdf/<repo>#<number>`, never a path into another
  repository's `devguide/`. A path breaks silently; an issue closes.
- Queue indexes are generated: `python devtools/scripts/devguide_index.py`. Edit the
  entries, never the list.

## Git commits

- Never add a `Co-Authored-By` trailer to commit messages. Commit messages must contain only the subject line and, when necessary, a body — no attribution footers of any kind.
- Direct pushes by the internal maintainers may use `[skip ci]` when rapid
  iteration warrants deferring tests. Omit it by default so the short smoke
  suite runs. Every skipped commit remains in the nightly full-suite backlog
  until a complete Linux matrix passes. Do not use `[skip ci]` on a pull
  request. Release candidates require all mandatory exact-candidate gates
  executed and verified, including through the authorized manual route when
  recovering an original producer and recorded artifact. A marker alone is not
  a gate waiver or a reason to reject complete exact-candidate evidence.

## Releases, citation, and Zenodo

- Read [`devguide/release_and_citation.md`](devguide/release_and_citation.md) before
  preparing a release or changing `CITATION.cff`, `.zenodo.json`, DOI badges, or
  citation text.
- `CITATION.cff` is the canonical user- and GitHub-facing citation record.
  `.zenodo.json`, when present, controls Zenodo ingestion and must agree with the
  shared title, creators, ORCIDs, and license.
- Public project-level surfaces use the stable MolSysMT concept DOI
  `10.5281/zenodo.1298752`. Never freeze a historical version DOI into a badge or
  governance rule. Exact-version DOI records are verified after GitHub publishes the
  release.
- A Git tag alone is not a Zenodo release. Publish a GitHub Release only after every
  exact-commit gate passes; the enabled Zenodo/GitHub integration archives that release.
- Run `python devtools/scripts/validate_citation.py` after citation changes. Use
  `python devtools/scripts/prepare_release.py <version>` to update release-specific
  citation fields instead of editing derived citation surfaces independently.

## Safety and tooling

- Prefer minimal, focused changes that respect the existing architecture and style.
- Do not run or document destructive git commands (such as `git reset --hard` or `git push --force`) in automated workflows.
- Avoid adding new external dependencies without considering their impact; reuse existing libraries and utilities already in the project when possible.
- Automated agents must respect sandboxing and should avoid network access unless explicitly required and permitted by the execution environment.
- In native MolSysMT objects (for example, `molsysmt.Topology` and `molsysmt.MolSys`), element IDs (`*_id` fields) are stored as strings; normalize incoming numeric IDs to strings and keep this invariant in converters, rebuilders, and tests.
- Verify style and syntax safety using applicable Ruff checks before committing
  or pushing executable/code changes (for example, `ruff check molsysmt`).
  For prose-only changes, select the relevant documentation/governance checks.

For more specialized guidance, consult the AGENTS files in `ai_assistant/`, `devguide/`, `docs/`, `coding/`, `molsysmt/form/`, and `tests/`.

## External Tooling Guides (Required for Development)

These guides are required reading for anyone developing this library. They describe how external tools must be used here.

- `SMONITOR_GUIDE.md` — Required guide for SMonitor integration and diagnostics.
- `ARGDIGEST_GUIDE.md` — Required guide for argument validation and explicit trusted delegation.
- `PYUNITWIZARD_GUIDE.md` — Required guide for unit management and Fast-Track conversion registration.
- `DEPDIGEST_GUIDE.md` — Required guide for dependency management and lazy loading.
- `ACKREDIT_GUIDE.md` — Required guide for optional scientific attribution and citation
  reporting.
- `GH_RUN_RECEPTOR_GUIDE.md` — Required guide for compact, truth-preserving inspection of
  GitHub Actions runs and the native-command fallback.
- `PYTEST_RECEPTOR_GUIDE.md` — Required guide for compact, truth-preserving pytest output
  in local and hosted development.

## Direct pushes and scoped local validation

Follow [the common checkpoint policy](MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints)
for authorized internal direct pushes by `dprada` and `LMMV`. Batch focused local
commits when remote visibility is unnecessary; a permitted interim CI skip is
conditional, never the default after every locally checked change. Retain local
results while tested code, inputs, environment and scope remain applicable.
Normally finish with an unskipped head and inspect its applicable CI, or explicitly
execute and verify those exact-head gates manually. Record missing evidence,
untested scope, owning issue and recovery route; administrative checks do not
clear full-suite backlog. External PRs, admission and publication require all
mandatory executed gates for the exact candidate and required installed file.
An authorized manual qualification retains the original producer and artifact
bytes/digest; a marker alone neither waives a gate nor disqualifies that evidence.

## Modular reusable tools

Before adding a feature, inspect existing tools and identify the owning module or
component. Implement or extend independently useful operations as documented reusable
tools in that owner, with their own contracts and tests; have consumers call them.
Keep task-specific decisions local and report missing sibling capabilities to the
provider with linked consumer evidence. Follow
[MOLSYSSUITE_GUIDE.md#modular-reusable-tools](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
for applicability, compatibility, performance and tracked exceptions.

## Durable working instructions

Keep technical findings in owning issues, fixes, tests and maintained guidance.
Place only accepted lasting contributor actions in root or appropriately scoped
instructions, following
[the common policy](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read [devguide/AGENTS.md](devguide/AGENTS.md)
and its local reporting protocol. Shared instruction proposals belong in
`uibcdf/molsyssuite`; cross-MOLI contracts belong in `uibcdf/moli`.

## Human-facing issue feedback

Surface actionable suspected defects, inconsistencies, missing analyses and
improvements, including uncertain or nonblocking findings. When working with a
human, offer an owning issue at a natural pause; retain existing reporting
authorization and respect declined/deferred disclosure. Follow
[the accepted feedback route](MOLSYSSUITE_GUIDE.md#human-facing-issue-feedback)
for ownership, uncertainty, privacy and exceptions.
