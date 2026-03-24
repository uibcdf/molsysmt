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
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to residue names (str) of the residues that are missing at each
        position. Only positions with missing residues are included.

    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    The function converts the (sub)system to a ``pdbfixer.PDBFixer`` object,
    calls ``findMissingResidues``, and maps the PDBFixer-internal residue indices
    back to the original group indices in the molecular system.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        temp_molecular_system.findMissingResidues()

        for group, substitution in temp_molecular_system.missingResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=substitution.name

    else:

        raise NotImplementedMethodError

    return output

