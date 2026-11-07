---
summary: Standalone NGLView HTML export includes unrequested molecular widget state
issue: uibcdf/molsysmt#631
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: reproduced
area: [form, docs]
guard: tests/third_party/nglview/test_write_html.py
normative:
blocked_by: []
supersedes: []
---

# Standalone NGLView HTML includes independent molecular widget data

**Reported:** 2026-11-06 during NGLView dependency-floor receiving under
uibcdf/molsysmt#524. An unexpected model count prompted a separate data-scope probe.
**Status:** Source correction and paired actual-provider qualification complete;
public delivery and board closeout follow.

## What

Before this repair, exporting only viewer A through
molsysmt.third_party.nglview.write_html also embedded independent viewer B's
initial PDB text, including its coordinates. B had no HTML view specification
and did not belong to A plus the required color registry's widget dependency
closure. Its synchronized loadFile message still entered the manager-state JSON.

The bounded reproduction uses fresh processes and two synthetic one-atom
trajectories with distinct PDB remarks and coordinates. No real private data is read:

    PYTHONDONTWRITEBYTECODE=1 python .pytest_cache/pre1-review-20261106/providers/nglview-pytraj-review/export-scope/run_probe.py

The [invocations](../../../.pytest_cache/pre1-review-20261106/providers/nglview-pytraj-review/export-scope/invocations.json)
retain exact commands, origins, stdout/stderr and native exits. Both processes
exit 0 because their assertions verify the observed defect and a filtered-state
control; this is not a passing fidelity result for the old wrapper.

## How

The former [wrapper](../../../molsysmt/third_party/nglview/write_html.py) delegated
to nglview.write_html with a one-view list and the complete frame_range.
Inspected NGLView 3.0.4 and 4.0.1 accept only fp, views and frame_range: there is
no state parameter or general keyword forwarding. Both prepare resources,
include the shared color registry and call ipywidgets.embed.embed_snippet
without restricting state.

ipywidgets explicitly documents that state=None includes every known widget
in the process-wide manager. The requested views restrict HTML view
specifications, but not that default manager state. NGLView synchronizes its
_ngl_msg_archive, which includes the initial loadFile structure blob even for
an unrelated widget whose _ngl_serialize flag is false.

### Implemented owner repair

The public wrapper now has ArgDigest, the lazy optional-provider guard and
skip_digestion=False. A specific NGLWidget type check rejects a different valid
viewer before private NGL hooks, since the generic view digester also admits
MolSysViewer objects.

It prepares the requested viewer's coordinate resources through the existing
NGLView _set_serialization hook. It builds dependency_state directly from that
viewer and the public nglview.color.ColormakerRegistry singleton, then supplies
the resulting state to the public embed_snippet API and html_template.
Existing CSS resources and complete coordinate structure serialization remain.
A finally block invokes _unset_serialization after success or failure.
The implementation neither serializes global state for later pruning nor
monkeypatches a shared embedding function.

The private preparation/cleanup hooks have matching contracts in inspected
NGLView 3.0.4 and 4.0.1. Reuse is necessary because the provider's public HTML
exporter does not accept the restricted state. This is a versioned integration
boundary requiring directed receiving when the provider changes.

### Requested GUI theme resource amendment

Root receiving passed 103 cases in each provider profile and reported doctest
exit 0 for the initial repair. That receipt is retained before this amendment;
it does not qualify the amended source. Root review then identified an additional
required resource when the requested viewer uses gui_style='ngl'.

In both inspected providers, view._widget_theme is an ordinary unsynchronized
attribute. It is absent from dependency_state even for a GUI-enabled viewer.
The original provider adds a theme through a process-global _INIT_VIEWS entry,
which can describe an unrelated last-created GUI view. The wrapper now adds
only the theme explicitly referenced by the requested view, when present. It
never reads that global last-created theme entry.

Synthetic before/after probes on 3.0.4 and 4.0.1 confirmed the missing theme and
its corrected inclusion, while the independent molecular B model/PDB remained
excluded. All four probes exited 0. Receipts are retained under the existing
export-scope cache as ngl304-before-theme.json, ngl401-before-theme.json,
ngl304-fixed-theme.json and ngl401-fixed-theme.json.

