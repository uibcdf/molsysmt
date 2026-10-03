(cookbook-migrating-h5msm)=
# Migrating an H5MSM file

*Moving a legacy molecular system into the modular H5MSM 0.5 schema.*

This recipe keeps a 0.3 or 0.4 source file and writes a separate 0.5 file. The
helper validates that the native system reconstructed from the source can be encoded
without dropping an unsupported field.

## Translating the file

```python
import molsysmt as msm

msm.h5msm.migrate_to_05("trajectory_04.h5msm", "trajectory_05.h5msm")
molsys = msm.h5msm.read("trajectory_05.h5msm")
print(molsys.structures.n_structures)
```

## Resolving unit errors

Legacy H5MSM 0.3/0.4 readers require explicit units. Dataset units are checked against any duplicated group/root declarations; equivalent spellings are accepted, but different scales or dimensions raise `FormatError`. A missing dataset unit may use a coherent explicit group/root declaration. Velocity units may be derived from explicit length/time declarations. B factors require their own unit because legacy writers negotiated it independently of coordinates; missing metadata never implies nm or ps. Public queries and iteration convert the resulting quantities to your active PyUnitWizard policy. Migration to 0.5 validates these units before writing.

If migration rejects a file, recover the correct declarations from the original
writer or its documented unit contract. Recreate the file with those units;
MolSysMT cannot infer a missing unit from the numerical values.

## Inspecting independent layers

Read only the domains needed for the next step:

```python
payload = msm.h5msm.read_layers(
    "trajectory_05.h5msm", layers=["chemical_states", "interactions"]
)
states = payload["chemical_states"]
analyses = payload["interactions"]
```

An absent layer has value `None`. An interaction layer can also contain an
analysis whose evaluated structures have zero observed interactions.

If a 0.5 file contains topology and chemical states without structures, load it
as a native `MolSys` before selecting atoms:

```python
molsys = msm.h5msm.read("topology_chemistry_05.h5msm")
subset = msm.extract(molsys, selection=[0])
assert subset.structures is None
msm.convert(subset, to_form="file:h5msm", output_filename="selected_05.h5msm")
```

The output retains the selected chemistry without fabricating coordinates.
Do not select structure indices unless a present domain declares that axis.

:::{seealso}
See {doc}`H5MSM 0.5 <../tools/form/file/h5msm_05>` for the schema API and
{ref}`the molecular system model <user-foundations-molecular-system-definition>`
for domain ownership.
:::
