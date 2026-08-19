---
summary: The README presents experimental surfaces as headline capabilities.
issue: uibcdf/molsysmt#186
status: open
opened: 2026-08-19
closed:
severity: medium
verification: measured
area: [docs, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: the README's headline capabilities are the experimental ones

**Reported:** 2026-08-19, during an external audit conducted as a reader arriving from
the forthcoming methods paper, by comparing every README claim against
`devtools/data/public_api_stability.json`.
**Status:** open. The README is accurate about what the code does; it is silent about
what the project itself guarantees.

## What

**The lead capability is classified `experimental` in full.** `README.md:184`:

> - **Native structure preparation.** Missing heavy atoms, terminal cappings,
>   hydrogen placement, solvation and ions — without requiring OpenMM or PDBFixer.

Every symbol behind that sentence is `experimental`:

```bash
$ python -c "
import json
d = json.load(open('devtools/data/public_api_stability.json'))['symbols']
print(sorted(k for k, v in d.items()
             if k.startswith('molsysmt.build.') and v['stability'] == 'stable'))"
[]
```

The same holds for `physchem.get_sasa`, `structure.get_secondary_structure`,
`structure.get_rmsf` and every `hbonds` entry, all of which the README's *What is inside*
section presents without qualification. None appears in
[`../../scientific_evidence_matrix.md`](../../scientific_evidence_matrix.md), which is
complete for the stable surface and does not cover the experimental one.

**One claim is false as written.** `README.md:64`, immediately under the hero example:

> Every step there but the last is MolSysMT's own: the preparation needs no OpenMM
> or PDBFixer installation.

The third preparation line of that example omits `engine`, and the default is OpenMM:

```bash
$ python -c "
import molsysmt as msm, inspect
for name in ('add_missing_terminal_cappings', 'add_missing_hydrogens', 'solvate'):
    print(name, inspect.signature(getattr(msm.build, name)).parameters['engine'].default)"
add_missing_terminal_cappings MolSysMT
add_missing_hydrogens OpenMM
solvate OpenMM
```

The example passes `engine='MolSysMT'` explicitly on the two lines that do not need it
and omits it on the one that does. As printed, the snippet requires OpenMM.

**A front-page link does not resolve.** `README.md:265` sends the reader to
`CONTRIBUTORS.md` for the full contributor list:

```bash
$ ls CONTRIBUTORS.md
ls: cannot access 'CONTRIBUTORS.md': No such file or directory
```

## How

Not a mechanism in code — a divergence between two records the project maintains
separately and does not cross-check.

`devtools/data/public_api_stability.json` is normative and honest: 123 stable, 57
experimental, 9 outside-contract, with `build` entirely in the second group.
`scientific_evidence_matrix.md` is generated and complete over the stable surface. The
README is written by hand against the code, so it describes what works rather than what
is promised, and nothing validates one against the other. `validate_public_api_stability.py`
checks the registry against the source; no gate checks prose against the registry.

The engine defaults are a narrower slip: the sentence at line 64 was true of the two
lines above it and was written as though it were true of all three.

## Why

**A referee will read both records.** The stability registry is one of the strongest
things in the repository — a machine-readable, honest, three-way classification of the
public surface. A reader who finds it after reading the README finds that the headline
feature is not in the contract, and the discovery is worse than the disclosure would have
been.

**The false claim is the one a reader tests first.** Preparation without OpenMM is the
differentiating claim. A reader in a minimal environment runs the hero snippet, hits a
missing-OpenMM error on the solvation line, and concludes the differentiator does not
hold — when it does, with one argument.

**`experimental` is a promise about change, not about quality.** `build` works; the audit
ran it. The registry says its signatures and semantics may move inside 1.x. A user
building a pipeline on `msm.build` deserves to know that from the page that recommends
it.

Severity is `medium`: nothing computed is wrong, and the underlying classification is
correct and public. What is defective is the public presentation of it.

## What is measured and what is assumed

Measured: the empty stable-symbol list for `molsysmt.build`; the three engine defaults;
the absence of `CONTRIBUTORS.md`; the absence of every named experimental symbol from the
generated evidence matrix; the README line numbers.

Assumed — *estimate*: that a reader would take *"Native structure preparation"* under
*What is inside* as a contractual capability. That is a judgement about how the page
reads, not a measurement.

## What was refuted

*The README overstates what the code does.* It does not. Every capability listed was
exercised during the audit and every one exists. The defect is that the page does not
carry the project's own stability classification, not that it invents capabilities.

*`build` is experimental because it is unfinished.* Not established, and probably wrong:
the LEaP parity suite in
`tests/build/build_peptide/test_build_peptide_molsysmt_MolSys.py` compares 40 random
sequences against an external builder. The classification looks like a deliberate
contract decision, which is exactly why the README should state it.

## Scope and exclusions

Covers `README.md`: the stability qualification of experimental surfaces, the engine
claim at line 64, and the broken `CONTRIBUTORS.md` link.

Excludes `docs/index.ipynb` and the documentation landing page, which were rewritten in
the 2026-07-29 positioning pass and were not re-audited against the registry here — they
should be, and that is a second document if it finds anything. Excludes the CI badge,
which is [#185](https://github.com/uibcdf/molsysmt/issues/185). Excludes the citation and
installation items already specified in
[`../../pending_proposals/presentation_and_citation_surface.md`](../../pending_proposals/presentation_and_citation_surface.md).
Excludes any change to the classifications themselves: promoting `build` to `stable` to
make the README true is a contract decision, not a documentation fix, and would need its
own evidence.

## Acceptance criteria

1. Every README capability whose symbols are `experimental` says so where it is claimed,
   in the project's own vocabulary.
2. The hero example runs in an environment without OpenMM, or the sentence beneath it
   stops claiming it does.
3. `CONTRIBUTORS.md` exists, or the link is removed.
4. A test asserts that no README capability bullet names a symbol the stability registry
   classifies `experimental` without the qualification, and that every repository-relative
   link in `README.md` resolves. This is the `guard`.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`. README line numbers refer to
that commit.
