# Pinned EST chemical-template control

This development fixture tests explicit template application to the deposited
EST pose in RCSB entry 1QKU. Tests are offline. Original entry/CCD bytes, revisions,
SHA-256 checksums and source URIs are retained in `manifest.json`.

- `1qku.cif.gz`: losslessly compressed full deposited entry, revision 1.4 dated
  2024-05-08. Native conversion yields 6,596 atoms and one structure.
- `EST.cif`: verbatim CCD component definition, modified 2011-06-04, 44 atoms and
  47 bonds. Its ideal/model coordinates are never used for this template.
- `est_template.h5msm`: deliberately curated 20-heavy-atom, 23-bond template with
  complete chemical assignments and stored H counts; no coordinate domain.
- `manifest.json`: explicit template/source atom correspondence, provenance,
  hydrogen inventory, expected stereo labels and artifact checksums.

The selected ligand has label asymmetry ID D, author chain A and author residue
600. Selection uses native `chain_id == "D"`; original full-system atom **indices**
are 5940–5959. Atom IDs are separate string values, not those indices.

## Curation and independent controls

The generator reads the existing mmCIF data-container form and builds a template
through public MolSysMT tools. It retains CCD heavy bonds and Kekule orders to
avoid claiming unsupported representation normalization. It selects the explicitly
named CACTVS 3.341 canonical SMILES descriptor, validates a unique exhaustive graph
correspondence with RDKit, and checks charges, aromaticity and H inventory against
CCD declarations. There are 24 stored H counts and zero explicit H atoms.

The descriptor's five assigned CIP centers agree with independent assignment from
the deposited 3D pose: C8 R, C9 S, C13 S, C14 S, C17 S. The pinned CCD atom-level
flag for C8 is S. The manifest records that discrepancy and the deliberate choice
of canonical-descriptor stereo; it does not infer the reason for the discrepancy
or blindly copy atom-level flags. These controls do not validate protonation,
conformer energy, receptor environment or a biological pharmacophore.

The regression requires the known six-atom aromatic ring and O3/O17 acceptors,
exact source-pose/identity preservation under nondefault units, and public H5MSM
chemical-value roundtrip. Explicit donor-H pairs remain absent until a separate
fixed-state H-placement operation provides actual atoms and geometry (#300).

## Reproducing the curation

Run from the repository root with the supported scientific development environment
and RDKit installed. Output goes to a separate directory for review:

```bash
python devtools/scripts/curate_est_template_fixture.py \
  --entry tests/physchem/data/chemical_templates/1qku.cif.gz \
  --ccd tests/physchem/data/chemical_templates/EST.cif \
  --output est_fixture_recurated
python -m pytest --receptor=llm tests/physchem/test_chemical_template_est.py
```

Curation refuses unexpected source checksums or ambiguous atom correspondence.
It is a fixture-specific generator, not a general CCD parser, automatic template
matcher or production preparation fallback. The runtime native-template route
needs neither RDKit nor Ackredit. Recuration uses RDKit explicitly and records its
version; it can change serialized HDF5 artifact bytes while retaining chemical
meaning. The manifest describes the exact committed artifact, not future bytes.

This provider contract control is related to uibcdf/molsysmt#298 and the consumer
request uibcdf/pharmacophoremt#22. It does not establish that the consumer's entire
ERalpha workflow has passed.
