import re

_pattern = re.compile(r"AF-[A-Za-z0-9]+-F[0-9]+(?:-model_v[0-9]+)?")

def is_form(item):
    """Checking whether an item matches the local AlphaFold id string format.

    Notes
    -----
    This check validates only the string pattern (`alphafold_id:AF-...` or
    `AF-...`) and does not perform any remote API validation.
    """

    if not isinstance(item, str):
        return False

    if item.startswith("alphafold_id:"):
        candidate = item.split("alphafold_id:", 1)[1]
    else:
        candidate = item

    return bool(_pattern.fullmatch(candidate))
