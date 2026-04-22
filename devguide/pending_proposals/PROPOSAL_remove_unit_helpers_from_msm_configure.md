# Proposal: Remove unit-related helpers from `molsysmt.configure`

## Status
Pending

## Purpose
Standardize configuration patterns across the **MolSysSuite** and avoid redundancy in MolSysMT.

## Motivation
Currently, MolSysMT provides helpers like `msm.configure.length_unit` which are simple wrappers around `pyunitwizard` configurations. This creates an inconsistent user experience when moving between tools in the suite (e.g., TopoMet might not have these helpers). 

## Recommendation
1. Remove all unit-specific attributes from the `molsysmt.configure` object.
2. Instruct users to use the `pyunitwizard` configuration module directly (accessible via `molsysmt.pyunitwizard.config` or similar).
3. Update all documentation and course modules to reflect this change.
