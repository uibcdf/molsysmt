# Migrating H5MSM Recipe Contract

Keep the 0.4 source file separate from the 0.5 output, use `molsys` for the
native result, and describe missing optional layers with `None`. The registered
`file:h5msm` adapter reads 0.5 and writes it by default; preserve the legacy-read
warning and source-preserving migration contract. Imported primary occupancies
and sparse alternate observations must keep their axes and missing values.

Preserve the default single-path H5MSM 0.5 whole-Topology projection: resident
stable inventory only, no unrelated domain payloads, explicit contextual-route
and requested-layer validation limits. Do not imply a constant-memory load.
