#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

import types

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = "file:crd"


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting the atom count from a CHARMM CRD header.

    Parameters
    ----------
    item : file:crd
        Input CHARMM coordinate file, in standard or extended format.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Declared atom count, read without materializing coordinates.


    .. versionadded:: 1.0.0
    """

    from molsysmt._private.files_and_directories import str_filename

    filename = str_filename(item)
    with open(filename, encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith("*"):
                continue
            return int(stripped.split()[0])

    from molsysmt._private.smonitor import FormatError

    raise FormatError("The CHARMM CRD header does not contain an atom count.")


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    """Getting source atom-position indices from a CHARMM CRD file.

    Parameters
    ----------
    item : file:crd
        Input CHARMM coordinate file, supplying the positional atom axis.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Source positions to return, retaining their order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Source positions, without renumbering a selected subset.
        indices=None returns None.

    Notes
    -----
    An unrestricted query reuses the header-count getter. Atom IDs are
    separate string labels obtained from the topological conversion route.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['POPC']['popc.crd']
    >>> get_atom_index_from_atom(molsys, indices=[2, 0, 2])
    [2, 0, 2]

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        return list(range(get_n_atoms_from_system(item, skip_digestion=True)))
    return list(indices)


# List of functions to be imported
__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
