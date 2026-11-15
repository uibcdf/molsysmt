# Alzheimer peptide synthesis content contract

Preserve the `course-alzheimer-peptide-synthesis` anchor, KLVFF construction,
explicit ACE/NME capping, helical-region geometry, static inspection, KLVFFAL
challenge and link to Module 25.

- Keep the native constructor as the default and LEaP explicitly optional.
  Caps belong in the ordered sequence, not unsupported builder keywords.
- Describe construction as an initial coordinate model. Neither construction nor
  capping establishes a complete chemical state, therapeutic activity or an
  energy minimum.
- Derive quartets from `chemical_states`, copy the capped model, and use public
  `structure` editors with angular quantities and `pbc=False`. The teaching
  targets phi -60, psi -45 and omega 180 degrees do not predict a stable helix.
- Measure achieved torsions with explicit display units and circular differences.
  Keep the source model unchanged and retain the initial-geometry limitations.
- Pre-generate the scene through `docs/generate_static_views/course_alzheimer_peptide.py`.
  Ordinary notebook pre-execution embeds the committed scene and must not export
  a new scene or require a live Python widget.

The actual-cell regression must check cap inventory/connectivity, independent
torsions, bond-length preservation and non-default unit policies. Receive the
scene's molecular payload and the built article separately; successful HTML
compilation alone does not establish their scientific correspondence.
