from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:smi')
def to_string_smiles(item, skip_digestion=False):
    """Read a .smi file and return smiles: strings (no rdkit required)."""

    results = []
    with open(item, 'r') as fff:
        for line in fff:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            smiles = line.split()[0]
            results.append('smiles:' + smiles)

    if len(results) == 1:
        return results[0]

    return results
