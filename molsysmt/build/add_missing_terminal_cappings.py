from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def add_missing_terminal_cappings(molecular_system, N_terminal=None, C_terminal=None, pH=7.4, 
                                  keep_ids=False, selection='all', syntax='MolSysMT', engine='PDBFixer',
                                  skip_digestion=False):
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
        If `True`, preserves the original atom and group ids. Otherwise, new IDs may be reassigned.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Selection of atoms or residues to which this operation applies. Can be a list of indices or a 
        query string following :ref:`MolSysMT selection syntax <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        Syntax used to parse the `selection` argument, if it is a string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'PDBFixer'
        Engine used to perform capping.

        * ``'MolSysMT'``: native implementation using internal residue templates and
          geometric peptide-bond construction. No external dependencies required.
          For ACE/NME capping, energy minimisation is recommended afterwards to
          relax the newly inserted groups.
        * ``'PDBFixer'``: delegates to PDBFixer's missing-atom and missing-residue
          machinery.

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

        conversion_extra_kwargs = {}
        if form_in in ['molsysmt.MolSys']:
            conversion_extra_kwargs['pdb_chain_id'] = 'chain_id'

        temp_molecular_system = convert(molecular_system, to_form='pdbfixer.PDBFixer', **conversion_extra_kwargs, skip_digestion=True)
        atom_indices_in_selection = select(temp_molecular_system, selection=selection, syntax=syntax, skip_digestion=True)
        atom_indices_in_components = get(temp_molecular_system, element='component', selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection', atom_index=True, skip_digestion=True)

        temp_molecular_system.findMissingResidues()

        for atom_indices_in_component in atom_indices_in_components:

            chain_index = get(temp_molecular_system, element='chain', selection='atom_index in @atom_indices_in_component',
                           chain_index=True, skip_digestion=True)[0]

            n_groups = get(temp_molecular_system, element='group',
                           selection='atom_index in @atom_indices_in_component', n_groups=True, skip_digestion=True)

            if N_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,0)]=[N_terminal]

            if C_terminal is not None:

                temp_molecular_system.missingResidues[(chain_index,n_groups)]=[C_terminal]

        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.addMissingAtoms()

        n_hs = get(temp_molecular_system, element='atom', selection='atom_type=="H"', n_atoms=True, skip_digestion=True)

        #if n_hs > 0:
        #    temp_molecular_system.addMissingHydrogens(pH)

        output_molecular_system = convert(temp_molecular_system, to_form=form_in, skip_digestion=True)


        # Adding terminal groups can change n_components or n_molecules; guard each set().
        if has_attribute(molecular_system, 'component_name', skip_digestion=True):
            aux_component_names = get(molecular_system, element='component', component_name=True, skip_digestion=True)
            _n_comp = get(output_molecular_system, element='component', n_components=True, skip_digestion=True)
            if _n_comp == len(aux_component_names):
                set(output_molecular_system, element='component', component_name=aux_component_names, skip_digestion=True)
            del aux_component_names

        if has_attribute(molecular_system, 'chain_name', skip_digestion=True):
            aux_chain_names = get(molecular_system, element='chain', chain_name=True, skip_digestion=True)
            _n_chain = get(output_molecular_system, element='chain', n_chains=True, skip_digestion=True)
            if _n_chain == len(aux_chain_names):
                set(output_molecular_system, element='chain', chain_name=aux_chain_names, skip_digestion=True)
            del aux_chain_names

        if has_attribute(molecular_system, 'chain_id', skip_digestion=True):
            aux_chain_ids = get(molecular_system, element='chain', chain_id=True, skip_digestion=True)
            _n_chain = get(output_molecular_system, element='chain', n_chains=True, skip_digestion=True)
            if _n_chain == len(aux_chain_ids):
                set(output_molecular_system, element='chain', chain_id=aux_chain_ids, skip_digestion=True)
            del aux_chain_ids

        if has_attribute(molecular_system, 'molecule_name', skip_digestion=True):
            aux_molecule_names = get(molecular_system, element='molecule', molecule_name=True, skip_digestion=True)
            _n_mol = get(output_molecular_system, element='molecule', n_molecules=True, skip_digestion=True)
            if _n_mol == len(aux_molecule_names):
                set(output_molecular_system, element='molecule', molecule_name=aux_molecule_names, skip_digestion=True)
            del aux_molecule_names

        if has_attribute(molecular_system, 'entity_name', skip_digestion=True):
            aux_entity_names = get(molecular_system, element='entity', entity_name=True, skip_digestion=True)
            _n_ent = get(output_molecular_system, element='entity', n_entities=True, skip_digestion=True)
            if _n_ent == len(aux_entity_names):
                set(output_molecular_system, element='entity', entity_name=aux_entity_names, skip_digestion=True)
            del aux_entity_names

        if n_hs > 0:
        
            from molsysmt.build import add_missing_hydrogens
            output_molecular_system = add_missing_hydrogens(output_molecular_system, pH=pH, skip_digestion=True)

        if keep_ids:
            raise NotImplementedError

        return output_molecular_system

    elif engine == 'MolSysMT':

        from molsysmt.basic import convert, get, select
        from molsysmt import pyunitwizard as puw
        from molsysmt.build._native_placers import (
            load_residue_template, place_missing_in_group, append_atoms_to_molsys,
            place_ace_group, place_nme_group, rebuild_molsys_with_new_groups,
        )
        from molsysmt.build.add_missing_heavy_atoms import add_missing_heavy_atoms

        if form_in != 'molsysmt.MolSys':
            native_ms = convert(molecular_system, to_form='molsysmt.MolSys', skip_digestion=True)
        else:
            native_ms = molecular_system

        # --- Case A: complete missing atoms in native terminal residues ---
        # Step A1: add missing sidechain/backbone heavy atoms (OXT excluded there).
        native_ms = add_missing_heavy_atoms(
            native_ms, selection=selection, syntax=syntax, engine='MolSysMT',
        )

        # Step A2: add OXT where get_missing_terminal_cappings reports it missing.
        # Skip when C_terminal is not None: the C-terminus will be capped by a new
        # group (NME), so OXT must not be inserted first.
        from molsysmt.build.get_missing_terminal_cappings import get_missing_terminal_cappings
        missing_oxt = get_missing_terminal_cappings(
            native_ms, selection=selection, syntax=syntax, engine='MolSysMT',
        ) if C_terminal is None else {}
        if missing_oxt:
            from molsysmt.build._native_placers import place_oxt_atom, append_atoms_to_molsys
            topo_a = native_ms.topology
            coords_a = puw.get_value(native_ms.structures.coordinates, to_unit='nm')
            n_structures_a = coords_a.shape[0]
            new_atom_info_a = []
            new_bonds_info_a = []
            n_orig_a = topo_a.n_atoms

            for group_idx, oxt_list in missing_oxt.items():
                if 'OXT' not in oxt_list:
                    continue
                gmask = topo_a.atoms['group_index'] == group_idx
                grow = topo_a.atoms[gmask]
                def _pos(aname):
                    r = grow[grow['atom_name'] == aname]
                    return coords_a[:, r.index[0], :] if len(r) else None
                C_pos  = _pos('C')
                CA_pos = _pos('CA')
                O_pos  = _pos('O')
                if C_pos is None or CA_pos is None or O_pos is None:
                    continue
                oxt_coords = place_oxt_atom(C_pos, CA_pos, O_pos, n_structures_a)
                oxt_idx = n_orig_a + len(new_atom_info_a)
                new_atom_info_a.append((group_idx, 'OXT', oxt_coords))
                # OXT is bonded to C
                C_idx_in_topo = grow[grow['atom_name'] == 'C'].index[0]
                new_bonds_info_a.append((int(C_idx_in_topo), oxt_idx))

            if new_atom_info_a:
                native_ms = append_atoms_to_molsys(native_ms, new_atom_info_a, new_bonds_info_a)

        # If no capping groups requested, we're done
        if N_terminal is None and C_terminal is None:
            output_molecular_system = convert(native_ms, to_form=form_in, skip_digestion=True) \
                if form_in != 'molsysmt.MolSys' else native_ms
            return output_molecular_system

        # --- Case B: insert ACE and/or NME as new groups ---

        # Rebuild component indices from bonds so component_type is guaranteed correct
        # regardless of the origin of the input system.
        # native_ms is always a fresh object at this point (returned by add_missing_heavy_atoms).
        native_ms.topology.rebuild_components(redefine_indices=True, redefine_ids=False,
                                              redefine_types=True, redefine_names=False)

        topo = native_ms.topology
        all_coords = puw.get_value(native_ms.structures.coordinates, to_unit='nm')
        n_structures = all_coords.shape[0]

        # Identify peptide/protein components in selection.
        # Component indices are derived from covalent connectivity (bonds), so they
        # are an objective property of the system — no dependency on external metadata.
        atom_indices_in_selection = select(
            native_ms, selection=selection, syntax=syntax, skip_digestion=True
        )
        component_indices = get(
            native_ms, element='component',
            selection='component_type in ["peptide", "protein"] and atom_index in @atom_indices_in_selection',
            component_index=True, skip_digestion=True,
        )
        if component_indices is None or len(component_indices) == 0:
            output_molecular_system = convert(native_ms, to_form=form_in, skip_digestion=True) \
                if form_in != 'molsysmt.MolSys' else native_ms
            return output_molecular_system

        # For each component determine the first and last group index
        mol_group_ranges = {}
        for comp_idx in component_indices:
            comp_atom_idxs = get(
                native_ms, element='atom',
                selection=f'component_index=={comp_idx}',
                atom_index=True, skip_digestion=True,
            )
            comp_group_idxs = sorted(
                topo.atoms.loc[comp_atom_idxs, 'group_index'].dropna().astype(int).unique().tolist()
            )
            if not comp_group_idxs:
                continue
            mol_group_ranges[int(comp_idx)] = (comp_group_idxs[0], comp_group_idxs[-1])

        extra_groups_before = {}   # mol_idx -> (group_name, {atom_name: coords(n_s,3)})
        extra_groups_after = {}

        for mol_idx, (first_g, last_g) in mol_group_ranges.items():

            if N_terminal is not None:
                tmpl_ace = load_residue_template(N_terminal)
                if tmpl_ace is not None:
                    # Get N, CA, C of the first residue
                    first_g_mask = topo.atoms['group_index'] == first_g
                    first_g_rows = topo.atoms[first_g_mask]
                    def _get_pos(atom_name_lookup):
                        rows = first_g_rows[first_g_rows['atom_name'] == atom_name_lookup]
                        if len(rows) == 0:
                            return None
                        idx = rows.index[0]
                        return all_coords[:, int(idx), :]   # (n_structures, 3)

                    N_pos  = _get_pos('N')
                    CA_pos = _get_pos('CA')
                    C_pos  = _get_pos('C')
                    if N_pos is not None and CA_pos is not None and C_pos is not None:
                        ace_atoms = place_ace_group(N_pos, CA_pos, C_pos, tmpl_ace, n_structures)
                        extra_groups_before[mol_idx] = (N_terminal, ace_atoms)

            if C_terminal is not None:
                tmpl_nme = load_residue_template(C_terminal)
                if tmpl_nme is not None:
                    # Get C, CA, N of the last residue
                    last_g_mask = topo.atoms['group_index'] == last_g
                    last_g_rows = topo.atoms[last_g_mask]
                    def _get_pos_last(atom_name_lookup):
                        rows = last_g_rows[last_g_rows['atom_name'] == atom_name_lookup]
                        if len(rows) == 0:
                            return None
                        idx = rows.index[0]
                        return all_coords[:, int(idx), :]
                    C_pos_last  = _get_pos_last('C')
                    CA_pos_last = _get_pos_last('CA')
                    N_pos_last  = _get_pos_last('N')
                    if C_pos_last is not None and CA_pos_last is not None and N_pos_last is not None:
                        nme_atoms = place_nme_group(
                            C_pos_last, CA_pos_last, N_pos_last, tmpl_nme, n_structures
                        )
                        extra_groups_after[mol_idx] = (C_terminal, nme_atoms)

        native_out = rebuild_molsys_with_new_groups(
            native_ms, mol_group_ranges, extra_groups_before, extra_groups_after,
        )
        output_molecular_system = convert(native_out, to_form=form_in, skip_digestion=True) \
            if form_in != 'molsysmt.MolSys' else native_out

        return output_molecular_system

    else:

        raise NotImplementedError


