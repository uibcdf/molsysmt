# Migrating H5MSM Recipe Contract

Keep the 0.4 source file separate from the 0.5 output, use `molsys` for the
native result, and describe missing optional layers with `None`. The recipe
must not imply that the registered `file:h5msm` adapter already reads 0.5.
