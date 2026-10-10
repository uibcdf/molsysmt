---
summary: Expose reusable fixed-state hydrogen-bond site directions through public geometry tools.
issue: uibcdf/molsysmt#375
status: open
opened: 2026-10-10
closed:
verification: inspected
area: [structure, physchem, pbc, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Fixed-state hydrogen-bond site directions

**Reported:** 2026-10-10, provider request from uibcdf/pharmacophoremt#41.
**Status:** Post-1.0 capability proposal; chemical recognition and geometry stay distinct.

## What

Provide general directed atom-pair geometry and compose it with fixed-state
hydrogen-bond site recognition. Donor-H directions derive from indexed observed
atoms. Acceptor directions require an explicitly named chemical/local-geometry
model with multiplicity and unsupported/undefined outcomes; they are not supplied
by the existing chemical inventory.

## How

Provider source inspected at `072aa9bdbfb9299f7e3256f9b27f6aae8ea52629` offers:

| Existing piece | Reuse | Missing contract |
|---|---|---|
| `physchem.get_hbond_sites` | Declared-state donor-H pairs and acceptor indices with rule/evidence. | Its contract explicitly excludes geometric directions. |
| `basic.get` | Form-agnostic coordinates, box and source axes. | Coordinate access does not define a directed-pair result or undefined-vector policy. |
| `structure.get_distances`, `get_angles`, `get_least_squares_plane` | General unit-aware scalar geometry and fitted planes. | Distances omit direction; a plane normal is not a universal lone-pair model. |
| `pbc.wrap_to_mic` | Reconstruction/wrapping of covalent components under its explicit policy. | Moving a component is not an immutable atom-pair displacement query. |
| Existing Rust MIC primitives and private periodic reconstruction helpers | Candidate calculation reuse after reviewing matching conventions. | Their internal functions are not a public form/unit/identity/image contract. |

The inspected public exports provide no directed atom-pair displacement operation
covering the consumer contract. Public geometry belongs in `structure`; periodic
image conventions/reconstruction belong in `pbc`; chemical direction interpretation
belongs in `physchem`. Consumers should compose these owners, retaining chemical
criteria locally only when genuinely pharmacophore-specific. Measure workloads
before adding new Rust routines rather than duplicating existing primitives.

Define ordered pairs and displacement sign, structure-axis order, length units,
dimensionless normalized directions, finite/zero-length handling and source maps.
For PBC, return the actually used image under the shared row-vector box convention
with an explicit reference participant. Test the selected MIC behavior, including
triclinic cells and ties; do not silently reconstruct images from a scalar distance.
Large structure selections require bounded chunked execution rather than dense
all-pairs materialization.

Then define fixed-state site geometry using recognized donor-H pairs, an explicit
acceptor model and a coherent state/structure association. Preserve directional
site multiplicity and atom correspondence. Unsupported chemistry or degenerate
geometry must remain unassessed or fail according to a documented policy; an
arbitrary default direction cannot masquerade as a calculated lone pair.

## Why

The consumer reports local donor-H subtraction and a legacy acceptor projection
from the first bonded neighbor, with a fallback axis when no neighbor exists.
That historical projection is a hypothesis heuristic, not an established general
lone-pair model. A shared molecular geometry tool would remove duplication while
PharmacophoreMT retains ownership of complementary ligand hypotheses and their
projection distances. This provider review did not execute the consumer source.

The [frozen scope](../release_1_0_scope.md#admission-rule) defers these new public
tools and scientific models. The existing molecular site inventory and interaction
detectors do not claim to supply them. Environment-dependent hydrogen refinement
in uibcdf/molsysmt#323 and aromaticity diagnostics in uibcdf/molsysmt#350 remain
separate concerns, not prerequisites to the elementary donor-vector operation.

## What is measured and what is assumed

Evidence is source/contract inspection and the consumer issue. No vector kernel,
acceptor model, scientific comparison or performance benchmark was executed for
this proposal. A donor-H vector is directly geometric; assigning an acceptor's
lone-pair directions requires additional scientific assumptions and evidence.

## What was refuted

Candidate acceptor indices do not encode lone-pair direction. A first-neighbor
projection or a fallback `[0, 0, 1]` cannot establish one. Providing donor vectors
alone would not complete the acceptor-model portion of this request. A public
geometry tool must not require the consumer to import private MIC helpers.

## Scope and acceptance criteria

- Validate ordered-pair and nonconsecutive structure selections, empty results,
  source maps and immutable input across forms supplying required attributes.
- Compare independently expected displacements/directions under changed length
  units, pair reversal, PBC images, zero/nonfinite geometry and reordered axes.
- For each named acceptor model, document its source, chemistry coverage,
  multiplicity and unsupported cases; test numerical geometry against an
  independent reference rather than the implementation's own formula.
- Exercise selected chemical-state coherence and preserve original method,
  parameters, units, evidence and producer versions in derived site results.
- Complete argument/dependency validation, scalability controls, docstrings,
  User Guide, Cookbook and course material before exporting the new tools.

No implicit protonation, hydrogen addition, environmental optimization, pocket
inference or pharmacophore projection policy is included. PharmacophoreMT can
continue its bounded donor-vector migration while recording this provider gap;
it need not create a new local lone-pair engine to unblock current workflows.
