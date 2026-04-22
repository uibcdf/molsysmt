# Proposal: Add aliases and singular/plural tolerance for Form names

## Status
Pending

## Purpose
Improve developer and user experience by allowing common variations or typos in form names during `convert()`, `get_form()`, and other core functions.

## Motivation
Users might instinctively type `molsysmt.Structure` (singular) instead of the canonical `molsysmt.Structures` (plural). Currently, this results in a `NotSupportedFormError` or a failure in form recognition. Since the intent is clear, the framework should be empathetic and resolve these aliases internally.

## Recommendation
Implement a normalization layer in the form recognition logic:
1. Create a mapping of common aliases (e.g., `molsysmt.Structure` -> `molsysmt.Structures`).
2. Add a basic pluralization/singularization check for known native forms.
3. Ensure this normalization happens early in the `arg_digest` process for the `to_form` and `from_form` arguments.
