# Reference bond-pair tutorial contract

Preserve `Tutorial_Get_bonded_atom_pairs`, its executed alanine example and
existing outputs. Reference pairs use local name positions or an explicit
parallel atom-index map; never describe their endpoints as atom names or IDs.
For the received saccharide/small-molecule/cap branches, keep flat list/tuple/
NumPy admission, input preservation, first-occurrence duplicate names,
endpoint/row ordering and family-specific unknown/error distinctions explicit.
Reference lookup neither reads coordinates nor assigns or edits system chemistry.

Keep the seven-entry-point index contract explicit: parallel name/index maps,
lexicographic row sorting, oxygen-first water endpoints, all-occurrence amino-
acid expansion, first-occurrence ion lookup and None/empty/error distinctions.
Keep scoped map validation explicit: nonnegative int64-range integers, exact
parallel length, repeated-index admission, scalar compatibility only for amino-
acid/ion routes, and catalogued errors before reference access. Existing trusted
skip routes require valid inputs; they do not validate malformed maps.
