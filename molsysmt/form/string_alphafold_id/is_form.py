import re

_pattern = re.compile(r"AF-[A-Za-z0-9]+-F[0-9]+(?:-model_v[0-9]+)?")

def is_form(item):
    """
    Checking whether an item is an instance of form string:alphafold_id.

    Parameters
    ----------
    item : string:alphafold_id
        Source item in string:alphafold_id form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    if not isinstance(item, str):
        return False

    if item.startswith("alphafold_id:"):
        candidate = item.split("alphafold_id:", 1)[1]
    else:
        candidate = item

    return bool(_pattern.fullmatch(candidate))
