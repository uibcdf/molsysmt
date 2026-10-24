(Cookbook_Weighting_PCA)=
# Weighting a structural ensemble

*Checking weighted covariance and principal-component projections.*

Use numerical atom weights to change how much each selected atom contributes
to collective motion. Fit a molecular ensemble and make wrapped participants
whole before PCA when your scientific comparison requires those operations.
This small example checks the calculation on bundled particle coordinates.

:::{versionadded} 1.0.0
:::

## Selecting observations and atom weights

Every weight addresses an atom position in the selection. Repeated structure
indices contribute repeated observations. Weights are finite, nonnegative
numerical factors with a positive sum; they are not divided by that sum.
Lists, tuples and numeric arrays are equivalent. Dimensionless quantities are
accepted; dimensional quantities and named weight models are unsupported.

```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.systems['particles 4']['traj_particles_4.xyznpy']
atom_indices, structure_indices = [2, 0], [2, 0, 2]
weights = [1.0, 4.0]
vectors, values = msm.structure.principal_component_analysis(
    molsys, selection=atom_indices, structure_indices=structure_indices,
    weights=weights, use_gpu=False)
```

## Reconstructing the covariance and projections

Use all selected x coordinates, then y, then z. Subtract each feature's mean
over structures, multiply by the square root of its atom's weight, and form
the population covariance. Each returned eigenvector is a row, ordered by
descending variance. Its sign and the basis inside a degenerate eigenspace
do not affect the covariance check.

```python
coordinates = msm.get(molsys, element='atom', selection=atom_indices,
    structure_indices=structure_indices, coordinates=True)
xyz = puw.get_value(coordinates, to_unit='nm')
features = xyz.transpose(0, 2, 1).reshape(len(xyz), -1)
centered = (features - features.mean(axis=0)) * np.sqrt(np.tile(weights, 3))
covariance = centered.T @ centered / len(centered)
eigenvalues = puw.get_value(values, to_unit='nm**2')
np.testing.assert_allclose(vectors.T @ np.diag(eigenvalues) @ vectors,
    covariance, atol=1e-12)
projections = centered @ vectors.T
np.testing.assert_allclose(np.mean(projections**2, axis=0), eigenvalues, atol=1e-12)
```

Numeric projections here use nm and their variances use nm². Eigenvalues follow
the active PyUnitWizard squared-length presentation unit. A single structure
has zero covariance; empty atom or structure populations reject explicitly.
PCA builds a dense covariance and performs a dense eigendecomposition; it is
not a streaming or sparse analysis.

:::{seealso}
:class: dropdown

- {ref}`Principal component analysis <Tutorial_Principal_component_analysis>`
- {ref}`Quantities and units <user-foundations-governance-quantities-and-units>`
- {func}`molsysmt.structure.principal_component_analysis`
:::
