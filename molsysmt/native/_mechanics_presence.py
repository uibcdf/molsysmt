"""Recognizing stored mechanics without projecting away its evidence."""


def has_stored_mechanics(mechanics):
    """Distinguish the default empty native domain from unsupported stored data.

    Inspect references only: arrays and reports need neither copying nor scanning.
    Empty tables/mappings still represent stored state. Unknown implementations or
    extensions cannot establish absence through the native parameter projection.
    """
    from .molecular_mechanics import MolecularMechanics

    if mechanics is None:
        return False
    if type(mechanics) is not MolecularMechanics:
        return True
    stored = vars(mechanics)
    return bool(stored.keys() - vars(MolecularMechanics()).keys()) or any(
        value is not None for value in stored.values()
    )
