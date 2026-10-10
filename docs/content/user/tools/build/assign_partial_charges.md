(Tutorial_Assign_Partial_Charges)=
# Assigning partial charges

*Attaching a validated named charge assignment to a detached molecular system.*

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.build.assign_partial_charges`
:::

```python
import molsysmt as msm

molsys = msm.build.assign_partial_charges(
    msm.systems['caffeine']['caffeine.sdf'], method='gasteiger_marsili')
assert molsys.molecular_mechanics.partial_charge_assignment['coverage'] == 'complete'
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See {ref}`user-foundations-entrance-demo-systems` for the bundled datasets.
:::

The input remains unchanged. The output retains its atoms, IDs, chemistry,
coordinates and analyses and stores charges in MolecularMechanics, independently
of ChemicalStates formal charges. Exactly one chemical state is required for
attachment; multiple states can be calculated separately through
{func}`molsysmt.physchem.get_partial_charges`. Existing charges are explicitly
replaced. Other force-field parameters and AutoDock labels are not assigned.
Named analyses retain their original snapshots; explicitly invalidate/recalculate
any analysis that depends on the changed mechanical parameters.

Native charges and numerical report totals always use elementary charge, even
when the active PyUnitWizard policy declares only length and time standards.
Assignment preserves that policy. The quantity-returning
{func}`molsysmt.physchem.get_partial_charges` instead requires a charge standard
and returns its requested presentation, for example coulomb.

Read {ref}`Tutorial_Partial_Charge_Assignment` for model prerequisites, units,
total-charge checks, projected scope, provenance, stale-assignment checks and
export limits. Mechanical assignments are **not persisted by H5MSM 0.5**.

:::{seealso}
:class: dropdown

- {ref}`cookbook-assigning-partial-charges`
- {ref}`Tutorial_Fixed_State_Hydrogens`
:::
