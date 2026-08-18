---
summary: The docstring generator rewrites public signatures instead of preserving them
issue: uibcdf/molsysmt#169
status: open
opened: 2026-08-18
closed:
severity: high
verification: reproduced
area: [docs, api, ci]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: the docstring generator rewrites the function instead of annotating it

**Reported:** 2026-08-18, after a full-suite run on `main` returned
`195 failed, 30 errors, 9760 passed`. The failures were traced to `93171c547`, a
commit whose stated purpose was to add documentation.
**Status:** open. The two batches of damage it has produced so far are repaired
(`9f4fbd515`, `30e3119a5`); the generator itself is untouched, so a third batch
will reproduce it.

## What

The tool used to add NumPy docstrings across the package does not insert a
docstring into an existing function. It **re-emits the function from the
documentation it generates**. Parameters the generated docstring does not
mention disappear from the signature, and bodies are replaced by whatever the
documentation implies — typically a thin delegation.

`93171c547` ("docs: synchronize docs/api and add missing public docstrings
across modules") is the batch that reached `origin/main`:

```bash
$ git show 93171c547 -- molsysmt/element/molecule/get_molecule_id.py
-def get_molecule_id(molecular_system, element='molecule', selection='all', redefine_indices=False,
+def get_molecule_id(molecular_system, element='molecule', selection='all', syntax='MolSysMT', skip_digestion=False):
```

Eleven public functions lost parameters in that single commit:

| Function | Parameters removed |
| --- | --- |
| `get_chain_id`, `get_component_id`, `get_entity_id`, `get_molecule_id` | `redefine_indices`, `redefine_ids` |
| `get_n_components` | `redefine_components` |
| `get_n_entities` | `redefine_entities` |
| `get_n_molecules` | `redefine_molecules` |
| `get_bonded_atom_pairs` | `group_name`, `atom_names`, `atom_indices`, `sorted` |
| `get_engine_forcefield` | `forcefield`, `water_model`, `implicit_solvent` |
| `get_forces` | `element`, `magnitude` |
| `get_non_bonded_potential_energy` | `platform` |
| `nglview.clear` | `skip_digestion` |

The same commit also **added an import that shadows a function with a module**.
`molsysmt/element/group/get_bonded_atom_pairs.py` gained:

```python
from molsysmt.element.group.get_group_type_from_group_name import get_group_type_from_group_name
```

Importing that submodule binds it as an attribute of the `molsysmt.element.group`
package, overwriting the function of the same name that `__init__.py` exports.
`molsysmt/native/_topology_infer.py:21` then receives a module and calls it:
`TypeError: 'module' object is not callable`.

## How

The mechanism is visible in what survives and what does not. Docstrings are
correct and complete; signatures are correct only where the docstring happened to
enumerate every parameter. That is the signature of generation, not annotation:
the docstring is the source and the code is the output, when it must be the other
way round.

Three shapes of damage, all from the same cause:

1. **Parameters dropped** — the docstring omits them, so the re-emitted signature
   omits them. Callers inside the package keep passing them.
2. **Bodies replaced** — a real implementation becomes a delegation. In the second
   batch, the five `element/group/*/get_group_db.py` modules were reduced to
   `from . import _db; return _db`, where `_db` **does not exist** in any of the
   five packages, and their imports (`gzip`, `pickle`, `group_names`) were deleted
   with the body.
3. **Semantics changed silently** — four functions had their `element` default
   changed from their own element type to `'atom'`:

   ```
   get_component_type   element='component' -> 'atom'
   get_entity_type      element='entity'    -> 'atom'
   get_group_type       element='group'     -> 'atom'
   get_molecule_type    element='molecule'  -> 'atom'
   ```

   This raises nothing. It returns a different array.

The third shape is the dangerous one. `devtools/scripts/validate_docstrings.py`,
added alongside the sweep, checks that docstrings exist and are well formed. No
check anywhere asserts that a documentation change leaves the signature alone.

## Why

`severity: high`, on three grounds.

It reached users. `93171c547` is on `origin/main`; anyone cloning between
2026-08-17 and 2026-08-18 got a package where `msm.convert()` on a PDB raises,
and where `select(molecule_type=="protein")` returns empty on a lysozyme because
component and molecule typing degraded to `unknown`.

It is not a one-off. Two batches, two sets of damage: 18 modules committed, 53
more in the batch that followed. The tool is still in use and the next batch will
produce a third.

And it defeats review. The commit is titled `docs:` and its diff is thousands of
docstring lines; the four altered signatures are invisible in it. That is why it
passed review, and why `[skip ci]` on a documentation commit felt safe.

## What is measured and what is assumed

Measured, on this checkout:

- Full suite at `HEAD` = `51102b03e`: `195 failed, 30 errors, 9760 passed, 11 skipped`,
  20 root causes. Run in a clean worktree with the built `_rust.abi3.so` copied in.
- Full suite after repairing 18 modules: `9980 passed, 11 skipped`, exit 0.
- Four root causes accounted for ~208 of the 225 failures and errors.
- Damage across `93171c547~1..HEAD`, by AST comparison of 1098 changed `.py` files:
  15 signatures or defaults altered, 3 bodies altered, 3 definitions removed, in
  18 files.
- Damage in the following uncommitted batch, same method over 1358 changed files:
  54 function bodies altered in 52 files, of 10512 functions compared. 28 files did
  not parse at all at one point during the run.
- `ruff check molsysmt` reports `All checks passed!` while 28 files under
  `molsysmt/form` fail `ast.parse`. Confirmed with `--no-cache`. See
  [uibcdf/molsysmt#170](https://github.com/uibcdf/molsysmt/issues/170).
- `devtools/data/public_api_stability.json` carries no signature information: the
  only fields present across all entries are `stability`, `introduced`, `owner`,
  `documentation`, `contract_tests` and `subtree_stability`. `get_molecule_id` has
  no entry.
- In the damaged `get_component_type`, signature and docstring both declare
  `element='atom'`, so they agree with each other and disagree with the correct
  value `'component'`.

Assumed:

- That the generator is a single tool used for all three batches. The damage
  pattern is identical across them, but the tool itself was not inspected — it is
  not in the repository.
- That no *other* committed batch predates `93171c547`. The comparison used it as
  the last known-good base because that is where the first failure appears; earlier
  batches were not audited.

## What was refuted

*The failures were caused by the batch in flight on 2026-08-18.* No. `get_molecule_id`
is byte-identical to `HEAD` and unmodified in that batch; the parameter was already
absent. The baseline run at clean `HEAD` returned more failures (225) than the
working tree did (218).

*The 28 files that failed to parse were an accumulating bug.* No — they were a
transient mid-write state and repaired themselves within a minute. The real damage
is the batch that completes successfully and leaves consistent, wrong code.

*`get_group_type_from_group_name` was deleted.* It was not: it lives in its own
module and resolves correctly. What changed was which of two divergent
implementations the package exports — and they disagree on vocabulary,
`'amino_acid'` versus `'amino acid'`. The rest of the package uses the spaced form
55 times and the tests 119 times.

*`close()` and `show_molsysmt` were lost.* Both were module extractions, not losses.
`close()` was reverted to inline by the repair, by decision; `show_molsysmt` had
been rewritten to delegate to `molsysmt.basic.view`, which would recurse back into
it through `to_nglview_NGLWidget`, and was reverted for that reason.

## Scope and exclusions

Covers the generator's contract: what a documentation pass is allowed to change.

Excludes the docstrings themselves, which are correct and are kept. Both repairs
restore the pre-batch code and re-inject the generated docstring, so no
documentation work was lost.

Excludes the question of who runs the generator and how, which is a process
matter for whoever owns the documentation campaign.

Excludes `molsysmt/element/group/get_group_type_from_group_name.py`, dead code in
`HEAD` carrying a vocabulary that disagrees with the rest of the package. It is a
latent trap — importing it by its obvious name breaks type inference silently —
but it predates this defect and deserves its own decision.

## Acceptance criteria

- The generator preserves the existing signature, body, imports and defaults, and
  edits only the docstring node — or is not used again on this repository.

- A guard that compares the AST of every changed `.py` **against its parent commit**
  and fails when a public signature, default or body changed. Names the `guard`
  field. This report used exactly that check; it costs seconds over 1358 files.

  The comparison basis must be the parent commit, not
  `devtools/data/public_api_stability.json`. That registry records
  `stability`, `introduced`, `owner`, `documentation`, `contract_tests` and
  `subtree_stability` — it does not record signatures, so there is nothing in it to
  compare against, and `get_molecule_id`, one of the eleven functions mutilated
  here, has no entry in it at all. The registry belongs in the guard only as the
  waiver: *this signature changed — is the change declared?*

- `devtools/scripts/validate_docstrings.py` gains, or is paired with, a check that a
  documented parameter list matches the actual signature in both directions. Today
  it can only detect a missing docstring, not a docstring that ate its function.

  This is worth doing and **it does not close this report**. Bidirectional
  validation detects only *disagreement* between docstring and signature, and this
  generator does not produce disagreement: it rewrites both, consistently. The
  damaged `get_component_type` reads

  ```python
  def get_component_type(molecular_system, element='atom', ...):
      """
      element : {'atom', 'group', ...}, default='atom'
  ```

  Signature and docstring agree on `'atom'`; the correct default was `'component'`.
  Any bidirectional check passes here, and the function silently returns one type
  per atom instead of one per component. Only comparison against the previous
  version catches the third shape of damage.

## Dependencies and risks

The obvious guard — reject any signature change — is too strict: deliberate API
changes are legitimate and the stability registry already records them. The guard
must key on *unrecorded* changes, or it will be disabled the first time someone
makes an intentional one.

Related, not blocking: [uibcdf/molsysmt#170](https://github.com/uibcdf/molsysmt/issues/170)
(ruff cannot see `molsysmt/form`) and
[uibcdf/molsysmt#171](https://github.com/uibcdf/molsysmt/issues/171) (no automatic
workflow runs the suite). Each independently would have caught this; together their
absence is why it survived a day on `main`.

## Provenance

Host: this development checkout, molsysmt at
`51102b03e` (baseline) and `e7f2e8ce9` (repaired). Python 3.13.14, pytest with
`-n 14 --dist loadfile`, `--receptor=llm`. 2026-08-18.
