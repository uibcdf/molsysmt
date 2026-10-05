# Peptide candidate report contract

Preserve `Tutorial_Peptide_Bond_Candidates`, source atom/group/structure indices,
typed aligned candidate arrays and roles, unit-bearing distances/parameters,
original producer versions and detached group coverage. Keep source adjacency,
chain/TER boundaries and conservative alternate-backbone/OXT policy explicit.
Do not imply automatic bond application, sequence repair or certified chemistry.
Numeric/all H5MSM 0.5 access reads one coordinate structure. Guard:
`tests/build/test_get_peptide_bond_candidates.py`.
