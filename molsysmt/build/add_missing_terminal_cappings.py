from molsysmt._private.argdigest import arg_digest


@arg_digest()
def add_missing_terminal_cappings(
    molecular_system,
    N_terminal=None,
    C_terminal=None,
    pH=7.4,
    keep_ids=False,
    selection="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    skip_digestion=False,
    *,
    attribute_policy="intersection",
    return_report=False,
):
    """
    Adding terminal cappings to peptides and proteins.

    This function adds chemical groups to the N- and/or C-termini of protein or peptide chains.
    These terminal groups can either neutralize terminal charges or simply complete missing atoms
    for a standard terminal residue. The resulting cappings are consistent with typical protonation
    states at the specified pH.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    N_terminal : str or None, default=None
        N-terminal cap to add. The native engine supports exactly 'ACE'
        (acetyl), or None to complete the existing uncapped terminus.
    C_terminal : str or None, default=None
        C-terminal cap to add. The native engine supports exactly 'NME'
        (N-methylamide), or None to complete the existing uncapped terminus.
        Primary-amide labels 'NH2' and 'NHE' are not supported by this tool's
        native reconstruction route.
    pH : float, default=7.4
        pH used for terminal hydrogen completion. Native completion uses a
        fixed amine threshold of 9.6; it does not assign a full chemical state.
    keep_ids : bool, default=False
        Whether to retain existing element ID labels during reconstruction.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection: a query string, 0-based atom indices, or a full
        Boolean mask on the source atom axis. Numeric selections have this same
        meaning for every syntax. Selecting any atom enables its whole group for
        native local completion. Requested ACE/NME caps apply to the complete
        peptide/protein covalent components touched by the selection; selecting
        an internal group does not turn that group into a chemical terminus.
        An empty selection with supported arguments returns an independent
        unchanged copy.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : {'MolSysMT', 'PDBFixer'}, default='MolSysMT'
        Reconstruction engine. Cap availability is engine-specific; PDBFixer
        requests follow its own reconstruction rules.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    attribute_policy : {'intersection', 'strict'}, default='intersection'
        Native atom-expansion policy. Intersection drops unsupported structural
        fields and force-field atom parameters with diagnostics; strict rejects
        those losses before publishing a result. PDBFixer supports intersection.
    return_report : bool, default=False
        Return a native molecular_system/report dictionary with exact int64
        source/output maps, generated atoms, introduced bonds, stage-local
        placement evidence and attribute losses. Available for MolSysMT only.

    Returns
    -------
    molecular system or dict
        By default, a new system in the input form. With return_report=True,
        a dictionary containing native MolSys and its detached
        molsysmt.terminal_completion@1 report, even for another input form.


    Raises
    ------
    NotSupportedFormError
        Raised if the input molecular system is in a non-supported form.

    ArgumentError
        Raised if an input argument value is invalid.

    StructuralInconsistencyError
        If native expansion/reporting cannot resolve one chemical state, or
        strict policy would lose structural attributes or atom parameters.

    NotImplementedMethodError
        If a native cap request is unsupported or supplied on the wrong end,
        including for an empty selection; or if an external engine is requested
        with an exact report or strict policy.


    Notes
    -----
    Common capping groups:
      - `'ACE'` for acetyl (N-terminal)
      - `'NME'` for N-methyl amide (C-terminal)

    The native profile is role-specific and case-sensitive. Unsupported cap
    requests raise before selection, copying or reconstruction, even when
    digestion is skipped. A primary carboxamide is chemically different from
    NME and is never substituted automatically. Other tools may recognize or
    construct additional cap labels; that does not extend this placement route.

    If no capping residues are provided, the function only completes missing terminal atoms
    in the native residues (which are often charged).

    The native engine delegates nonterminal heavy-atom repair to its bounded
    placement tool. Unsupported side-chain gaps remain missing with
    ``UnassessedResidueWarning``, even if terminal completion succeeds. Inspect
    ``get_missing_heavy_atoms`` as well as ``get_missing_terminal_cappings``.
    PDBFixer can choose additional reconstructions, so whole-system atom counts
    need not match between engines.

    Selection is resolved before atom insertion. Local heavy-atom completion,
    missing OXT and terminal N-bound hydrogens are restricted to selected source
    groups; terminal detection uses the complete system context. Explicit caps
    operate on selected covalent components. Ambiguous chain backbones contribute
    no inferred ends and emit UnassessedPeptideBackboneWarning; local completion
    of other assessed chains remains available. Explicit caps require a single
    unambiguous linear backbone per selected component. Group indices remain stable during
    local atom insertion, and component populations are resolved again from those
    groups after repair. The source is not modified.

    Native atom expansion requires one selected chemical state. Existing atom
    assignments, state identity/provenance and observed coordinates survive.
    Added chemical fields remain unknown and connectivity is partial; capping
    geometry does not assign a complete chemical state. Existing atom IDs are
    retained, but inserted groups can change indices. Named interaction analyses
    retain their definitions and remapped axes while observations and evaluated
    coverage are cleared for recalculation. Unsupported structural attributes
    and force-field atom parameters are dropped with a diagnostic. Assign and
    validate the intended terminal chemistry separately before further preparation.

    Native completion archives a terminal_completion@1 operation record in the
    returned ChemicalStates, retaining earlier history. With return_report=True,
    even an empty selection records its unchanged outcome. Exact source/output
    maps retain every original atom; inverse maps use -1 for generated atoms.
    Introduced bonds use the final output atom axis and include new-to-new
    edges. Steps retain their own local axes and placement evidence. These
    historical indices do not change after extraction or reordering. Reports
    omit coordinate arrays and do not certify a complete chemical state,
    steric quality, a rotamer or an energy minimum. The optional result always
    contains native MolSys so its maps describe the actual returned atom order.
    An unchanged multistate default copy remains supported; no state is chosen
    arbitrarily for an operation report. Select one state to request evidence.

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
    >>> molsys = msm.build.build_peptide('AlaValPro', engine='MolSysMT')
    >>> result = msm.build.add_missing_terminal_cappings(molsys,
    ...     N_terminal='ACE', C_terminal='NME', return_report=True)
    >>> result['report']['generated_atom_indices'].shape
    (12,)
    >>> molsys = result['molecular_system']
    >>> msm.convert(molsys, to_form='string:amino_acids_3')
    'AceAlaValProNme'


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Add missing terminal cappings <Tutorial_Add_missing_terminal_cappings>`

    .. versionadded:: 1.0.0
    """

    import numpy as np

    from molsysmt._private.smonitor import ArgumentError
    from molsysmt.basic import copy, get_form, select

    if engine == "MolSysMT":
        for argument, value, supported in (
            ("N_terminal", N_terminal, "ACE"),
            ("C_terminal", C_terminal, "NME"),
        ):
            if value not in (None, supported):
                from molsysmt._private.smonitor import NotImplementedMethodError

                raise NotImplementedMethodError(
                    method="native terminal cap reconstruction",
                    arguments={argument: value},
                    caller="molsysmt.build.add_missing_terminal_cappings",
                    message=(
                        "Native terminal completion supports only N_terminal=None "
                        "or 'ACE' and C_terminal=None or 'NME'; "
                        f"requested {argument}={value!r}."
                    ),
                )

    if engine != "MolSysMT" and (return_report or attribute_policy != "intersection"):
        from molsysmt._private.smonitor import NotImplementedMethodError

        raise NotImplementedMethodError(
            method="external terminal completion with exact report or strict attribute policy",
            caller="molsysmt.build.add_missing_terminal_cappings",
        )

    # Resolve the source atom population once, before any reconstruction changes
    # atom positions. Numeric/Boolean selectors do not depend on query syntax.
    if selection is None:
        raise ArgumentError(
            "selection", caller="molsysmt.build.add_missing_terminal_cappings"
        )
    if isinstance(selection, str):
        source_atoms = select(molecular_system, selection=selection, syntax=syntax)
    elif np.asarray(selection).dtype.kind == "b":
        source_atoms = select(molecular_system, mask=selection)
    else:
        source_atoms = select(molecular_system, selection=selection)
    if not source_atoms and not return_report:
        return copy(molecular_system)

    output_molecular_system = None
    form_in = get_form(molecular_system)

    if engine == "PDBFixer":
        from molsysmt.basic import convert, get, has_attribute, select, set

        conversion_extra_kwargs = {}
        if form_in in ["molsysmt.MolSys"]:
            conversion_extra_kwargs["pdb_chain_id"] = "chain_id"

        temp_molecular_system = convert(
            molecular_system,
            to_form="pdbfixer.PDBFixer",
            **conversion_extra_kwargs,
            skip_digestion=True,
        )
        atom_indices_in_selection = source_atoms
        atom_indices_in_components = get(
            temp_molecular_system,
            element="component",
            selection='component_type in ["peptide", "protein"] \
                                         and atom_index in @atom_indices_in_selection',
            atom_index=True,
            skip_digestion=True,
        )

        temp_molecular_system.findMissingResidues()

        for atom_indices_in_component in atom_indices_in_components:
            chain_index = get(
                temp_molecular_system,
                element="chain",
                selection="atom_index in @atom_indices_in_component",
                chain_index=True,
                skip_digestion=True,
            )[0]

            n_groups = get(
                temp_molecular_system,
                element="group",
                selection="atom_index in @atom_indices_in_component",
                n_groups=True,
                skip_digestion=True,
            )

            if N_terminal is not None:
                temp_molecular_system.missingResidues[(chain_index, 0)] = [N_terminal]

            if C_terminal is not None:
                temp_molecular_system.missingResidues[(chain_index, n_groups)] = [
                    C_terminal
                ]

        temp_molecular_system.findMissingAtoms()
        temp_molecular_system.addMissingAtoms()

        n_hs = get(
            temp_molecular_system,
            element="atom",
            selection='atom_type=="H"',
            n_atoms=True,
            skip_digestion=True,
        )

        # if n_hs > 0:
        #    temp_molecular_system.addMissingHydrogens(pH)

        output_molecular_system = convert(
            temp_molecular_system, to_form=form_in, skip_digestion=True
        )

        # Adding terminal groups can change n_components or n_molecules; guard each set().
        if has_attribute(molecular_system, "component_name", skip_digestion=True):
            aux_component_names = get(
                molecular_system,
                element="component",
                component_name=True,
                skip_digestion=True,
            )
            _n_comp = get(
                output_molecular_system,
                element="component",
                n_components=True,
                skip_digestion=True,
            )
            if _n_comp == len(aux_component_names):
                set(
                    output_molecular_system,
                    element="component",
                    component_name=aux_component_names,
                    skip_digestion=True,
                )
            del aux_component_names

        if has_attribute(molecular_system, "chain_name", skip_digestion=True):
            aux_chain_names = get(
                molecular_system, element="chain", chain_name=True, skip_digestion=True
            )
            _n_chain = get(
                output_molecular_system,
                element="chain",
                n_chains=True,
                skip_digestion=True,
            )
            if _n_chain == len(aux_chain_names):
                set(
                    output_molecular_system,
                    element="chain",
                    chain_name=aux_chain_names,
                    skip_digestion=True,
                )
            del aux_chain_names

        if has_attribute(molecular_system, "chain_id", skip_digestion=True):
            aux_chain_ids = get(
                molecular_system, element="chain", chain_id=True, skip_digestion=True
            )
            _n_chain = get(
                output_molecular_system,
                element="chain",
                n_chains=True,
                skip_digestion=True,
            )
            if _n_chain == len(aux_chain_ids):
                set(
                    output_molecular_system,
                    element="chain",
                    chain_id=aux_chain_ids,
                    skip_digestion=True,
                )
            del aux_chain_ids

        if has_attribute(molecular_system, "molecule_name", skip_digestion=True):
            aux_molecule_names = get(
                molecular_system,
                element="molecule",
                molecule_name=True,
                skip_digestion=True,
            )
            _n_mol = get(
                output_molecular_system,
                element="molecule",
                n_molecules=True,
                skip_digestion=True,
            )
            if _n_mol == len(aux_molecule_names):
                set(
                    output_molecular_system,
                    element="molecule",
                    molecule_name=aux_molecule_names,
                    skip_digestion=True,
                )
            del aux_molecule_names

        if has_attribute(molecular_system, "entity_name", skip_digestion=True):
            aux_entity_names = get(
                molecular_system,
                element="entity",
                entity_name=True,
                skip_digestion=True,
            )
            _n_ent = get(
                output_molecular_system,
                element="entity",
                n_entities=True,
                skip_digestion=True,
            )
            if _n_ent == len(aux_entity_names):
                set(
                    output_molecular_system,
                    element="entity",
                    entity_name=aux_entity_names,
                    skip_digestion=True,
                )
            del aux_entity_names

        if n_hs > 0:
            from molsysmt.build import add_missing_hydrogens

            output_molecular_system = add_missing_hydrogens(
                output_molecular_system, pH=pH, skip_digestion=True
            )

        if keep_ids:
            raise NotImplementedError

        return output_molecular_system

    elif engine == "MolSysMT":
        from molsysmt import pyunitwizard as puw
        from molsysmt.basic import convert, get, select
        from molsysmt.build._native_placers import (
            append_atoms_to_molsys,
            load_residue_template,
            place_ace_group,
            place_nme_group,
            rebuild_molsys_with_new_groups,
        )
        from molsysmt.build.add_missing_heavy_atoms import add_missing_heavy_atoms

        if form_in != "molsysmt.MolSys":
            native_ms = convert(
                molecular_system, to_form="molsysmt.MolSys", skip_digestion=True
            )
        else:
            native_ms = molecular_system

        from molsysmt._private.reconstruction import Reconstruction, template_evidence

        reconstruction = Reconstruction(native_ms)
        trace_supported = (
            native_ms.chemical_states is not None
            and native_ms.chemical_states.n_chemical_states == 1
        )
        if return_report and not trace_supported:
            from molsysmt._private.smonitor import StructuralInconsistencyError

            raise StructuralInconsistencyError(
                reason="Reconstruction evidence requires exactly one chemical state.",
                caller="molsysmt.build.add_missing_terminal_cappings",
            )
        parameters = dict(
            N_terminal=N_terminal,
            C_terminal=C_terminal,
            pH=pH,
            keep_ids=keep_ids,
            attribute_policy=attribute_policy,
            selection_syntax=syntax,
        )

        # Atom insertion preserves the group axis while sorting the expanded
        # atom table. Carry groups, never stale atom positions, through this stage.
        selected_groups = np.unique(
            native_ms.topology.atoms.loc[source_atoms, "group_index"].astype(int)
        ).tolist()
        group_selection = f"group_index in {selected_groups}"

        def native_result(output):
            if trace_supported:
                result = reconstruction.finish(
                    output,
                    "molsysmt.terminal_completion@1",
                    parameters,
                    source_atoms,
                    selected_groups,
                )
                if return_report:
                    return result
            return (
                convert(output, to_form=form_in, skip_digestion=True)
                if form_in != "molsysmt.MolSys"
                else output
            )

        if not source_atoms:
            return native_result(native_ms.copy())

        # --- Case A: complete missing atoms in native terminal residues ---
        # Step A1: add missing sidechain/backbone heavy atoms (OXT excluded there).
        heavy_result = add_missing_heavy_atoms(
            native_ms,
            selection=selected_groups,
            syntax="MolSysMT",
            engine="MolSysMT",
            attribute_policy=attribute_policy,
            return_report=trace_supported,
        )
        if trace_supported:
            native_ms = heavy_result["molecular_system"]
            reconstruction.add(heavy_result["report"], "native_heavy_atom_completion")
        else:
            native_ms = heavy_result

        # Step A2: add OXT where get_missing_terminal_cappings reports it missing.
        # Skip when C_terminal is not None: the C-terminus will be capped by a new
        # group (NME), so OXT must not be inserted first.
        from molsysmt.build.get_missing_terminal_cappings import (
            get_missing_terminal_cappings,
        )

        missing_oxt = (
            get_missing_terminal_cappings(
                native_ms,
                selection=selected_groups,
                syntax="MolSysMT",
                engine="MolSysMT",
            )
            if C_terminal is None
            else {}
        )
        if missing_oxt:
            from molsysmt.build._native_placers import (
                append_atoms_to_molsys,
                place_oxt_atom,
            )

            topo_a = native_ms.topology
            coords_a = puw.get_value(native_ms.structures.coordinates, to_unit="nm")
            n_structures_a = coords_a.shape[0]
            new_atom_info_a = []
            new_bonds_info_a = []
            oxt_evidence = []
            n_orig_a = topo_a.n_atoms

            for group_idx, oxt_list in missing_oxt.items():
                if "OXT" not in oxt_list:
                    continue
                gmask = topo_a.atoms["group_index"] == group_idx
                grow = topo_a.atoms[gmask]

                def _pos(aname, grow=grow):
                    r = grow[grow["atom_name"] == aname]
                    return coords_a[:, r.index[0], :] if len(r) else None

                C_pos = _pos("C")
                CA_pos = _pos("CA")
                O_pos = _pos("O")
                if C_pos is None or CA_pos is None or O_pos is None:
                    reconstruction.unassessed.append(
                        dict(
                            group_index=int(group_idx),
                            reason="OXT requires observed C, CA and O anchors",
                        )
                    )
                    continue
                oxt_coords = place_oxt_atom(C_pos, CA_pos, O_pos, n_structures_a)
                oxt_idx = n_orig_a + len(new_atom_info_a)
                new_atom_info_a.append((group_idx, "OXT", oxt_coords))
                # OXT is bonded to C
                C_idx_in_topo = grow[grow["atom_name"] == "C"].index[0]
                new_bonds_info_a.append((int(C_idx_in_topo), oxt_idx))
                oxt_evidence.append(
                    dict(
                        group_index=int(group_idx),
                        anchor_atom_indices=[
                            int(grow[grow["atom_name"] == name].index[0])
                            for name in ("C", "CA", "O")
                        ],
                    )
                )

            if new_atom_info_a:
                native_ms, step = append_atoms_to_molsys(
                    native_ms,
                    new_atom_info_a,
                    new_bonds_info_a,
                    attribute_policy=attribute_policy,
                    return_report=True,
                )
                reconstruction.add(
                    step, "carboxylate_axis_reflection", evidence=oxt_evidence
                )

        # Step A3: add H2, H3 at N-terminus if missing (free NH3+ / NH2).
        # Only when N_terminal is None (no ACE will be prepended).
        if N_terminal is None:
            from molsysmt.build._native_placers import (
                h_bond_length,
                place_hydrogens_on_parent,
            )

            topo_n = native_ms.topology
            coords_n = puw.get_value(native_ms.structures.coordinates, to_unit="nm")
            n_structures_n = coords_n.shape[0]
            new_atom_info_n = []
            new_bonds_info_n = []
            hydrogen_evidence = []

            from molsysmt.chemical_states import get_peptide_termini

            termini = get_peptide_termini(
                native_ms, selection=group_selection, on_ambiguous="report"
            )
            reconstruction.unassessed.extend(
                dict(
                    chain_index=int(row["chain_index"]),
                    reason=row.get("reason", "ambiguous backbone"),
                )
                for row in termini["chains"]
                if row["status"] == "unassessed"
            )
            if C_terminal is not None:
                from molsysmt.chemical_states._peptide_termini import warn_unassessed

                warn_unassessed(termini)
            for nterm_group_idx in termini["n_terminal_group_indices"]:
                gmask = topo_n.atoms["group_index"] == nterm_group_idx
                grow = topo_n.atoms[gmask]
                existing_names = frozenset(grow["atom_name"].tolist())
                # The amine's pKa is around 9.6: NH3+ below it, neutral NH2 above. `pH`
                # is already accepted here and documented as governing protonation
                # states; this step was the one place that never consulted it, so the
                # terminus came out charged at every pH (uibcdf/molsysmt#176).
                expected_h = ["H2", "H3"] if pH < 9.6 else ["H2"]
                missing_h = [h for h in expected_h if h not in existing_names]
                if not missing_h:
                    continue

                def _pos_n(aname, grow=grow):
                    r = grow[grow["atom_name"] == aname]
                    return coords_n[:, r.index[0], :] if len(r) else None

                N_p = _pos_n("N")
                H_p = _pos_n("H")
                CA_p = _pos_n("CA")
                if N_p is None or H_p is None or CA_p is None:
                    reconstruction.unassessed.append(
                        dict(
                            group_index=int(nterm_group_idx),
                            reason="terminal H placement requires observed N, H and CA anchors",
                        )
                    )
                    continue

                n_total_so_far = topo_n.n_atoms + len(new_atom_info_n)
                h_arrays = place_hydrogens_on_parent(
                    N_p, [H_p, CA_p], 2, "sp3", h_bond_length("N"), n_structures_n
                )
                N_idx_in_topo = grow[grow["atom_name"] == "N"].index[0]
                for k, h_name in enumerate(missing_h):
                    h_coord = h_arrays[k]
                    new_atom_info_n.append((nterm_group_idx, h_name, h_coord))
                    new_bonds_info_n.append((int(N_idx_in_topo), n_total_so_far + k))
                hydrogen_evidence.append(
                    dict(
                        group_index=int(nterm_group_idx),
                        anchor_atom_indices=[
                            int(grow[grow["atom_name"] == name].index[0])
                            for name in ("N", "H", "CA")
                        ],
                        hybridization="sp3",
                        bond_length_nm=h_bond_length("N"),
                        pH_charge_threshold=9.6,
                        generated_atom_names=missing_h,
                    )
                )

            if new_atom_info_n:
                native_ms, step = append_atoms_to_molsys(
                    native_ms,
                    new_atom_info_n,
                    new_bonds_info_n,
                    attribute_policy=attribute_policy,
                    return_report=True,
                )
                reconstruction.add(
                    step,
                    "local_sp3_terminal_hydrogen_placement",
                    evidence=hydrogen_evidence,
                )

        # If no capping groups requested, we're done
        if N_terminal is None and C_terminal is None:
            return native_result(native_ms)

        # --- Case B: insert ACE and/or NME as new groups ---

        # Rebuild component indices from bonds so component_type is guaranteed correct
        # regardless of the origin of the input system.
        # native_ms is always a fresh object at this point (returned by add_missing_heavy_atoms).
        native_ms.rebuild_components(
            redefine_indices=True,
            redefine_ids=False,
            redefine_types=True,
            redefine_names=False,
        )

        topo = native_ms.topology
        all_coords = puw.get_value(native_ms.structures.coordinates, to_unit="nm")
        n_structures = all_coords.shape[0]

        # Identify peptide/protein components in selection.
        # Component indices are derived from covalent connectivity (bonds), so they
        # are an objective property of the system — no dependency on external metadata.
        # The selection evaluator resolves this local via @atom_indices_in_selection.
        atom_indices_in_selection = select(  # noqa: F841
            native_ms, selection=group_selection, syntax="MolSysMT", skip_digestion=True
        )
        component_indices = get(
            native_ms,
            element="component",
            selection='component_type in ["peptide", "protein"] and atom_index in @atom_indices_in_selection',
            component_index=True,
            skip_digestion=True,
        )
        if component_indices is None or len(component_indices) == 0:
            return native_result(native_ms)

        from molsysmt._private.smonitor import StructuralInconsistencyError
        from molsysmt.chemical_states import get_peptide_termini

        # Component membership selects the population; stored backbone direction
        # supplies its endpoints, independently of atom/group storage order.
        termini = get_peptide_termini(
            native_ms,
            selection=f"component_index in {list(map(int, component_indices))}",
        )
        mol_group_ranges = {}
        cap_status = {}
        for comp_idx in component_indices:
            comp_atoms = get(
                native_ms,
                selection=f"component_index=={int(comp_idx)}",
                atom_index=True,
            )
            comp_groups = frozenset(
                topo.atoms.loc[comp_atoms, "group_index"].dropna().astype(int)
            )
            rows = [
                row
                for row in termini["chains"]
                if comp_groups.intersection(row["group_indices"])
            ]
            if len(rows) != 1 or rows[0]["cyclic"]:
                raise StructuralInconsistencyError(
                    reason="Explicit capping requires one linear named peptide backbone per selected covalent component.",
                    caller="molsysmt.build.add_missing_terminal_cappings",
                )
            row = rows[0]
            mol_group_ranges[int(comp_idx)] = (
                row["n_terminal_group_index"],
                row["c_terminal_group_index"],
            )
            cap_status[int(comp_idx)] = (row["n_capped"], row["c_capped"])

        extra_groups_before = {}  # mol_idx -> (group_name, {atom_name: coords(n_s,3)})
        extra_groups_after = {}

        for mol_idx, (first_g, last_g) in mol_group_ranges.items():
            if N_terminal is not None and not cap_status[mol_idx][0]:
                tmpl_ace = load_residue_template(N_terminal)
                if tmpl_ace is not None:
                    # Get N, CA, C of the first residue
                    first_g_mask = topo.atoms["group_index"] == first_g
                    first_g_rows = topo.atoms[first_g_mask]

                    def _get_pos(atom_name_lookup, first_g_rows=first_g_rows):
                        rows = first_g_rows[
                            first_g_rows["atom_name"] == atom_name_lookup
                        ]
                        if len(rows) == 0:
                            return None
                        idx = rows.index[0]
                        return all_coords[:, int(idx), :]  # (n_structures, 3)

                    N_pos = _get_pos("N")
                    CA_pos = _get_pos("CA")
                    C_pos = _get_pos("C")
                    if N_pos is not None and CA_pos is not None and C_pos is not None:
                        ace_atoms = place_ace_group(
                            N_pos, CA_pos, C_pos, tmpl_ace, n_structures
                        )
                        extra_groups_before[mol_idx] = (N_terminal, ace_atoms)

            if C_terminal is not None and not cap_status[mol_idx][1]:
                tmpl_nme = load_residue_template(C_terminal)
                if tmpl_nme is not None:
                    # Get C, CA, N of the last residue
                    last_g_mask = topo.atoms["group_index"] == last_g
                    last_g_rows = topo.atoms[last_g_mask]

                    def _get_pos_last(atom_name_lookup, last_g_rows=last_g_rows):
                        rows = last_g_rows[last_g_rows["atom_name"] == atom_name_lookup]
                        if len(rows) == 0:
                            return None
                        idx = rows.index[0]
                        return all_coords[:, int(idx), :]

                    C_pos_last = _get_pos_last("C")
                    CA_pos_last = _get_pos_last("CA")
                    N_pos_last = _get_pos_last("N")
                    if (
                        C_pos_last is not None
                        and CA_pos_last is not None
                        and N_pos_last is not None
                    ):
                        nme_atoms = place_nme_group(
                            C_pos_last, CA_pos_last, N_pos_last, tmpl_nme, n_structures
                        )
                        extra_groups_after[mol_idx] = (C_terminal, nme_atoms)

        native_out, step = rebuild_molsys_with_new_groups(
            native_ms,
            mol_group_ranges,
            extra_groups_before,
            extra_groups_after,
            attribute_policy=attribute_policy,
            return_report=True,
        )
        cap_evidence = [
            template_evidence(name, load_residue_template(name))
            for name in sorted(
                {
                    entry[0]
                    for entry in list(extra_groups_before.values())
                    + list(extra_groups_after.values())
                }
            )
        ]
        reconstruction.add(step, "native_planar_terminal_caps", evidence=cap_evidence)
        return native_result(native_out)

    else:
        raise NotImplementedError
