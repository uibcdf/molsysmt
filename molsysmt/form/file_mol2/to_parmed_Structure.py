from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:mol2')
@dep_digest('parmed')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to parmed.Structure.

    Parameters
    ----------
    item : file:mol2
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Converted molecular system representation.
    """

    from molsysmt.form.parmed_Structure import extract
    from ._reader import read_mol2

    tmp_item, _ = read_mol2(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item
