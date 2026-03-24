from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import *

@arg_digest()
def get_missing_residues(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    Identify residues that are missing from a molecular system relative to a reference sequence.

    This function compares the residues present in the molecular system against the
    sequence inferred from the structure and returns a mapping of insertion positions
    (group indices) to the names of the residues that should be present at those
    positions but are absent.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of the system.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'PDBFixer'}, default 'PDBFixer'
        Backend used to detect missing residues. Only 'PDBFixer' is currently
        supported.

    Returns
    -------
    dict
        Dictionary mapping ``(chain_index, insertion_position)`` tuples to
        lists of residue names (str).  ``chain_index`` is the 0-based index of
        the chain in the (sub)system; ``insertion_position`` is the 0-based
        index within that chain's *structural* sequence before which the missing
        residues should be inserted (matches PDBFixer's ``missingResidues``
        convention).  For insertions after the last residue of a chain the
        ``insertion_position`` equals the number of residues in that chain.

    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    The function converts the (sub)system to a ``pdbfixer.PDBFixer`` object and
    calls ``findMissingResidues``.  PDBFixer's ``missingResidues`` attribute is a
    ``dict`` with ``(chain_index, insertion_position)`` keys and
    ``[residue_name, ...]`` values; this function returns that dict directly.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findMissingResidues()

        for (chain_index, insertion_position), residue_names in temp_molecular_system.missingResidues.items():
            output[(chain_index, insertion_position)] = residue_names

    else:

        raise NotImplementedMethodError

    return output

