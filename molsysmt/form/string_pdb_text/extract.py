from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:pdb_text')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form string:pdb_text.

    Parameters
    ----------
    item : string:pdb_text
        Source item in string:pdb_text form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.

    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import copy
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        from .to_molsysmt_MolSys import to_molsysmt_MolSys
        from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text
        tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                      skip_digestion=True)
        tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item

