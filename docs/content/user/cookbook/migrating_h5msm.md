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

:::{seealso}
See {doc}`H5MSM 0.5 <../tools/form/file/h5msm_05>` for the schema API and
{ref}`the molecular system model <user-foundations-molecular-system-definition>`
for domain ownership.
:::
