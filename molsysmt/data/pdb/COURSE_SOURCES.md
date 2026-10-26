# Original course PDB sources

`course_sources.json` records source URLs, retrieval date, exact SHA-256 hashes
and original lengths for 5XJH, 6EQE, 6LU7 and 1K4C. The PDB files are unchanged
archive bytes, not prepared molecular models. The manifest links each entry's
structure page for original authorship and publication references.

The [wwPDB usage policy](https://www.wwpdb.org/about/usage-policies) dedicates PDB
archive data under CC0 1.0 and encourages attribution of the original authors.
This applies to these data files, independently of MolSysMT's software license.

Use the public `msm.systems` catalog for offline access. Reading PDB records
preserves deposited identifiers; subsequent bond completion and chemical
preparation are separate operations with their own contracts.

To verify committed files or restore missing ones from byte-identical originals:

```bash
python molsysmt/data/_make/course_pdb_sources.py --source-directory /path/to/originals
```

Only explicit `--download` permits retrieval from RCSB. The generator rejects a
changed archive response or existing mismatched file without replacing it. It
does not silently refresh pinned examples when archive contents change.
