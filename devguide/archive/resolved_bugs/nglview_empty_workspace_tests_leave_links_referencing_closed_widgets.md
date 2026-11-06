---
summary: NGLView empty-workspace tests leave links referencing closed widgets
issue: uibcdf/molsysmt#598
status: resolved
opened: 2026-11-05
closed: 2026-11-06
severity: medium
verification: reproduced
area: [tests, basic]
guard: tests/basic/view/test_empty_view_contract.py::test_closed_empty_ngl_workspace_keeps_later_widget_embedding_valid
normative:
blocked_by: []
supersedes: []
---

# Empty-workspace tests retain links to closed NGL widgets

## What

Running the empty-workspace tests before the HTML export guard raises
AttributeError on a closed NGLWidget comm. The exporter passes alone. A two-module
serial run reproduces the full CI failure (45 passes, one failure).

## How

NGLWidget constructs player widgets and jslinks. Closing the root widget leaves
links referring to its closed comm. NGLView's HTML writer uses ipywidgets'
global manager state, so an unrelated later export traverses those links.
The test fixture now disposes all widgets created by each NGL case, including
links, while preserving every pre-existing widget. It initializes the provider
before taking the test-owned registry snapshot. Registry inspection is confined
to test resource management; no runtime global monkeypatch or fallback is added.

## Why and acceptance

Tests own their created resource graph. The new guard closes one empty workspace
inside that scope, then embeds an independent live widget with the actual
ipywidgets serializer. The serial two-module run passes 46 cases after cleanup;
the broader serial NGL selection passes 83 cases, including the new embedding
guard, native widget parity and all existing HTML/representation controls. No expected test is
skipped, no export assertion is removed, and HTML writer behavior is unchanged.

The upstream global-export limitation for application-owned closed widget links
is not claimed fixed. No external provider issue has been published: external
publication requires the maintainer's separate reviewed authorization.

## Provenance

Linux/Python 3.14.7, NGLView 4.0.1, ipywidgets 8.1.9; main ed09f6453 plus PR
1c88e785b and owner receiving corrections. Baseline receipt:
.pytest_cache/543-ngl-lifecycle-baseline.xml; repaired two-module receipt:
.pytest_cache/543-ngl-lifecycle-repaired.xml (private local source evidence).

## Resolution — 2026-11-06

The current serial empty-workspace, complete NGL tools and native widget-parity selection passes 83 cases without failure or omission. The actual widget serializer runs after test-owned empty-workspace cleanup, retaining all existing HTML/representation assertions and pre-existing widgets. No production serializer monkeypatch, skipped export or application-level closed-widget claim is introduced. Browser rendering and the upstream application-owned limitation remain separate.

Verified source: cddc3f3a613282693126549654233d2fd1d739a4. Existing implementation originated in
ab789897bad51a7258f366aadc01840895d6366e; no new production fix is claimed by
this closeout. The new NMR guard belongs to the received source above.
[Exact source, JUnit digests and scope](../../../devtools/data/ordered_bug_closeout_594_598_20261106.json)
retain these independent profiles and their overlapping counts. Existing failed
full-suite history, remaining version-matrix/installed gates and release authority
are not changed by this bounded bug closure.
