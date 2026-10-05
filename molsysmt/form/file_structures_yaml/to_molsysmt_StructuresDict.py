from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@dep_digest("yaml")
@arg_digest(form="file:structures_yaml")
def to_molsysmt_StructuresDict(item, skip_digestion=False):
    """
    Converting from file:structures_yaml to molsysmt.StructuresDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.StructuresDict
        Resulting object in molsysmt.StructuresDict form.


    Raises
    ------
    FormatError
        If the schema version is unsupported or a quantity record, unit,
        field binding or sparse-site axis is invalid. Legacy alternate
        coordinates and B factors without negotiated units are rejected.

    Notes
    -----
    Schema 0.1 uses its historical canonical units for top-level fields;
    schema 0.2 verifies each quantity record and its expected field and unit.

    .. versionadded:: 1.0.0
    """

    import yaml

    with open(item, "r", encoding="utf-8") as file_handle:
        data = yaml.safe_load(file_handle)

    from molsysmt.form._structures_yaml import decode_structures

    return decode_structures(data)
