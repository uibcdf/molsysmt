# Proposal: Selective native format parsers after 1.0

**Status:** post-1.0 proposal
**Priority:** medium; format-dependent
**Scope:** binary trajectory and chemistry file adapters

## Why this proposal exists

MolSysMT currently uses mature optional libraries as parser backends for some
formats. This is appropriate before 1.0 because it reduces implementation risk
and provides a broad compatibility baseline. It also has costs:

- installation and runtime dependencies larger than the requested operation;
- semantic loss when an intermediate object cannot represent source fields;
- additional conversions and memory copies;
- startup or JIT costs outside MolSysMT's control;
- limited control over streaming, diagnostics, and malformed-input policy.

A measured instance of that last cost, recorded on 2026-08-03: MDTraj's DCD reader
announces the detected format with `printf`, on every open **and** on every read,
with no verbosity switch. Reading one DCD attribute produced four lines; a short
loop produced twenty-six. Because the writer is C, the output cannot be captured
with `contextlib.redirect_stdout`; MolSysMT now redirects the file descriptor
around those calls (`_private/backend_output.py`, switchable through
`configure.silence_backend_stdout`). biotraj, a fork of the same plugin, ships
those lines commented out.

This is evidence about diagnostics ownership, **not** a reason to write a parser.
Silencing four lines does not justify owning specification drift, a variant corpus,
fuzzing, and a platform wheel matrix. It does establish one requirement for
whenever a native reader is written: **diagnostics are the caller's to control**.
A native backend must route every message through the MolSysMT catalog with an
explicit verbosity argument, and must never write to standard output on its own.

Native parsers could remove those costs, but owning a parser also means owning
specification drift, edge cases, security review, performance maintenance, and
a permanent compatibility corpus. Native implementation is therefore not an
automatic goal for every supported format.

## Architectural rule

Parser backends remain private behind form adapters. Public functions, form
names, normalized attributes, errors, and native representations must not
depend on which backend parses the bytes. This permits an external backend and
a native backend to coexist during validation and permits later replacement
without an API migration.

An external parser is a byte/record decoder, not the authority for MolSysMT
semantics. The adapter remains responsible for mapping IDs, units, chemical
states, structures, mechanics, provenance, missingness, and unsupported source
features.

## Candidate order

1. **XTC and DCD:** strongest candidates because native chunked decoding can
   improve streaming, dependency weight, and predictable performance. A small
   Rust core should be evaluated for safety and speed.
2. **MOL2:** plausible later candidate because it is textual and the current
   source-token validator already defines part of the contract. Variant syntax,
   property sections, multi-record behavior, and annotation ownership must be
   specified first.
3. **Other textual coordinate/topology formats:** evaluate only when an
   external backend causes measured fidelity, performance, or deployment pain.
4. **Complex cheminformatics formats:** retain mature toolkits unless MolSysMT
   has a concrete differentiating requirement and a sufficient conformance
   corpus.

## Adoption gates for one native parser

A format-specific proposal must provide:

- an authoritative specification and licensing review;
- a corpus covering valid variants, malformed inputs, boundary sizes, and
  third-party-generated files;
- differential tests against at least two mature readers where available;
- exact unit, precision, endianness, compression, and missingness rules;
- chunked/streaming behavior for large data;
- deterministic structured errors with record or byte location;
- fuzzing or property-based malformed-input tests;
- benchmarks demonstrating a material benefit;
- a fallback and rollback plan during at least one release cycle.

The native backend must match the same normalized MolSysMT contract as the
external backend. Differences are classified as source-reader defects,
external-backend losses, or intentional documented policy—not silently hidden
behind backend selection.

## Rust boundary

Rust is preferred when binary parsing, decompression, or large-array movement
dominates. The boundary should expose small typed buffers and metadata rather
than MolSysMT domain objects. Python remains responsible for form dispatch,
units, chemical semantics, reports, and public exceptions. The extension must
support Python 3.11, 3.12, and 3.13 and must not introduce a mandatory build
toolchain for users installing published wheels.

## Non-goals before 1.0

- Replacing ParmEd, MDTraj, or other working parsers merely to remove an
  intermediary.
- Copying third-party implementations.
- Expanding the public API around backend names.
- Blocking Tier 1 promotion when the encapsulated external backend satisfies
  fidelity, selection, dependency, and test contracts.

## Success criteria

A native parser is successful only if it yields a measurable improvement in at
least one of fidelity, streaming scalability, installation footprint, startup,
or throughput without reducing compatibility or scientific traceability. The
external backend can be retired only after the native path passes the complete
corpus on all supported Python versions and at least one released version has
provided a safe comparison or fallback path.
