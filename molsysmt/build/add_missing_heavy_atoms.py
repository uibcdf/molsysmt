from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest()
def add_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer'):
    """
    Adding missing non-hydrogen atoms to a molecular system.

    This function checks for missing heavy atoms (non-hydrogens) in a molecular system and adds
    them when possible. The missing atoms are identified based on known residue templates and
    inferred topological context. The coordinates of new atoms are estimated using internal
    geometry rules or external reconstruction engines such as PDBFixer.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to which missing
        heavy atoms will be added.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms that define the residues or molecules to analyze.
        Can be provided as indices (list, tuple, array of 0-based integers) or as a string using any
        of the supported :ref:`selection syntaxes <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        :ref:`Selection syntax <Introduction_Selection>` used when `selection` is a string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'PDBFixer'
        Engine used to rebuild the missing atoms. If `'MolSysMT'` is chosen, internal geometry
        templates are used. If `'PDBFixer'` is selected, the external PDBFixer engine is called.

    Returns
    -------
    molecular system
        A molecular system with the missing heavy atoms added, in the same form as the input system.

    Raises
    ------
    NotSupportedFormError
        Raised if the input molecular system is in an unsupported format.

    ArgumentError
        Raised if one or more input arguments are invalid.

    EngineError
        Raised if the specified engine fails to rebuild the atoms.

    Notes
    -----
    This function adds only non-hydrogen atoms (heavy atoms) that are missing from standard
    residues. Hydrogen atoms can be added using other tools or methods.

    The list of supported molecular systems' forms is detailed in:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    The list of supported selection syntaxes is available at:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.build.get_missing_heavy_atoms`
        Identify heavy atoms that are missing based on residue templates.

    :func:`molsysmt.basic.remove`
        Remove atoms from a molecular system.

    :func:`molsysmt.basic.contains`
        Check whether specific elements are present in a molecular system.

    :func:`molsysmt.build.build_peptide`
        Build capped peptide structures from amino acid sequences.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.build.build_peptide('AAA')
    >>> msm.get(molsys, selection='atom_name=="CB"', n_atoms=True)
    3
    >>> molsys = msm.build.remove(molsys, selection='atom_name=="CB"')
    >>> msm.get(molsys, selection='atom_name=="CB"', n_atoms=True)
    0
    >>> molsys = msm.build.add_missing_heavy_atoms(molsys)
    >>> msm.get(molsys, selection='atom_name=="CB"', n_atoms=True)
    3

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:  
       :ref:`User Guide > Tools > Build > Add missing heavy atoms <Tutorial_Add_missing_heavy_atoms>`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get_form, convert, select, get, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="PDBFixer":

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary')
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary')
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary')
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary')

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.missingTerminals = {}

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, syntax=syntax)

        aux_dict = {}

        for group, atoms in temp_molecular_system.missingAtoms.items():
            if group.index in group_indices_in_selection:
                aux_dict[group]=[]
                for atom in atoms:
                    aux_dict[group].append(atom)

        temp_molecular_system.missingAtoms = aux_dict

        temp_molecular_system.addMissingAtoms()

        output_molecular_system = convert(temp_molecular_system, to_form=form_out)

        set(output_molecular_system, element='component', **atts_from_components, skip_digestion=True)
        set(output_molecular_system, element='molecule', **atts_from_molecules, skip_digestion=True)
        set(output_molecular_system, element='chain', **atts_from_chains, skip_digestion=True)
        set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)

        del(group_indices_in_selection, temp_molecular_system)
        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

    else:

        raise NotImplementedMethodError


    return output_molecular_system

