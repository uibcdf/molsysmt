# Proposal: Add `pdb:` as an alias for `pdb_id:` in string forms

## Status
Pending

## Purpose
Improve user experience by allowing a more intuitive prefix for PDB ID strings.

## Motivation
Currently, MolSysMT recognizes `pdb_id:XXXX` or just `XXXX` for PDB entries. However, many users instinctively try `pdb:XXXX`. Returning an error or failing to recognize the form in this case creates unnecessary friction.

## Recommendation
Update the string form recognition logic (likely in `molsysmt/form/string_pdb_id/`) to accept `pdb:` as a valid prefix, standardizing it internally to `pdb_id:`.
