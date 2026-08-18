from molsysmt._private.argdigest import arg_digest
from io import StringIO

@arg_digest(form='string:pdb_text')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):
    """
    Converting from string:pdb_text to molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : string:pdb_text
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.PDBFileHandler
        Converted molecular system representation.
    """

    from molsysmt.native import PDBFileHandler

    tmp_item = StringIO(item)

    return PDBFileHandler(tmp_item, io_mode='r')

