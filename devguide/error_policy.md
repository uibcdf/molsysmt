"""
MolSysMT Developer Guide — Error and Warning Policy
"""

# Error and Warning Policy

## Single Source of Truth
All diagnostics must emit through SMonitor catalogs. Do not hardcode warning
or error messages in code paths.

## Exceptions
All custom exceptions must inherit from `smonitor.integrations.CatalogException` (or a local wrapper). 
They should define a `catalog_key` that matches an entry in `molsysmt/_private/smonitor/catalog.py`.

Example:
```python
class ArgumentError(MolSysMTCatalogException):
    catalog_key = "ArgumentError"
```

## Warning Categories
Warnings should inherit from `smonitor.integrations.CatalogWarning`. Use the `warn` or `warn_once` helpers from `molsysmt._private.smonitor` to emit them.

## Required Extras
Follow `SIGNALS` contracts in `molsysmt/_private/smonitor/catalog.py`.
