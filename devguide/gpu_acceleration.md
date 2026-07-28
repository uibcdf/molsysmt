# GPU Acceleration Status

MolSysMT 1.0 has no supported GPU kernel backend.

The pre-1.0 CUDA and Taichi experiments covered different subsets of the API
and did not form one coherent, validated capability. They were removed with
the Numba runtime so that the release does not advertise a backend matrix it
cannot guarantee.

Public `use_gpu` and `gpu_backend` arguments remain accepted as compatibility
inputs. Automatic requests use the bundled Rust CPU kernels. An explicit
`use_gpu=True` request emits `GpuNotAvailableWarning` and then uses the same CPU
path. No successful fallback may be reported as GPU execution.

Future acceleration must be designed around the Rust kernel architecture and
must define, per operation:

- supported devices and platforms;
- precision and numerical tolerances;
- transfer and device-residency semantics;
- fallback and error behavior;
- installed-artifact and scientific-property tests;
- benchmarks that include transfer and initialization costs.

The design work is tracked in
`pending_proposals/rust_gpu_backend_options.md`. It is post-1.0 work and is not
part of the current release contract.
