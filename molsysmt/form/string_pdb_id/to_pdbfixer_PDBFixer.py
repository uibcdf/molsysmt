from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:pdb_id')
@dep_digest('pdbfixer')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_id to pdbfixer.PDBFixer.

    Parameters
    ----------
    item : string:pdb_id
        Source item in string:pdb_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pdbfixer.PDBFixer
        Resulting object in pdbfixer.PDBFixer form.

    .. versionadded:: 1.0.0
    """

    from pdbfixer import PDBFixer

    from ..pdbfixer_PDBFixer.extract import extract

    from molsysmt.form.string_pdb_id import _extract_pdb_id
    tmp_item = PDBFixer(pdbid=_extract_pdb_id(item))
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item

