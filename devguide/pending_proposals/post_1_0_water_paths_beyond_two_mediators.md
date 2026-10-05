---
summary: Post-1.0 water paths beyond two mediators
issue: uibcdf/molsysmt#338
status: open
opened: 2026-10-05
closed:
verification: inspected
area: [api, structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Post-1.0 water paths beyond two mediators

## What

Evaluate whether water-mediated hydrogen-bond analysis should extend beyond the implemented exact one- and two-water paths.

## How

Start from a concrete scientific/client use case and attributable reference definition. Define path order, complete simultaneous hydrogen-bond legs, participant roles, orientation, duplicate/cycle semantics and periodic image composition. Bound search growth and preserve sparse results, atom/structure queries and evidence. Compare a bounded maximum order with explicit network queries before choosing an API.

## Why

The interaction roadmap leaves paths through more than two waters as an extension. The implemented `hbond_water_path` offers exact order one or two. Preserve this question in an owned issue, without implying that longer paths are already meaningful or promised.

## What is inspected and what is assumed

The public function and its order contract were inspected in `molsysmt/interactions/water_bridges/get_water_bridges.py`. No new network benchmark or biological significance is demonstrated here.

## What was refuted

Supporting two mediators does not establish arbitrary-order correctness, manageable cost or independent scientific value. A geometric chain without all simultaneous leg evidence is not automatically a water bridge.

## Scope and exclusions

Post-1.0 under the [scope freeze](../release_1_0_scope.md). Existing one/two-water methods and their attributed leg definitions remain unchanged. This is a go/no-go study, not an approved implementation commitment.

## Acceptance criteria

- Establish reference-backed use cases and decide whether a longer-path extension is justified.
- If accepted, define many-body participants, explicit leg evidence, determinism, cycle/duplicate policy and PBC references.
- Verify sparse selection and persistence against independent path examples and measure worst-case combinatorial/working memory cost.
- Record the decision, including a justified rejection, and any resulting implementation follow-up.

