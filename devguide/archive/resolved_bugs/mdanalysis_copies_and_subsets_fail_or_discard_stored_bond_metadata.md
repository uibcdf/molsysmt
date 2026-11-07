---
summary: MDAnalysis copies and subsets fail or discard stored bond metadata
issue: uibcdf/molsysmt#628
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [form, metadata, extract]
guard: tests/form/MDAnalysis_Universe/test_copy_and_subset_metadata.py
normative:
blocked_by: []
supersedes: []
---

# MDAnalysis copies fail and subsets discard stored bond metadata

**Reported:** 2026-11-06 during the optional-provider review under #524.
**Status:** Source correction and paired actual-provider receiving complete;
public delivery and board closeout follow.

## What

For an MDAnalysis Universe with explicitly stored bond orders, type labels and
mixed guessed flags, full public extraction and conversion back to the same form
discard those declarations. Reordered AtomGroup views and selected structures
have the same problem. Stored forces are omitted during materialization.

A source containing orders `[1.5, 2, None]`, types `['aromatic', 'opaque-class',
'dative']` and guessed flags `[False, True, False]` returned orders
`[None, None, None]`, byte labels `[b'aromatic', b'opaque-c', b'dative']` and flags
`[False, False, False]`. A missing type could instead erase all labels. The source
object and reader cursor remained unchanged.

Independent copying failed separately. `msm.copy(universe)` raised
`TypeError: __deepcopy__() takes exactly 0 positional arguments (1 given)`.
`msm.copy(atomgroup)` raised `AttributeError` because that form had no copy adapter.

