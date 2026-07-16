# Forms and Conversions

This document defines the current adapter and conversion contract. Historical
adapter implementation notes are archived under `archive/assessments/`.

## Form adapter contract

Form adapters live under `molsysmt/form/`. Each adapter module defines:

- `form_name`;
- `form_type`;
- `form_info`;
- `attributes` and `has_attribute`;
- applicable topological, structural, or general piping targets;
- `_convert_to`, mapping supported target form names to converter callables or
  lazy converter-module names.

Detailed file layout and dependency rules are defined in
`form_adapter_implementation.md`.

## Discovery and dependencies

Adapters are discovered lazily. Optional dependency ownership is defined by
`molsysmt/_depdigest.py`; adapters must not introduce their own competing
dependency registry. Soft dependencies are imported inside guarded functions,
never unconditionally at module import time.

## Conversion resolution

The current one-to-one resolver in `molsysmt/basic/convert.py` supports:

1. a direct edge from the source adapter to the target adapter; or
2. a two-edge route through `molsysmt.MolSys` when both edges exist.

It does **not** perform a general shortest-path search over the conversion graph.
Multiple-input conversions use registered shortcuts and attribute-based assembly
logic, with a MolSys route where explicitly supported.

Do not document or rely on arbitrary multi-hop conversion. A broader graph
resolver would be a new architectural feature requiring deterministic routing,
lossiness and cost policies, cycle detection, dependency-aware edge selection,
and dedicated tests.

## Converter registration

Register a converter only when it is callable for the documented source and
target contract. A placeholder that raises `NotImplementedMethodError` must not
be present in `_convert_to`, because registration advertises an executable edge.

Converter values may be callables or strings naming the converter module and
function. String entries preserve lazy imports; `_convert_one_to_one` imports the
module only when that edge is traversed.

Converters must:

- preserve documented semantics or explicitly document intrinsic loss;
- normalize native element IDs to strings;
- preserve coordinate, box, and time units through PyUnitWizard boundaries;
- accept the standard selection and structure-index arguments that apply to the
  represented data;
- import optional libraries lazily under DepDigest control.

MolSysMT canonical lengths are in nm and time is in ps. Angles derived from box
geometry follow the API's radians convention; converters must not generally
standardize angular data to degrees.

## Attribute declarations and piping

`attributes.py` records the adapter capability contract used by dispatch. A
declared attribute must be deliverable through the public `get()` path for every
documented element scope. Delivery may be direct or may use the adapter's
declared piping target.

This is intentionally a public-delivery definition, not merely a statement that
the source object's Python class stores a field directly. If native presence must
be distinguished from converted delivery in the future, add explicit metadata;
do not overload one boolean with two contradictory meanings.

For attributes available from more than one element scope, every corresponding
getter must exist or the pipe target must provide it. For example, coordinates
declared for both atoms and the system must work for both explicit atom requests
and the default system request.

Known delivery gaps are tracked under `pending_bugs/` and take precedence over
historical claims of complete adapter verification.

## Forms with partial source information

A source containing coordinates but no topology must not invent semantic
topology. Likewise, a topology-only form must not advertise structures. Where a
format contains only partial labels, a converter may construct only the topology
that can be justified from those labels and must document the inferred fields.

File handlers should accept the documented path-like representation at public
boundaries. Internal reader objects must not be assumed to retain a recoverable
filename after construction unless their actual API guarantees it.

## Validation obligations

For every supported conversion edge, tests should cover:

- direct execution through `msm.convert`;
- representative selection and structure slicing;
- ID, shape, dtype, and unit invariants;
- lossless round-trip parity where the formats can represent equivalent data;
- explicit expectations for intentionally lossy formats;
- missing optional dependency behavior;
- lazy-import behavior for soft dependencies.

The adapter linter checks structural conformance. It is not evidence of semantic
parity or scientific correctness.
