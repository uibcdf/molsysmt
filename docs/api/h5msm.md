(api-h5msm)=
# H5MSM

Reading versioned native domains and explicitly selecting an output schema.
The default writer remains 0.5; 0.6 is experimental. See
{ref}`user-tools-form-h5msm-05` and {ref}`user-tools-form-h5msm-06` for the
storage, association, query and memory contracts.

```{eval-rst}
.. automodule:: molsysmt.h5msm
   :members: read, write, read_layers, read_axis_sizes, write_layers, append_structures, migrate_to_05, migrate_04_to_05
```
