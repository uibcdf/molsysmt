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

    lowered = item.lower()

    if lowered.startswith("pdb_id:"):
        candidate = lowered.split("pdb_id:", 1)[1]
        return bool(pattern.fullmatch(candidate))

    if lowered.startswith("pdb_"):
        candidate = lowered.split("pdb_", 1)[1]
        return bool(pattern.fullmatch(candidate) or pattern_extended.fullmatch(candidate))

    # Tolerance alias: 'pdb:XXXX' is NOT official syntax — accepted silently
    # to avoid frustrating users who type it by mistake.
    if lowered.startswith("pdb:"):
        candidate = lowered.split("pdb:", 1)[1]
        return bool(pattern.fullmatch(candidate))

    return bool(pattern.fullmatch(lowered))
