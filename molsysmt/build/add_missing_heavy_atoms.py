from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def add_missing_heavy_atoms(molecular_system, selection='all', syntax='MolSysMT', engine='PDBFixer', skip_digestion=False):
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

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", pdb_chain_id='chain_id',
                                        skip_digestion=True)
        
        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary', skip_digestion=True)
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary', skip_digestion=True)
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary', skip_digestion=True)
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary', skip_digestion=True)

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.missingTerminals = {}

        group_indices_in_selection = select(molecular_system, element='group', selection=selection, syntax=syntax, skip_digestion=True)

        aux_dict = {}

        for group, atoms in temp_molecular_system.missingAtoms.items():
            if group.index in group_indices_in_selection:
                aux_dict[group]=[]
                for atom in atoms:
                    aux_dict[group].append(atom)

        temp_molecular_system.missingAtoms = aux_dict

        temp_molecular_system.addMissingAtoms()

        output_molecular_system = convert(temp_molecular_system, to_form=form_out, skip_digestion=True)

        set(output_molecular_system, element='component', **atts_from_components, skip_digestion=True)
        set(output_molecular_system, element='molecule', **atts_from_molecules, skip_digestion=True)
        set(output_molecular_system, element='chain', **atts_from_chains, skip_digestion=True)
        set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)

        del(group_indices_in_selection, temp_molecular_system)
        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

    elif engine == 'MolSysMT':

        from molsysmt.basic import convert, get_form
        from molsysmt import pyunitwizard as puw
        from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms
        from molsysmt.build._native_placers import (
            load_residue_template, place_missing_in_group, append_atoms_to_molsys,
        )

        # Work in native form
        if form_in != 'molsysmt.MolSys':
            native_ms = convert(molecular_system, to_form='molsysmt.MolSys', skip_digestion=True)
        else:
            native_ms = molecular_system

        missing_atoms = get_missing_heavy_atoms(
            native_ms, selection=selection, syntax=syntax, engine='MolSysMT',
        )

        if not missing_atoms:
            output_molecular_system = native_ms.copy() if form_in == 'molsysmt.MolSys' else molecular_system
            return convert(output_molecular_system, to_form=form_out, skip_digestion=True) \
                if form_in != form_out else output_molecular_system

        topo = native_ms.topology
        all_coords = puw.get_value(native_ms.structures.coordinates, to_unit='nm')
        n_structures = all_coords.shape[0]

        new_atom_info = []   # list of (group_idx, atom_name, coords(n_structures, 3))
        new_bonds_info = []  # list of (abs_idx1, abs_idx2) — resolved after atom list is built

        # Track new atom indices by (group_idx, atom_name) for bond resolution
        new_atom_index_map = {}  # (group_idx, atom_name) -> new_atom_idx
        n_orig = topo.n_atoms

        for group_idx, missing_names in missing_atoms.items():
            group_name = topo.groups.loc[group_idx, 'group_name']
            template = load_residue_template(group_name)
            if template is None:
                continue

            placed = place_missing_in_group(topo, all_coords, group_idx, missing_names, template)
            if not placed:
                continue

            for atom_name in missing_names:
                if atom_name not in placed:
                    continue
                new_idx = n_orig + len(new_atom_info)
                new_atom_index_map[(group_idx, atom_name)] = new_idx
                new_atom_info.append((group_idx, atom_name, placed[atom_name]))

        # Resolve bonds: add template bonds that involve at least one new atom
        new_atom_name_by_group = {}
        for (gidx, aname), nidx in new_atom_index_map.items():
            new_atom_name_by_group.setdefault(gidx, {})[aname] = nidx

        for group_idx, name_to_new_idx in new_atom_name_by_group.items():
            group_name = topo.groups.loc[group_idx, 'group_name']
            template = load_residue_template(group_name)
            if template is None:
                continue

            # Build name → atom_idx for existing atoms of this group
            gmask = topo.atoms['group_index'] == group_idx
            exist_rows = topo.atoms[gmask]
            existing_name_to_idx = dict(
                zip(exist_rows['atom_name'], exist_rows.index.tolist())
            )
            # Merge with new atoms
            all_name_to_idx = {**existing_name_to_idx, **name_to_new_idx}

            for b1, b2 in template['bonds']:
                if b1 not in name_to_new_idx and b2 not in name_to_new_idx:
                    continue   # bond between two existing atoms (already in topology)
                if b1 not in all_name_to_idx or b2 not in all_name_to_idx:
                    continue
                new_bonds_info.append((all_name_to_idx[b1], all_name_to_idx[b2]))

        native_out = append_atoms_to_molsys(native_ms, new_atom_info, new_bonds_info)
        output_molecular_system = convert(native_out, to_form=form_out, skip_digestion=True) \
            if form_in != 'molsysmt.MolSys' else native_out

    else:

        raise NotImplementedMethodError


    return output_molecular_system

