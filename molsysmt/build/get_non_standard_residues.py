from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import *

@arg_digest()
def get_non_standard_residues(molecular_system, selection='all', syntax='MolSysMT', engine='MolSysMT'):
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

    engine : {'MolSysMT', 'PDBFixer'}, default 'MolSysMT'
        Backend used to detect non-standard residues.

        * ``'MolSysMT'``: native implementation using MolSysMT's built-in
          amino-acid database (~817 entries from MDTraj/PDB).  Works with any
          supported form; no external dependency required.
        * ``'PDBFixer'``: delegates to ``pdbfixer.findNonstandardResidues``
          (~150-entry substitution table).  Also reads MODRES records when the
          source is a PDB/mmCIF file.

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
    When ``engine='MolSysMT'`` the detection relies on the ``name_to_type``
    table in :mod:`molsysmt.element.group.amino_acid.group_types`, which maps
    ~817 residue names (standard + non-standard amino acids, D-forms,
    protonation-state variants, PTMs) to their canonical 3-letter codes.  A
    residue is reported as non-standard when its name maps to a *different*
    standard code (e.g. ``'MSE'`` → ``'MET'``).  Residues that map to
    ``'XAA'`` (completely unknown) are not reported.

    .. versionadded:: 1.0.0
    """

    output = {}

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt.element.group.amino_acid import get_standard_name

        group_indices = select(molecular_system, element='group', selection=selection, syntax=syntax)
        group_name_list = get(molecular_system, element='group', selection=group_indices,
                              group_name=True)

        for group_idx, group_name in zip(group_indices, group_name_list):
            standard = get_standard_name(group_name)
            if standard is not None:
                output[int(group_idx)] = standard

    elif engine=="PDBFixer":

        from molsysmt.basic import convert, get_form, select

        group_indices_in_selection = select(molecular_system, element='group', selection=selection)

        tmp_item = convert(molecular_system, to_form="pdbfixer.PDBFixer", selection=selection,
                                        syntax=syntax)

        tmp_item.findNonstandardResidues()

        for group, substitution in tmp_item.nonstandardResidues:
            original_group_index = group_indices_in_selection[group.index]
            output[original_group_index] = substitution if isinstance(substitution, str) else substitution.name

    else:

        raise NotImplementedMethodError

    return output

