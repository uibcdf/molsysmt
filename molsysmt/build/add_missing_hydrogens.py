from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def add_missing_hydrogens(molecular_system, pH=7.4, engine='OpenMM', skip_digestion=False):
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

    from molsysmt.basic import convert, get_form, get

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine=="OpenMM":

        from molsysmt.basic import set

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary', skip_digestion=True)
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary', skip_digestion=True)
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary', skip_digestion=True)
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary', skip_digestion=True)

        temp_molecular_system = convert(molecular_system, to_form="openmm.Modeller", skip_digestion=True)
        log_residues_changed = temp_molecular_system.addHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out, skip_digestion=True)

        _n_comp = get(output_molecular_system, element='component', n_components=True, skip_digestion=True)
        if _n_comp == len(next(iter(atts_from_components.values()))):
            set(output_molecular_system, element='component', **atts_from_components, skip_digestion=True)
        _n_mol = get(output_molecular_system, element='molecule', n_molecules=True, skip_digestion=True)
        if _n_mol == len(next(iter(atts_from_molecules.values()))):
            set(output_molecular_system, element='molecule', **atts_from_molecules, skip_digestion=True)
        _n_chain = get(output_molecular_system, element='chain', n_chains=True, skip_digestion=True)
        if _n_chain == len(next(iter(atts_from_chains.values()))):
            set(output_molecular_system, element='chain', **atts_from_chains, skip_digestion=True)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            _n_ent = get(output_molecular_system, element='entity', n_entities=True, skip_digestion=True)
            if _n_ent == len(next(iter(atts_from_entities.values()))):
                set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            _n_ent = get(output_molecular_system, element='entity', n_entities=True, skip_digestion=True)
            if _n_ent == len(next(iter(atts_from_entities.values()))):
                set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    elif engine=='PDBFixer':

        from molsysmt.basic import set

        atts_from_components = get(molecular_system, element='component', component_name=True,
                                   output_type='dictionary', skip_digestion=True)
        atts_from_molecules = get(molecular_system, element='molecule', molecule_name=True,
                                  output_type='dictionary', skip_digestion=True)
        atts_from_chains = get(molecular_system, element='chain', chain_id=True, chain_name=True,
                               output_type='dictionary', skip_digestion=True)
        atts_from_entities = get(molecular_system, element='entity', entity_name=True,
                                 output_type='dictionary', skip_digestion=True)

        temp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer", skip_digestion=True)
        temp_molecular_system.addMissingHydrogens(pH=pH)
        output_molecular_system = convert(temp_molecular_system, to_form=form_out, skip_digestion=True)

        _n_comp = get(output_molecular_system, element='component', n_components=True, skip_digestion=True)
        if _n_comp == len(next(iter(atts_from_components.values()))):
            set(output_molecular_system, element='component', **atts_from_components, skip_digestion=True)
        _n_mol = get(output_molecular_system, element='molecule', n_molecules=True, skip_digestion=True)
        if _n_mol == len(next(iter(atts_from_molecules.values()))):
            set(output_molecular_system, element='molecule', **atts_from_molecules, skip_digestion=True)
        _n_chain = get(output_molecular_system, element='chain', n_chains=True, skip_digestion=True)
        if _n_chain == len(next(iter(atts_from_chains.values()))):
            set(output_molecular_system, element='chain', **atts_from_chains, skip_digestion=True)
        if form_out=='molsysmt.MolSys':
            output_molecular_system.topology.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                              redefine_names=True, redefine_types=True)
            _n_ent = get(output_molecular_system, element='entity', n_entities=True, skip_digestion=True)
            if _n_ent == len(next(iter(atts_from_entities.values()))):
                set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)
        elif form_out=='molsysmt.Topology':
            output_molecular_system.rebuild_entities(redefine_indices=True, redefine_ids=True,
                                                     redefine_names=True, redefine_types=True)
            _n_ent = get(output_molecular_system, element='entity', n_entities=True, skip_digestion=True)
            if _n_ent == len(next(iter(atts_from_entities.values()))):
                set(output_molecular_system, element='entity', **atts_from_entities, skip_digestion=True)


        del(atts_from_components, atts_from_molecules, atts_from_chains, atts_from_entities)

        del(temp_molecular_system)

    elif engine == 'MolSysMT':

        from molsysmt.basic import convert, get, select
        from molsysmt import pyunitwizard as puw
        from molsysmt.element.group.amino_acid import (
            get_expected_hydrogens, get_standard_name, group_names, get_group_db
        )
        from molsysmt.build._native_placers import (
            append_atoms_to_molsys, h_bond_length, load_residue_template,
            place_hydrogens_on_parent, _infer_hybridization,
        )

        if form_in != 'molsysmt.MolSys':
            native_ms = convert(molecular_system, to_form='molsysmt.MolSys', skip_digestion=True)
        else:
            native_ms = molecular_system

        topo = native_ms.topology
        all_coords = puw.get_value(native_ms.structures.coordinates, to_unit='nm')
        n_structures = all_coords.shape[0]

        # For each group determine terminal status
        # Rebuild components to ensure component_type is derived from bonds
        topo.rebuild_components(redefine_indices=True, redefine_ids=False,
                                redefine_types=True, redefine_names=False)

        # Group-level metadata
        n_groups = topo.n_groups

        # Determine first/last group of each component (peptide/protein)
        comp_first = {}   # comp_idx -> first group_idx
        comp_last  = {}   # comp_idx -> last group_idx
        for g in range(n_groups):
            g_atoms = topo.atoms[topo.atoms['group_index'] == g]
            if g_atoms.empty:
                continue
            c_idx = int(topo._get_component_indices().loc[g_atoms.index[0]])
            if c_idx not in comp_first:
                comp_first[c_idx] = g
            comp_last[c_idx] = g

        # Detect disulfide bonds: CYS–CYS SG–SG bonds
        disulfide_groups = {}   # used as a set (keys only)
        bonds = topo._get_chemical_state_bonds()
        if bonds is not None and len(bonds) > 0:
            for _, brow in bonds.iterrows():
                a1 = int(brow['atom1_index'])
                a2 = int(brow['atom2_index'])
                row1 = topo.atoms.loc[a1]
                row2 = topo.atoms.loc[a2]
                if (row1['atom_name'] == 'SG' and row2['atom_name'] == 'SG'):
                    disulfide_groups[int(row1['group_index'])] = True
                    disulfide_groups[int(row2['group_index'])] = True

        # Collect all atom_name→atom_index mappings per group (for bond neighbor lookup)
        group_name_to_idx = {}   # group_idx -> {atom_name: atom_idx}
        for g in range(n_groups):
            g_atoms = topo.atoms[topo.atoms['group_index'] == g]
            group_name_to_idx[g] = dict(zip(g_atoms['atom_name'], g_atoms.index.tolist()))

        new_atom_info  = []   # (group_idx, atom_name, coords(n_s,3))
        new_bonds_info = []   # (new_idx1, new_idx2) or (existing_idx, new_idx)

        n_atoms_so_far = topo.n_atoms   # running counter for new atom indices

        for g in range(n_groups):
            g_atoms = topo.atoms[topo.atoms['group_index'] == g]
            if g_atoms.empty:
                continue

            gname = topo.groups.loc[g, 'group_name'] if g < len(topo.groups) else None

            canonical = get_standard_name(gname) if gname else None
            lookup = canonical if canonical is not None else gname

            if gname in ('ACE', 'NME'):
                # Place missing H atoms on pre-existing capping groups via template bonds.
                template = load_residue_template(gname)
                if template is None:
                    continue
                present_hs = {a for a in g_atoms['atom_name']
                              if a.startswith('H') or
                              (len(a) >= 2 and a[0].isdigit() and a[1] == 'H')}
                name_to_idx = group_name_to_idx[g]
                # Build parent → [H, ...] map from template bonds
                capping_parent_to_hs = {}
                for b1, b2 in template['bonds']:
                    b1h = b1.startswith('H') or (len(b1) >= 2 and b1[0].isdigit() and b1[1] == 'H')
                    b2h = b2.startswith('H') or (len(b2) >= 2 and b2[0].isdigit() and b2[1] == 'H')
                    if b1h and not b2h:
                        capping_parent_to_hs.setdefault(b2, []).append(b1)
                    elif b2h and not b1h:
                        capping_parent_to_hs.setdefault(b1, []).append(b2)
                for par_name, h_names in capping_parent_to_hs.items():
                    missing_hs_here = [h for h in h_names if h not in present_hs]
                    if not missing_hs_here:
                        continue
                    par_idx = name_to_idx.get(par_name)
                    if par_idx is None:
                        continue
                    par_pos = all_coords[:, int(par_idx), :]
                    # Heavy neighbors of par_name within the template
                    neigh_positions = []
                    for b1, b2 in template['bonds']:
                        b1h = b1.startswith('H') or (len(b1) >= 2 and b1[0].isdigit() and b1[1] == 'H')
                        b2h = b2.startswith('H') or (len(b2) >= 2 and b2[0].isdigit() and b2[1] == 'H')
                        if not b1h and not b2h:
                            nb = b2 if b1 == par_name else (b1 if b2 == par_name else None)
                            if nb is not None:
                                nb_idx = name_to_idx.get(nb)
                                if nb_idx is not None:
                                    neigh_positions.append(all_coords[:, int(nb_idx), :])
                    # For NME N: also add C from the preceding residue (peptide bond)
                    if gname == 'NME' and par_name == 'N':
                        n_atom_idx = name_to_idx.get('N')
                        if n_atom_idx is not None and bonds is not None and len(bonds) > 0:
                            for _, brow in bonds.iterrows():
                                a1, a2 = int(brow['atom1_index']), int(brow['atom2_index'])
                                other = a2 if a1 == n_atom_idx else (a1 if a2 == n_atom_idx else None)
                                if other is not None:
                                    if int(topo.atoms.loc[other, 'group_index']) != g:
                                        neigh_positions.append(all_coords[:, other, :])
                    # CH3 (ACE) and C (NME methyl) are sp3; N is sp3 for amide H placement
                    bond_len = h_bond_length('C') if par_name in ('CH3', 'C') else h_bond_length(par_name[0])
                    placed = place_hydrogens_on_parent(
                        par_pos, neigh_positions, len(missing_hs_here), 'sp3', bond_len, n_structures
                    )
                    for h_name, h_coords in zip(missing_hs_here, placed):
                        new_atom_info.append((g, h_name, h_coords))
                        h_new_idx = n_atoms_so_far + len(new_atom_info) - 1
                        new_bonds_info.append((int(par_idx), h_new_idx))
                continue

            elif lookup not in group_names:
                continue   # skip non-amino-acid groups

            # Terminal status
            c_idx = int(topo._get_component_indices().loc[g_atoms.index[0]])
            is_n_term = (comp_first.get(c_idx) == g)
            is_c_term = (comp_last.get(c_idx) == g)
            is_disulfide = (g in disulfide_groups)

            present_names = g_atoms['atom_name'].tolist()
            present_heavy = [a for a in present_names
                             if not (a.startswith('H') or
                                     (len(a) >= 2 and a[0].isdigit() and a[1] == 'H'))]
            present_hs = {a for a in present_names
                          if a.startswith('H') or
                          (len(a) >= 2 and a[0].isdigit() and a[1] == 'H')}

            expected_hs = get_expected_hydrogens(
                gname, present_atom_names=present_names, pH=pH,
                is_n_terminal=is_n_term, is_c_terminal=is_c_term,
                is_disulfide=is_disulfide,
            )
            if expected_hs is None:
                continue

            missing_hs = [h for h in expected_hs if h not in present_hs]
            if not missing_hs:
                continue

            # Get the variant bonds to know parent → H relationships
            db = get_group_db(lookup)

            # Select best variant.
            # When H atoms are present, primary criterion is maximum overlap with
            # their names (to avoid picking a variant that uses a different naming
            # convention for the same physical atoms).  Secondary: fewest extra
            # heavy atoms (tightest heavy-atom fit).
            best_variant = None
            best_h_overlap = -1
            best_extra = None
            present_heavy_set = {a for a in present_heavy}
            for variant in db['topology']:
                variant_heavy = {a for a in variant['atoms']
                                 if not (a.startswith('H') or
                                         (len(a) >= 2 and a[0].isdigit() and a[1] == 'H'))}
                if present_heavy_set <= variant_heavy:
                    extra = len(variant_heavy) - len(present_heavy_set)
                    variant_hs = {a for a in variant['atoms']
                                  if a.startswith('H') or
                                  (len(a) >= 2 and a[0].isdigit() and a[1] == 'H')}
                    h_overlap = len(present_hs & variant_hs)
                    if (best_extra is None or
                            h_overlap > best_h_overlap or
                            (h_overlap == best_h_overlap and extra < best_extra)):
                        best_extra = extra
                        best_h_overlap = h_overlap
                        best_variant = variant
            if best_variant is None:
                best_variant = db['topology'][0]

            # Build parent→Hs map from variant bonds
            parent_to_hs = {}   # atom_name -> [h_name, ...]
            for b1, b2 in best_variant['bonds']:
                h, par = None, None
                b1_is_h = b1.startswith('H') or (len(b1) >= 2 and b1[0].isdigit() and b1[1] == 'H')
                b2_is_h = b2.startswith('H') or (len(b2) >= 2 and b2[0].isdigit() and b2[1] == 'H')
                if b1_is_h and not b2_is_h:
                    h, par = b1, b2
                elif b2_is_h and not b1_is_h:
                    h, par = b2, b1
                if h is not None and h in missing_hs:
                    parent_to_hs.setdefault(par, []).append(h)

            # For each parent, place its missing Hs
            name_to_idx = group_name_to_idx[g]   # existing atoms in this group

            # Also include neighbour atom indices from adjacent groups for backbone N
            # N-H placement needs C(i-1) — bond partner from bonds DataFrame
            def _get_pos(aname, name_to_idx=name_to_idx):
                """Coords (n_s,3) for atom_name in this group, or None."""
                idx = name_to_idx.get(aname)
                if idx is None:
                    return None
                return all_coords[:, int(idx), :]

            for par_name, h_names in parent_to_hs.items():
                par_pos = _get_pos(par_name)
                if par_pos is None:
                    continue   # parent not present — skip

                # Find heavy-atom neighbors of parent in the variant
                variant_heavy_neigh = []
                for b1, b2 in best_variant['bonds']:
                    b1_is_h = b1.startswith('H') or (len(b1) >= 2 and b1[0].isdigit() and b1[1] == 'H')
                    b2_is_h = b2.startswith('H') or (len(b2) >= 2 and b2[0].isdigit() and b2[1] == 'H')
                    if not b1_is_h and not b2_is_h:
                        if b1 == par_name:
                            variant_heavy_neigh.append(b2)
                        elif b2 == par_name:
                            variant_heavy_neigh.append(b1)

                # Positions of existing heavy neighbors within the group
                neigh_positions = []
                for nb_name in variant_heavy_neigh:
                    pos = _get_pos(nb_name)
                    if pos is not None:
                        neigh_positions.append(pos)

                # For backbone N: add C from previous residue via bonds table
                if par_name == 'N' and len(neigh_positions) < 2:
                    n_atom_idx = name_to_idx.get('N')
                    if n_atom_idx is not None:
                        for _, brow in bonds.iterrows():
                            a1 = int(brow['atom1_index'])
                            a2 = int(brow['atom2_index'])
                            other = None
                            if a1 == n_atom_idx:
                                other = a2
                            elif a2 == n_atom_idx:
                                other = a1
                            if other is not None:
                                other_gidx = int(topo.atoms.loc[other, 'group_index'])
                                if other_gidx != g:
                                    neigh_positions.append(all_coords[:, other, :])

                par_element = par_name[0] if par_name else 'C'
                bond_len = h_bond_length(par_element)
                hybridization = _infer_hybridization(par_name, variant_heavy_neigh, lookup)

                n_hs = len(h_names)
                placed = place_hydrogens_on_parent(
                    par_pos, neigh_positions, n_hs, hybridization, bond_len, n_structures
                )

                for h_name, h_coords in zip(h_names, placed):
                    new_atom_info.append((g, h_name, h_coords))
                    h_new_idx = n_atoms_so_far + len(new_atom_info) - 1
                    par_existing_idx = name_to_idx[par_name]
                    new_bonds_info.append((par_existing_idx, h_new_idx))

        if new_atom_info:
            native_out = append_atoms_to_molsys(native_ms, new_atom_info, new_bonds_info)
        else:
            native_out = native_ms

        output_molecular_system = convert(native_out, to_form=form_in, skip_digestion=True) \
            if form_in != 'molsysmt.MolSys' else native_out

    else:

        raise NotImplementedError


    return output_molecular_system
