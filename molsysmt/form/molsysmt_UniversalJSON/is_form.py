def is_form(item):
    """Check whether *item* is a `molsysmt.native.universal_json.UniversalJSON` instance."""

    item_fullname = item.__class__.__module__ + '.' + item.__class__.__name__
    return item_fullname == 'molsysmt.native.universal_json.UniversalJSON'
