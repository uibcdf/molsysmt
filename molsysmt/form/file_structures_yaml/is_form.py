from pathlib import Path


def is_form(item):
    """
    Checking whether an item is an instance of form file:structures_yaml.

    Parameters
    ----------
    item : file:structures_yaml
        Source item in file:structures_yaml form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """
    if isinstance(item, Path):
        item = str(item)

    if not isinstance(item, str):
        return False

    if not (item.endswith('.yaml') or item.endswith('.yml')):
        return False

    path = Path(item)
    if not path.is_file():
        return False

    try:
        import yaml
    except ImportError:
        return False

    try:
        with path.open('r', encoding='utf-8') as file_handle:
            data = yaml.safe_load(file_handle)
    except Exception:
        return False

    if not isinstance(data, dict):
        return False

    return data.get('format', None) == 'molsysmt' and data.get('kind', None) == 'structures'
