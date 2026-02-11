import re

pattern = re.compile(r"[0-9][A-Za-z0-9_]{3}")
pattern_extended = re.compile(r"0{4}[0-9][A-Za-z0-9_]{3}")

def is_form(item):
    """Checking whether an item matches the local PDB id string format.

    Notes
    -----
    This check validates only the string pattern (`pdb_id:XXXX`, `pdb_XXXX`,
    or `XXXX`) and does not perform any remote server validation.
    """

    if not isinstance(item, str):
        return False

    if item.startswith("pdb_id:"):
        candidate = item.split("pdb_id:", 1)[1]
        return bool(pattern.fullmatch(candidate))

    if item.startswith("pdb_"):
        candidate = item.split("pdb_", 1)[1]
        return bool(pattern.fullmatch(candidate) or pattern_extended.fullmatch(candidate))

    return bool(pattern.fullmatch(item))
