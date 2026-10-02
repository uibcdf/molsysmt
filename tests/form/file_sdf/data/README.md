# Synthetic SDF reference corpus

`reference_corpus.json` contains 46 single-record SDF inputs for 17 synthetic,
achiral molecular graphs. It covers V2000/V3000, explicit aromatic and Kekule
encodings, nitrogen heterocycles, fused rings, nitro groups, carboxylate,
quaternary ammonium, a zwitterion, phosphate, sulfate, isotopic labels, amide,
sulfoxide, azide, nitrile and a halogenated saturated ring. Hydrogens are explicit.
Three additional records exercise the unsupported valence-override boundary;
their rejection is required, not counted as successful ligand conversion.

The snapshot records the actual RDKit producer version. Regenerate from the
repository root with an optional RDKit installation:

```bash
python devtools/scripts/generate_sdf_reference_corpus.py
```

The generator does not call the MolSysMT parser. Atom counts, bond counts and net
formal charges are specified independently in its case table; the atom/bond
assignments and SDF text come from the reference toolkit. The native contract
tests consume this committed snapshot without importing RDKit. Optional live
comparison reads both source and native-written files without sanitization or
hydrogen removal, so a chemical-perception change is not mistaken for declared
CTAB data. No external ligand database or RDKit source code is redistributed.

These fixtures establish bounded compatibility, not stereochemical validation,
general valence validation, force-field preparation or RDKit-equivalent coverage.
