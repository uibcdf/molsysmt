import re

# Valid SMILES characters (organic subset + brackets + bonds + ring closures + stereo)
_valid_chars = re.compile(r'^[BCNOPSFIbcnops\[\]()\-=#$:./\\@%\d\*\+]+$')
# At least one SMILES-specific structural feature (not just bare uppercase letters)
_structural = re.compile(r'[bcnops()\[\]=#$@/\\\d]|Cl|Br')


def is_form(item):

    if not isinstance(item, str) or not item:
        return False

    # Explicit prefix: always recognized
    if item.startswith('smiles:'):
        return len(item) > 7

    # Try rdkit if available: authoritative parse
    try:
        from rdkit import Chem
        from rdkit.RDLogger import DisableLog, EnableLog
        DisableLog('rdApp.error')
        try:
            mol = Chem.MolFromSmiles(item)
        finally:
            EnableLog('rdApp.error')
        return mol is not None
    except ImportError:
        pass

    # Regex fallback: valid SMILES chars + at least one structural feature
    # (avoids false positives with pure uppercase amino-acid sequences)
    return bool(_valid_chars.match(item)) and bool(_structural.search(item))
