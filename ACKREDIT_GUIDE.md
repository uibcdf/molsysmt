<!--
SYNCHRONIZED MOLSYSSUITE GUIDE — DO NOT EDIT COMPONENT COPIES.
Canonical source: https://github.com/uibcdf/ackredit/blob/main/standards/ACKREDIT_GUIDE.md
-->

# Ackredit Integration Guide

Source of truth for integrating **Ackredit** into a host library, following the
**MolSysSuite** standards.

## What is Ackredit

Ackredit records which algorithms, datasets and dependencies a run **actually reached**,
and turns that into a citation report with full provenance.

It exists against the alternative: asking users to cite a whole library because they
installed it. A run that never took the iterative branch should not cite the iterative
paper, and a list built from what a library *contains* cannot make that distinction.

## Why this matters in this library

- **Your work gets cited for what it did.** Papers, datasets and methods your library
  rests on are credited when the code that needs them runs, not when someone imports you.
- **Your users stop guessing.** They receive a bibliography in BibTeX, CSL-JSON, LaTeX or
  Markdown, covering your library and everything under it.
- **Provenance, not a list.** The report says which of your functions led to which
  citation, including citations that arrived through a library you call.
- **Nothing breaks without it.** Ackredit is an optional dependency, and the pattern in
  section 1 is what keeps your library working when it is absent.

## Optional MolSysSuite scientific clients

