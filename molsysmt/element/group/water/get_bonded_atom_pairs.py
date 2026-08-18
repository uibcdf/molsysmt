import numpy as np

_sorted=sorted

def get_bonded_atom_pairs(atom_names, atom_indices=None, sorted=True):
    """
    Getting standard intra-group covalent bonded atom pairs for water residues.


    Parameters
    ----------
    atom_names : numpy.ndarray, list, or tuple
        Names of atoms in the group.
    atom_indices : int, list, tuple, or numpy.ndarray, default=None
        Atom indices (0-based) to include.
    sorted : bool, default=True
        Whether to sort the returned bonded atom pairs.

    Returns
    -------
    list of tuple of str
        List of bonded atom name pairs.


    .. versionadded:: 1.0.0
    """

    from molsysmt.element.atom import get_atom_type_from_atom_name

    if len(atom_names)>=3:

        if atom_indices is None:
            atom_indices = list(range(len(atom_names)))

        O = None
        Hs = []

        for atom_index, atom_name in zip(atom_indices, atom_names):

            atom_type = get_atom_type_from_atom_name(atom_name)

            if atom_type=='O':
                O=atom_index
            elif atom_type=='H':
                Hs.append(atom_index)

        if sorted:
            return  _sorted([[O,Hs[0]], [O,Hs[1]]])
        else:
            return  [[O,Hs[0]], [O,Hs[1]]]

    else:

        return []
