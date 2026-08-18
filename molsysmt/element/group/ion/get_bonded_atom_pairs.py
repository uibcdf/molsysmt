from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
import numpy as np


_sorted=sorted

@arg_digest()
def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True, skip_digestion=False):
    """
    Getting standard intra-group covalent bonded atom pairs for ion residues.


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
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of tuple of str
        List of bonded atom name pairs.


    .. versionadded:: 1.0.0
    """

    n_atoms=len(atom_names)

    if n_atoms==1:

        return []

    else:

        from molsysmt.element.group.ion import group_names, get_group_db

        if group_name not in group_names:
            raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.element.group.ion.get_bonded_atom_pairs")
        if atom_indices is None:
            atom_indices = np.arange(len(atom_names), dtype=int).tolist()

        aux_group_names = [group_name]

        for aux_group_name in aux_group_names:

            db = get_group_db(aux_group_name)
            
            is_in = -1
            for ii,jj in enumerate(db['atom_name']):
                if np.all(np.isin(atom_names, jj)):
                    is_in=ii
                    break

            if is_in!=-1:

                bonds = []
                for i,j in db['bonds']:
                    ii = db['atom_name'][is_in][i]
                    jj = db['atom_name'][is_in][j]
                    if ii in atom_names:
                        if jj in atom_names:
                            iii = atom_indices[atom_names.index(ii)]
                            jjj = atom_indices[atom_names.index(jj)]
                            if iii<jjj:
                                bonds.append([iii,jjj])
                            else:
                                bonds.append([jjj,iii])
                if sorted:
                    return _sorted(bonds)
                else:
                    return bonds

