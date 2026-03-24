from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError
from .names import atom as atom_type_from_name

@arg_digest()
def get_atom_type_from_atom_name(atom_name):
    """
    Infer the chemical element (atom type) from a standard atom name string.

    Looks up the atom name in the internal ``atom_type_from_name`` dictionary and
    returns the corresponding element symbol. If the name is not found, a warning is
    printed and the string ``'UNK'`` is returned.

    Parameters
    ----------
    atom_name : str
        Standard atom name as used in PDB/topology files (e.g. ``'CA'``, ``'OW'``,
        ``'HB2'``).

    Returns
    -------
    str
        Element symbol of the atom (e.g. ``'C'``, ``'O'``, ``'H'``, ``'N'``), or
        ``'UNK'`` if the name is not recognised.

    Notes
    -----
    The mapping is stored in
    ``molsysmt.element.atom.names.atom`` and covers common atom names from standard
    biomolecular force fields. Unrecognised names produce a printed warning rather
    than raising an exception.

    .. versionadded:: 1.0.0
    """

    try:
        return atom_type_from_name[atom_name]
    except Exception:
        print(f'The atom_name {atom_name} was not recognized')
        return 'UNK'
        #raise ValueError('Atom name '+atom_name+' has not known atom type.')

