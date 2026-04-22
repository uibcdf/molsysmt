# Proposal (Suite-wide): Dimensionality-aware standard units in PyUnitWizard

## Status
Pending (Dependency for MolSysMT 1.0.0)

## Purpose
Simplify the process of defining standard units and forms in PyUnitWizard by adding a smart configuration helper.

## Motivation
Currently, setting multiple standard units is "green" (primitive). Users need a way to add standards without manually checking if a standard for that dimension already exists.

## Recommendation
Implement `puw.configure.add_standard_units(standards)` with the following logic:
1. Input: A list or dictionary of units.
2. For each unit:
    - Check its dimensionality (e.g., length, time).
    - If a standard unit for that dimensionality is already registered: Remove the old one and insert the new one.
    - If not: Simply add the new standard to the list.
3. This ensures the standards list remains lean and consistent.
