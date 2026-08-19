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

### Building the value a getter returns

`INTERFACES.md`, *Scalar types in returned values*, says what a getter must
deliver. This is how to build it, and the two are not the same question: the
delivered types are already guaranteed by a normalisation step in
`molsysmt/basic/get.py`, so what follows is about not creating work for it.

**Leave the array in C for as long as possible.** `ndarray.tolist()` converts a
whole array to native Python types in one pass; iterating it with `enumerate` or
indexing it element by element allocates one boxed NumPy scalar per element, and
those are what the normalisation step then has to walk and convert.

The measured difference is worth having where the value is built row by row.
Replacing `DataFrame.itertuples()` with `frame[[...]].to_numpy().tolist()` in the
bond-pair getter cost 98.5 ms instead of 15.0 ms for an identical result over
65 442 bonds — 6.6x — because `itertuples` builds a namedtuple and two scalars per
row. Prefer `int(np.count_nonzero(...))` over returning the NumPy integer for the
same reason: it costs nothing and the value arrives native.

Two cautions, both learned the hard way in `uibcdf/molsysmt#172`:

- **A pandas nullable column does not convert the way it looks.** `to_numpy()` on
  an `Int64` column yields an object array, not `int64`. With no missing values the
  leaves come out as native `int` and the values match; forcing
  `to_numpy(dtype='int64')` is *slower*, because it adds a pass to avoid a problem
  that does not arise. Check for nulls rather than forcing a dtype.
- **An array feeding fancy indexing must stay an array.** In a getter that both
  iterates one array and uses another as `other[indices]`, converting the wrong one
  raises `only integer scalar arrays can be converted to a scalar index`. The rule
  is per variable, not per function, and three attempts to apply it mechanically
  across the cross-level getters failed on exactly this.

Where a getter mixes iteration, scalar indexing and fancy indexing over the same
kind of variable — as the thirteen cross-level getters in `molsysmt_Topology` do —
the conversion is not worth doing mechanically. Measured there, the loop improves
1.48x while the enclosing call moves about 1 %, and the delivered types are correct
either way. Write new getters the fast way; do not rewrite those.

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
