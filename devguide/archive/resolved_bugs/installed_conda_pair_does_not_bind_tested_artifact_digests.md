---
summary: Bind installed Conda pair evidence to the tested artifact digests
issue: uibcdf/molsysmt#775
status: resolved
opened: 2026-11-17
closed: 2026-11-17
severity: high
verification: reproduced
area: [ci]
guard: devtools/tests/test_conda_pair_receipts.py
normative:
blocked_by: []
supersedes: []
---

# Installed Conda evidence must identify the files tested

The [release gate](../../release_gate.md) requires the four Python minors
for each platform to install the same MolSysMT artifact and the whole pair
to use one noarch MolSysViewer artifact. At `a62d5be86`, the installed
validator accepted a canonical staging record with any well-formed SHA-256.
The same filename, channel and URL passed with either 64 `a` characters
or 64 `b` characters as the digest. The shell route for promotion verified
success of the requested matrix and checked its staging digest separately.
The pinned suite verifier confirmed run/source/attempt and exact jobs/steps.
The two checks had no comparison of installed and requested package bytes.
This was reproduced with synthetic records. The earlier historical installs
retain their original evidence and identities.

## Resolution

Each successful installed validation records the two actual Conda package
records' channels, URLs, filenames and SHA-256 values in
`installed-pair.json`, alongside the full source SHA, run ID, attempt and
running Python minor. The retained environment artifact carries both this
receipt and the existing explicit environment export. Artifact names include
the attempt, so a previous attempt cannot satisfy a later successful matrix.

The promotion workflow verifies the native run with the same suite action.
It then downloads the recorded attempt's receipts and checks their exact
coverage, source, run, attempt and Python identity. It checks staging
channel, native platform or noarch, requested version/build filenames and
digests. Each platform's cells must agree on MolSysMT identity, and all cells
must agree on MolSysViewer identity. Before any promotion, the requested
native filename and digest must match the tested file for that platform.
The assembled pair identity is retained with the suite matrix receipt and
can be checked against the separately selected producer artifacts before
tagging.

## Receiving

The local cohort used Pytest Receptor with sequential execution and a 2 GiB
enforced memory limit on Python 3.14.7. All 40 selected cases passed with zero
skips. Receptor and JUnit agree with the native exit. Peak use was 217 MiB
with zero own swap. The cohort exercises staging provenance, release routing
and installed closure, along with a synthetic complete sixteen-cell run.
It rejects a wrong build, missing cell, mixed Python/source/run/attempt,
mismatched digest across cells for either package and a same-version
promotion with another digest. The actual shell step accepts the stipulated
tested digest and refuses the mismatch before producing positive evidence.
All 15 fast release checks, Ruff and the developer-guide indexes also pass.

This is offline verification of the gate. The exact hosted sixteen-cell run,
its retained artifacts and the download/promotion receiving remain subject
to #334 and the existing coordinated release pause.

## Noarch archive follow-up — 2026-11-17

MolSysViewer reproduced a false refusal in `63c221176`. Its noarch producer
uses `--package-format tar.bz2`, while the verifier initially accepted only
`.conda` for MolSysViewer. The same sixteen-cell control passed for
`.conda` and failed for `.tar.bz2`. [MolSysViewer producer workflow](https://github.com/uibcdf/molsysviewer/blob/eeb6808c59afbd1deb3d70dc105e06e79a3f2aa3/.github/workflows/build_and_upload_conda_packages.yaml#L173).

The verifier now accepts the two exact Conda archive suffixes for the
MolSysViewer filename. Staging URL, channel, noarch subdirectory, version,
build and SHA-256 still contribute to validation. All cells must agree on
the exact filename, URL and digest. Mixed formats with the same digest and
unknown suffixes are rejected. MolSysMT's native artifact requires `.conda`.

All 43 offline cases pass, including execution of the promotion shell step
with a `.tar.bz2` MolSysViewer receipt. Pytest Receptor and JUnit agree with
the native exit. The exact installed release remains pending.
