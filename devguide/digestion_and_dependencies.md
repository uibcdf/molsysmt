# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- All public functions must validate inputs with `@arg_digest`.
- The ArgDigest configuration lives in `molsysmt/_argdigest.py`.
- Place `@dep_digest` **below** `@arg_digest` so it works on normalized args.
- For quantity strings, digesters must parse with `puw.parse.parse(...)`
  (not `puw.parse(...)`), following the current PyUnitWizard API layout.

### Universal Digestion
As of the 1.0.0 stabilization, *every* function in *every* form module (including internal delegates like `get`, `set`, and `extract` inside `__init__.py`) must be decorated with `@arg_digest`. This ensures that data normalization happens even in deep conversion chains.

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `scripts/validate_dependencies.py`.

### 🚀 High-Performance Lazy Loading (Sprint Decision)
To ensure near-instantaneous `import molsysmt` in all environments (HPC, Cloud, Notebooks), we have implemented a **String-Based Lazy Registry**:

1. **`_convert_to` dictionaries**: In every form's `__init__.py`, the values in the `_convert_to` dictionary must be **strings** representing the function name (e.g., `'to_molsysmt_MolSys'`), not the function objects themselves.
2. **Dynamic Resolution**: `molsysmt.basic.convert` uses `importlib` to resolve these strings only when the specific conversion path is triggered.
3. **Outcome**: This architectural pattern prevents Python from parsing and loading submodule code for soft dependencies (like OpenMM or MDTraj) unless they are actually used.

## Single Source of Truth
Dependency status and form mapping live in `molsysmt/_depdigest.py`.

Key configuration fields:
- `LIBRARIES` (hard vs soft)
- `MAPPING` (form directory → library)
- `SHOW_ALL_CAPABILITIES`
- `EXCEPTION_CLASS`

## Maintenance
When moving a dependency from hard → soft:
1) Move imports inside functions.
2) Add `@dep_digest`.
3) Update `_depdigest.py`.
4) Ensure form mapping exists.
5) Ensure `_convert_to` uses strings.
