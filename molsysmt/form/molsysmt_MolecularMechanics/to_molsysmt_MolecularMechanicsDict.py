from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolecularMechanics')
def to_molsysmt_MolecularMechanicsDict(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolecularMechanics to molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.

    .. versionadded:: 1.0.0
    """

    tmp_item = item.to_dict()

    if not is_all(atom_indices):

        if tmp_item['formal_charge'] is not None:
            tmp_item['formal_charge'] = tmp_item['formal_charge'][atom_indices]

        if tmp_item['partial_charge'] is not None:
            tmp_item['partial_charge'] = tmp_item['partial_charge'][atom_indices]

        if tmp_item['atom_ff_type'] is not None:
            tmp_item['atom_ff_type'] = tmp_item['atom_ff_type'][atom_indices]

    return tmp_item
