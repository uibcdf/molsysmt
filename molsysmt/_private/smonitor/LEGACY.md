# Legacy warnings and exceptions

MolSysMT keeps `_private/warnings` and `_private/exceptions` for backward
compatibility. New messages and user guidance live in the smonitor catalog:
`molsysmt/_private/smonitor/catalog.py`.

Planned direction:
- Use the catalog as the single source of truth for messages and hints.
- Keep legacy classes as thin wrappers that emit smonitor events.
- Remove custom message composition from legacy classes once all callsites
  rely on the catalog.
