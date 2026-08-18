from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from file:pdb to file:mol2.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:mol2
        Resulting object in file:mol2 form.


    .. versionadded:: 1.0.0
    """

    from .to_parmed_Structure import to_parmed_Structure
    from molsysmt.form.parmed_Structure.to_file_mol2 import to_file_mol2 as parmed_Structure_to_file_mol2

    tmp_item = to_parmed_Structure(item, skip_digestion=True)
    tmp_item = parmed_Structure_to_file_mol2(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, skip_digestion=True)

    return tmp_item

