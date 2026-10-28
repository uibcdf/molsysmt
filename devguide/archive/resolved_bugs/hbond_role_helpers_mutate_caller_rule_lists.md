---
summary: Hydrogen-bond role helpers mutate caller-owned rule lists.
issue: uibcdf/molsysmt#506
status: resolved
opened: 2026-10-27
closed: 2026-10-28
severity: medium
verification: reproduced
area: [interactions, molsysviewer]
guard: tests/interactions/hbonds/test_role_rule_ownership.py
normative:
blocked_by: []
supersedes: []
---

# Hydrogen-bond role helpers mutate caller-owned rule lists.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** resolved; caller-owned containers remain unchanged.

## What

The classic `interactions.hbonds.get_donor_atoms()` and `get_acceptor_atoms()` modify caller-owned inclusion/exclusion lists when appending default rules. Reusing a list repeatedly accumulates duplicates and can carry one helper's rules into other calculations.

Native independently reproduced during expert-addon receiving, uibcdf/molsysmt#421 / uibcdf/molsysviewer#264. Source basis 667f03b9ab6e91d1f97fb02676c5222ef9e1ca31; Python 3.14. The later 40a8ac2ea governance change does not alter these scientific files. No Viewer calls are needed. No consumer workaround has been added.

## How

```python
import molsysmt as msm
builder = msm.MolSysBuilder()
for name, kind in [("O", "O"), ("H", "H")]:
    builder.add_atom(atom_name=name, atom_type=kind)
builder.add_group([0, 1], group_name="HOH")
builder.add_bond(0, 1)
molsys = builder.build()

for name in ["get_donor_atoms", "get_acceptor_atoms"]:
    method = getattr(msm.interactions.hbonds, name)
    inclusion_rules = ["atom_type=='O'"]
    exclusion_rules = []
    for attempt in [1, 2]:
        method(molsys, inclusion_rules=inclusion_rules, exclusion_rules=exclusion_rules)
        print(name, attempt, inclusion_rules, exclusion_rules)
```

The donor input inclusion list grows from 1 to 3 to 5 entries and exclusions from 0 to 2 to 4. Acceptor inclusion grows from 1 to 4 to 7 and exclusions from 0 to 3 to 6. Digestion returns list inputs themselves; `+=` appends shared defaults in place. Tuples are separately normalized by the native digester. This is distinct from repaired donor-pair ordering #258 and missing bonded-to empty operands #355.

## Why

Caller parameters should remain stable across repeated and related scientific calls. Please fix in the native owner and add pytest coverage for both helpers, inclusion and exclusion independently, None/string/tuple/list inputs, default flags on/off, repeated calls, shared lists across helpers and global default-rule independence. Preserve role/pair/index semantics; do not change the scientific rules merely to remove mutation.


## What is measured and what is assumed

The standalone native proof uses no Viewer call. Source 667f03b9a and the
subsequent governance-only 40a8ac2ea have identical scientific implementations.
This receiving validates a bounded chemical role contract, not general
protonation correctness or new interaction-detection science.

## What was refuted

The existing repaired #258 concerns interleaved donor-H membership; #355 concerns
empty bonded-to operands. The directional selector registry #148 does not
resolve helper-level parameter/rule ownership. No matching owning report was
found before opening this issue.

## Scope and exclusions

Native classic role helpers and their explicit expert facade only. No consumer
copy, scientific rule replacement, parser translation, hidden hydrogen addition
or topology preparation is introduced. Modern profile recognition retains its
separate contract and prerequisites.

## Acceptance criteria

Implement the native correction with addressable pytest guards for both helpers
and the operational matrix requested above. Preserve source atom correspondence,
independent result ownership and scientific default meanings. Receive the owner
fix separately before lifting the documented facade limitation.

## Dependencies and risks

The scientific owner must define the durable behavior. Source availability of a
thin wrapper does not qualify every input/container/syntax path.

## Resolution — 2026-10-28

Both helpers now concatenate enabled defaults into independent local lists
instead of extending the supplied list in place. ArgDigest still normalizes
None/string/tuple/list inputs at the public boundary. Custom/default inclusion
and exclusion meanings, union-before-exclusion semantics, native pair sorting
and original source indices are unchanged. The exported default lists retain
their existing public types and values.

The guard covers both helpers, four input representations and all four default
flag combinations; repeated calls, shared lists across helpers, the same list
for both roles, exported defaults passed as input, and independent returned
arrays are checked. Initial red run: 11 failed, 26 passed. Corrected matrix:
37 passed; including the existing interleaved-pair/detector regressions and
both public doctests, 43 passed with Pytest Receptor and 12 workers.

Docstrings correct the accepted rule-container contract (the acceptor text
incorrectly said dictionary). Both role tutorials and the Alzheimer/Enzyme
course narratives explain input ownership and enabled defaults; their existing
scientific code and stored outputs are retained. No existing Cookbook recipe
relies on mutating these inputs. The strict parallel documentation build,
Ruff and public API/default checks pass. Unit/PBC/compiled-backend behavior is
unaffected, and no new chemical method or third-party implementation is used.

The mixed internal/external rule language defect is separately reproduced and
remains owned by uibcdf/molsysmt#507. Consumer receiving and removal of its
current limitation will be performed explicitly; this source fix alone is not
installed-package or universal chemistry qualification.
