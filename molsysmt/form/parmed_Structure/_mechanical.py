"""Reading actual ParmEd charge assignments without its zero fallback."""


def assigned_partial_charges(item):
    """Return known charges and None for atoms with no charge assignment.

    ParmEd's public ``charge`` property supplies 0.0 for unassigned atoms.
    ``_charge`` is the provider's stored atom assignment; an assigned AtomType
    can supply the charge when that field is absent. No chemistry is perceived.
    """
    values = []
    for atom in item.atoms:
        value = getattr(atom, "_charge", None)
        if value is None:
            value = getattr(getattr(atom, "atom_type", None), "charge", None)
        values.append(None if value is None else float(atom.charge))
    return values