The public regressions are addressable through:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/form/MDAnalysis_Universe/test_copy_and_subset_metadata.py
```

## How

The shared owner, `molsysmt/form/MDAnalysis_Universe/_subset.py`, used
`MDAnalysis.Merge` to construct a topology. That provider route omitted connection
orders and guessed flags, and converted type labels to fixed-width `S8` bytes.
The adapter copied coordinates, velocities, cells and time into `MemoryReader`,
but omitted forces.

The Universe copy adapter used Python `deepcopy`, reaching a provider Timestep
copy hook incompatible with the memo argument. The AtomGroup form did not export
a copy operation.

The local repair uses the provider's independent Universe copy protocol for full
copies. AtomGroup copying returns its original ordered view on an independent
parent, retaining unselected parent atoms as context. Extraction and same-form
conversion materialize selected atoms through the existing shared subset owner.
Retained connections receive detached source orders, type labels and guessed
flags by mapped endpoints, without interpreting them or reconstructing native
chemistry. The selected reader also retains represented forces. Selecting
structures does not copy the complete parent trajectory before selecting them.
Uniform and reversed time axes, source cursor restoration and the existing typed
rejection of irregular selected times remain intact.

Both public copy wrappers expose the standard `skip_digestion=False` control and
include deterministic topology-only examples. A separate supplemental regression
module, `tests/form/MDAnalysis_Universe/test_copy_connection_ownership.py`, contains
10 public bond-addition ownership cases. These are separate from the original
30-case counterexample baseline and do not change its frozen file.

## Why

These are ordinary independent-data operations. Losing numerical order, an
unrecognized source label or the distinction between stored and guessed
connectivity changes the evidence available to later consumers. Truncation makes
some recorded labels impossible to recover. Chemical perception cannot recover
the original declaration or substitute for copying it.

## What is measured and what is assumed

**Reproduced:** small public calls against the official MDAnalysis 2.8.0 CPython
3.12 wheel and installed MDAnalysis 2.10.0 produced the same loss and copy
failures. The matrix covers Universe and AtomGroup copying, full and partial
extraction, same-form conversion and AtomGroup-to-Universe conversion. Every
source snapshot remained unchanged.

**Native baseline, executed by the coordinating agent before production edits:**
the command above returned exit 1 with **26 failed and 4 passed**. Failures comprise
18 lost/truncated bond-field cases, 4 lost-force cases, 2 cases where a missing
type erased peer labels, and the two independent-copy failures. The four identity
cases with `copy_if_all=False` passed. The test file was frozen at SHA-256
`ece4d0dae0cc15215cebca19a30c0cc4ce38454b2c32d362658b70a745986afa`.

Local baseline evidence is retained under
`.pytest_cache/pre1-review-20261106/628-copy-subset-counterexamples.xml` and
`628-copy-subset-counterexamples-invocation.json`. The
`providers/mdanalysis-review/` child directory holds verified wheel acquisition,
public snapshots, source inspections and failed preliminary probes.

**Inspected, not executed:** upstream source at
`f44c1e09001791b302840f90390275d11ef69497` retains the same Merge loss mechanism.
That inspection is not an executed qualification of the 2.11.0 release.

**Implemented, not qualified:** the bounded repair and documentation changes are
present locally. Passing repaired pytest results are not yet claimed.

**Wrapper examples executed without pytest:** the two deterministic copy
docstrings produced 10 attempted examples and zero failures on each of the
2.8.0/Python 3.12 and 2.10.0/Python 3.14 profiles. Their small doctest-runner
receipts are `copy-doctests-candidate-2.8.0-py312.json` and
`copy-doctests-current-2.10.0-py314.json` in the provider review cache. These results
do not replace the coordinator's full regression qualification.

## What was refuted

Raising the floor to a recent installed version does not fix this mechanism:
public 2.8.0 and installed 2.10.0 exhibit it, and current upstream source still
omits the fields. The NumPy-compatible minimum review remains owned by #524.
Routing through native MolSysMT chemistry would also be inappropriate: the
operation must retain opaque provider labels without interpreting them.

The possibility that provider copies alias connection annotation lists was
tested rather than inferred. Real 2.8.0/Python 3.12 and 2.10.0/Python 3.14 probes
covered 10 routes each: provider topology and Universe copies, public Universe
and AtomGroup copies, full extraction, and all-atom structure selection, including
topology-only inputs where meaningful. Every output had distinct connection
value/type/order/guessed containers. Calling public `add_bonds` on each output
left all source values and annotation lengths unchanged. The evidence files are
`copy-ownership-candidate-2.8.0-py312.json` and
`copy-ownership-current-2.10.0-py314.json` under the provider review cache. This
refutes that alias hypothesis on the observed providers; no additional full-copy
reconstruction was introduced. These small probes are not pytest qualification.

## Scope and exclusions

The scope is independent Universe and AtomGroup operations retaining labels,
formal charges, connection metadata, and represented coordinates, velocities,
forces, cells and time. AtomGroup selections retain local index meaning and
external atom order; structures follow their requested order. Provider units,
source arrays and the source reader position are protected.

No bond perception, force-field assignment, native-domain reconstruction,
dependency-floor change or new reader is introduced. Arbitrary application
attributes and provider subclass extensions need their own preservation
contract. Explicit empty atom or structure subset selections remain unsupported
by the in-memory materializer; copying a complete topology-only Universe does not
fabricate structures. Irregular selected time axes remain explicitly unsupported
instead of being replaced with fabricated uniform time.

## Acceptance criteria

- The frozen public regressions pass on the actual public minimum-candidate and
  current-provider profiles, with native process results retained by the coordinator.
- Copying, extraction and same-form conversion preserve exact stored values and
  independence. A missing type does not erase another bond's type.
- Existing MDAnalysis structural, subset, PDB-writing and parity tests pass,
  retaining current selections and explicit time-axis restrictions.
- User Guide, form, Cookbook and shared course guidance match the supported
  operations. Existing code examples and outputs remain unchanged.
- Relevant Ruff, dependency-laziness and documentation/reporting checks pass.

## Dependencies and risks

The repair reuses the existing subset owner and public MDAnalysis copy protocol.
Provider acquisition and runtime floors remain separate work under #524. Other
forms and native chemical stores are outside this change. The provider's full
copy protocol owns reader copying; selected operations retain the existing
selected-structure materialization boundary.

## Provenance

Linux x86-64, 2026-11-06. Public candidate reproduction: Python 3.12.12, NumPy
2.3.5, official MDAnalysis 2.8.0 wheel SHA-256
`239a1297dc18ef3523941551fc306c356e2215c4b116c2d351e8487b86dc8ced`.
Current-provider reproduction and native baseline: Python 3.14.7, NumPy 2.4.6,
MDAnalysis 2.10.0. Public-call snapshots record local MolSysMT HEAD
`dd60ee7d6855a21f24759def1d387abfbbb6a818`; the frozen baseline precedes the
production repair. No environment was installed, created or downgraded for
provider probes. The repair agent did not execute pytest.

## Resolution — 2026-11-06

Source `f81ba20255e37df2fcc972f9015dcd17f6763d1b` replaces the failing Python
deep-copy route with the provider copy protocol and supplies AtomGroup copy.
Selected materialization restores stored connection types, orders and guessed
flags without interpreting them, and includes available forces. AtomGroup copy
retains an independent full parent context; extract creates a compact selected
Universe. Documentation states that distinction and the existing irregular-time
limitation.

The addressable guard above exercises actual public copying, extraction and
same-form conversion, detached source/context, selected atoms and structures,
nullable and long connection labels and force arrays. Ten additional ownership
cases protect independent connection edits. The suspected provider connection
aliasing was not reproduced on the actual public 2.8/2.10 routes, so no redundant
connectivity rebuild was added.

Root receiving with public MDAnalysis 2.8/Python 3.12/public support floors and
2.10/Python 3.14 passes **155 cases each**, no omissions, native exits zero.
The original 26 failures/four passes remain recorded. A first root selection
exited five because it named a nonexistent test directory; a newer origin
probe incorrectly requested unused fasteners and exited one before pytest.
Both harness mistakes are retained and excluded from passing evidence. The
final minimum overlay exposes only the needed verified fasteners module.
Nine provider PDB-default warnings remain visible in each accepted run.

Shared conversion/descriptor/docs receiving passes 1,271; registered scientific
evidence passes 97 cases for 64 nodes without omissions. Scopes overlap. The
[portable receipt](../../../devtools/data/mdanalysis_runtime_receiving_524_628_20261106.json)
retains source hashes, public artifacts, origins, attempts and limits. Optional
`MDAnalysis>=2.8.0` is declared separately in `33a702bfa638464848a77c57c642627595c759ed`.
That floor addresses consumed NumPy2/controlled-guessing boundaries; it alone
does not repair these consumer defects. This is finite source receiving, not
all-platform, every-reader/writer, installed-package or Viewer qualification.
Public source delivery and actual board closure are recorded separately.
