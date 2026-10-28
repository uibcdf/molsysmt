---
summary: Expose source-preserving FASTA ingestion for downstream consumers.
issue: uibcdf/molsysmt#513
status: resolved
opened: 2026-10-28
closed: 2026-10-28
verification: reproduced
area: [form]
guard: tests/form/file_fasta/test_source_records.py
normative:
blocked_by: []
supersedes: []
---

# Source-preserving FASTA ingestion

## What

PeptideMT needs original record text and occurrence correspondence before its
own scientific admission. Ordinary FASTA-to-SeqRecord conversion legitimately
removes whitespace and does not carry the original text. This is an additive
format-ingestion capability, not a normalization defect or a new sequence class.
Consumer ownership and migration are tracked by uibcdf/peptidemt#5.

## Inspected basis

The existing public file:fasta adapter delegates normalized conversions to lazy
Biopython SeqIO. The exact PeptideMT W1 `inputs.py` source cited by the issue
was inspected at 4901130bdb1b1277004b616eff2742b87e72c6e8. It preserves full
headers, raw record text, case, whitespace, stops and leading M; scientific
alphabet/length/chemistry checks remain consumer-owned. There is no local
PeptideMT checkout, and no consumer code or dependency is changed here.

## Chosen boundary

Expose `msm.form.file_fasta.parse_records(fasta_text, source_label=None)` and
`read_records(item)` as documented public adapter tools, with argument digestion
and explicit skip controls. They return a JSON-compatible
`molsysmt.fasta_source@1` dictionary containing an opaque source label, verbatim
blank preamble and ordered records. Each record contains its source record
index, complete header, joined unnormalized sequence, verbatim record text and
half-open character span into the original decoded input. This is not a new
molecular-system form or chemical assignment store.

Only CR/LF/CRLF line terminators are removed from the joined sequence view.
Everything else is retained, including blank/duplicate headers, repeated/empty
sequences, spaces, lowercase, stop/modification symbols and leading M.
Nonblank content before the first header rejects with FormatError rather than
losing an unnamed occurrence. Blank preamble and empty input remain observable.
File reading uses strict UTF-8 without newline translation; decoding failures
retain their cause. These tools do not normalize, validate a biological alphabet,
construct topology/coordinates, deduplicate or invoke Biopython. Existing
normalized conversions remain untouched.

## Acceptance

Focused tests must protect complete round-trip text reconstruction, source spans,
occurrence order, repeated/empty records, CR/LF/CRLF and mixed line endings,
Unicode, whitespace/symbols/case, malformed preambles, explicit input errors,
file/text parity and missing-file/decoding behavior. A clean subprocess must
prove the new route works while Bio imports are denied. Retain the old public
conversion's normalized sequence values in an independent regression.

Documentation covers the public adapter, conceptual source correspondence,
sequence-comparison recipe and relevant course module. Provider implementation
is distinct from consumer migration, installed package qualification and 1.0.

## Resolution — 2026-10-28

Accepted and implemented at the chosen public adapter boundary. Both tools
reuse one private record-boundary interpreter; file and text paths have the
same schema and preserve original input without requiring an optional engine.
No consumer scientific policy, Bio parser or new molecular form is copied into
this capability. The contract is bounded record ingestion, including literal
sequence comments/symbols, not universal FASTA dialect or alphabet admission.

The first regression run found the expected absent public capability (22
failed, one old-conversion test passed). The implemented direct cases and both
public doctests pass (25 cases). The complete FASTA adapter suite plus doctests
passes 53 cases with Pytest Receptor and 12 workers. Tests protect the full
text reconstruction, raw source spans, newline/Unicode edge cases, repeated
and empty records, unsupported inputs and independent outputs. A fresh Python
subprocess blocks every Bio import and still reads a file successfully. The
old public normalized SeqRecord conversion remains unchanged, including spaces,
case, full descriptions, repeated records, empty sequences and leading M.

Docstrings define every schema field and the deliberate line-joining view.
The six-cell FASTA form page retains its structure and now includes the public
reader contracts. The Topology foundation and sequence comparison recipe
separate source occurrence indices from molecular group indices. Course
Module 13 adds a small executed text-only example and its function inventory;
other biological code/outputs are retained and not reexecuted. The full strict
parallel Sphinx build passes without warnings or notebook errors. Existing
source-wide schema and heading checks pass; dependency leakage, adapter
contracts, public signatures, docstrings and Ruff are checked before closeout.

This is a resident reader: it retains raw and joined sequence views in memory;
no streaming, H5MSM persistence, topology construction or performance claim is
made. UTF-8 is explicit, no filename/label authenticates molecular identity,
and character spans are not byte offsets. Consumer migration and dependency
qualification remain open in uibcdf/peptidemt#5. Availability in committed source
does not publish a package or establish a released minimum dependency version.
