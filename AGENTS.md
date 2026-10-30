# MolSysMT Repository Agents Guide

## Mandatory MolSysSuite instructions

Read and follow `MOLSYSSUITE_GUIDE.md` before working in this repository.

Within their stated scope, its common rules take precedence over this file
and any nested `AGENTS.md`. Local instructions may refine them; deviations
require the documented policy exception process.

The synchronized guide is owned by `uibcdf/molsyssuite`. It includes the
[reusable-tool ownership rules](MOLSYSSUITE_GUIDE.md#modular-reusable-tools)
and [working-instruction rules](MOLSYSSUITE_GUIDE.md#durable-working-instructions).
For work under `devguide/`, also read `devguide/AGENTS.md` and its local
reporting protocol. Keep repository-specific instructions below.

## Local working context

This document defines MolSysMT-specific working rules for agents and human contributors.
More specific `AGENTS.md` files in subdirectories refine or override these rules within their scope.

## Scope

- This file applies to every file in the repository unless a more specific `AGENTS.md` in a subdirectory states otherwise.
- Among local rules, the more specific `AGENTS.md` refines the root; the
  mandatory MolSysSuite layer remains above both within its stated scope.

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
- Chemical-property interpretation belongs in `physchem`, state-dependent
  connectivity tools in `chemical_states`, stable inventory and sequence tools
  in `topology`, geometric operations in `structure`, and periodic reconstruction
  and image conventions in `pbc`. Stored chemical assignments remain owned by
  `ChemicalStates`; reusable tools must not create competing chemical stores.
- Hydrogen-bond-specific site definitions, local directional models and occurrence
  detection belong together in `interactions.hbonds`. Recognition and directions
  remain independent public tools: neither requires previously calculated hydrogen
  bonds. They reuse general chemistry, connectivity, geometry and periodic tools
  from their owning modules. Reusability alone does not determine module ownership.
- `Topology` owns stable atoms, groups, molecules, entities and chains; it has no
  bond/component/state facade, including while attached to `MolSys`. `ChemicalStates`
  owns stored bonds, assignments and state-local components. Supply stable context
  explicitly when chemical reconstruction needs it. Stable molecule membership is
  declared once during construction and does not follow later connectivity edits.
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

## Local reporting tools

Read `devguide/reporting_protocol.md` and `devguide/AGENTS.md` for the local
report paths and metadata. `python devtools/scripts/devguide_issue.py open`
scaffolds an owning issue and report; use its documented close/sync routes.
Run `python devtools/scripts/validate_devguide.py` and
`python devtools/scripts/devguide_index.py --check` after lifecycle changes.
The release gate retains the offline validator; board synchronization is separate.

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