The accepted [MolSysSuite client policy](https://github.com/uibcdf/molsyssuite/blob/main/devguide/ackredit_client_policy.md)
applies to new or changed optional scientific method/result attribution boundaries.
Utilities without such boundaries record non-applicability. Guide distribution
does not establish runtime adoption or published compatibility.

- Keep bibliographic declarations offline in host constants, checked against the
  original work. Load Ackredit and register records only when an attribution
  boundary is requested. Importing the host must not import Ackredit or perform
  network/filesystem work.
- Use supported public `register_item`, `scope` and `track_item` operations at the
  branch actually reached. Distinguish criterion, adapted reference implementation
  and executed software in host result context. Track per calculation or meaningful
  child operation, not per pair/frame/occurrence. Completed evaluated-empty analyses
  retain provenance; failures cannot claim successful completion.
- Applications own sessions. Contribute to the current session; do not replace it
  with an isolated component session or subtract deduplicated session IDs to infer
  a result's references.
- Each result retains detached bibliographic records and original producer versions,
  including references reused by other results. Reading a saved result preserves
  that provenance without crediting another calculation.
- Absence preserves results and host-owned provenance. Provider failures emit host
  catalog diagnostics and preserve completed science without claiming successful
  tracking. Isolate provider errors without swallowing scientific exceptions.
- Libraries must not automatically enable import hooks, auto tracking, enrichment,
  journals or reminders. Applications may explicitly opt into documented features.
- Use a real provider to test observed credit, reused references across two results,
  enclosing workflows, empty results, genuine absence, failure, detached ownership,
  fresh-process lazy import and fresh readers retaining original versions without
  new credit. An installed flag or mocked success is insufficient.
- Verify provider floors and published dependency closure for each claimed Python
  minor. Keep the client's existing support range; editable pilot evidence does not
  authorize a public extra or installation claim.

The reviewed API under uibcdf/ackredit#75 provides `capture`,
`Attribution` and `get_attribution` operations. Consumer adoption and published
installation remain separate gates. The first reviewed contract ships in
public **Ackredit 0.9.0** on the `uibcdf` Conda channel; use `ackredit>=0.9.0`
as its minimum version. The [installation evidence](https://github.com/uibcdf/ackredit/blob/main/docs/content/about/installation.md)
records the exact noarch archive, Linux/macOS arm64 × Python 3.11–3.14 installed
matrix and clean public Linux/Python 3.14 receiving check. Clients still qualify
their own supported environments and releases. Older tags do not contain this
API. Its [compatibility contract](https://github.com/uibcdf/ackredit/blob/main/docs/content/user_guide/portable_attribution.md)
keeps schema 1 readable in later releases and versions structural changes with
a new schema ID. Do not read private registries, copy renderers
or treat journals of IDs as a portable bibliography. The MolSysMT pilot at
`e21f03d9992b87af2cc9285211adee888462be41` is consumer evidence; its
`molsysmt.scientific_attribution@1` schema remains local.

### Portable calculation capture (reviewed contract)

Applications own the session and may capture each result without replacing it:

```python
import ackredit

with ackredit.session("workflow"):
    with ackredit.capture(
        "conversion", context={"producer": "client", "version": "1"}
    ) as run:
        with ackredit.scope("client.convert"):
            ackredit.register_item(
                id="software:example:2", type="software", title="Example", version="2"
            )
            ackredit.track_item(
                "software:example:2",
                roles=["executed_software"],
                context={"software": "example", "version": "2"},
            )
    result_references = run.attribution.to_dict()
    workflow_references = ackredit.get_attribution().to_dict()

saved = ackredit.Attribution.from_dict(result_references)
bibliography = saved.report(format="bibtex")
```

Each enclosing capture observes reused references even if the session already
credited them. Nested captures observe completed child work in the same session;
explicit isolated sessions are independent. Exceptions propagate and completed
child credits remain; a partial capture is not proof of successful science.

The `ackredit.attribution@1` object carries `name`, producer `context`, complete
`items`, contextual `uses` and a `usage_tree`, alongside its `schema` field.
Use entries carry `item_id`, `used_by`, `roles` and JSON `context`. Roles belong
to uses, not the bibliographic work: `scientific_criterion`,
`reference_implementation`, `executed_software` and `software_description` are
recommended conventions, not an exhaustive vocabulary. A software reference
and its description articles share `context.software` and `context.version`;
articles alone can also be cited with that context. Distinct software versions
use distinct bibliographic IDs. Conflicting metadata for one observed ID raises
catalog-backed `ACKREDIT-E011` instead of overwriting original provenance.

Export/import detaches JSON data. Reading or rendering never registers or credits
records, loads scientific backends, or enriches DOIs. Unknown schema versions and
invalid payloads are refused with `ACKREDIT-E010`. Store this payload beside a
host's scientific data without changing the host's serialization contract.
Journals continue to store identifiers; they do not persist contextual uses.
Legacy plain credits resolve bibliography at workflow snapshot time; captured
or contextual credits retain the records observed at use time.

A MolSysSuite client needing other initialization/session semantics records a
reviewed member-owned exception with the affected rule, reason, owner and issue,
interim controls, expiry and removal condition. Provider implementation and member
runtime adoption remain separate.

## Function providers and prepared credit (stable from 0.11.0)

Ackredit's principal maintainer accepted `prepare_credit`, `observe_calls` and
`ackredit.provider@1` on 2026-10-06 under
[Ackredit #84](https://github.com/uibcdf/ackredit/issues/84) /
[#87](https://github.com/uibcdf/ackredit/issues/87), coordinated with
[MolSysSuite #97](https://github.com/uibcdf/molsyssuite/issues/97) and
[MOLI #46](https://github.com/uibcdf/moli/issues/46). Public **0.11.0** delivers
the accepted bounded compatibility promise after exact-file source, installed,
real receiving and public-channel verification. Use `ackredit>=0.11.0` when
requiring that stable-provider promise. Public 0.10.0/0.10.1 provide these
capabilities under their original
provisional contract; **they are not a stable-provider version floor**.
The released portable minimum remains `ackredit>=0.9.0`.

From public 0.11.0, the reviewed signatures and meanings
remain compatible across later patch/minor versions, including pre-1.0 and 1.x.
Incompatible changes follow the
[deprecation policy](https://github.com/uibcdf/ackredit/blob/main/docs/content/about/stability.md).
Later readers retain `ackredit.provider@1` interpretation; incompatible declaration
schema/meaning changes require a new identifier and unknown identifiers are refused.
Client adoption, release qualification and synchronization of this guide remain
separate. Observation is an explicit application choice; scientific libraries
must not automatically enable it.

### Dependency-free provider declaration

A third-party library can publish this ordinary module dictionary (for example,
in `example_provider.py` or imported from its own `_citations.py`). All metadata
below is illustrative; authors supply their actual original bibliography.

```python
__ackredit__ = {
    "schema": "ackredit.provider@1",
    "software": {"name": "Example", "version": "2.4.0"},
    "items": [
        {
            "id": "example:software:2.4.0",
            "type": "software",
            "title": "Example",
            "version": "2.4.0",
        },
        {"id": "example:method", "type": "article", "title": "Example method"},
    ],
    "functions": {
        "normalize": [
            {"item_id": "example:software:2.4.0", "roles": ["executed_software"]},
            {"item_id": "example:method", "roles": ["software_description"]},
        ],
    },
}


def normalize(values):
    total = sum(values)
    return [value / total for value in values]
```

Declaration and import credit nothing and require no Ackredit dependency.
All schema fields are required. `software` has exactly non-empty `name` and
`version`; `items` supplies unique non-empty IDs and JSON-compatible records;
`functions` maps direct export names to non-empty use lists. Each use contains
exactly `item_id` and `roles`, a list of non-empty role names, and references
resolve locally. Keep software releases under distinct IDs. Function metadata
`function.__ackredit__ = {"uses": [...]}` can supply the same uses instead;
if both declarations name an export, they must agree. A producer's decorator
can attach that attribute and return the original function unchanged.
The role list may be empty when no role is declared; it remains unspecified
rather than receiving an inferred relationship.

### Explicit application observation

```python
import ackredit
import example_provider

with ackredit.session("analysis"), ackredit.scope("pipeline"):
    with ackredit.observe_calls(example_provider):
        with ackredit.capture("normalization") as run:
            values = example_provider.normalize([1, 3])
    saved_references = run.attribution.to_json()

bibliography = ackredit.Attribution.from_json(saved_references).report("bibtex")
```

Only entry into declared synchronous exports or execution of awaited coroutines
earns their references. Entry does not establish scientific success. Context-local
nested/concurrent leases restore original module exports after the last exit;
expired owners stop recording. Threads do not automatically inherit context.
Pre-activation aliases, generators, descriptors, custom module subclasses, native
internal calls and subprocesses are outside the guarantee. Ordinary PEP 562
modules resolve only declared missing exports; their loader's caching/import
side effects cannot be rolled back. Invalid declarations receive `ACKREDIT-E012`
before observation/registration; recording or restoration gaps receive
`ACKREDIT-W019`. Application warning-as-error filters remain effective.
See the complete
[provider contract](https://github.com/uibcdf/ackredit/blob/main/docs/content/user_guide/function_providers.md).

### Explicit fixed credit at the host's completion boundary

```python
import ackredit

ackredit.register_item(
    id="backend:software:2", type="software", title="Backend", version="2"
)
credit = ackredit.prepare_credit(
    "backend:software:2",
    "host.convert",
    roles=["executed_software"],
    context={"software": "Backend", "version": "2"},
)
with ackredit.session("conversion"), ackredit.capture("result") as run:
    with ackredit.scope("host.convert"):
        converted = backend_convert([1, 3])  # scientific exceptions propagate
        credit()  # the host decides that this operation earned its reference
saved_references = run.attribution.to_json()
```

Preparation validates and detaches one already registered reference and fixed
roles/context; it credits nothing. The zero-argument callable contributes to the
current session and every active capture, including reused references. It creates
no scientific scope or success interpretation. Changed/deleted registered
bibliography receives `ACKREDIT-E010` before credit. Optional clients diagnose
provider failures and preserve completed science. Clients retaining compatibility
with 0.9.0 can keep their public `track_item` fallback; importing the host must
still defer Ackredit until its requested attribution boundary. Fixed preparation
reduces repeated declaration work without removing registry/capture checks; use
meaningful operations rather than instrumenting every scalar iteration.

No additional recorder, automatic enrichment, hook, journal or reminder is
required by provider promotion.

## Recorder evidence (stable from 0.12.0)

On 2026-10-06 the maintainer explicitly accepted `AttributionEvidence`, bounded
`capture(record_evidence=True)` / `.evidence` provider-observer collection and
explicit integrated workflow/CLI reporting under
[Ackredit #114](https://github.com/uibcdf/ackredit/issues/114). Source classification
is stable. Qualified public **0.12.0** delivers its bounded forward promise
under #127 after exact-source, same-file installed/real receiving and independent
public verification. Use `ackredit>=0.12.0` when requiring these evidence
contracts; the [delivery receipt](https://github.com/uibcdf/ackredit/blob/main/devtools/conda-build/receipts/ackredit_0.12.0_public_2026-10-07.json) retains the proof. **Public 0.11.0 retains its
original provisional evidence classification**. Do not infer a stable-evidence
minimum from the existing stable-provider minimum `>=0.11.0`.

From public 0.12.0, retain reviewed signatures and meanings across later
patch/minor releases, including remaining pre-1.0 and 1.x, under the existing
deprecation/removal policy. Retain interpretation of
`ackredit.attribution_evidence@1` and `ackredit.attribution_evidence_explanation@1`;
incompatible structural/meaning changes require new identifiers. Source
acceptance, exact-file public delivery, guide-copy synchronization and actual
consumer adoption remain separate. Standalone validation and the general 1.0
source commitment were separately accepted under #125 below; their delivery
boundaries are not implied by the evidence decision.

- Preserve complete detached original attribution/bundles. One evidence entry
  belongs to each original occurrence by position, including repeated names or
  inputs. Producers own truthful association; readers do not authenticate it.
- Preserve three separate planes: metadata field sources, selected/unsupported/
  unobserved boundaries and diagnosed recording gaps. `null` means unrecorded;
  `[]` means no declarations supplied. Neither proves complete instrumentation,
  absence of failures or absence of citable work.
- Automatic collection is explicitly opt-in and bounded to active overlapping
  provider observers/captures in the same session. Retain positive deduplicated
  selection, successfully credited original provider fields and owning W019
  diagnostic identities. Other recorder origins remain unknown; additional
  integration needs a concrete owning use case.
- Scientific failure/cancellation does not itself become a recording gap or
  completed-backend credit. Partial recording retains successful origins and
  diagnosed gaps. Application warning-as-error policy can stop the scientific
  body; observer/scope cleanup and capture ownership retain their reviewed limits.
- Saved reading/rendering needs no producer or service, creates no credit and
  never emits a stored diagnostic again. Source locators and recorder identities
  are declarations, not execution/scientific truth or authenticated provenance.
- Default original reports remain unchanged. Explicit integrated workflow output
  retains original numbering, bibliography, versions, roles and graph, with
  declarations beside their own occurrence. Content and association are promised;
  cosmetic whitespace is not universally frozen. CLI selection requires evidence
  input and workflow output, refuses invalid combinations and input overwrite.

See the [accepted contract and guards](https://github.com/uibcdf/ackredit/blob/main/devguide/recorder_evidence_contract_review.md)
and [evidence user guide](https://github.com/uibcdf/ackredit/blob/main/docs/content/user_guide/attribution_evidence.md).
Clients decide whether to request these optional facts; this guide neither enables
observation automatically nor certifies a client release. Consumer guide copies
are synchronized centrally and are never repaired locally.

## Standalone validation (stable from 0.12.0)

The maintainer promoted `validate_provider(module) -> dict` on 2026-10-06 under
[Ackredit #125](https://github.com/uibcdf/ackredit/issues/125). Pass an already
imported trusted ordinary module. The operation reuses the observer's parser and
returns a detached merged `ackredit.provider@1` declaration, preserving original
software/items and returned role order/duplicates. Each call reads current
metadata. Invalid declarations raise `ValueError` with catalog `ACKREDIT-E012`.
It does not call science, credit uses, register bibliography, patch exports,
change observer ownership or query DOIs. Selected lazy loaders retain their
producer-owned caching/import effects. Validation alone does not establish
current-registry compatibility, citation truth or successful scientific use.

Qualified public **0.12.0** delivers the bounded public forward promise under
#127; use `ackredit>=0.12.0` for standalone validation. The same-file installed/
receiving matrices, public verification and fresh installation are retained in
the delivery receipt above. Public 0.11.0
lacks this standalone export and is not its version floor. Existing portable
`>=0.9.0`, stable-provider `>=0.11.0` and recorder-evidence delivery boundaries
remain distinct. Author validation is optional; hosts need not add it to normal
execution. See the [provider author guide](https://github.com/uibcdf/ackredit/blob/main/docs/content/user_guide/provider_authors.md).

## General 1.0 source commitment (public delivery pending)

Under #125 the maintainer also accepted the documented stable API's signatures
and meanings for future 1.x, preserving the existing major-removal/two-minor
deprecation policy and separately versioned saved-reader/plugin/report contracts.
The general public promise begins with a separately authorized, qualified public
1.0.0. This is source acceptance, not a release/tag, automatic guide-copy rollout,
mandatory client adoption or change to a host's optional-provider behavior.
Private implementation and cosmetic whitespace are not universally frozen;
scientific success, complete instrumentation and arbitrary publication-tool
compatibility are not inferred. Original public artifacts retain their historical
contracts. Review [API stability](https://github.com/uibcdf/ackredit/blob/main/docs/content/about/stability.md)
and the [accepted contract map](https://github.com/uibcdf/ackredit/blob/main/devguide/archive/general_stability_review.md).
Consumer copies remain synchronized through the central registry, never locally
repaired.

## Eager demonstration profile

Sections 1–6 and the worked examples below describe the existing eager profile
for deliberate eager integrations and third-party demonstrations. Its template
is tested against the example libraries. Optional MolSysSuite scientific clients
use the deferred profile above; do not copy eager import/registration into them.

## 1. Centralization File: `_ackredit.py`

Hosts centralize their integration in `_ackredit.py`. The following template is
for the eager demonstration profile; deferred clients load the provider only at
their attribution boundary.

The single rule this file exists to enforce: **the host keeps working when Ackredit is absent**. Every name it exports must therefore have a fallback with the *same signature* as the real one, or the host will break precisely in the case the pattern was meant to protect.

### Template for `_ackredit.py`:

```python
"""Ackredit integration for this library.

Ackredit is an optional dependency. This module must import cleanly and expose the
same names whether or not it is installed.
"""

try:
    import ackredit
    from ackredit import (
        add_injection,
        bind,
        bound_items,
        credit_bound,
        register_item,
        report,
        scope,
        scoped_usage,
        track_item,
    )

    ACKREDIT_INSTALLED = True

except ImportError:
    ACKREDIT_INSTALLED = False
    ackredit = None

    def register_item(**item):
        pass

    def bind(target, items):
        pass

    def bound_items(target):
        return []

    def add_injection(target_module, items):
        pass

    def credit_bound(target):
        return []

    def track_item(item_id, used_by=None, *, roles=(), context=None):
        pass

    def scoped_usage(target, credit_bound=False):
        def deco(fn):
            return fn

        return deco

    class scope:
        def __init__(self, name, credit_bound=False):
            self.name = name

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    def report(format="markdown", **kwargs):
        return "Ackredit is not installed."
```

Note what the fallbacks return: `bound_items` and `credit_bound` return an empty list, not `None`, so host code that iterates their result behaves identically in both modes. `scope` is a class, because it is used as a context manager.

## 2. Static Registration

In your host library's `__init__.py` or a dedicated setup file, register your items and bindings using the centralized `_ackredit.py`:

```python
from ._ackredit import bind, register_item

register_item(
    id="molsysmt:software",
    type="software",
    title="MolSysMT",
    authors=["Prada-Gracia, Diego", "Moreno-Vargas, Liliana M."],
    doi="10.5281/zenodo.1298752",
)

bind(target="molsysmt.basic.convert", items=["molsysmt:software"])
```

Copy the fields from the work's own record — its `CITATION.cff`, its DOI, its published
author list — and never write one from memory. In particular, **never write a truncation
as a name**. Putting `"et al."` at the end of the list makes BibTeX credit a person
surnamed "al." with the given name "et", and that reaches a manuscript. List the authors,
and let the bibliography style decide how many of them to print.

## 3. Dynamic Tracking

Use the decorators and tracking functions in your modules:

```python
from .._ackredit import scoped_usage, track_item


@scoped_usage(target="molsysmt.basic.convert")
def convert(item, to_form):
    track_item("molsysmt:software")
    # implementation...
```

`bind` declares what a target *may* require; it credits nothing on its own. When a function's citations do not depend on the code path taken, let the binding carry them instead of repeating the ids in the body:

```python
from .._ackredit import scoped_usage, track_item


@scoped_usage(target="molsysmt.basic.convert", credit_bound=True)
def convert(item, to_form, method="default"):
    # the bound items are credited on every call
    if method == "experimental":
        track_item("molsysmt:paper:2026:experimental")
```

## 4. Reporting

Expose a reporting function for the end user:

```python
from ._ackredit import report


def cite(format="markdown"):
    return report(format=format)
```

## 5. Advanced Features

These call the module directly, which is why the template imports `ackredit` as well as the individual names. Guard them with `ACKREDIT_INSTALLED`, because the fallback binds `ackredit` to `None`.

### Auto-Discovery of Dependencies

An application explicitly choosing automatic discovery enables hooks before the
imports it wants to observe. This is an application choice; optional scientific
libraries must not enable hooks in their own initialization:

```python
from ._ackredit import ACKREDIT_INSTALLED, ackredit

if ACKREDIT_INSTALLED:
    ackredit.enable_import_hooks()
```

Discovery sees imports that happen after it is enabled; a package already loaded is not
discovered. Ackredit loads **numpy** itself through ArgDigest (until
`uibcdf/argdigest#15`), so discovery never sees numpy. For a package that may already be
loaded, register its citation and declare an injection: an injection is credited whether
its package was imported before the hooks or after.

```python
if ACKREDIT_INSTALLED:
    # "numpy:paper:2020" registered from the work's own record, as in Static Registration.
    ackredit.add_injection("numpy", ["numpy:paper:2020"])
```

### Session Persistence

An application may explicitly choose a persistence journal for a long-running
workflow. Libraries must not enable it automatically; a journal is not a detached
result bibliography:

```python
from ._ackredit import ACKREDIT_INSTALLED, ackredit

if ACKREDIT_INSTALLED:
    ackredit.enable_persistence("ackredit_session.json")
```

## 6. Check that the integration is live

The `try`/`except ImportError` above is deliberately silent, so a host with Ackredit installed but mis-integrated looks exactly like a host without it: everything succeeds and nothing is ever recorded.

Do not let that state pass unnoticed. Expose the flag, and assert it where it matters:

```python
from ._ackredit import ACKREDIT_INSTALLED


# in the host's test suite, when ackredit is a test dependency
def test_ackredit_integration_is_active():
    assert ACKREDIT_INSTALLED
```

If `ACKREDIT_INSTALLED` is `False` while `pip show ackredit` succeeds, the import in `_ackredit.py` is raising `ImportError` for some other reason and being swallowed. Reproduce it by importing the names outside the `try` block.

By following this pattern, the host library remains functional even if Ackredit is not installed, while providing full citation support for users who have it.

## Required behavior (non-negotiable)

1.  **The host works without Ackredit.** Every name `_ackredit.py` exports has a fallback
    with the *same signature* as the real one. A fallback that has drifted breaks your
    library precisely in the case the pattern exists to protect.
2.  **Declare offline, credit at runtime.** The eager demonstration profile registers
    and binds at import. Optional MolSysSuite clients keep declarations in offline
    constants and defer provider registration until use. `track_item` belongs in the
    code path actually reached; importing a library never earns scientific credit.
3.  **Bind the unconditional, track the conditional.** If a citation depends on the path
    taken, call `track_item` on that branch. `credit_bound=True` is for the coarse case
    and credits on every call, which is why it is opt-in.
4.  **Never write a truncation as a name.** `"et al."`, `"and others"` and `"..."` are
    rendering decisions, not people. Written into `authors`, BibTeX turns them into a
    person and the bibliography credits someone who does not exist.
5.  **Do not silence the integration.** In the eager template, `try`/`except ImportError` is deliberately
    quiet, so a host with Ackredit installed but mis-integrated is indistinguishable from
    one without it. Assert `ACKREDIT_INSTALLED` where it matters — section 6.
    Deferred clients distinguish genuine absence from a broken provider and emit
    catalog diagnostics for failures, as required by the optional profile above.

## SMonitor Integration

Ackredit's diagnostics are catalog-driven, so a host sees stable codes rather than
free-form messages, and nothing is swallowed. The ones a host is most likely to meet:

| code | when |
| --- | --- |
| `ACKREDIT-W004` | a `CITATION.cff` it found could not be parsed |
| `ACKREDIT-W005` | no citation information could be discovered for a package |
| `ACKREDIT-W006` | DOI metadata could not be fetched, so an item is reported with what is known |
| `ACKREDIT-W008` | a citation plugin from another package failed to load |
| `ACKREDIT-W011` | `pdflatex` is absent, so no PDF was produced |
| `ACKREDIT-E004` | a report format that does not exist was requested |

Each carries the typed facts of its occurrence, so a host can filter or report them
through its own SMonitor integration. `ackredit.dependency_info()` reports which optional
features the environment supports.

## Worked examples

The Ackredit repository carries two host libraries under `examples/` that integrate it
exactly as described here — `dummy_solver`, and `dummy_pipeline` which calls it, so
citations cross a library boundary. Their `_ackredit.py` is this document's template,
asserted byte-identical by the test suite, so what you read here is what runs there.
