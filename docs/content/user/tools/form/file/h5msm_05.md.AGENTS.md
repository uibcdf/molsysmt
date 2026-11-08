# H5MSM 0.5 Page Contract

Document that public `molsysmt.convert` writes H5MSM 0.5 and that the
legacy file-form adapters still handle some 0.3/0.4 operations.
Keep migration examples source-preserving and describe unsupported fields as
errors rather than silent conversion. Use native indices, not element IDs,
when explaining structure-to-state mappings.
Preserve topology layer 4 naming declarations, registry/code validation, unknown
old context and the unchanged H5MSM 0.5 root.

Preserve the default single-path H5MSM 0.5 whole-Topology projection: resident
stable inventory only, no unrelated domain payloads, explicit contextual-route
and requested-layer validation limits. Do not imply a constant-memory load.
