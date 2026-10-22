---
summary: Inherited native constructors reject valid count arguments
issue: uibcdf/molsysmt#404
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: medium
verification: reproduced
area: [native, argdigest, api, copy]
guard: tests/native/test_inherited_constructors.py
normative: devguide/native_queries.md
blocked_by: []
supersedes: []
---

# Inherited native constructors reject valid count arguments

**Reported:** Discovered while qualifying subclass copying and serialization in
uibcdf/molsysmt#121. The original fixtures used explicitly trusted construction.
**Status:** The bounded MolSysMT correction is implemented and contract-tested;
local documentation and governance gates pass.

## What

Inheriting ChemicalStates, MolSys or Topology in another module rejects valid
atom counts, including the default zero, before constructing the native domain:

```python
from molsysmt.native import ChemicalStates

class Child(ChemicalStates):
    pass

Child(n_atoms=2)  # ArgumentError before the correction
```

An initial regression run with `python -m pytest --receptor=llm -n 12
 tests/native/test_inherited_constructors.py` failed 38 of 74 cases. Remaining
invalid-input checks passed, but that alone did not demonstrate the correct
argument was being rejected. The final tests also check the refused argument.

## How

ArgDigest deliberately derives a method's `caller` from its runtime receiver
module. Inheriting a constructor changes that key; MolSysMT's count digesters
recognize the original native constructor keys. The first failed argument was
`n_atoms`, masking the same restriction on group, component, molecule, entity,
chain and bond counts in Topology/MolSys.

The three native constructors now declare their base value contract through
ArgDigest's existing decorator-context mechanism, `native_constructor`. The
seven count digesters consult that explicitly declared context when present;
other callers retain their existing dispatch and value semantics. This keeps
the ChemicalStates Boolean refusal and the existing Topology/MolSys integer
behavior, including their historical Boolean acceptance. It does not introduce
a stricter count API under the guise of fixing inheritance.

Closed signatures reject an attempted public `native_constructor` keyword.
The context is not a new user argument, a digestion bypass, a global caller
rewrite, or an alternative validation implementation. Negative dimensions and
other storage-domain constraints retain their existing downstream checks.
ArgDigest's normalization and function-contract lookup are unchanged.

## Why

Client subclasses must be constructible normally before their extension state
can be meaningfully qualified for copying. Requiring a public caller to disable
validation merely to construct a valid subclass is not an acceptable contract.
The defect affects ordinary and indirect inheritance even without custom code
or new molecular forms. It does not prove that subclass-specific scientific
operations or form registration are supported.

## What is measured and what is assumed

**Contract-tested:** 4,899 tests passed without omissions, with 12 workers and
Pytest Receptor in 60.23 seconds. Scope: native classes, private argument
digesters, basic get/compare/contains/is_composed_of, native
Topology/MolSys/Structures and H5MSM adapters, and interactions. The 732 visible
warnings occupy 11 groups, including legacy H5MSM, synthetic memory probes,
pandas migration, comparison unit stripping, synthetic atom names and existing
merge/conversion policies. No warning has been hidden by this correction.

The final focused module has 88 cases: external and indirect inheritance;
default, positional and keyword counts; every hierarchy count; invalid values
and the correct refused parameter; ChemicalStates Boolean refusal; historical
hierarchy Boolean behavior; closed keyword admission; ordinary subclass
construction followed by independent native/Python copying of slots and cycles;
and unchanged basic query-flag semantics. Existing copy, pickle and native bond
fixtures no longer bypass constructor validation for these subclasses.

All 14 fast release gates, package/new-test Ruff, public docstring fidelity
(247 functions) and public signature stability pass. Native class docstrings
pass 49 doctest examples. Common Core module 4 retains identical code cells,
execution counts and saved outputs. These are local source checks, not a final
release qualification.

No performance benchmark or installed-client qualification is claimed.

## What was refuted

- The failure is not missing topology/chemical information: an empty default
  constructor fails before storage construction.
- Changing only `n_atoms` would leave six hierarchy count arguments broken.
- Globally accepting integer counts would weaken get/compare Boolean query flags.
- Guessing validation from an arbitrary `.__init__` suffix could admit unrelated
  functions. Only explicitly declared native context selects this value contract.
- Altering ArgDigest's runtime-owner rule locally would affect mixin consumers,
  normalization and function contracts beyond this bounded correction.

## Scope and exclusions

No provider source, public signature, dependency floor, physical-unit convention,
scientific criterion, H5MSM schema or release identity changes. Ackredit is not
applicable to this validation correction. Foundations, Toolbox, Cookbook and
Common Core module 4 explain normal inherited construction and distinguish it
from registering another molecular-system form. Notebook code and saved outputs
are unchanged.

General explicit contract ownership for inherited decorated methods is proposed
in [uibcdf/argdigest#37](https://github.com/uibcdf/argdigest/issues/37), with the
existing runtime-key/display-name separation in uibcdf/argdigest#18 retained.
That provider proposal does not block this bounded fix. If a compatible public
provider contract-owner mechanism becomes available and is adopted by MolSysMT,
reevaluate replacing this local constructor value context; do not remove it
without the same inheritance and query-contract guards. #121 remains separate
and active for its remaining acceptance work.

## Acceptance criteria

- Ordinary and indirect subclasses construct with defaults and valid counts.
- Every inherited count follows its base validation rules; invalid input names
  the correct rejected parameter.
- User calls cannot inject the internal decorator context.
- Queries keep their existing Boolean/count distinction.
- Constructed subclass copies retain concrete types, slots, cycles and separate
  mutable extension data.
- Documentation/governance checks pass and the archived record names the guard.

## Provenance

2026-10-22; existing Linux development environment; Python 3.14.7;
ArgDigest `0.16.0+1.g6dabaf7`. No auxiliary environment was created.