ThemeManager is a singleton in both inspected versions: two GUI views may
legitimately share the same theme. The new single regression therefore uses
two natural phases. B enables its GUI while A has no theme, so B's theme must
be excluded from A's export. A then enables its own GUI, so its explicitly
referenced theme/CSS and view specification must be included while B's
molecular data stays excluded. This does not invent separate themes when the
provider intentionally shares one. The prior eight cases, including the
coordinate/unit assertions, are preserved; root receiving of the nine-case
module is pending. No pytest was run by the implementing agent.

### Transitive embedding API floor

NGLView 3.0.4 declares ipywidgets>=7. The exact official ipywidgets 7.0.0 wheel
was acquired and SHA-256 verified without installation. Its embed.py already
defines html_template (line 43), dependency_state (line 105),
embed_data with explicit state (line 138) and embed_snippet with explicit
state (line 186), with the required contract. No higher ipywidgets floor is
needed for these APIs.

The [artifact receipt](../../../.pytest_cache/pre1-review-20261106/providers/nglview-pytraj-review/export-scope/ipywidgets7-api-artifact.json)
records wheel SHA-256
44be54c52b68db4b59b246e67051076aaee9141441e7b009c865f7202512d63f.
This establishes source/API availability in 7.0.0, not execution of an old
7.x runtime on current Python. Actual synthetic exports used ipywidgets 8.1.9.

## Why

A standalone molecular-view export is commonly shared as one selected scene.
Independent molecular data can be recoverable from its HTML without appearing
in the displayed scene. This is an export-scope defect with a possible
confidentiality consequence. The controlled evidence establishes synthetic
extra data, not a real private-data disclosure or remote transfer.

## What is measured and what is assumed

| Observation | NGLView 3.0.4 | NGLView 4.0.1 |
| --- | --- | --- |
| Raw provider export includes independent B's PDB | yes | yes |
| Former MolSysMT wrapper includes B's PDB | yes | yes |
| B belongs to A plus registry's dependency closure | no | no |
| B has an HTML view specification | no | no |
| Unrestricted manager models in the fresh two-view probe | 40 | 40 |
| Explicit dependency-state control models | 19 | 19 |
| Control retains A and excludes B/model/PDB | yes | yes |
| Plain probe native exit | 0 | 0 |

These counts characterize the isolated probes, not a general model-count
invariant. Receipts select models by their actual model_id:
[3.0.4](../../../.pytest_cache/pre1-review-20261106/providers/nglview-pytraj-review/export-scope/ngl304-receipt.json),
[4.0.1](../../../.pytest_cache/pre1-review-20261106/providers/nglview-pytraj-review/export-scope/ngl401-receipt.json).
No unrelated trajectory-coordinate resource was observed; the demonstrated
extra molecular data is B's initial PDB and archived structure message.

The existing coordinate/unit test is preserved. It decodes every float32
coordinate structure, verifies the external structure count and conversion
from nm to angstroms, and checks source coordinates. Added guards cover:

- exclusion of B while retaining A's PDB and required registry state/view;
- ordinary and explicitly trusted calls;
- an unrelated widget whose embed serializer raises, proving global state
  cannot be collected first and pruned afterward;
- finally cleanup after a destination error, preserving the original exception;
- a legitimate MolSysViewer object rejected by the NGL-specific boundary.

No pytest or doctest was run by the implementing agent. Root receiving owns
those results and any closure decision.

## What was refuted

- Extra models are necessarily required references: B is outside the selected
  viewer plus registry's dependency closure.
- Only a harmless identifier is included: B's complete synthetic loadFile PDB,
  including coordinates, is recoverable from the HTML.
- A selected-view list restricts all manager state: the documented default
  state is process-wide.
- Upgrading NGLView to 4.0.1 alone fixes the scope: the same extra PDB is present.
- Exactly one NGLModel is a valid general assertion: independent global widgets
  can exist. Coordinate checks must select the requested view.model_id.

