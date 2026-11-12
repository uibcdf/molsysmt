---
summary: Demo catalog contradicts bundled source identities and structure counts
issue: uibcdf/molsysmt#715
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
area: [docs, data]
guard: tests/test_demo_catalog.py
normative:
blocked_by: []
supersedes: []
---

# Aligning the demo catalog with its bundled evidence

## What

The Python catalog and generated notebook describe 1L2Y as 20 structures;
both PDB MODEL records and native coordinate metadata establish 38. The 1CEN
title/summary identify CENP-B, whereas the deposited COMPND/TITLE declare
CELLULASE CELC complexed with cellohexaose. The 1L17 PDB description calls it
apo L99A; its SEQADV instead records Ile3Val, and PDB/native groups retain VAL3
and LEU99. The collection key groups distinct examples, not identical systems.

Additional inspected discrepancies are the 35-amino-acid villin summary versus
36 in 1VII SEQRES/ATOM records, a named native villin trajectory with one stored
structure, and the XYZNpy description implying one plain NPY array instead of
consecutive shape and coordinate records. The notebook also advertises every
tutorial and suite as completely offline, beyond what bundled data guarantees.

## How

Human-facing fields in molsysmt/systems.py are written independently of the
bundled records. The notebook's generator reflects them faithfully, so successful
execution cannot establish their scientific correctness. Its stored output
inherits these mistakes. Current root is b5e10d8e2; no scientific data have been
changed to fit the catalog.

## Why

A user may select or report the wrong molecular example, confuse amino-acid
counts with structure counts, or assume file representations share identical
axes. Correct source identity and scope matter for reproducible examples.

## Evidence and scope

Use deposited PDB title/compound/sequence declarations, metadata-only H5MSM
coordinate shapes and small XYZNpy record reads. The 149,640 OpenMM PDB atom
records, alanine's 22 atoms and caffeine SDF's 24 atoms agree with their stated
counts. Small BCIF 2NZT metadata supports human hexokinase II and its deposited
glucose-related ligands; no ligand inhibition/protonation model is certified.
This bounded review does not establish every biological/functional claim in
the full catalog or exact equivalence between different file realizations.

Keep dictionary/file keys and data bytes. Correct the descriptions and the
notebook terminology/offline and legacy-format limits, retaining its six cells,
anchor and dynamic generator. Re-execute that actual notebook through the
maintained runner with one worker, then inspect the produced article. No parser,
scientific method, molecular preparation, dependency or public API is added.
Ackredit has no new third-party algorithm to register in this correction.

## Acceptance

- Source-backed public descriptions identify the corrected molecular examples
  and declared structure/amino-acid counts; baseline negative cases fail before
  the correction and positive controls remain meaningful.
- The catalog notebook actually executes, including the bundled native query;
  its rendered output comes from systems.info/categories and covers registered
  entries/files, not manually edited HTML results.
- Existing data/file keys and input bytes remain unchanged.
- Relevant local tests, notebook schemas, documentation links/HTML and lint pass;
  original failed attempts and bounded resource observations remain available.

## Provenance

2026-11-11; Linux/Python 3.14.7. Read-only source inspection, PDB streaming line
counts and HDF5 metadata, with no full molecular trajectory materialization.
The first private XYZNpy probe incorrectly assumed a structured dtype; inspecting
the existing adapter and both real NPY records corrected that probe. This is
not a parser failure. Source receiving uses the previously declared pinned
support/client composition; installed/final-candidate acceptance remains paused.

## Bounded receiving

The source-backed baseline has eight failures and three positive controls. The
same catalog guards after correction pass eleven cases; an overlapping PDB
example complement adds two passing cases. Baseline failures remain retained.
The actual catalog notebook executes through the maintained runner with one
worker and --force; its two cells complete, and its output contains 304 atoms,
20 groups and 38 structures. All 27 systems and 64 file explanations exactly
match the current metadata. No rendered table was manually replaced.

The six notebook cells, hidden generator tag and generator code survive. Registry
keys, file keys and all non-metadata Python AST in systems.py are unchanged.
The checked bundled data and qualified native binary retain their byte hashes.
The code-fingerprint guidance is also reconciled with the existing runner:
imported metadata changes require forced execution, and a skipped/upgraded mark
cannot prove the catalog was regenerated. This changes no execution algorithm.


Five existing notebook-runner CLI controls and all fifteen fast release checks
also pass, with applicable Ruff checks. The corrected cohort and actual notebook
keep the source/native/input hashes unchanged during their execution. The
initial count audit reads metadata or streams records; the actual notebook
then assembles the small 38-structure Trp-Cage example intentionally. These are
separate scopes, not a claim that every operation avoids coordinate reads.
Complete strict HTML on clean af4ac5daa finishes with zero warnings. The actual
article matches all 27 systems and 64 file descriptions and preserves its
eight internal references/anchors, visible native result and hidden generator.

## Resolution — 2026-11-11

Implementation af4ac5daa changes catalog descriptions and documentation, not
molecular data, registry/file keys or non-metadata Python logic. The selected
guard independently reads deposited compound/sequence labels, atom records,
coordinate-axis metadata and record layouts before comparing the public claims.
It therefore rejects the actual wrong identities/counts instead of merely
requiring headings or particular output formatting. Eight original failures,
three original positive controls and the later thirteen passing cases are retained.

The actual notebook is forced through the maintained runner: two code cells
complete, its generator code stays unchanged and the run mark records that
execution. The runner guide now accurately explains code fingerprints and why
changes in imported catalog data require --force. Five existing runner CLI
controls, fifteen fast release gates, queue checks and applicable Ruff checks pass.
The first HTML-inspection probe failed on a newline inside a two-word phrase;
normalizing inspection whitespace corrected the probe without changing content.

The bounded HTML service uses one CPU, a 2-GiB hard memory cap and no own swap.
It peaks at about 1.65 GiB, keeps at least 13.82 GiB host memory available and
records no memory-high/max/OOM events or reserve stop. Earlier focused phases
stay below 0.39 GiB. Source/data/native input hashes remain unchanged within
each phase; the source attribution explicitly records the dirty b5e10d8e2
worktree delta later committed as af4ac5daa.

The [receiving receipt](../../../devtools/data/demo_catalog_receiving_715_20261111.json)
contains exact scopes, versions, input/artifact hashes, original failures,
commands and resource observations. The complete source suite remains received
only at 6acad4f35; these later metadata/guard changes have their own focused
receiving. Broader #378, #713/#615 causality, format freeze, published dependency
floor, exact final pair and installed/platform gates remain open. No release
or publication is authorized by this documentation correction.
