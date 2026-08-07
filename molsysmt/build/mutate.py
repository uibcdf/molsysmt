from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentChoiceError, StructuralInconsistencyError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def mutate(molecular_system, mutations=None, keys='group_index', selection="all", syntax='MolSysMT', engine='MolSysMT'):
    """
    Apply point mutations to one or more residues of a molecular system.

    This function replaces specified residues with different amino acids, rebuilds
    missing heavy atoms, and optionally re-adds hydrogens. The mutated structure is
    returned in the same form as the input.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.

    mutations : list of str, or dict, or None, default None
        Mutations to apply. Accepted formats depend on the ``keys`` parameter:

        - **list of str**: Each string must follow the pattern
          ``"<from_name>-<group_id>-<to_name>"`` (e.g. ``"ALA-42-GLY"``).
        - **dict with** ``keys='group_index'``: Maps group indices (int) to target
          residue names (str).
        - **dict with** ``keys='group_id'``: Maps group IDs (int or str) to target
          residue names (str). Raises an error if the ID is ambiguous.
        - **dict with** ``keys='group_name'``: Maps source residue names (str) to
          target residue names (str); all matching residues within ``selection``
          are mutated.

    keys : {'group_index', 'group_id', 'group_name'}, default 'group_index'
        Interpretation of the keys in a dict-style ``mutations`` argument.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection used as a mask when resolving group identifiers.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    engine : {'MolSysMT', 'PDBFixer'}, default 'MolSysMT'
        Backend used to apply mutations.

        * **PDBFixer** — removes the old sidechain and rebuilds it via
          template-based Kabsch alignment followed by force-field energy
          minimisation (Langevin + LocalEnergyMinimizer).  Requires OpenMM
          and PDBFixer.
        * **MolSysMT** — removes the old sidechain, keeps backbone atoms
          (N, CA, C, O, OXT), and places the new sidechain by Kabsch
          alignment against a JSON residue template.  No energy minimisation
          is performed; it is strongly recommended to minimise the structure
          afterwards to resolve any steric clashes.

    Returns
    -------
    molecular system
        A new molecular system with the requested mutations applied, missing heavy
        atoms rebuilt, and hydrogens re-added if the original system contained them.
        Returned in the same form as the input.

    Raises
    ------
    ArgumentChoiceError
        Raised when a mutation string specifies a source residue name that does not
        match the actual residue at the given group ID.

    StructuralInconsistencyError
        Raised when a group ID maps to more than one residue in the system.

    NotImplementedMethodError
        Raised if the requested ``engine`` is not supported.

    Notes
    -----
    All target residue names are converted to uppercase before being passed to the
    engine. After applying mutations the engine calls ``findMissingResidues``,
    ``findMissingAtoms``, and ``addMissingAtoms`` to produce a chemically complete
    structure. If the original system contained hydrogen atoms, ``addMissingHydrogens``
    is called at pH 7.4.

    .. versionadded:: 1.0.0
    """

    if engine=="PDBFixer":

        from molsysmt.basic import get, convert, get_form, contains, select

        if isinstance(mutations, (tuple, list)):

            group_indices = []
            to_group_names = []

            for mutation_string in mutations:
                old_group_name, group_id, new_group_name = mutation_string.split('-')
                group_id = str(group_id)
                aux_index, group_name = get(molecular_system, element='group',
                        selection=f'group_id=="{group_id}"', mask=selection,
                        group_index=True, group_name=True)
                if group_name[0].lower()!=old_group_name.lower():
                    raise ArgumentChoiceError(
                        argument="mutations",
                        value=old_group_name,
                        choices=[group_name[0]],
                        caller="molsysmt.build.mutate",
                        message=f"The group with id {group_id} is {group_name[0]} and not {old_group_name}."
                    )
                group_indices.append(aux_index[0])
                to_group_names.append(new_group_name)


        elif isinstance(mutations, dict):
            if keys=='group_index':
                group_indices = list(mutations.keys())
                to_group_names = list(mutations.values())
            elif keys=='group_id':
                group_ids = [str(ii) for ii in mutations.keys()]
                to_group_names = list(mutations.values())
                group_indices = []
                for ii in group_ids:
                    aux_indices = get(molecular_system, element='group',
                            selection=f'group_id=="{ii}"', mask=selection,
                            group_index=True)
                    if len(aux_indices)>1:
                        raise StructuralInconsistencyError(
                            reason=f"There are multiple groups with the group_id: {ii}",
                            caller="molsysmt.build.mutate"
                        )
                    else:
                        group_indices.append(aux_indices[0])
            elif keys=='group_name':
                group_indices = []
                to_group_names = []
                for from_name, to_name in mutations.items():
                    aux_indices = get(molecular_system, element='group',
                            selection='group_name==@from_name', mask=selection, group_index=True)
                    for aux_index in aux_indices:
                        group_indices.append(aux_index)
                        to_group_names.append(to_name)

        to_group_names = [name.upper() for name in to_group_names]

        form_in = get_form(molecular_system)
        tmp_molecular_system = convert(molecular_system, to_form="pdbfixer.PDBFixer")

        from_group_names, group_ids, in_chain_ids = get(tmp_molecular_system, element='group',
                                                        selection=group_indices, group_name=True, group_id=True,
                                                        chain_id=True)

        for group_id, from_group_name, to_group_name, in_chain_id in zip(group_ids, from_group_names, to_group_names, in_chain_ids):
            mutation_string = "-".join([from_group_name,str(group_id),to_group_name])
            tmp_molecular_system.applyMutations([mutation_string], in_chain_id)

        tmp_molecular_system.findMissingResidues()
        tmp_molecular_system.findMissingAtoms()
        tmp_molecular_system.addMissingAtoms()

        if contains(tmp_molecular_system, selection='atom_type=="H"'):
            tmp_molecular_system.addMissingHydrogens(7.4)

        tmp_molecular_system = convert(tmp_molecular_system, to_form=form_in)

        return tmp_molecular_system

    elif engine == 'MolSysMT':

        from molsysmt.basic import get, convert, get_form, contains
        from molsysmt.basic import remove as msm_remove
        from molsysmt.build.add_missing_heavy_atoms import add_missing_heavy_atoms
        from molsysmt.build.add_missing_hydrogens import add_missing_hydrogens

        # Backbone heavy atoms that are kept across any amino-acid mutation.
        # OXT is retained when present (C-terminal residues).
        _BACKBONE_HEAVY = frozenset({'N', 'CA', 'C', 'O', 'OXT'})

        # ── parse mutations ──────────────────────────────────────────────────
        if isinstance(mutations, (tuple, list)):
            group_indices  = []
            to_group_names = []
            for mutation_string in mutations:
                old_group_name, group_id, new_group_name = mutation_string.split('-')
                group_id = str(group_id)
                aux_index, group_name = get(molecular_system, element='group',
                        selection=f'group_id=="{group_id}"', mask=selection,
                        group_index=True, group_name=True)
                if group_name[0].lower() != old_group_name.lower():
                    raise ArgumentChoiceError(
                        argument='mutations', value=old_group_name,
                        choices=[group_name[0]], caller='molsysmt.build.mutate',
                        message=f"Group with id {group_id} is {group_name[0]}, not {old_group_name}."
                    )
                group_indices.append(aux_index[0])
                to_group_names.append(new_group_name)

        elif isinstance(mutations, dict):
            if keys == 'group_index':
                group_indices  = list(mutations.keys())
                to_group_names = list(mutations.values())
            elif keys == 'group_id':
                group_ids = [str(ii) for ii in mutations.keys()]
                to_group_names = list(mutations.values())
                group_indices = []
                for ii in group_ids:
                    aux_indices = get(molecular_system, element='group',
                            selection=f'group_id=="{ii}"', mask=selection,
                            group_index=True)
                    if len(aux_indices) > 1:
                        raise StructuralInconsistencyError(
                            reason=f"Multiple groups with group_id: {ii}",
                            caller='molsysmt.build.mutate'
                        )
                    group_indices.append(aux_indices[0])
            elif keys == 'group_name':
                group_indices  = []
                to_group_names = []
                for from_name, to_name in mutations.items():
                    aux_indices = get(molecular_system, element='group',
                            selection='group_name==@from_name', mask=selection,
                            group_index=True)
                    for aux_index in aux_indices:
                        group_indices.append(aux_index)
                        to_group_names.append(to_name)

        to_group_names = [name.upper() for name in to_group_names]

        # ── convert to native form ───────────────────────────────────────────
        form_in      = get_form(molecular_system)
        had_h        = contains(molecular_system, selection='atom_type=="H"')
        tmp          = convert(molecular_system, to_form='molsysmt.MolSys', skip_digestion=True)

        # ── 1. Rename groups ─────────────────────────────────────────────────
        for group_index, new_name in zip(group_indices, to_group_names):
            tmp.topology.groups.at[group_index, 'group_name'] = new_name
            tmp.topology.groups.at[group_index, 'group_type'] = 'amino acid'
        tmp.topology._groups_dirty = True

        # ── 2. Strip non-backbone atoms from every mutated group ─────────────
        atoms_to_remove = []
        for group_index in group_indices:
            atoms_in_group = tmp.topology.atoms[
                tmp.topology.atoms['group_index'] == group_index
            ]
            non_backbone = atoms_in_group.index[
                ~atoms_in_group['atom_name'].isin(_BACKBONE_HEAVY)
            ].tolist()
            atoms_to_remove.extend(non_backbone)

        if atoms_to_remove:
            tmp = msm_remove(tmp, selection=atoms_to_remove, skip_digestion=True)

        # ── 3. Rebuild sidechain heavy atoms (Kabsch alignment on backbone) ──
        tmp = add_missing_heavy_atoms(tmp, engine='MolSysMT')

        # ── 4. Re-add hydrogens if original system had them ──────────────────
        if had_h:
            tmp = add_missing_hydrogens(tmp, engine='MolSysMT')

        return convert(tmp, to_form=form_in, skip_digestion=True)

    else:
        raise NotImplementedMethodError
