# MolSysMT Data Assets Guide

This guide applies to files under `molsysmt/data/`.

## Source of truth

- Bundled data artifacts in `molsysmt/data/` are generated from the scripts in `molsysmt/data/_make/`.
- Do not hand-edit generated binary assets (`.h5msm`, `.msmpk`, trajectories, compressed structure files) unless there is no reproducible generator path.
- If a bundled artifact violates a contract, rerun the relevant generator first and inspect the regenerated result before patching the artifact.

## Regeneration workflow

- Use the generator script that owns the artifact whenever possible.
- If a script produces several outputs, keep the regeneration scope as narrow as practical, but preserve the same generation path used by the script.
- When a generator depends on online sources, record which external source was used and which identifiers were requested.

## Validation after regeneration

- Validate topology identifiers and names after regeneration, especially:
  - `component_id`
  - `molecule_id`
  - `entity_id`
  - `chain_id`
- Preserve explicit identifiers from the source format when they exist.
- Only use fallback identifiers when the source format does not define them explicitly.
- Run targeted tests for the affected form adapters and any downstream integrations that rely on the regenerated artifact.

## Documentation

- If a data issue reveals an undocumented generation rule, update this file or the corresponding developer documentation in the same change.