## Scope and exclusions

The repair owns MolSysMT's standalone NGLView HTML boundary. It does not change
upstream packages, NGLView molecular converters or the separate #630 work.
Only synthetic data was tested. Browser rendering, JavaScript execution and
offline asset availability are separate qualification claims. The shared color
registry remains an explicit resource; filtering global color-style
definitions is outside the independent molecular-widget scope.

## Acceptance criteria

1. The selected viewer retains its structure, all coordinate structures,
   angstrom resource contract and unchanged native source data.
2. Independent molecular widgets and their archived PDB payloads are absent;
   required widget dependencies, color-registry state/view and the requested
   viewer's GUI theme/CSS/view are present. An unrelated GUI view's theme is
   excluded when the requested viewer has no theme.
3. No global state collection, post-export pruning or global monkeypatch is
   used. An unrelated failing embed serializer is never called.
4. Temporary serialization resources are cleared after success and errors,
   and the original destination error propagates.
5. The guard module and updated docstring pass on supported baseline/current
   providers before closure; API-floor inspection is not frontend validation.

## Dependencies and risks

ipywidgets provides the needed public state-restriction API from its accepted
7.0.0 minimum. NGLView's resource hooks remain private, with an explicitly
inspected version boundary. Future provider receiving must retain dependency,
resource and cleanup guards. No upstream issue or remote write was made by
the implementing agent.

## Provenance

Synthetic probes ran on the existing Linux host with Python 3.14.7, NumPy 2.4.6,
ipywidgets 8.1.9 and NGLView 3.0.4 public source / installed 4.0.1. Receipts use
2026-11-07 UTC timestamps for work initiated on 2026-11-06 local time.
The 3.0.4 source archive SHA-256 is
e7ea100e77bfbf52bc89aaac5692da4358c86be4de103c78c34c76076f4bc9a8.

Reproduction writes only ignored-cache synthetic HTML and receipts. Production
edits are restricted to the wrapper, its mirrored test module and this report.

## Resolution — 2026-11-06

Source `fae9ab5575383018a19ca8fac484f7ea3300da9d` replaces unbounded manager-state delegation with an explicit
widget dependency closure. Only the requested view, its shared color registry
and its explicitly referenced GUI theme/resources are prepared and embedded.
Unrelated molecular widget data is neither serialized first nor pruned later.
Native NGL resource preparation retains all requested structures and angstrom
coordinates; finally cleanup executes even when writing fails. A different
valid MolSysViewer is rejected before the NGL hooks.

Both final actual NGLView 3.0.4/Python 3.12 and 4.0.1/Python 3.14 selections pass 104,
no omissions, native exits 0. This includes nine dedicated HTML cases and the
real public doctest. The cases assert coordinate values/units, A's retained PDB,
B's excluded PDB/model, required resource/view specs, no global serialization
before filtering, normal/trusted write-error cleanup, wrong-viewer rejection
and two-phase GUI-theme scope. They check molecular/state behavior rather than
just model counts or an existing HTML file.

Pre-theme receiving passed 103 per provider, but review then reproduced a
required unsynchronized theme omission. The final guard excludes B's theme
when A has no GUI theme, then includes the shared theme actually referenced by
A after A enables its GUI; B's molecular state stays excluded. Original
coordinate/unit assertions are retained. Source-only inspection of the official
ipywidgets 7.0.0 payload verifies that the public state-embedding APIs already
exist; no invented higher transitive floor is added. Runtime receiving uses 8.x.

User Guide tutorial/form and course module 06 explain exported scope, required
resources and structure selection for smaller exports. Their code, outputs,
anchors, IDs and metadata are unchanged. The
[portable receipt](../../../devtools/data/nglview_runtime_receiving_524_630_631_20261106.json)
retains public artifacts, native exits, prior failed assumptions, theme probes,
private-provider-hook bounds and source/installed/browser limits. It does not
claim unrelated trajectory-buffer exposure, arbitrary-data isolation or visual
acceptance. Public delivery and actual board closeout remain separate.
