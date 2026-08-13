---
summary: Declared selection syntaxes are not implemented consistently.
issue: uibcdf/molsysmt#148
status: resolved
opened: 2026-08-13
closed: 2026-08-13
severity: medium
verification: reproduced
area: [selection, api, docs]
guard: tests/basic/select/test_syntax_capabilities.py
normative: devguide/api_surface.md
blocked_by: []
supersedes: []
---

# Declared selection syntaxes that are not implemented

**Role:** resolved defect. **Written:** 2026-08-06, by the MolSysViewer side,
after a downstream README claim could not be verified. **Resolved:** 2026-08-13
with an executable, directional registry shared by validation, dispatch tests,
public introspection, and documentation.

## The problem

`molsysmt/supported/syntaxes.py` declares seven selection syntaxes. Four of the
fourteen `(syntax, direction)` cells work. The remaining ten fail, in four
distinct ways, and one of them — `MDAnalysis` — is named in the user
documentation as available.

The argument digester accepts all seven: `digest_syntax` validates against
`lowercase_syntaxes`, so `syntax='ParmEd'` passes validation and then fails
inside `select`. A user reads acceptance by the validator as a promise.

## Evidence

Measured on 2026-08-06 against the working tree, from
`msm.systems['T4 lysozyme L99A']['181l.bcif.gz']` converted to
`molsysmt.MolSys`. `select` was called with a dialect-appropriate query;
`to_syntax` was called with `atom_index in [0,1,2]`.

| syntax | `select(syntax=…)` | `select(to_syntax=…)` |
|---|---|---|
| `MolSysMT` | **ok** (1289 atoms) | `NotSupportedSyntaxError` |
| `MolSysMT_NEW` | `NotSupportedSyntaxError` | `NotSupportedSyntaxError` |
| `Amber` | `NotImplementedMethodError` | `NotImplementedMethodError` |
| `MDAnalysis` | `NotImplementedConversionError` | `NotImplementedMethodError` |
| `MDTraj` | **ok** (1289 atoms) | **ok** → `'index 0 1 2'` |
| `ParmEd` | `NotSupportedSyntaxError` | `NotSupportedSyntaxError` |
| `NGLView` | `NotImplementedMethodError` | **ok** → `'@0,1,2'` |

Source of each outcome, in `molsysmt/basic/selector/`:

- **`ParmEd` and `MolSysMT_NEW`** are absent from both `_dict_select` and
  `_dict_indices_to_selection`, so `select` raises `NotSupportedSyntaxError`
  for a value the digester just accepted. The declared list and the dispatch
  tables are two independent sources of truth that disagree.
- **`Amber`** is a stub: both `amber.select` and `amber.indices_to_selection`
  raise `NotImplementedMethodError` unconditionally.
- **`NGLView`** is asymmetric by construction:
  `nglview.indices_to_selection` is fully implemented (atom, group and chain
  levels), while `nglview.select` raises. Translation out works; parsing in
  does not.
- **`MDAnalysis`** is the interesting one. `mdanalysis.select` is *complete* —
  it converts to `MDAnalysis.Universe` and calls `select_atoms`. It fails only
  because the conversion is missing. Three forms convert to
  `MDAnalysis.Universe` (`MDAnalysis_Universe`, `MDAnalysis_AtomGroup`,
  `file_pdb`), against **twenty** that convert to `mdtraj.Topology`. That ratio
  is the whole difference between the two dialects.
- **`MolSysMT`** is absent from `_dict_indices_to_selection`, so indices cannot
  be translated into MolSysMT's own syntax. This may be deliberate; it is not
  stated anywhere.

**Evidence label: implemented / not implemented as tabulated above. No cell is
contract-tested across input forms** — see the next section.

## Why CI does not see it

`tests/basic/select/test_public_input_errors.py` covers `syntax="MDAnalysis"`
in two tests, and both pass. They use the `t4_pdb_file` fixture — a PDB file,
which is exactly one of the three forms that can reach
`MDAnalysis.Universe`. From a `molsysmt.MolSys`, the form the library is built
around and the one downstream viewers hold in memory, the same call raises:

```
NotImplementedConversionError: No conversion implemented from
'molsysmt.MolSys' to 'MDAnalysis.Universe'
```

The tests are not wrong; they are single-form. The gap is invisible because no
test walks `supported.syntaxes` against more than one input form.

## Why it reaches users

`docs/content/user/foundations/language/selection_grammar.ipynb`
(`Introduction_Selection`) states:

> The `syntax` argument can delegate a query to another installed ecosystem
> parser, including `MDTraj` and `MDAnalysis`.

