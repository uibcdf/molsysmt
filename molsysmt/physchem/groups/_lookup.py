"""Shared per-residue property-table lookup with dummy-residue tolerance.

The ``physchem`` group functions map each residue name to a value in a property
table (charge, hydrophobicity, polarity, ...). Systems built from dummy atoms
(coarse beads, alchemical placeholders, synthetic probe atoms such as TopoMT's
DFND ``AR``/``DUM`` catalog) carry residue names that have no table entry. This
helper treats those dummy residues as chemically neutral instead of raising, so
``physchem`` functions can run over whole systems that contain dummy entries,
while genuine unknown residues still raise so real gaps are not masked.
"""

from molsysmt._private.smonitor import UnknownGroupInTableError


# Placeholder / dummy residue names treated as chemically neutral.
NEUTRAL_GROUP_NAMES = {'DUM', 'X'}


def group_table_value(values, group_name, neutral=0.0, table='property', caller=None):
    """
    Return the property value for ``group_name`` from a residue table.


    Parameters
    ----------
    values : object
        Argument values.
    group_name : str
        Name of the chemical group (residue).
    neutral : object, default=0.0
        Argument neutral.
    table : str, default='property'
        Name of the property table, used to say which one has no entry.
    caller : str, optional
        Qualified name of the public function to name in the failure.

    Returns
    -------
    float
        ``values[group_name.upper()]`` when present; ``neutral`` for dummy
        residues.


    Raises
    ------
    UnknownGroupInTableError
        If ``group_name`` is neither in ``values`` nor a recognised dummy
        residue.
    """
    key = group_name.upper()
    try:
        return values[key]
    except KeyError:
        if key in NEUTRAL_GROUP_NAMES:
            return neutral
        # Raising here is deliberate — see the module docstring: a genuine gap must
        # not be read as a neutral value. What is reported is not: the bare KeyError
        # named only the residue, so it read as an internal defect rather than as a
        # system the caller has to decide about (uibcdf/molsysmt#179).
        raise UnknownGroupInTableError(
            group_name=group_name, table=table, caller=caller) from None
