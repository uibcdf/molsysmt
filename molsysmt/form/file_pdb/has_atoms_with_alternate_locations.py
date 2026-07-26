def has_atoms_with_alternate_locations(filename):
    """Returning whether a PDB file contains alternate-location records."""

    from molsysmt.native import PDBFileHandler

    handler = PDBFileHandler(filename)
    try:
        return any(
            atom.alternate_location
            for model in handler.content.models
            for atom in model.atoms
        )
    finally:
        handler.close()
