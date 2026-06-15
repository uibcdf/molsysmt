"""Shared per-residue property-table lookup with dummy-residue tolerance.

The ``physchem`` group functions map each residue name to a value in a property
table (charge, hydrophobicity, polarity, ...). Systems built from dummy atoms
(coarse beads, alchemical placeholders, synthetic probe atoms such as TopoMT's
DFND ``AR``/``DUM`` catalog) carry residue names that have no table entry. This
helper treats those dummy residues as chemically neutral instead of raising, so
``physchem`` functions can run over whole systems that contain dummy entries,
while genuine unknown residues still raise so real gaps are not masked.
"""

# Placeholder / dummy residue names treated as chemically neutral.
NEUTRAL_GROUP_NAMES = {'DUM', 'X'}


def group_table_value(values, group_name, neutral=0.0):
    """Return the property value for ``group_name`` from a residue table.

    Parameters
    ----------
    values : dict
        Residue-property table keyed by upper-case residue name.
    group_name : str
        Residue name (case-insensitive).
    neutral : float, default 0.0
        Value returned for dummy residues in :data:`NEUTRAL_GROUP_NAMES`.

    Returns
    -------
    float
        ``values[group_name.upper()]`` when present; ``neutral`` for dummy
        residues.

    Raises
    ------
    KeyError
        If ``group_name`` is neither in ``values`` nor a recognised dummy
        residue.
    """
    key = group_name.upper()
    try:
        return values[key]
    except KeyError:
        if key in NEUTRAL_GROUP_NAMES:
            return neutral
        raise
