---
summary: Hydrogen-bond default role rules fail with external syntax.
issue: uibcdf/molsysmt#507
status: resolved
opened: 2026-10-27
closed: 2026-10-28
severity: medium
verification: reproduced
area: [interactions, molsysviewer]
guard: tests/interactions/hbonds/test_role_rule_syntax.py
normative:
blocked_by: []
supersedes: []
---

# Hydrogen-bond default role rules fail with external syntax.

**Reported:** 2026-10-27 during expert-addon receiving.
**Status:** resolved; rule languages have explicit independent ownership.

## What

The classic `interactions.hbonds.get_donor_atoms()` and `get_acceptor_atoms()` accept `syntax='MDTraj'` but feed their internal MolSysMT default rules to the MDTraj parser, so a valid user selection fails before role recognition.

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
    try:
        print(name, method(molsys, selection="index 0", syntax="MDTraj"))
    except Exception as error:
        print(name, type(error).__name__, str(error))
```

Donors fail while parsing `(atom_type=='O') bonded to (atom_type=='H')`; acceptors fail while parsing `atom_type=='O'`. `index 0` itself is valid and reaches the internal rule loop. Numeric selection/native MolSysMT syntax supplies independent working comparisons. The repaired #148 establishes directional selector availability; it does not fix this higher-level helper's mixed rule languages. #355 concerned valid empty bonded-to operands, not MDTraj parsing of the built-in rules.

## Why

The explicit public syntax parameter should govern the documented input consistently. Please separate internal default-rule language from the user's selection syntax and clarify the custom inclusion/exclusion rule-language contract. Do not add a consumer translation or infer an unsupported syntax. Native pytest should cover both helpers, numeric and equivalent supported external selections, defaults enabled/disabled, custom rules, empty/no-H cases, donor-H pairing and invalid/unsupported syntax rejection. Preserve scientific rule meanings and original atom indices.


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

The two readers delegate rule application to one small private hydrogen-bond
helper. It uses the existing public form-agnostic selection tool; no second
parser, chemical store or recognition model is introduced. User selection and
custom inclusion/exclusion expressions use the declared `syntax`. Enabled
defaults retain MolSysMT syntax. All inclusions are combined before exclusions,
so default/custom precedence is preserved. Supplied lists are never extended.
Default scientific expressions, source indices and donor-H sorting are unchanged.

The custom-rule language is now documented explicitly. Unsupported syntax or
malformed user rules reject through the normal public argument/selection
boundary, without translation or retries. Numeric masks and external strings
retain source correspondence. A donor mask filters anchors, not their attached
H atoms; no-H queries retain the #508 empty-pair contract. Acceptor no-match
outputs now explicitly retain int64 shape (0,), rather than NumPy's inferred
floating dtype for an empty Python list.

Initial independent syntax matrix: 22 failed, 13 passed, with the default rules
being rejected by MDTraj's parser. After repair, 78 role/ownership/pair cases
and both doctests pass. A wider run passes 347 native classic/modern H-bond,
legacy namespace, topology-path and addon-role regressions with Pytest Receptor
and 12 workers. Expected legacy-format/artificial-memory-budget diagnostics
remain visible. The new expert receiving cases assert mutable-list independence,
MDTraj rules, explicit donor-H correspondence and unchanged scene state.

Both docstrings/tutorials, the selection-syntax foundation, Alzheimer/Enzyme
course narratives and current addon guidance describe the language boundary.
Existing scientific examples and outputs are retained. No affected Cookbook
recipe uses custom classic role rules; no unrelated recipe is added. Strict
parallel documentation, Ruff, dependency leakage, public signature and docstring
checks pass. This source repair does not qualify an installed package, universal
chemical recognition, a new scientific profile or a release. #509/#511 remain
separate owner work; modern site/profile recognition is unchanged.
