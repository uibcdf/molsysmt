# Digestion and Dependencies

## Argument Digestion (`arg_digest`)
- Public functions that accept user-facing values requiring normalization should
  validate them with `@arg_digest`; classes, predicates, compatibility wrappers,
  and thin helpers follow their local contract.
- The ArgDigest configuration lives in `molsysmt/_argdigest.py`.
- Place `@dep_digest` **below** `@arg_digest` so it works on normalized args.
- For quantity strings, digesters must parse with `puw.parse.parse(...)`
  (not `puw.parse(...)`), following the current PyUnitWizard API layout.

Important scope rule:

- `@arg_digest` is the normalization boundary for public and semi-public API
  entrypoints;
- it is not the place to encode all kernel-facing preparation needed by hot
  numerical wrappers;
- when a hot wrapper needs shape normalization or paired-unit alignment before
  entering `molsysmt.lib`, that logic should live next to the kernel layer
  rather than being forced into generic public digestion.

This rule was clarified during the March 2026 performance pass. The motivating
example was structural coordinates:

- public digestion remains responsible for validating external inputs;
- `basic.get()` remains responsible for user-facing retrieval semantics;
- `molsysmt.lib.structure._kernel_inputs` now holds the extra preparation
  required specifically by structure kernels.

### Digestion boundaries

Public functions and adapter entry points use `@arg_digest` when they accept
user-facing values requiring normalization. Small private helpers must remain
focused and should not be decorated merely to satisfy a blanket rule. Trusted
internal calls may use `skip_digestion=True` only after every input has been
normalized at a clear boundary.

### Explicit trusted delegation

MolSysMT has no value-passport protocol. The pre-1.0 `ValidatedPayload`
experiment was removed because it had no live consumer and required an extra
certification model for every participating digester. No replacement wrapper
or token was introduced.

`skip_digestion=True` bypasses digestion for the complete call. It is appropriate
only for controlled internal delegation where the caller has already proved all
type, shape, unit, selection, and cross-argument invariants. It still incurs
ordinary Python call overhead and must not be described as zero cost.

```python
# The public boundary validates every argument.
normalized = public_operation(user_input)

# A private implementation may delegate without repeating digestion only when
# it owns `normalized` and has established the complete target contract.
result = decorated_delegate(normalized, skip_digestion=True)
```

If one argument is still user-controlled, partially normalized, or interpreted
by the target's digester, use the ordinary decorated call. Fine-grained
performance problems such as an expensive canonical-unit predicate belong in
the responsible unit library or a kernel-input preparation helper, not in a
generic identity-based certification container.

## Dependency Policy
MolSysMT distinguishes **hard** vs **soft** dependencies:
- Hard: required for core functionality.
- Soft: optional features; must be lazily imported.

Rules:
- Never import soft dependencies at module top-level.
- Use `@dep_digest(library)` to guard optional functionality.
- Validate architecture with `devtools/scripts/validate_dependencies.py`.

### Package lazy loading
MolSysMT uses lazy loading to reduce import work without promising a fixed
startup time across environments:

1. **Package-Level PEP 562 Lazy Loading**: The package entry point uses PEP 562
   `__getattr__` and `__dir__` for the registered public surface. Core startup
   configuration and diagnostics are still imported eagerly. A May 2026 run
   measured a reduction from 3.34 seconds to approximately 500 ms; reproduce
   that benchmark before treating it as current.
2. **Lazy converter registry**: `_convert_to` currently accepts callables and
   strings naming converter modules. Prefer strings where importing the
   converter would eagerly load optional or expensive code. Existing callable
   entries remain valid and should be migrated only with tests.
3. **Dynamic Resolution**: `molsysmt.basic.convert` and the package-level
   `__getattr__` resolve registered code on demand and cache package attributes
   after successful resolution.

### Native kernel startup

Native Rust kernels are compiled into the installed extension. MolSysMT has no
kernel warm-up API; applications may import the public namespaces they need
when eager module loading is useful.

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
5) Prefer lazy string converter entries when they avoid eager optional imports.

## PyUnitWizard Interaction Policy

The current ecosystem split after the March 2026 audit is:

- PyUnitWizard provides reusable quantity extraction and conversion services;
- MolSysMT uses those services at the API boundary and, where necessary, inside
  local kernel-input helpers;
- MolSysMT should not fork PyUnitWizard semantics locally, but it may add
  kernel-specific preparation steps when PyUnitWizard's generic extraction is
  not sufficient on its own.

This is why MolSysMT now depends on PyUnitWizard's expanded extraction API
(`value_type`, `dtype`) while still keeping its own shape and pairing helpers
for structure kernels.
