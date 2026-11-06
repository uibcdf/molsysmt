---
summary: Mechanical readers confuse Boolean query flags with physical parameter values.
issue: uibcdf/molsysmt#584
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [basic, argdigest]
guard: tests/basic/get/test_mechanical_query_flags.py
normative:
blocked_by: []
supersedes: []
---

# Mechanical readers confuse Boolean query flags with physical parameter values

**Reported:** native receiving during PR #543, reproduced on 2026-11-05.
**Status:** resolved; reader/value separation and surrounding contracts pass.

## What

After `msm.set(molsys, constraints="none")`, `msm.get(molsys,
constraints=True)` raises `ArgumentError` instead of returning the stored policy.
The same Boolean-reader collision affects eleven additional scalar mechanical
attributes. False requests are also rejected instead of being ignored.

```bash
python -m pytest tests/basic/get/test_mechanical_query_flags.py -k 'system_mechanical and constraints' --receptor=llm -n 2
```

Baseline on source `6005bb4bc`: six failures in 5.08 s, covering constraints
and flexible constraints in MolSys, MolecularMechanics and MolecularMechanicsDict.

## How

Shared property digesters validate a physical value even when their caller is
`basic.get`, whose attribute keywords are Boolean requests. Existing flag
handling in some mechanics digesters is inconsistent; a physical-model string
can also be accepted as a truthy reader request.

Use the existing private query-flag validator, generalized from chemical-state
metadata to attribute requests. Its seven existing consumers keep the same
behavior. Sixteen scalar mechanics digesters explicitly delegate their
`basic.get` branch to it. Native MolSys queries reuse those same validated
contracts; physical setter/converter branches remain separate.

## Why

Clients need supported inspection without private container reads or a consumer
workaround. Reading a stored request must not claim engine execution, infer a
physical policy from True/False or normalize stored quantities using a physical
input parser. This is independent of #582's future effective-recipe design.

## What is measured and what is assumed

The initial public audit exercises both flags for all scalar mechanical readers.
Twelve reject Boolean requests: constraints, flexible_constraints,
non_bonded_method, cutoff_distance, switch_distance, ewald_error_tolerance,
hydrogen_mass, rigid_water, solute_dielectric, solvent_dielectric,
salt_concentration and kappa. Forcefield, water_model, implicit_solvent and
dispersion_correction already accept Booleans; they now share the strict reader
contract. Per-atom charge/type attributes have separate atom-level contracts.

## What was refuted

The source policy is stored successfully; the failure happens before delivery.
This is not a request to treat a Boolean as an engine constraint model. Existing
container None/unset behavior and explicit converter `constraints=None` retain
their separate meanings.

## Scope and exclusions

Boolean scalar mechanics query requests in generic/native reads, including
dictionary forms, mixed ordered requests and absent values. No new mechanics
parameterization, provider, unit policy, scientific attribution event or H5MSM
mechanics persistence. Setter/converter admission and #581's physical constraint
translation remain independently tested. No public signature changes.

## Acceptance criteria

- True reads the stored value; False omits the request for value/dictionary output.
- Mixed requests retain order and false-valued physical parameters as data.
- Missing settings return None without filling defaults or editing the source.
- Non-Boolean reader requests fail with the existing catalog diagnostic.
- Boolean reader flags cannot be used as physical constraint policies.
- All existing chemical-state flag, setter and engine-translation guards pass.

## Provenance

Linux, shared Python 3.14.7 development environment. Published Pytest Receptor,
two workers for the initial guard and one OpenMM/BLAS thread per process.

## Resolution and receiving

The common flag helper now lives in the private `_attribute_query` module;
the existing chemical-state metadata consumers retain its exact behavior.
Mechanical readers reach that helper only under the basic-get caller context.
Native queries already delegate value contracts under that same context, so no
second native implementation is needed. Other caller branches retain physical
value validation, including rejection of Boolean constraint policies.

All 152 new public cases pass within the broader 1,193-case run. They cover
sixteen scalar settings in three source forms, native MolSys parity, True/False,
unset values, unit-bearing settings, physical False returned as data, mixed
ordered/dictionary queries and malformed flags. The actual engine constraint
and explicit-None conversion controls remain green. Reading stored requests in
an Ackredit capture produces no executed-software credit.

Receiving additionally passes 313 published-support-floor cases, 23
setter/conversion cases and 569 documentation/doctest cases. Suites overlap.
Docstrings, Foundations, Toolbox, Cookbook, course and native-query guidance
explain the distinction. The three prose-only notebook edits retain executable
cells, outputs and metadata. The course also corrects the existing description
of multiple get results from tuple to ordered list. Ruff, dependency imports,
API stability, course and developer-guide checks pass.

See the [receipt](../../../devtools/data/mechanical_query_flags_receiving_584_20261105.json)
for commands, source identity, provider origins/hashes and evidence boundaries.
The first broad selection named a nonexistent `tests/basic/set` directory and
exited 5 without running cases; the corrected run and actual setter files above
are the passing evidence. No skipped selection is counted as a pass. Hosted
and installed/platform release qualification remain separate under #334.
