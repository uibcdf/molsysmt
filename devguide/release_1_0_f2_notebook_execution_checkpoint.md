# F2 Notebook-Execution Audit Checkpoint

**Date:** 2026-07-28  
**Stage:** F2 — applicable Common Core and changed-behavior notebook execution  
**Status:** `IN PROGRESS`  
**Repository mutation during execution:** none

## Scope Reconstruction

F2 requires the complete 20-notebook Common Core plus every course notebook
affected by current API or behavior changes. Comparing the course at the F1
migration commit `f5d96218b` with the current tree identifies 20 changed
notebooks:

- three Common Core notebooks;
- four MolSysBuilder path notebooks;
- four PDB Frontier path notebooks;
- four Trajectory Management path notebooks;
- four Performance Optimization path notebooks;
- one Scalability path notebook.

The union of the complete Common Core and those changed notebooks is therefore
**37 notebooks**: 20 Common Core plus 17 additional Path notebooks.

The two earlier ledger entries saying that five lifecycle notebooks executed
belong to the MolSysBuilder vertical. They do not prove this F2 union. Embedded
execution counts are also not accepted as exact-current-commit evidence:
outputs are cleared from most course notebooks and no durable execution
artifact records the complete F2 selection.

## Audit Method

The audit loaded notebooks with `nbformat` and executed them in memory through
`nbclient.NotebookClient`, using a fresh Python kernel per notebook, a 90-second
cell timeout, and the notebook's own directory as its working directory.
Executed notebook outputs were not written back to the repository.

The first pass selected 26 deterministic, noninteractive notebooks. Eleven
were deliberately deferred because their code requires a PDB download, a live
viewer interaction, or both. A sandbox-only kernel socket denial occurred on
the first attempt; it was an infrastructure refusal before any cell executed
and is not counted as a notebook result. The run was repeated with permission
to start local Jupyter kernels.

## Results

### Deterministic execution

- **14 passed**
- **12 failed**
- **0 repository files changed**

Passing notebooks:

- Common Core: 03, 07, 08, 10, 12, 17, and 20;
- Alzheimer Path: 28;
- Enzyme Path: 28 and 49;
- Antiviral Path: 28 and 49;
- Biophysics Path: 28 and 49.

The four currently affected MolSysBuilder path notebooks all pass, confirming
the useful part of the earlier five-notebook lifecycle evidence.

### Deterministic failures

| Notebook | Observed failure | Initial ownership classification |
| --- | --- | --- |
| Core 02 — Native Forms | `MolSys -> TopologyDict` conversion is not implemented | notebook expectation or conversion-delivery decision |
| Core 09 — System Modification | scalar `chain_id='PROTEIN'` rejected by digestion | API/digestion contract requires investigation |
| Core 13 — Iterating | `element='structure'` rejected | notebook uses a noncanonical element term |
| Core 16 — Comparing | `AxisError` inside comparison | probable library defect |
| Core 18 — Merging | internal `merge(..., keep_ids=...)` keyword mismatch | probable library/decorator contract defect |
| Core 19 — Extraction and Removal | `NotImplementedMethodError` during the demonstrated workflow | form/method delivery gap requires attribution |
| Alzheimer 47 — Trajectory Management | `TypeError: unhashable type: 'list'` | composite-system trajectory path requires investigation |
| Alzheimer 48 — Scalability | `chunk_size` rejected as an attribute | notebook uses an obsolete iterator contract |
| Alzheimer 49 — Performance | root `molsysmt.get_distances` no longer exists | notebook uses an obsolete API location |
| Enzyme 47 — Trajectory Management | requests the last 50 structures from a 20-structure fixture | notebook data assumption is invalid |
| Antiviral 47 — Trajectory Management | `TypeError: unhashable type: 'list'` | composite-system extraction requires investigation |
| Biophysics 47 — Trajectory Management | missing `popc_membrane.h5msm` demo-manifest key | notebook/demo-asset mismatch |

These classifications are triage, not fix decisions. Each probable library
failure must be reproduced through the public API before changing either code
or documentation.

### Deferred execution

Eleven notebooks remain unevaluated in this pass:

- network only: Core 01, Core 14, Core 15, and the four Path 29 PDB Frontier
  notebooks;
- interactive only: Core 05, Core 06, and Core 11;
- network plus interactive: Core 04.

F2 must not report these as passing based on static inspection or stored
outputs. Network examples should preferentially use bundled systems when the
lesson does not specifically teach remote acquisition. Interactive notebooks
need an explicit headless/noninteractive validation contract rather than a
fake click selection.

## Resume Point

Resume F2 in this order:

1. reproduce and classify the 12 deterministic failures individually;
2. fix library defects where the documented behavior is valid;
3. update obsolete notebook calls or invalid fixture assumptions where the
   library contract is already correct;
4. rerun the 26 deterministic notebooks from clean kernels;
5. design and execute the network and interactive validation lane for the
   remaining 11;
6. record exact commit, environment, selection, and results in a durable F2
   closure artifact before marking the stage `DONE`.

F2 is not blocked: it is a bounded active stage with explicit remaining work.
The formal release-plan completion remains 90% because Segment F earns weight
only when its complete exit gate passes.
