from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import *

@arg_digest()
def get_non_standard_residues(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    Identify non-standard residues in a molecular system and suggest standard replacements.

    This function detects residues whose names are not part of the standard set
    recognised by the backend and maps their group indices to the names of the
    standard residues that can be used as replacements.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used to restrict the search to a subset of the system.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'PDBFixer'}, default 'PDBFixer'
        Backend used to detect non-standard residues. Only 'PDBFixer' is currently
        supported.

    Returns
    -------
    dict
        Dictionary mapping group (residue) indices (int) in the original molecular
        system to the names (str) of the closest standard residue replacements
        suggested by the backend.

    Raises
    ------
    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    The function converts the (sub)system to a ``pdbfixer.PDBFixer`` object, calls
    ``findNonstandardResidues``, and maps the PDBFixer-internal residue indices
    back to the original group indices in the molecular system.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        tmp_item = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        tmp_item.findNonstandardResidues()

        for group, substitution in tmp_item.nonstandardResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index]=substitution.name

    else:

        raise NotImplementedMethodError

    return output

