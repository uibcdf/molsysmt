from molsysmt._private.digestion import digest

@digest()
def add_missing_hydrogens(molecular_system, pH=7.4, engine='OpenMM'):
    """
    Adding missing hydrogen atoms to a molecular system.

    This function adds hydrogen atoms that are missing from a molecular system,
    based on its topology, standard chemical templates, and a selected pH. The
    added atoms are positioned using predefined rules for protonation states and
    geometry constraints.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` 
        to which hydrogens will be added.

    pH : float, default 7.4
        Approximate pH used to determine the protonation state of ionizable groups.

    engine : {'MolSysMT', 'OpenMM', 'PDBFixer'}, default 'OpenMM'
        The engine used to perform hydrogen placement. The engine determines
        residue protonation states and adds atoms accordingly.

    Returns
    -------
    molecular system
        A new molecular system with hydrogens added, returned in the same form
        as the input.

    Raises
    ------
    NotSupportedFormError
        Raised if the input molecular system is not in a supported form.

    ArgumentError
        Raised if an input argument does not meet the expected format or conditions.

    EngineError
        Raised if the selected engine fails to perform hydrogen addition.

    Notes
    -----
    Hydrogen atoms are added based on standard residue templates and general
    rules for protonation. Ionizable side chains (e.g., ASP, GLU, HIS) are adjusted
    according to the provided pH.

    The list of supported molecular systems' forms is available at:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    See Also
    --------
    :func:`molsysmt.build.has_hydrogens`
        Check whether a molecular system contains hydrogen atoms.

    :func:`molsysmt.build.add_missing_heavy_atoms`
        Add missing non-hydrogen atoms to a molecular system.

    :func:`molsysmt.basic.contains`
        Check for the presence of specific atoms or molecules.

    Examples
    --------
    The following example illustrates the use of the function:

    >>> import molsysmt as msm
    >>> molsys = msm.convert('181L', selection='molecule_type=="protein"')
    >>> msm.build.has_hydrogens(molecular_system)
    False
    >>> molsys = msm.build.add_missing_hydrogens(molsys, pH=7.4)
    >>> msm.build.has_hydrogens(molsys)
    True

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Add missing hydrogens <Tutorial_Add_missing_hydrogens>`

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import convert, get_form, get, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller")
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components)
        set(output_molecular_system, element='molecule', **atts_from_molecules)
        set(output_molecular_system, element='chain', **atts_from_chains)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    elif engine=='PDBFixer':

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary')

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")
        temp_molecular_system.addMissingHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components)
        set(output_molecular_system, element='molecule', **atts_from_molecules)
        set(output_molecular_system, element='chain', **atts_from_chains)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            set(output_molecular_system, element='entity', **atts_from_entities)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    else:

        raise NotImplementedError


    return output_molecular_system

