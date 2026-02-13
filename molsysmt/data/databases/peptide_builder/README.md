# Peptide Builder Database

This directory stores template data used by `molsysmt.build.build_peptide` with `engine='MolSysMT'`.

## Contents

- `amber14sb.json.gz`: serialized peptide templates (topology + coordinates + connectors).
- `make_peptide_builder_db.py`: generator script for rebuilding the database from AmberClassic LEaP libraries.

## Regeneration

Run from the repository root:

```bash
python molsysmt/data/databases/peptide_builder/make_peptide_builder_db.py \
  --amberclassic-root /path/to/AmberClassic
```

By default, the script expects LEaP libraries:

- `dat/leap/lib/amino12.lib`
- `dat/leap/lib/aminont12.lib`
- `dat/leap/lib/aminoct12.lib`

The output file is `amber14sb.json.gz` in this same directory.

AmberClassic public repository:

- https://github.com/Amber-MD/AmberClassic/
