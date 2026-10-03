# Original AutoDock Vina reference inputs

These nine files are unmodified examples from
[`ccsb-scripps/AutoDock-Vina` commit `3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645`](https://github.com/ccsb-scripps/AutoDock-Vina/tree/3c65c0b3e6c2c1d183f6a175ecb65e3c5ba91645/example).
The upstream Apache License 2.0 is retained in `LICENSE`. Original field widths,
trailing spaces, SD properties and unsupported flags are preserved. Do not
normalize a source to make the native adapter accept it.

`manifest.json` records each upstream path and original SHA-256. Its literal
counts, branch serial pairs, ROOT/BRANCH fragment memberships and supported
stereo controls describe the pinned inputs independently of MolSysMT output.
The fragment memberships were transcribed from the original record scopes;
counts refer to stored atoms, not inferred hydrogen inventories. The SDF
stereo control is source atom index 7: R for P59 and S for P69, checked with
the accurate RDKit CIP labeler. Source net formal charge comes from the CTAB,
including `M CHG`, not the PDBQT charge sum. The live optional reader checks
remain separate from these frozen observations.

| Case | SDF atoms / bonds | PDBQT atoms / branches | Initial native SDF profile |
| --- | --- | --- | --- |
| 1IEP ligand | 69 / 73 | 40 / 7 | Reject declared atom valence |
| 1S63 ligand | 29 / 32 | 30 / 6 | Reject missing CTAB version |
| 5X72 P59 | 39 / 42 | 25 / 2 | Explicit RDKit stereo provider |
| 5X72 P69 | 39 / 42 | 25 / 2 | Explicit RDKit stereo provider |
| 1IEP rigid receptor | — | 2,702 / 0 | — |

The two rejected SDF sources are legitimate comparison inputs outside the
current bounded profile, not corrupted controls or successful conversion
coverage. 1IEP declares valence 4 on source atom index 31 and formal charge +1
in `M CHG`. 1S63 has no version marker, and its prepared PDBQT contains one
additional H. The sources must remain available when those boundaries are
extended under MolSysMT #215. Admitting them requires deliberate semantics,
not deleting fields, assuming missing H counts are zero or hiding a fallback.

All five PDBQT inputs carry existing preparation decisions. Reading and
rewriting their labels, charges, coordinates and trees checks format fidelity;
it does not validate charge models, chemical typing, selected torsions,
hydrogen preparation or docking affinity. Matching atoms by coordinates is
used only for these already aligned, pinned examples: require a unique match
of the same chemical element within 0.002 angstrom, and explicitly account
for 1S63's reference-only H. This is not a general molecular identity method.

Tests consume this committed corpus without another checkout or network
access. Independent RDKit, MDAnalysis and Vina checks are optional and skip
explicitly when their provider is absent. No upstream executable/library is
made a MolSysMT runtime dependency by this data collection. Related provider
work is uibcdf/molsysmt#214/#215; consumer acceptance is
uibcdf/dockingmt#33 and torsion-policy differences are uibcdf/dockingmt#17.
