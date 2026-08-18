import re

# UniProt accession: 6 or 10 chars
# Format: [OPQ][0-9][A-Z0-9]{3}[0-9] or [A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}
_pattern = re.compile(
    r"[OPQ][0-9][A-Z0-9]{3}[0-9]"
    r"|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}"
)

def is_form(item):
    """
    Checking whether an item is an instance of form string:uniprot_id.

    Parameters
    ----------
    item : string:uniprot_id
        Source item in string:uniprot_id form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    if not isinstance(item, str):
        return False

    if item.startswith("uniprot_id:"):
        candidate = item.split("uniprot_id:", 1)[1]
    else:
        candidate = item

    return bool(_pattern.fullmatch(candidate))
