# Peptide chemical reference fragments

These data are derived from Meeko's `meeko/data/residue_chem_templates.json` at
commit `1eac18bd6d1111f35f9f1abaa8af502c2668d054`. The original file's SHA-256 is
`535dc75a2cc5db579a3114090c9ab1273892c556cb7cc1a850ce2c4cd57c7cde`.
The unmodified source bytes are retained as a deterministic gzip snapshot in
`molsysmt/data/_make/peptide_templates/`. The upstream LGPL 2.1 license is retained
in `MEEKO_LICENSE.txt`; this copied/derived data have a separate upstream license
from MolSysMT's implementation. Source and curation metadata are embedded in JSON.

Regenerate offline from the repository root:

```bash
python molsysmt/data/_make/make_peptide_chemical_templates.py
```

Curation requires RDKit. Normal template construction requires neither RDKit nor
Meeko. Heavy bonds, explicit neighbor-H counts, formal charges and aromatic flags
come from the selected source SMILES; conjugation follows the recorded curation
model. Port-associated implicit H represent missing external bonds and are
excluded from stored H counts. The native factory closes peptide/disulfide ports,
declares selected terminal chemistry and backbone conjugation, then assigns
complete connectivity. CYM explicitly selects upstream state `CYX-`.

These fragments leave stereochemistry unspecified and do not contain geometry,
force-field parameters or environmental protonation predictions. They are not
standalone complete molecules until the factory closes every port. Regression:
`tests/physchem/test_get_peptide_chemical_template.py` checks full-graph valence,
independent state charges, hydrogen inventories, conjugation, explicit links,
native independence, correspondence and H5MSM roundtrips.
