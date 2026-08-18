from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to openmm.PDBFile.

    Parameters
    ----------
    item : string:pdb_text
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.PDBFile
        Converted molecular system representation.
    """

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFile(tmp_item)

    return tmp_item

