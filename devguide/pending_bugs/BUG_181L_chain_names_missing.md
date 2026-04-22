# Bug: Missing chain names in T4 Lysozyme (181L) internal system

## Status
Pending

## Description
When running `msm.info(lysozyme, element='chain')` on the internal system `systems['T4 lysozyme L99A']['181l.h5msm']`, the `chain_name` attribute returns `nan` instead of the expected identifiers (e.g., 'A').

## Evidence
Observed during the Master's review of Module 5. Other formats of the same system (like PDB or MMTF) might contain this information, suggesting a loss of metadata during the H5MSM conversion or internal database preparation.

## Recommended Action
1. Audit the `181l.h5msm` file in the internal database.
2. Re-generate the file ensuring all topological attributes (chain names, IDs) are correctly preserved from the source PDB/MMTF.
