# PDBQT resident and indexed storage measurements

**Role:** operational measurements for uibcdf/molsysmt#434.
**Date:** 2026-10-23. Source/dependency identities and individual trials are in
[the JSON receipt](../../devtools/data/pdbqt_storage_benchmark_20261023.json).

## Reproducing the comparison

From the repository root and its development environment:

```bash
python devtools/scripts/benchmark_pdbqt_storage.py --output /tmp/pdbqt-storage.json --structures 256 2048 8192 --atoms 64 --chunk 16 --repeats 2
```

The generator writes each synthetic model separately. Each trial uses a fresh
interpreter; a different four-model fixture warms imports, unit handling,
native metadata and file-copy machinery before recording the baseline.
Actual handler opening then validates every model. Source hashes must remain
unchanged throughout measurement. Temporary inputs/outputs are cleaned, and
fixture hashes and dimensions are retained. These are storage fixtures, not
independent chemical ground truth or docking trajectories.

Page-cache state is uncontrolled. Opening is a cold **handler** operation,
not a cold-disk benchmark. Two repetitions support these bounded observations,
not a statistical regression threshold or a universal speed claim. Linux
VmRSS and resource high-water marks are reported separately. The latter
includes opening, queries, sequential traversal and streamed file copying.

## Dated measurements

The table reports medians. Additional peak is `peak_bytes - baseline_peak_bytes`
within each trial, converted to MiB; it is not total process memory. The common
imported/warmed runtime itself occupies approximately 168 MiB here.

| Structures × atoms | Input MiB | Resident additional peak MiB | Indexed additional peak MiB | Resident opening s | Indexed opening s |
| --- | ---: | ---: | ---: | ---: | ---: |
| 256 × 64 | 1.24 | 3.29 | 2.52 | 0.267 | 0.293 |
| 2,048 × 64 | 9.92 | 19.84 | 3.59 | 2.222 | 2.371 |
| 8,192 × 64 | 39.67 | 79.38 | 5.44 | 8.457 | 8.999 |

For the largest input, total measured peak is approximately 246.9 MiB resident
and 172.8 MiB indexed. Retained VmRSS growth immediately after opening is
approximately 42.0 MiB versus 3.0 MiB. Both retain model indexes and IDs;
indexed storage avoids the complete source text and its decode buffers.

For that same case, a four-structure nonconsecutive/repeated query takes a
median 4.00 ms resident versus 4.32 ms indexed. Traversing all structures in
16-structure blocks takes 7.34 s versus 7.72 s; full byte-preserving file copy
takes 34.6 ms versus 53.9 ms. The first 16-structure query after opening takes
14.8 ms versus 16.0 ms. Time to the first usable block includes the 8.5–9.0 s
opening/validation cost; query-only timing must not conceal that work.

## Interpreting the result

Indexed storage trades modest additional file/stat operations for substantially
lower working memory in this profile. It does not make full validation constant
time or uniformly beat resident access. Reuse an indexed handler for repeated
queries: convenience calls on a file path open and validate their own resources,
and the universal facade may perform several metadata queries during setup.

Resident input remains appropriate when the whole source is small and an
independent snapshot is desired. Text input is already resident; distinguish
its caller-owned text from additional working memory. Explicit complete text,
coordinate or native-system outputs necessarily materialize their requested
results. The mapped known-source `read_poses` remains an eager reader.

The indexed working set includes structure ranges/IDs, one parsed reference
model, preserved preamble metadata, a current model and requested coordinate
blocks. Very large individual models or metadata can dominate that bound.
There is no memory mapping, persistent index, compressed-file random access,
or claim that the whole process uses only the coordinate array size.

## Durable guards

`tests/native/test_pdbqt_indexed_file_handler.py` checks selected byte ranges,
absence of resident read_bytes on file iteration, no complete text payload on
file copying, source-change rejection, independent descriptor leases, concurrent
queries, interruption and atomic destination preservation. Its allocation guard
opens a larger ensemble under tracemalloc and rejects source-sized text copies;
the separate RSS measurements above observe the actual process footprint.

Original Vina files and a live generated Vina ensemble supply bounded real-input
and coordinate-reference controls. These do not certify arbitrary PDBQT dialects,
chemical preparation, every platform, or installed release artifacts.
