# Competitive Landscape and Vision

MolSysMT aims to provide a form-agnostic, unit-aware interface across molecular
data representations, analysis kernels, builders, optional third-party engines,
and visualization. This is a strategic direction, not evidence that MolSysMT
already supersedes mature specialist libraries.

The dated March 2026 comparison and capability inventory are archived under
`archive/assessments/` because several absolute claims were not reproducibly
supported and implementation status has changed.

## Evidence-based comparison dimensions

External comparisons should use reproducible workflows and current releases:

- accepted data forms and conversion fidelity;
- topology, trajectory, and selection semantics;
- units and numerical precision;
- analysis breadth and scientific parity;
- building and repair behavior;
- eager, chunked, CPU-parallel, and GPU execution;
- optional-dependency isolation and import cost;
- diagnostics and failure integrity;
- documentation, examples, release cadence, and community adoption.

Architectural breadth is a strength only when capability claims are backed by
delivery tests. Delegating to a backend does not automatically provide uniform
semantics, errors, units, or support across all input forms.

## Current differentiators worth strengthening

- a common molecular-system abstraction and conversion ecosystem;
- native topology/structure separation and declarative forms;
- selection and attribute access across multiple representations;
- integrated construction, analysis, visualization, and unit handling;
- explicit soft-dependency management;
- an educational course organized around scientific workflows.

## Current credibility constraints

The highest-value improvements are reliability rather than more headline
features: explicit form tiers, attribute-delivery validation, conversion
fidelity metadata, scientific reference tests, failure-safe heavy execution,
API stability governance, and executable documentation synchronization.

Any future scorecard should include the compared versions, environment, test
systems, exact commands, raw results, and known unsupported cases. Marketing
language must not be promoted into a normative developer contract.