`MDTraj` is true from any form. `MDAnalysis` is true only from a PDB file or an
MDAnalysis object. Per `DOCUMENT_POLICY.md` ("current code and executable tests
take precedence over prose"), this is a documentation defect *or* a software
defect, and the choice between those two readings is the decision this proposal
asks for.

The reach is not limited to MolSysMT. MolSysViewer exposes `syntax=` on its own
public surface (`view.regions.add(..., syntax=…)`, `make_regions_by`,
`view.hide/show`) and digests it against **this** list, so every declared-but-
absent dialect is re-promised downstream. We are correcting our own README to
name only `MolSysMT` and `MDTraj` until this is resolved.

## Proposed outcome

Three options, not mutually exclusive. The recommendation is **A + C now, B on
its own merit**.

**A. Make the declared list mean something.** Derive `syntaxes` from the
dispatch tables, or assert at import time that every declared syntax has an
entry in at least one direction, with the direction recorded. A user who passes
`syntax='ParmEd'` should be refused by the digester with a message naming the
dialect and the reason — not by a `NotSupportedSyntaxError` raised deep inside
`select` after validation has already said yes.

**B. Implement `molsysmt.MolSys` → `MDAnalysis.Universe`.** This is the single
change that makes the documented promise true, since every other form can reach
`MolSys`. It is a real conversion with fidelity obligations (topology,
elements, charges, box), so it belongs to the conversion-fidelity work in
`conversion_fidelity_and_molsysdict_v1.md`, not to a documentation fix. It
should not be started to close this report.

**C. State the asymmetry where the user reads it.** `Introduction_Selection`
should carry the matrix above, or its honest summary: parsing *in* is available
for `MolSysMT` and `MDTraj` from any form and for `MDAnalysis` from PDB files
and MDAnalysis objects; translating *out* is available for `MDTraj` and
`NGLView`.

### Exclusions

Implementing `Amber` or `ParmEd` parsing is **not** proposed. Neither is
removing `MolSysMT_NEW`, whose presence in the list looks like in-flight work
this document has no visibility into. If the answer for a dialect is "never",
deleting it from `syntaxes` is cheaper than any of the above.

## Acceptance criteria

1. A coverage test parametrised over `supported.syntaxes` × {`select`,
   `to_syntax`} × at least {`molsysmt.MolSys`, a file form}, asserting each cell
   is either *implemented* or raises a **specific, dialect-naming** error. The
   test encodes the matrix, so any future divergence between the declared list
   and the dispatch tables fails CI instead of surfacing to a user.
2. No syntax passes `digest_syntax` and then fails with
   `NotSupportedSyntaxError` inside `select`.
3. `Introduction_Selection` agrees with that test.
4. If B is done: parity-tested against `MDTraj` selections on the same system,
   not merely implemented.

## Risks and dependencies

- Deriving `syntaxes` from the dispatch tables changes what `digest_syntax`
  accepts. Any caller passing a dialect that only ever failed later will now
  fail earlier and more clearly, but the exception *type* changes. That is an
  API-visible change and belongs in `api_stability_registry.md`.
- Option B depends on MDAnalysis being installed; the conversion must stay
  optional and must not become an import-time dependency.

## Resolution — 2026-08-13

MolSysMT now distinguishes selection input from selection-translation output.
The accepted input syntaxes are MolSysMT, MDTraj, and MDAnalysis; the accepted
outputs are MDTraj and NGLView. The registry records the conditional conversion
scope of each direction, and the digesters reject every unavailable direction
before dispatch.

`msm.supported.syntaxes()` exposes that matrix. The historical
`molsysmt.supported.syntaxes` data-module import remains compatible for
MolSysSuite consumers, including MolSysViewer, and remains callable if Python
binds the submodule onto the parent package. The User Guide, public docstring,
support table, and Common Core module 07 now state the same contract.

Implementing a broad `molsysmt.MolSys -> MDAnalysis.Universe` conversion remains
conversion-fidelity work; this fix does not falsely generalize its scope.

---

## Appendix — unrelated defect found while measuring

Not part of this proposal; found on the way. **Resolved and archived as
[`form_conversions_importing_nonexistent_modules.md`](../archive/resolved_bugs/form_conversions_importing_nonexistent_modules.md)**,
where it turned out to be three cases rather than one. Kept here in summary only.

`molsysmt/form/file_prmtop/to_molsysmt_MolSys.py` imports a module that has
never existed in that form directory:

```python
from .to_molsysmt_Structures import to_molsysmt_Structures   # line 8
```

`git log` shows no `file_prmtop/to_molsysmt_Structures.py` at any point. The
name is also never used in the function body — the code below it builds an
empty `Structures()`, with a comment explaining that a prmtop carries only
topology. So the import is dead **and** fatal: every
`file:prmtop → molsysmt.MolSys` conversion raises

```
ModuleNotFoundError: No module named 'molsysmt.form.file_prmtop.to_molsysmt_Structures'
```

Deleting the line appears to be the whole fix. Reproduced with
`msm.convert(msm.systems['pentalanine']['pentalanine.prmtop'], to_form='molsysmt.MolSys')`.
