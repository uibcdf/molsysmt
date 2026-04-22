# Bug: Numerical noise in coordinates after `set()` with strings

## Status
Pending

## Description
When setting coordinates using a string with units (e.g., Angstroms), the retrieved value in the default unit (e.g., Nanometers) shows significant numerical noise (e.g., `0.10000000149011612` instead of `0.1`).

## Evidence
Reported during the Master's review of Module 6:
`msm.set(lysozyme, ..., coordinates='[1.0, 4.0, -2.0] angstroms')`
returns:
`[[[0.10000000149011612 0.4000000059604645 -0.20000000298023224]]] nanometer`

## Possible Causes
1. **PyUnitWizard String Parsing:** The conversion from string to float might be using `float32` internally or introducing noise during the unit scaling.
2. **Native Storage:** Native objects like `Structures` might be defaulting to `float32` arrays, losing precision during the write/read cycle.

## Recommended Action
1. Audit the string-to-float64 conversion in `pyunitwizard`.
2. Ensure that native MolSysMT objects use `float64` for structural data unless explicitly requested otherwise.
