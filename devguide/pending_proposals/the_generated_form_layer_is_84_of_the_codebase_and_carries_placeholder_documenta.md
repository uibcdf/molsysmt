---
summary: The generated form layer is 84% of the codebase and carries placeholder documentation.
issue: uibcdf/molsysmt#189
status: open
opened: 2026-08-19
closed:
verification: measured
area: [form, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Proposal: decide what the form layer's volume costs, before 1.x freezes it

**Raised:** 2026-08-19, during an external audit, on reading
`molsysmt/form/molsysmt_Topology/get_topological_attributes.py`.
**Status:** proposed, and deliberately not scoped as pre-1.0 work. What is proposed for
now is a decision and a measurement, not a rewrite.

## What

The form layer is 84% of the Python in the package, and it is materialised code: the
attribute catalogue crossed with the form registry, one function per cell, each with a
generated docstring.

```bash
$ find molsysmt/form -name '*.py' -exec cat {} + | wc -l ; find molsysmt/form -name '*.py' | wc -l
363813
1690
$ find molsysmt -name '*.py' -exec cat {} + | wc -l ; find molsysmt -name '*.py' | wc -l
431007
2565
$ grep -rhc '^def ' --include='*.py' molsysmt/form | awk '{s+=$1} END {print s}'
10443
```

One file holds 490 of those functions:

```bash
$ wc -l molsysmt/form/molsysmt_Topology/get_topological_attributes.py
18013
$ grep -c '^def ' molsysmt/form/molsysmt_Topology/get_topological_attributes.py
490
```

Their documentation is generated and says nothing:

```bash
$ grep -rn 'Resulting object in object form' --include='*.py' molsysmt | wc -l
8810
$ grep -rn 'Argument [a-z_]*\.$' --include='*.py' molsysmt | wc -l
9976
```

A representative body, complete:

```python
@arg_digest(form=form)
def get_formal_charge_from_system(item, skip_digestion=False):
    """
    Getting formal charge from system in form molsysmt.Topology.

    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    return get_formal_charge_from_atom(item, skip_digestion=True)
```

Nineteen lines of documentation over one line of delegation, repeated at the scale of the
matrix.

What is proposed is not a rewrite. It is that the project decide, and record, which of
these three the form layer is — because the answer changes what should be done and the
repository currently behaves as though it were all three at once:

1. **Source.** Then the volume is real, it is read and edited by hand, and the generated
   docstrings are a documentation defect at scale.
2. **A build product.** Then it should be generated at build or import time from the
   catalogue and the per-form specifications, and it should not be 1,690 tracked files.
3. **Source with a generator of record.** Then the generator is normative, the files are
   its output, and no metric computed over the repository — line counts, function counts,
   coverage denominators — should mix it with hand-written code without saying so.

## How

The pieces for option 3 already exist. `devtools/scripts/scaffold_form.py` writes a
conforming adapter directory; `devtools/scripts/generate_form_declarations.py` writes
`form.json` for every plugin; `devtools/scripts/validate_form_adapters.py` audits
delivery against the catalogue. What is missing is the statement that these are the
authority and the files are downstream of them.

The immediately actionable part, whichever option wins:

- Report metrics split. Line counts, test counts and coverage should be reported for the
  hand-written package and the materialised layer separately. 81% coverage over 67,758
  statements means something different when most statements are 490 near-identical
  delegations.
- Give the generated docstrings a template that carries the catalogue's own description
  of the attribute and its units. The information exists in the attribute catalogue; the
  generator does not read it.

Option 2 is the largest change and is out of scope for 1.x under the deprecation policy,
because import-time generation would move the public `molsysmt.form.<plugin>.<function>`
paths that `api_surface.md` currently treats as addressable.

## Why

**Every metric in the paper will be computed over this.** A methods paper reporting size,
test count or coverage reports 84% of a number that describes a materialised matrix.
That is not dishonest, and it becomes so the moment a reader assumes otherwise. Stating
the split is cheaper than defending the aggregate.

**The documentation cost is already visible on the public surface.** The same generator
habit produced the 49 placeholder parameters on the stable root API,
[#187](https://github.com/uibcdf/molsysmt/issues/187). That entry fixes the symptom
where it is contractual; this one is about the source of it.

**It is a maintenance surface, not only a size.** `788fe1d50`, *"stop seven adapters
importing the target form's identity converter"*, is the shape of defect a materialised
matrix produces: one mistake, replicated mechanically, found seven times. The
form-adapter delivery gate exists precisely because per-cell correctness cannot be held
by reading.

**The moment matters.** 1.0 freezes the public surface for the 1.x line. Deciding after
the tag is deciding under a compatibility constraint that does not exist today.

## What is measured and what is assumed

Measured: all counts above, with the commands shown; the 564 direct conversion functions
across the layer; the existence and purpose of the three devtools scripts.

Assumed — *estimate*: that most of the 363,813 lines are mechanically generated rather
than hand-written. The sampled files support it strongly and the docstring counts
corroborate it, but no per-file classification was performed, and some adapters contain
substantial hand-written logic — `molsysmt_Topology/set.py` at 3,398 lines is not
boilerplate.

Not measured: how much of the layer is actually exercised. Coverage is reported for
`molsysmt.form` against an 80% threshold, but coverage of generated delegations does not
distinguish a tested route from a route that happens to be crossed.

## What was refuted

*The volume is duplication that could simply be deleted.* It is not duplication in the
refactoring sense. Each cell is a distinct (form, attribute) pair with a real, sometimes
form-specific, implementation. The question is where the cells should live, not whether
they are needed.

*This is the same theme as the attribute-centric architecture proposal.* It is not.
[`attribute_centric_molecular_system_model.md`](attribute_centric_molecular_system_model.md)
concerns what a molecular system is and which attributes a form may hold. This concerns
how the resulting matrix is materialised, documented and measured, and it stands whatever
that model becomes.

## Scope and exclusions

Covers the decision, the metric-reporting split, and the docstring template used by the
generators.

Excludes any change to public import paths under `molsysmt.form`, which the deprecation
policy governs. Excludes the form-adapter delivery debt, which is
[#139](https://github.com/uibcdf/molsysmt/issues/139). Excludes the 1.0 release path
entirely: nothing here should block F6.

## Acceptance criteria

1. A normative document states which of the three the form layer is, and
   `devguide/form_adapter_implementation.md` agrees with it.
2. Repository metrics quoted in the developer guide, the README, or the paper report the
   hand-written and materialised layers separately, with the command that produces each.
3. The docstring template used by `scaffold_form.py` emits the attribute's catalogue
   description and units instead of `Argument item.` and *"Resulting object in object
   form"*.

## Dependencies and risks

The risk of deciding is small; the risk of not deciding is that 1.x freezes the current
arrangement by default, and the paper quotes an aggregate nobody has split.

## Provenance

Measured 2026-08-19 on Linux 7.0.0-28-generic x86_64, Python 3.13.14, MolSysMT
`0.21.0+325.g7cedab74a` at repository commit `b9a2098e4`.
