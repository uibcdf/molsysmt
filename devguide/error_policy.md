"""
MolSysMT Developer Guide — Error and Warning Policy
"""

# Error and Warning Policy

## Single Source of Truth
All diagnostics must emit through SMonitor catalogs. Do not hardcode warning
or error messages in code paths.

## Exceptions
Legacy exceptions may exist for compatibility, but they must emit SMonitor
events and use catalog templates.

## Warning Categories
Warnings should be specific, actionable, and carry context in `extra`.

## Required Extras
Follow `SIGNALS` contracts in `molsysmt/_private/smonitor/catalog.py`.
