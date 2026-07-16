# Form Adapter Implementation and QA

The local authority for adapter code is `molsysmt/form/AGENTS.md`. This document
summarizes the maintained workflow and the limits of current automation.

## Package contract

An adapter under `molsysmt/form/<adapter>/` declares:

- `form_name`, `form_type`, and `form_info`;
- `bonds_are_explicit` and `bonds_can_be_computed`;
- `piped_topological_attribute`, `piped_structural_attribute`, and
  `piped_any_attribute`;
- `is_form`, `attributes`, and `has_attribute`;
- `_convert_to`, containing callable converters or lazy import strings;
- operation functions and iterators appropriate to that form.

Lazy converter strings are preferred where they avoid importing soft
dependencies, but callable entries are currently supported. Do not claim a
string-only registry until it is enforced and migrated.

File names use forms such as `file_pdb`; registered names use `file:pdb`.
Class adapters commonly use an underscore directory such as `openmm_Topology`
and a dotted registered name such as `openmm.Topology`. Verify conventions in
adjacent adapters rather than deriving names mechanically.

## Dependencies and digestion

Soft dependencies are imported inside functions and guarded with `@dep_digest`
where required. Public adapter operations should use `@arg_digest` when they
accept user-facing arguments; private helpers must not. Avoid decorating a
predicate in a way that turns a normal non-match into an error.

## Piping and delivery

Piping is an optimization and capability route for bulk attribute requests.
Targets must be registered forms and preserve the attributes being requested.
Keep direct getters when they are part of the adapter surface, and test both
direct adapter behavior and public `molsysmt.get()` delivery.

An `attributes=True` declaration is invalid unless the public path can deliver
the attribute with correct shape, units, indexing, and `None` semantics.

## Iterators and heavy support

Only adapters that implement a usable context-managed `StructuresIterator`
should advertise `_heavy_support`. Placeholder iterator classes are not a
capability. Follow the chunk conventions in `SCALABILITY.md` and test partial
chunks, selections, structure indices, and resource cleanup.

## Scaffolding

`devtools/scripts/scaffold_form.py` can create a starting adapter skeleton:

```bash
python devtools/scripts/scaffold_form.py \
    --name <adapter_directory> \
    --type <class|file|string> \
    [--class-name <qualified_class>]
```

Generated files are placeholders, not a conforming scientific implementation.
Replace stubs, declare real capabilities, add dependency guards, and add tests.

## Validation

Run:

```bash
python devtools/scripts/validate_dependencies.py
python devtools/scripts/validate_form_adapters.py
pytest tests/form/<adapter>
```

The form validator checks imports, selected declarations, types, converter-map
presence, context-manager methods for active heavy forms, complete explicit tier
classification, and static reachability of declared attributes through a direct
getter, a registered form-independent derivation, or a usable
topological/structural pipe. Existing delivery debt is encoded in
`devtools/data/form_attribute_delivery_baseline.json`; the validator accepts a
strict subset of that debt but rejects new unreachable declarations.

Derived attributes use dependency metadata from `molsysmt.attribute.attributes`
and implementations registered in
`molsysmt/_private/attribute_derivation.py`. Prefer a shared derivation from an
available source attribute over duplicated adapter getters or a conversion that
copies unrelated data. A declaration still requires a direct getter, registered
derivation, or valid pipe; dependency metadata alone is not executable behavior.

This static reachability check does not prove correct values, shapes, units,
indexing, `None` semantics, conversion fidelity, decorator correctness, or
iterator output behavior. Those claims still require executable contract and
scientific tests.

## Required tests

At minimum, test recognition/non-recognition, public attribute delivery,
selection and structure indexing, topology counts and bonds, structural shapes
and units, conversion type and fidelity, dependency absence, and cleanup of any
opened resource. Round trips are useful only when the target formats can
preserve the attributes being asserted.
