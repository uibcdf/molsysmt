from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest()
def add_missing_heavy_atoms(
    molecular_system,
    selection="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    skip_digestion=False,
):
    """
    Adding missing non-hydrogen atoms to a molecular system.

    This function checks for missing heavy atoms (non-hydrogens) in a molecular system and adds
    them when possible. The missing atoms are identified based on known residue templates and
    inferred topological context. The coordinates of new atoms are estimated using internal
    geometry rules or external reconstruction engines such as PDBFixer.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : object, default='MolSysMT'
        Argument engine.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
    The native engine repairs standard residues and selected incomplete MSE and SEP
    residues from exact chemical templates. MSE and SEP are matched by atom name,
    element, and connectivity; missing atoms are placed from local coordinates.
    Residues with ambiguous side-chain gaps or conflicting chemistry are left
    unchanged with an ``UnassessedResidueWarning``. Modified residues without
    curated templates are also reported as unassessed. Hydrogen atoms require a
    separate operation. Coordinate placement is an estimate and does not replace
    experimental refinement.

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
    >>> molsys = msm.remove(molsys, selection='atom_name=="CB"')
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

    from molsysmt.basic import convert, get, get_form, select, set

    output_molecular_system = None
    form_in = get_form(molecular_system)
    form_out = form_in

    if engine == "PDBFixer":
        temp_molecular_system = convert(
            molecular_system,
            to_form="pdbfixer.PDBFixer",
            pdb_chain_id="chain_id",
            skip_digestion=True,
        )

        atts_from_components = get(
            molecular_system,
            element="component",
            component_name=True,
            output_type="dictionary",
            skip_digestion=True,
        )
        atts_from_molecules = get(
            molecular_system,
            element="molecule",
            molecule_name=True,
            output_type="dictionary",
            skip_digestion=True,
        )
        atts_from_chains = get(
            molecular_system,
            element="chain",
            chain_id=True,
            chain_name=True,
            output_type="dictionary",
            skip_digestion=True,
        )
        atts_from_entities = get(
            molecular_system,
            element="entity",
            entity_name=True,
            output_type="dictionary",
            skip_digestion=True,
        )

        temp_molecular_system.findMissingResidues()
        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.missingTerminals = {}

        group_indices_in_selection = select(
            molecular_system,
            element="group",
            selection=selection,
            syntax=syntax,
            skip_digestion=True,
        )

        aux_dict = {}

        for group, atoms in temp_molecular_system.missingAtoms.items():
            if group.index in group_indices_in_selection:
                aux_dict[group] = []
                for atom in atoms:
                    aux_dict[group].append(atom)

        temp_molecular_system.missingAtoms = aux_dict

        temp_molecular_system.addMissingAtoms()

        output_molecular_system = convert(
            temp_molecular_system, to_form=form_out, skip_digestion=True
        )

        # Adding atoms can merge previously isolated fragments, changing n_components/n_molecules.
        # Only restore metadata at each level if the count is unchanged.
        n_comp_out = get(
            output_molecular_system,
            element="component",
            n_components=True,
            skip_digestion=True,
        )
        if n_comp_out == len(next(iter(atts_from_components.values()))):
            set(
                output_molecular_system,
                element="component",
                **atts_from_components,
                skip_digestion=True,
            )

        n_mol_out = get(
            output_molecular_system,
            element="molecule",
            n_molecules=True,
            skip_digestion=True,
        )
        if n_mol_out == len(next(iter(atts_from_molecules.values()))):
            set(
                output_molecular_system,
                element="molecule",
                **atts_from_molecules,
                skip_digestion=True,
            )

        n_chain_out = get(
            output_molecular_system, element="chain", n_chains=True, skip_digestion=True
        )
        if n_chain_out == len(next(iter(atts_from_chains.values()))):
            set(
                output_molecular_system,
                element="chain",
                **atts_from_chains,
                skip_digestion=True,
            )

        n_ent_out = get(
            output_molecular_system,
            element="entity",
            n_entities=True,
            skip_digestion=True,
        )
        if n_ent_out == len(next(iter(atts_from_entities.values()))):
            set(
                output_molecular_system,
                element="entity",
                **atts_from_entities,
                skip_digestion=True,
            )

        del (group_indices_in_selection, temp_molecular_system)
        del (
            atts_from_components,
            atts_from_molecules,
            atts_from_chains,
            atts_from_entities,
        )

    elif engine == "MolSysMT":
        from warnings import warn

        import numpy as np

        from molsysmt import pyunitwizard as puw
        from molsysmt._private.residue_templates import CURATED_MODIFIED_RESIDUES
        from molsysmt._private.smonitor import UnassessedResidueWarning
        from molsysmt.basic import convert, get_form, select
        from molsysmt.build._modified_residue_repair import assess_modified_residue
        from molsysmt.build._native_placers import (
            append_atoms_to_molsys,
            load_residue_template,
            place_missing_in_group,
        )
        from molsysmt.build.get_missing_heavy_atoms import get_missing_heavy_atoms

        # Work in native form
        if form_in != "molsysmt.MolSys":
            native_ms = convert(
                molecular_system, to_form="molsysmt.MolSys", skip_digestion=True
            )
        else:
            native_ms = molecular_system

        topo = native_ms.topology
        selected_groups = select(
            native_ms, element="group", selection=selection, syntax=syntax
        )
        from molsysmt.element.group.amino_acid import get_standard_name
        from molsysmt.element.group.amino_acid.group_names import group_names

        for group_idx in selected_groups:
            group_name = topo.groups.at[int(group_idx), "group_name"]
            if (
                group_name not in CURATED_MODIFIED_RESIDUES
                and group_name not in group_names
                and get_standard_name(group_name) is not None
            ):
                warn(
                    UnassessedResidueWarning(
                        group_name=group_name,
                        group_index=int(group_idx),
                        reason="no exact curated repair template",
                    ),
                    stacklevel=2,
                )

        missing_atoms = get_missing_heavy_atoms(
            native_ms,
            selection=selection,
            syntax=syntax,
            engine="MolSysMT",
        )

        for group_idx in selected_groups:
            group_idx = int(group_idx)
            group_name = topo.groups.at[group_idx, "group_name"]
            if group_name not in CURATED_MODIFIED_RESIDUES or group_idx in missing_atoms:
                continue
            _, reason = assess_modified_residue(
                topo, group_idx, [], load_residue_template(group_name), None
            )
            if reason:
                warn(
                    UnassessedResidueWarning(
                        group_name=group_name,
                        group_index=group_idx,
                        reason=reason,
                    ),
                    stacklevel=2,
                )

        if not missing_atoms:
            output_molecular_system = (
                native_ms.copy() if form_in == "molsysmt.MolSys" else molecular_system
            )
            return (
                convert(output_molecular_system, to_form=form_out, skip_digestion=True)
                if form_in != form_out
                else output_molecular_system
            )

        all_coords = puw.get_value(native_ms.structures.coordinates, to_unit="nm")

        new_atom_info = []  # list of (group_idx, atom_name, coords(n_structures, 3))
        new_bonds_info = []  # list of (abs_idx1, abs_idx2) — resolved after atom list is built

        # Track new atom indices by (group_idx, atom_name) for bond resolution
        new_atom_index_map = {}  # (group_idx, atom_name) -> new_atom_idx
        n_orig = topo.n_atoms

        for group_idx, missing_names in missing_atoms.items():
            group_name = topo.groups["group_name"].values[group_idx]
            template = load_residue_template(group_name)
            if template is None:
                if get_standard_name(group_name) is not None:
                    warn(
                        UnassessedResidueWarning(
                            group_name=group_name,
                            group_index=group_idx,
                            reason="no exact native placement template",
                        ),
                        stacklevel=2,
                    )
                continue

            curated = group_name in CURATED_MODIFIED_RESIDUES
            if curated:
                if len(topo._chemical_states) != 1:
                    reason = "multiple chemical states cannot be preserved by this repair"
                    anchors = None
                else:
                    anchors, reason = assess_modified_residue(
                        topo, group_idx, missing_names, template, all_coords
                    )
                if reason:
                    warn(
                        UnassessedResidueWarning(
                            group_name=group_name,
                            group_index=group_idx,
                            reason=reason,
                        ),
                        stacklevel=2,
                    )
                    continue

            placed = {}
            for atom_name in missing_names:
                placed.update(
                    place_missing_in_group(
                        topo,
                        all_coords,
                        group_idx,
                        [atom_name],
                        template,
                        anchor_names=anchors[atom_name] if curated else None,
                    )
                )
            if not placed:
                continue

            if curated:
                name_to_idx = dict(zip(template["atoms"], range(len(template["atoms"]))))
                bad_geometry = False
                for atom1, atom2 in template["bonds"]:
                    for new_name, neighbor in ((atom1, atom2), (atom2, atom1)):
                        if new_name not in placed:
                            continue
                        existing_rows = topo.atoms[
                            (topo.atoms["group_index"] == group_idx)
                            & (topo.atoms["atom_name"] == neighbor)
                        ]
                        if existing_rows.empty:
                            continue
                        ideal = np.linalg.norm(
                            np.asarray(template["coords_nm"])[name_to_idx[new_name]]
                            - np.asarray(template["coords_nm"])[name_to_idx[neighbor]]
                        )
                        actual = np.linalg.norm(
                            placed[new_name] - all_coords[:, existing_rows.index[0], :],
                            axis=1,
                        )
                        if np.any(np.abs(actual - ideal) > 0.04):
                            bad_geometry = True
                if bad_geometry:
                    warn(
                        UnassessedResidueWarning(
                            group_name=group_name,
                            group_index=group_idx,
                            reason="placed bond geometry conflicts with observed coordinates",
                        ),
                        stacklevel=2,
                    )
                    continue

            for atom_name in missing_names:
                if atom_name not in placed:
                    continue
                new_idx = n_orig + len(new_atom_info)
                new_atom_index_map[(group_idx, atom_name)] = new_idx
                if curated:
                    element = template["elements"][template["atoms"].index(atom_name)]
                    new_atom_info.append((group_idx, atom_name, placed[atom_name], element))
                else:
                    new_atom_info.append((group_idx, atom_name, placed[atom_name]))

        # Resolve bonds: add template bonds that involve at least one new atom
        new_atom_name_by_group = {}
        for (gidx, aname), nidx in new_atom_index_map.items():
            new_atom_name_by_group.setdefault(gidx, {})[aname] = nidx

        for group_idx, name_to_new_idx in new_atom_name_by_group.items():
            group_name = topo.groups.loc[group_idx, "group_name"]
            template = load_residue_template(group_name)
            if template is None:
                continue

            # Build name → atom_idx for existing atoms of this group
            gmask = topo.atoms["group_index"] == group_idx
            exist_rows = topo.atoms[gmask]
            existing_name_to_idx = dict(
                zip(exist_rows["atom_name"], exist_rows.index.tolist())
            )
            # Merge with new atoms
            all_name_to_idx = {**existing_name_to_idx, **name_to_new_idx}

            curated = group_name in CURATED_MODIFIED_RESIDUES
            existing_pairs = {
                frozenset((int(row.atom1_index), int(row.atom2_index)))
                for row in topo._get_chemical_state_bonds().itertuples()
            }
            for bond_number, (b1, b2) in enumerate(template["bonds"]):
                if not curated and b1 not in name_to_new_idx and b2 not in name_to_new_idx:
                    continue  # bond between two existing atoms (already in topology)
                if b1 not in all_name_to_idx or b2 not in all_name_to_idx:
                    continue
                i1, i2 = all_name_to_idx[b1], all_name_to_idx[b2]
                if frozenset((i1, i2)) in existing_pairs:
                    continue
                if curated:
                    new_bonds_info.append((i1, i2, template["bond_orders"][bond_number]))
                else:
                    new_bonds_info.append((i1, i2))

        if not new_atom_info:
            output_molecular_system = (
                native_ms.copy() if form_in == "molsysmt.MolSys" else molecular_system
            )
            return (
                convert(output_molecular_system, to_form=form_out, skip_digestion=True)
                if form_in != form_out
                else output_molecular_system
            )

        native_out = append_atoms_to_molsys(native_ms, new_atom_info, new_bonds_info)
        output_molecular_system = (
            convert(native_out, to_form=form_out, skip_digestion=True)
            if form_in != "molsysmt.MolSys"
            else native_out
        )

    else:
        raise NotImplementedMethodError

    return output_molecular_system
