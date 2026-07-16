# Testing Form Adapters

Form tests establish delivered behavior, not merely the presence of modules or
functions. Historical adapter-specific repair notes are archived under
`archive/assessments/`.

## Two required levels

1. Test adapter functions directly to isolate parsing, getters, conversion, and
   iterator behavior.
2. Test the public route (`get`, `convert`, `select`, or `Iterator`) to exercise
   form discovery, capability gating, piping, digestion, and units.

A passing direct getter does not prove the public route works, and a structural
adapter validator does not replace either level.

## Capability matrix

Use `molsysmt._private.form_tier.FORM_TIERS` for tier membership. Use the adapter's
`attributes` and `_heavy_support` declarations as claims to be tested, not as
test oracles. If a declared attribute cannot be delivered, fix the declaration
or implementation and record the defect; do not weaken the test to accept
silent `None`.

## Deterministic fixtures

Prefer bundled systems or small programmatically built fixtures. A fixture must
contain the hierarchy and attributes relevant to the form. Avoid treating one
protein-only fixture as proof for waters, ions, ligands, alternate locations,
multiple models, bond orders, or metadata.

Network identifier forms need separately marked online tests and offline tests
for lazy import, cache behavior, and actionable failure. Ordinary form suites
must not require network access.

## Assertions

Assert, where applicable:

- recognized type/form and non-match behavior;
- numbers, names, IDs, indices, hierarchy, and bond pairs;
- element IDs remain strings in native objects;
- coordinates `(n_structures, n_atoms, 3)` in nm;
- box `(n_structures, 3, 3)` in nm and time in ps;
- selection and non-contiguous structure-index ordering;
- `None` versus absent-attribute semantics;
- output type and scientifically relevant conversion fidelity;
- iterator chunk boundaries, context management, and cleanup;
- missing soft-dependency behavior without eager imports.

Getter return shape varies by attribute and public API contract. Do not apply a
blanket “all per-element getters return lists” rule without checking adjacent
forms and the consuming public operation.

## Conversions

Test each declared direct edge and the public route that uses it. Check only
attributes the target representation can preserve, and document known loss.
When a route uses `molsysmt.MolSys` as an intermediate, include a test that would
detect loss or reindexing at both edges.

## Heavy forms

Follow `SCALABILITY.md`. Framework tests with synthetic reducers are necessary
but do not certify an adapter. Each advertised heavy attribute needs real-form
tests for full, partial, selected, and empty/invalid requests plus eager parity.

## Local validation

```bash
python devtools/scripts/validate_dependencies.py
python devtools/scripts/validate_form_adapters.py
pytest tests/form/<adapter>
```

Use the smallest relevant suite during development and expand to public API and
integration tests before declaring a capability supported.
