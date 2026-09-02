---
summary: Validators that check form instead of intent admit conforming emptiness.
issue: uibcdf/molsysmt#187
status: resolved
opened: 2026-08-19
closed: 2026-09-02
severity: high
verification: measured
area: [docs, api, ci]
guard: devtools/tests/test_validate_docstrings.py
normative:
blocked_by: []
supersedes: []
---

# Bug: a gate that checks form gets filled with form

**Reported:** 2026-08-19, during the external audit
([`../assessments/external_audit_august_2026.md`](../assessments/external_audit_august_2026.md)),
as a documentation defect on the stable surface. **Rewritten the same day**, after the
originating commit was traced: the placeholders are the instance, the gate criterion is
the theme.
**Status:** resolved. The docstring criterion and stable surface are repaired. The
scientific-evidence and devguide-guard findings are tracked independently by
uibcdf/molsysmt#196 and uibcdf/molsysmt#197.

## What

On 2026-08-18, one commit documented the package:

```bash
$ git show 30e3119a5 --shortstat --format='%ad %s' --date=short
2026-08-18 docs: add NumPy docstrings across the package and reorganize content/developer [skip ci]
 1495 files changed, 184251 insertions(+), 5206 deletions(-)

$ git show 30e3119a5 | grep -c '^+.*Resulting object in object form'
8810
$ git show 30e3119a5 | grep -c '^+.*Argument [a-z_]*\.$'
953
```

`validate_docstrings.py` passed on all of it, correctly, because what it checks was
satisfied: every signature parameter appears in the `Parameters` section, every
documented default matches the signature, no phantom parameters, `Returns` present.

What arrived is 184,251 lines that meet the criterion and inform no reader. On the
stable root surface, 18 of the 50 documented symbols now describe 49 parameters as
`Argument <name>.`, including the argument that selects one of 89 destinations:

```python
>>> help(msm.convert)
    to_form : object, default=None
        Argument to_form.
```

`molsysmt.get` is the shape of the problem in one docstring: nine paragraphs of
hand-written `Notes` on chemical states, mixed element levels and derived attributes,
above four parameters described by restating their names.

## How

Not a defect in the sweep and not a defect in the validator as written. A defect in the
**criterion**, which is the thing a generated contribution optimises against.

A validator that encodes *intent* cannot be satisfied without the underlying property
holding. A validator that encodes *form* can be satisfied by conforming output. The
distinction is invisible while contributions are hand-written at human scale, and it is
the binding constraint once they are not: **generation scales exactly to the gate, and
not one step past it.**

Classified by that criterion, the twelve release-gate validators plus the docstring gate
divide as follows. This is the inventory, and it is the useful part of this entry.

| Gate | Checks | Class |
| --- | --- | --- |
| `validate_form_adapters.py` | every `attributes=True` declaration against a real getter, pipe, converter or transitive route | **intent** |
| `validate_demo_assets.py` | actual HDF5 hierarchy sizes against `demo_manifest.json` | **intent** |
| `validate_dependencies.py` | absence of real top-level soft-dependency imports | **intent** |
| `check_rust_hot_paths.py` | absence of libm rounding calls in kernel inner loops | **intent** |
| `audit_conversion_fidelity.py` | the discovered edge set against an accepted-debt baseline | **intent** |
| `validate_api_stability.py` | AST-discovered exports are all classified, none stale, none internal | intent on coverage, **form on content** — a registry classifying everything `stable` passes |
| `validate_function_tiers.py` | declared tiers consistent with the stability registry | consistency; inherits the blind spot above |
| `validate_scientific_evidence.py` | every stable scientific API classified; each cited node **is defined** in the test tree | intent on coverage, **form on the evidence** — it confirms the test exists, not that it passes or asserts anything |
| `validate_citation.py` | exact agreement of title, DOI, licence and dates across `CITATION.cff`, `.zenodo.json` and the README | cross-record consistency; **form on the values** |
| `validate_devguide.py` | front matter fields, vocabularies, resolvable links, current indexes, and that a `guard` **names a file that exists** | **form** — a guard that never fails the defect passes |
| `validate_course.py` | manifests, toctrees, labels, module numbering | **form**, and appropriately so: the contract is structural |
| `validate_resources.py` | YAML schema of the resource manifests | **form**, appropriately so |
| `validate_docstrings.py` | parameter presence, default fidelity, `Returns` presence | **form on the content** — the one that was filled |

Five gates are strong. Three are structural contracts where form is the whole point and
nothing is wrong. The remaining five share one shape: they verify that a record is
complete and well-formed, and are silent on whether it says anything. `validate_docstrings.py`
is the one that has already been exercised at scale.

Two of the silent five matter beyond documentation:

