# Chemical group database generation

**Role:** operational maintenance guide
**Owner:** uibcdf/molsysmt#368
**Evidence:** contract-tested on small multi-block CCD inputs; no full-CCD
performance or regenerated-corpus qualification is claimed.

## Inputs and invocation

The four legacy entry points delegate to the shared private generator in
[`molsysmt/data/_make/_chemical_group_database.py`](../molsysmt/data/_make/_chemical_group_database.py).
They use the installed `mmcif.io.IoAdapter` parser for all CCD data blocks,
selecting only `chem_comp`, `chem_comp_atom` and `chem_comp_bond`. They do not use
the public coordinate converter, which serves a different molecular-system
contract. Importing an entry point performs no parsing or writing.

Supply a local `components.cif` or `components.cif.gz` and a new or empty output
directory. These commands run from the repository root; replace the source path
with the CCD snapshot being reviewed:

```bash
python -m molsysmt.data.databases.amino_acids.make_amino_acids_db --ccd components.cif --output-dir generated/amino_acids
python -m molsysmt.data.databases.ions.make_ions_db --ccd components.cif --output-dir generated/ions
python -m molsysmt.data.databases.saccharides.make_saccharides_db --ccd components.cif --output-dir generated/saccharides
python -m molsysmt.data.databases.small_molecules.make_small_molecules_db --ccd components.cif --output-dir generated/small_molecules
```

All four commands support `--help`, including direct execution of their script
paths. There are no downloads, implicit current-directory outputs, GROMACS
installation assumptions, or automatic replacement of bundled databases.

For amino acids, the default CCD/RTP allowlist is the bundled amino-acid group
names. Repeated `--amino-acid-name` arguments replace that allowlist. Repeated
`--rtp` arguments add explicitly supplied local GROMACS RTP connectivity
variants. RTP atom types, charges and bonded-potential parameters are not
imported; bonds to neighboring groups (`+` or `-` atom prefixes) are excluded.

The amino-acid and ion commands accept one explicit `--extra` JSON input using
the existing `topology` variant schema. No supplemental file is read by default.
For example, the existing ionic aliases can be included with
`--extra molsysmt/data/databases/ions/extra.json`. Supplemental connectivity is
validated before writing. The amino-acid supplement's two MET variants with
undeclared OXT endpoints were corrected under uibcdf/molsysmt#380 using the
bounded revision route below. Both supplied supplements now pass the structural
validation; other malformed supplements are still rejected.

## Reference selection and reader schemas

Selection preserves the legacy database partition:

- Amino acids require membership in the chosen allowlist and one of the supported
  peptide-linking or peptide-terminal component types.
- Saccharides have a component type containing `saccharide`.
- Ions and small molecules use `non-polymer` or `other` component types. A name
  ending in ` ion`, ignoring case and surrounding whitespace, selects the ion
  database; other names select the small-molecule database.
- `UNL` is excluded. An absent family produces an empty, valid group-name index.

The name rule is a reference-table classification convention, not a general
ion detector based on formal charge. This tooling does not assign chemical
states, protonation, aromaticity, bond orders or coordinates.

Each family writes sorted first-character buckets `<prefix>.pkl.gz` and a sorted
`group_names.pkl.gz`. Amino-acid, saccharide and small-molecule records retain
`name` and `topology` variants with atom names and pairs of bonded atom names.
Ion records retain `name`, `three_letter_code`, `atom_name` variants and common
pairs of bonded atom indices. Supplemental ion variants must have the same
connectivity in that positional representation; incompatible variants are
rejected instead of losing information.

CCD canonical and alternate atom-name variants preserve source atom order and
connectivity. An absent, unknown or inapplicable alternate name falls back to
the canonical name. Duplicate atom names, unresolved bond endpoints, inconsistent
component references, duplicate component identifiers and incomplete category
rows are rejected. Only selected families require atom inventories, so unrelated
component families need not provide them.

## Provenance, reproducibility and resource custody

`generation_manifest.json` records the generator schema/profile, MolSysMT,
mmCIF and Python versions, input basenames and SHA-256 hashes, the amino-acid
allowlist, group count and each output file's SHA-256. Keep the exact source
commit with this receipt when reviewing a regeneration: the package version
alone does not identify changes made on an unreleased branch.

Output ordering, pickle protocol 4, compression settings and the zero gzip
timestamp are fixed. Repeating generation with the same source bytes, arguments,
generator code and environment produces identical output bytes and manifests.
This is not a cross-version guarantee for pickle or the parser. Input order for
RTP/JSON supplementation determines variant order and is preserved in provenance.

