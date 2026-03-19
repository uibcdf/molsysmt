import re

# UniProt accession: 6 or 10 chars
# Format: [OPQ][0-9][A-Z0-9]{3}[0-9] or [A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}
_pattern = re.compile(
    r"[OPQ][0-9][A-Z0-9]{3}[0-9]"
    r"|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
)

def is_form(item):
    """Check whether item matches a UniProt accession number string format.

    Notes
    -----
    Validates only the string pattern (`uniprot_id:P12345` or `P12345`) and
    does not perform remote server validation.
    """

    if not isinstance(item, str):
        return False

    if item.startswith("uniprot_id:"):
        candidate = item.split("uniprot_id:", 1)[1]
    else:
        candidate = item

    return bool(_pattern.fullmatch(candidate))