- **`validate_scientific_evidence.py` confirms a cited test is defined, not that it
  runs.** The evidence matrix reports 43 validated with zero gaps on that basis. Nothing
  in the gate distinguishes a passing oracle from a test that errors during fixture
  setup — which is the state four curated tests are in right now
  ([#182](https://github.com/uibcdf/molsysmt/issues/182)), though those four are not
  themselves cited evidence.
- **`validate_devguide.py` requires a `guard` to name an existing file.** The protocol's
  closing condition is "a test that fails if the defect returns"; the gate checks that a
  path exists. Every entry closed by this audit will satisfy the gate whether or not its
  guard would have caught the defect.

## Why

**This is the constraint on maintaining the codebase with machine assistance, stated
precisely.** The strategy is deliberate: `argdigest`, `smonitor`, `depdigest` and the
machine-readable registries exist so that a small team can hold a large surface, and the
audit that produced this entry is evidence that it works — claims were checked by
executing registries rather than by reading, and the strongest findings came from gates
that already existed. The variable it depends on is not the quality of the assistance. It
is the specificity of the gates. Every gate that checks form is a surface where volume
will grow without being read.

**The instance is on the contractual surface at the moment it freezes.** Those 18 symbols
are `stable` in `devtools/data/public_api_stability.json`. 1.x promises their signatures
and does not say what four of `get`'s arguments do.

**It is what an agent is handed.** MolSys-AI is being built on MolSysMT as an assistant
and later an agent ([#192](https://github.com/uibcdf/molsysmt/issues/192)). The tool
description an LLM agent receives for a function is its docstring. The text it would be
given to decide how to call `convert` is `Argument to_form.` A human infers the argument
from the examples; an agent is handed the parameter table.

Severity is raised from `medium` to `high` on the rewrite. Nothing computed is wrong. The
gate criterion determines whether the project's maintenance model holds, and one gate has
already demonstrated the failure at a scale of 184,251 lines in a single day.

## What is measured and what is assumed

Measured: the commit, its file and line counts, and the two placeholder counts it
introduced; the original 18 stable root symbols and 49 parameters, by iterating the
stability registry and matching `^\s*Argument (\w+)\.$` against `inspect.getdoc`; the
assertion set of each validator, read from source; the release-gate membership list in
`release_gate.py`. A complete stable-function audit on 2026-09-02 found 60 affected
functions and 205 parameters typed as `object` and described with the generated
restatement.

The classification column is judgement applied to a measured assertion set, not a
measurement. Reasonable disagreement is possible on `validate_api_stability.py` and
`validate_citation.py`, which are strong on the axis they check and silent on a different
one.

Assumed — *estimate*: that the sweep was machine-generated. The commit shape makes no
other explanation plausible, and the entry does not depend on it: a hand-written sweep of
the same size would raise the same question about the criterion.

## What was refuted

*The generator's template is the cause.* This was the first reading and it is too narrow.
A better template fixes 8,810 strings and leaves the criterion that accepted them, so the
next generated surface passes the same way.

*The docstring validator is not run.* It is, `test_validate_docstrings.py` is in
`devtools/tests/`, and it passes. It checks what it was written to check.

*Every gate has this problem.* It does not. Five are genuinely intent-checking, and
`validate_form_adapters.py` — which refuses a declared attribute unless a real delivery
route exists — is the model the others should be measured against.

## Scope and exclusions

Covers the docstring criterion and the stable public-function docstrings. The normative
rule and maintained gate inventory remain part of this resolution.

The scientific-evidence validator is now tracked by uibcdf/molsysmt#196. The devguide
guard validator and protocol wording are tracked by uibcdf/molsysmt#197. They were split
because each requires its own contract, risks, and regression guard.

Excludes the ~9,000 remaining placeholder occurrences inside `molsysmt/form/`: correcting
the criterion and the template is what prevents their return, and regenerating the layer
is a separate change. Excludes `validate_course.py` and `validate_resources.py`, which
are structural contracts where form is the subject. Excludes rewriting
`validate_api_stability.py` and `validate_citation.py`, which are strong on their own
axis; their blind spots are recorded here as inventory, not as work items.

## Acceptance criteria

1. `validate_docstrings.py` rejects a parameter description that restates the parameter
   name, an empty description, and a `Returns` description matching the generated
   phrasing. This is the `guard`.
2. No `stable` symbol documents a parameter as `Argument <name>.`, and none types a
   parameter `object` where a concrete type or union applies.
3. `AGENTS.md` states the rule: a gate must be satisfiable only by the property it exists
   to protect, never by conforming output. New validators are reviewed against it.
4. `devtools_and_ci.md` carries the inventory above, so the classification is maintained
   rather than rediscovered.
5. The scientific-evidence finding is independently tracked by uibcdf/molsysmt#196.
6. The devguide-guard finding is independently tracked by uibcdf/molsysmt#197.

## Resolution

`validate_docstrings.py` now parses each parameter's type and description in addition to
its name and default. On functions classified `stable` by the public API registry, it
rejects empty descriptions, descriptions that only restate the parameter name, the
generated `Resulting object in object form.` return description, and the non-informative
parameter type `object`. The restriction to stable functions is deliberate: the gate
protects the contractual surface without turning the generated and experimental form
layer into hidden 1.0 scope.

Mutation tests establish that each forbidden pattern independently fails the content
check, while an informative control passes. The stable-surface repair replaces the 205
affected parameter entries across 60 functions with concrete types and operational
descriptions. Two examples that failed when their own submodules were collected now
import the callable explicitly.

The maintained gate inventory describes this as a bounded semantic floor. It does not
claim that a validator can judge arbitrary prose. The two other weak-gate findings were
split into uibcdf/molsysmt#196 and uibcdf/molsysmt#197 rather than being nominally closed
by unrelated changes.

Validation on 2026-09-02:

- `python -m pytest devtools/tests/test_validate_docstrings.py -p no:rerunfailures
  --receptor=llm`: 10 passed;
- doctests for all 60 changed package modules: 27 passed;
- `python devtools/scripts/validate_docstrings.py`: 201 public functions passed;
- `ruff check molsysmt devtools/scripts/validate_docstrings.py
  devtools/tests/test_validate_docstrings.py`: passed;
- `python devtools/scripts/release_gate.py`: 13 of 13 fast gates passed.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `08d2fef2a`. Commit `30e3119a5` is dated
2026-08-18.
