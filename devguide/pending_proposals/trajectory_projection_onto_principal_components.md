# Proposal: Projecting Trajectories onto Principal Components

## Status and scope

This is a post-contract extension proposal. The accepted PCA contract returns
covariance eigenvectors and eigenvalues; it does not project trajectory frames.
This proposal records a possible projection capability without overloading the
meaning of the existing outputs.

## Why this is useful

Eigenvectors describe collective coordinate directions, but essential-dynamics
workflows usually also need the per-frame scores along selected modes. Those
scores make it possible to plot trajectories in PC space, compare ensembles,
cluster conformations, and reconstruct motion along a mode.

Keeping projection explicit avoids calling an eigenvector matrix a projection
and allows users to reuse a fitted basis on a different trajectory.

## Candidate API designs

Evaluate both of these designs before implementation:

1. add an explicit output mode to
   `molsysmt.structure.principal_component_analysis()`; or
2. add a focused function such as
   `molsysmt.structure.project_onto_principal_components()` that accepts a
   molecular system, eigenvectors, the training mean, and selected mode indices.

The second design is preferable if fitting and transformation need separate
lifecycles, because it makes projection onto an externally supplied or reused
basis unambiguous.

## Required mathematical contract

The proposal must define:

- the feature ordering used to flatten `(n_atoms, 3)` coordinates;
- how the training mean is returned, stored, and applied;
- whether structures are aligned before fitting or projection;
- whether atom weights affect only fitting or also the projection metric;
- the output shape `(n_structures, n_modes)`;
- score units, which are coordinate units for dimensionless eigenvectors;
- mode ordering and eigenvector sign arbitrariness;
- behavior when projecting a system with incompatible atom correspondence.

Projection must not silently refit the PCA basis or recenter against the target
trajectory's own mean when a training mean was supplied.

## Validation

Before acceptance:

1. project an analytic diagonal-covariance trajectory and compare scores with
   direct dot products;
2. verify reconstruction from all modes to numerical tolerance;
3. verify projection of a second trajectory with the original training mean;
4. compare with an independently implemented NumPy or scikit-learn oracle under
   an explicitly matched covariance convention;
5. test unit propagation and atom-correspondence failures;
6. update the User Guide, Cookbook, and all four course paths.

## Exclusions

This proposal does not authorize adding scikit-learn as a hard dependency,
changing the accepted eigenvector/eigenvalue return contract, or embedding a
stateful fitted PCA model in `MolSys` without a separate architecture decision.
