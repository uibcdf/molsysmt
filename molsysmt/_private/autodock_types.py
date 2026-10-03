"""Decoding explicit AutoDock4 labels without assigning chemical properties."""

# Standard labels from the AutoDock4 parameter table. Pseudoatoms and
# macrocycle closure labels need distinct contracts and are deliberately absent.
AUTODOCK4_ELEMENTS = {
    label: label
    for label in (
        "C",
        "N",
        "O",
        "P",
        "S",
        "H",
        "F",
        "I",
        "Mg",
        "Mn",
        "Zn",
        "Ca",
        "Fe",
        "Cl",
        "Br",
        "Si",
        "At",
    )
}
AUTODOCK4_ELEMENTS.update({"A": "C", "NA": "N", "OA": "O", "SA": "S", "HD": "H"})


def decode_atom_ff_type(label, scheme):
    """Decode one label in a named, bounded typing scheme."""
    if scheme != "autodock4":
        raise ValueError("typing_scheme must be 'autodock4'.")
    if not isinstance(label, str) or label not in AUTODOCK4_ELEMENTS:
        raise ValueError(f"Unsupported AutoDock4 atom_ff_type: {label!r}.")
    return AUTODOCK4_ELEMENTS[label]
