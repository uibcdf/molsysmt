from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
import numpy as np

_sorted = sorted

def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):
    """
    Getting standard intra-group covalent bonded atom pairs for terminal capping residues.


    Parameters
    ----------
    group_name : str
        Name of the chemical group (residue).
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

    from . import group_names, get_group_db

    if group_name not in group_names:
        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.element.group.terminal_capping.get_bonded_atom_pairs")
    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    db = get_group_db(group_name)
        
    is_in = -1
    for ii,jj in enumerate(db['topology']):
        if np.all(np.isin(atom_names, jj['atoms'])):
            is_in=ii
            break

    if is_in!=-1:
        bonds = []
        for ii,jj in db['topology'][is_in]['bonds']:
            if ii in atom_names:
                if jj in atom_names:
                    iii = atom_indices[atom_names.index(ii)]
                    jjj = atom_indices[atom_names.index(jj)]
                    if iii<jjj:
                        bonds.append([iii,jjj])
                    else:
                        bonds.append([jjj,iii])

    else:

        print(group_name, atom_names)

        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.element.group.terminal_capping.get_bonded_atom_pairs")
    if sorted:
        return _sorted(bonds)
    else:
        return bonds

