from molsysmt._private.digestion import digest

@digest()
def add_missing_terminal_cappings(molecular_system, N_terminal=None, C_terminal=None, pH=7.4, 
                                  keep_ids=False, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    Adding terminal cappings to peptides and proteins.

    This function adds chemical groups to the N- and/or C-termini of protein or peptide chains. 
    These terminal groups can either neutralize terminal charges or simply complete missing atoms 
    for a standard terminal residue. The resulting cappings are consistent with typical protonation 
    states at the specified pH.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to which terminal 
        cappings will be added.

    N_terminal : str or None, default None
        Residue name to cap the N-terminus. If `None`, the missing atoms are added to the 
        native terminal residue without introducing a separate cap. Use `'ACE'` to cap with 
        an acetyl group, or other recognized residue names.

    C_terminal : str or None, default None
        Residue name to cap the C-terminus. If `None`, the missing atoms are added to the 
        native terminal residue without introducing a separate cap. Use `'NME'` to cap with 
        a N-methyl amide group, or other recognized residue names.

    pH : float, default 7.4
        Approximate pH used to determine the protonation states of terminal groups and nearby residues.

    keep_ids : bool, default False
        If `True`, preserves the original atom, group, and molecule IDs. Otherwise, new IDs may be reassigned.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Selection of atoms or residues to which this operation applies. Can be a list of indices or a 
        query string following :ref:`MolSysMT selection syntax <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        Syntax used to parse the `selection` argument, if it is a string.

    engine : {'PDBFixer'}, default 'PDBFixer'
        Engine used to perform capping. Determines atom placement and protonation based on templates.

    Returns
    -------
    molecular system
        A new molecular system with modified termini, in the same form as the input system.

    Raises
    ------
    NotSupportedFormError
        Raised if the input molecular system is in a non-supported form.

    ArgumentError
        Raised if an input argument value is invalid.

    Notes
    -----
    Common capping groups:
      - `'ACE'` for acetyl (N-terminal)
      - `'NME'` for N-methyl amide (C-terminal)

    If no capping residues are provided, the function only completes missing terminal atoms 
    in the native residues (which are often charged).

    The list of supported molecular system forms is detailed in:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    See Also
    --------
    :func:`molsysmt.build.build_peptide`
        Construct a peptide sequence with optional terminal cappings.

    :func:`molsysmt.build.add_missing_heavy_atoms`
        Add missing non-hydrogen atoms to standard residues.

    :func:`molsysmt.basic.info`
        Inspect the content and composition of a molecular system.

    :func:`molsysmt.physchem.get_charge`
        Calculate the total or partial charge of a system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AlaValPro')
    >>> molsys = msm.build.add_missing_terminal_cappings(molsys, N_terminal='ACE', C_terminal='NME')
    >>> msm.physchem.get_charge(capped_system)
    0.0 elementary_charge
    >>> msm.convert(molsys, to_form='string:amino_acids_3')
    'AceAlaValProNme'

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Add missing terminal cappings <Tutorial_Add_missing_terminal_cappings>`

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get_form

    output_molecular_system = None
    form_in = get_form(molecular_system)

    if engine == 'PDBFixer':

        from molsysmt.basic import convert, get, select, has_attribute, set
        from pdbfixer.pdbfixer import Sequence

        temp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer')
        atom_indices_in_selection = select(temp_molecular_system, selection=selection, syntax=syntax)
        atom_indices_in_components = get(temp_molecular_system, element='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True)

        temp_molecular_system.findMissingResidues()

        for atom_indices_in_component in atom_indices_in_components:

            chain_index = get(temp_molecular_system, element='chain', selection='atom_index in @atom_indices_in_component',
                           chain_index=True)[0]

            n_groups = get(temp_molecular_system, element='group',
                           selection='atom_index in @atom_indices_in_component', n_groups=True)

            if N_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,0)]=[N_terminal]

            if C_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,n_groups)]=[C_terminal]

        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.addMissingAtoms()

        n_hs = get(temp_molecular_system, element='atom', selection='atom_type=="H"', n_atoms=True)

        #if n_hs > 0:
        #    temp_molecular_system.addMissingHydrogens(pH)

        output_molecular_system = convert(temp_molecular_system, to_form=form_in)

        if has_attribute(molecular_system, 'component_name'):
            component_names = get(molecular_system, element='component', component_name=True)
            set(output_molecular_system, element='component', component_name=component_names)

        if has_attribute(molecular_system, 'molecule_name'):
            molecule_names = get(molecular_system, element='molecule', molecule_name=True)
            set(output_molecular_system, element='molecule', molecule_name=molecule_names)

        if has_attribute(molecular_system, 'entity_name'):
            entity_names = get(molecular_system, element='entity', entity_name=True)
            set(output_molecular_system, element='entity', entity_name=entity_names)

        if n_hs > 0:
        
            from molsysmt.build import add_missing_hydrogens
            output_molecular_system = add_missing_hydrogens(output_molecular_system, pH=pH)

        if keep_ids:
            raise NotImplementedError

        return output_molecular_system

    else:

        raise NotImplementedError


