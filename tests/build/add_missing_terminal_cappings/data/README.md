# Terminal reconstruction reference

`1hsg.pdb.gz` contains the unchanged public RCSB PDB 1HSG download from
https://files.rcsb.org/download/1HSG.pdb, retrieved on 2026-11-10 and compressed
with a zero gzip timestamp. Decompressed SHA-256:
`d430675c358060808ef614002cfdcfcfa824714d89f1240adf5749d2ba60fed2`.
This is the exact original input identified in MolSysMT #558.

The tests separate reading declared connectivity from explicitly choosing native
bond inference. With the declared graph alone, peptide termini remain unassessed.
The bounded inference/completion control checks correspondence and preserved
observed coordinates. It does not assess a biological protonation hypothesis,
chemical completeness, docking readiness or generated geometry quality.
