from molsysmt._private.argdigest import arg_digest

@arg_digest(form='MDAnalysis.AtomGroup')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from MDAnalysis.AtomGroup to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_MolSys import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_MolSys
    from molsysmt._private.variables import is_all

    indices = item.indices

    if not is_all(atom_indices):
        indices = indices[atom_indices]

    tmp_item = MDAnalysis_Universe_to_molsysmt_MolSys(item.universe, atom_indices=indices, 
                                                      structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
