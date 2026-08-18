from molsysmt._private.argdigest import arg_digest
from io import StringIO

@arg_digest(form='string:pdb_text')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):
    """
    Converting from string:pdb_text to molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : string:pdb_text
        Source item in string:pdb_text form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.PDBFileHandler
        Resulting object in molsysmt.PDBFileHandler form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import PDBFileHandler

    tmp_item = StringIO(item)

    return PDBFileHandler(tmp_item, io_mode='r')

