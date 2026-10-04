(Tutorial_Assign_AutoDock_Types)=
# Assigning AutoDock types

*Attaching a complete named typing report to a detached native system.*

{func}`molsysmt.build.assign_autodock_atom_types` calls the general chemical
classifier and returns a new `MolSys`. Exactly one nonempty chemical state is
required for the current mechanical storage. The source's chemistry, atom IDs,
structures, charges and named analyses remain unchanged.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.build.assign_autodock_atom_types`
:::

## Attaching a named profile

```python
import molsysmt as msm

molsys = msm.build.assign_autodock_atom_types(
    msm.systems['caffeine']['caffeine.sdf'], typing_scheme='autodock4')
report = molsys.molecular_mechanics.atom_type_assignment
assert report['rule_version'] == 'chemical_environment@1'
```

Inspect {ref}`Tutorial_AutoDock_Typing` for the exact profile, prerequisites and
exclusions. Mechanical labels and their report live in `MolecularMechanics`;
they do not create a competing chemical store or establish full force-field
parameterization. The operation retains every source structure. Native copying
may materialize an entire sequence; this attachment route is not streaming.

## Preserving parent assignments

Copy and pickle retain producer versions. Atom extraction retains parent labels
and projects per-atom rule evidence and source maps. Original evaluated scope
and source atom count remain explicit. The extracted fragment is not classified
again in isolation. Coordinates and atom names are not typing inputs.

The report binds ordered values to chemistry and the selected state. PDBQT
export rejects a stale named report or a mismatched scheme before opening the
output file. Direct edits to chemical tables or label storage are detected there;
ordinary `atom_ff_type` property replacement clears named typing attribution.
Such unqualified replacement makes the labels a caller declaration, with the
writer's existing element and field validation. It does not certify chemistry.

Strict composition rejects separate named assignments without a joint calculation.
Intersection composition keeps compatible label columns and warns while clearing
their original typing attribution. Existing analyses retain their snapshots;
explicitly invalidate analyses whose evidence depends on changed mechanics.

## Exporting explicitly

Partial charges are a separate named operation. You can calculate charges and
types in either order. The PDBQT writer requires coordinates, explicit labels,
finite charges and `typing_scheme='autodock4'`; it retains every indexed H.
A ligand torsion tree and H-merging protocol are separate caller choices.

Named labels emit a `REMARK MOLSYSMT_ATOM_TYPES` JSON summary with scheme,
rule version, original software, source coverage and projection status. Native
PDBQT reading preserves labels but does not restore the complete assignment
report. `MolecularMechanics` is experimental and excluded from H5MSM 0.5;
its persistence remains planned for 0.6. Do not expect a 0.5 round trip to carry
these assignments.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_AutoDock_Typing`
- {ref}`Tutorial_Assign_Partial_Charges`
- {ref}`cookbook-native-pdbqt`
:::