Parsing, selection and supplemental validation finish before output creation.
A nonempty destination is refused and its contents are preserved. Parser logs
and compression scratch use a managed temporary directory retired on success
and failure. The parser materializes the selected categories from all blocks;
the route does not promise bounded-memory streaming of the complete CCD.

The manifest is written last as a completion record. An output I/O failure can
leave partial files in the explicitly supplied destination; writing the whole
directory is not an atomic transaction. Preserve or remove that failed output
deliberately before retrying in a new or empty directory.

## Reviewing a bundled-data update

Generate into a separate directory first. Review membership changes, naming
variants and connectivity against the selected source snapshot; use the
existing group readers to check downstream delivery. Record input hashes and
the generator commit before replacing bundled assets. Do not equate a parser
contract test with scientific validation of all generated chemistry.

The regression guard is
[`tests/data/databases/test_ccd_generators.py`](../tests/data/databases/test_ccd_generators.py).
It exercises the real parser and existing readers with multiple data blocks,
quoted and multiline fields, scalar categories, naming variants, explicit
RTP/JSON supplements, gzip input, malformed input, output custody and byte
reproducibility. A curated real MSE CCD component additionally checks its
selenium connectivity.

```bash
python -m pytest tests/data/databases/test_ccd_generators.py --receptor=llm -n12
```

## Revising an existing amino-acid supplement

When a reviewed supplement changes but the complete historical CCD/RTP source
set is unavailable, use
[`revise_amino_acid_supplements.py`](../molsysmt/data/_make/revise_amino_acid_supplements.py).
It replaces changed variants in trusted legacy buckets by exact equality with
an explicit previous supplement. Every replacement must match exactly one
original variant; missing or ambiguous baselines fail before writing. It
preserves group membership, record metadata and variant counts/order, and
validates all variants in the affected buckets after replacement. Revised
supplements must retain the same group keys, metadata and variant positions.

This maintenance route does not infer chemical changes, reconstruct the original
force-field inputs, or accept arbitrary untrusted pickle files. It writes only
affected buckets and a completion manifest, using the same deterministic writer
as full generation. It writes no group-name index because membership is unchanged.
Output custody and non-atomic I/O behavior follow the rules above.

For #380, the original source commit is
`4393d9fdc0d09a0312b8b8218514444f1278a25d`. Using a fresh `generated/met-input`
directory, reproduce the correction from those exact historical inputs:

```bash
mkdir -p generated/met-input
git show 4393d9fdc0d09a0312b8b8218514444f1278a25d:molsysmt/data/databases/amino_acids/M.pkl.gz > generated/met-input/M.pkl.gz
git show 4393d9fdc0d09a0312b8b8218514444f1278a25d:molsysmt/data/databases/amino_acids/extra.json > generated/met-input/molsysmt-380-previous-extra.json
python -m molsysmt.data._make.revise_amino_acid_supplements --source-dir generated/met-input --previous-extra generated/met-input/molsysmt-380-previous-extra.json --extra molsysmt/data/databases/amino_acids/extra.json --output-dir generated/met-revised
```

Review the result before replacing assets. For this correction, only MET variants
4 and 5 in `M.pkl.gz` lose the undeclared `C`–`OXT` edge; their 19-atom inventories
and all other variants are preserved. The graph matches the N-terminal peptide
NMET reference in
[AmberClassic](https://github.com/Amber-MD/AmberClassic/blob/656e5c6fcb05149e6aa936e1d69d1426b37ea3c7/dat/leap/lib/aminont12.lib#L2133),
with `H1` renamed to `H` for the second naming variant. This is connectivity
evidence; it assigns no charges or chemical states. The CCD-derived MET variants
that include OXT remain available for their distinct inventories.

The retained
[`supplement_revision_manifest.json`](../molsysmt/data/databases/amino_acids/supplement_revision_manifest.json)
records original/revised input hashes, changed variant indices, output hashes,
the reported runtime version and hashes of the actual generator and common tool
source files. These source hashes identify the code even when a development
environment's installed version metadata describes an older build. Reproducing
the bucket bytes is independent of such manifest version fields; full manifest
reproducibility also requires identical generator code and environment.

The guard
[`test_amino_acid_supplement_revision.py`](../tests/data/databases/test_amino_acid_supplement_revision.py)
checks endpoint integrity, the independent Amber NMET graph, reader delivery with
reordered external atom indices, preservation of OXT-bearing variants and
unrelated records, provenance, custody and rejected ambiguous revisions.
