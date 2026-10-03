"""Auditing PDBQT-specific information omitted by native projections or writing."""

from molsysmt.basic.conversion_report import ConversionIssue

PDBQT_FORMS = {"file:pdbqt", "string:pdbqt_text"}


def audit_pdbqt(item, source_form, target_form, selection, structure_indices, syntax):
    from molsysmt._private.pdbqt_adapter import identity_selection
    from molsysmt._private.variables import is_all

    issues = []

    def dropped(attribute, reason, scope):
        issues.append(ConversionIssue(attribute=attribute, reason=reason, scope=scope))

    identity = (
        source_form in PDBQT_FORMS
        and target_form in PDBQT_FORMS
        and identity_selection(item, source_form, selection, structure_indices, syntax)
    )
    if identity:
        return issues
    if source_form in PDBQT_FORMS:
        from molsysmt._private.pdbqt import read

        record = read(item, text=source_form == "string:pdbqt_text")
        if record["torsion_tree"] is not None:
            dropped(
                "pdbqt_torsion_tree",
                "Native domains have no store for ROOT/BRANCH layout or TORSDOF; retain get_torsion_tree() separately.",
                "source_metadata",
            )
        if record["remarks"]:
            dropped(
                "pdbqt_remarks",
                "Native domains do not preserve arbitrary PDBQT REMARK records.",
                "source_metadata",
            )
        if any(atom["record"] == "HETATM" for atom in record["atoms"]):
            dropped(
                "pdbqt_record_type",
                "Native atom tables do not retain the ATOM/HETATM record distinction.",
                "source_metadata",
            )
        if target_form in {"molsysmt.Topology", "molsysmt.Structures"}:
            dropped(
                "partial_charge",
                "This reduced domain does not retain explicit partial charges.",
                "molecular_mechanics",
            )
            dropped(
                "atom_ff_type",
                "This reduced domain does not retain AutoDock atom labels.",
                "molecular_mechanics",
            )
    if target_form in PDBQT_FORMS and source_form == "molsysmt.MolSys":
        from molsysmt.basic import extract

        selected = (
            item
            if is_all(selection) and is_all(structure_indices)
            else extract(
                item,
                selection=selection,
                structure_indices=structure_indices,
                syntax=syntax,
            )
        )
        if selected.chemical_states is not None:
            if any(len(state.bonds) for state in selected.chemical_states._states):
                dropped(
                    "bond_inventory",
                    "PDBQT stores at most supplied tree branch bonds, with no full graph or bond-order inventory.",
                    "chemical_state",
                )
            if selected.chemical_states.n_chemical_states > 1:
                dropped(
                    "chemical_state_inventory",
                    "PDBQT cannot retain multiple chemical states or their assignments.",
                    "chemical_state",
                )
        if selected.interactions:
            dropped(
                "interactions",
                "PDBQT does not store named interaction analyses.",
                "interactions",
            )
        if selected.structures is not None:
            for attribute in (
                "box",
                "time",
                "velocities",
                "temperature",
                "potential_energy",
                "kinetic_energy",
            ):
                if getattr(selected.structures, attribute, None) is not None:
                    dropped(
                        attribute,
                        f"PDBQT cannot retain structural {attribute}.",
                        "structures",
                    )
        mechanics = selected.molecular_mechanics
        if mechanics is not None and any(
            getattr(mechanics, attribute, None) is not None
            for attribute in mechanics.to_dict()
            if attribute not in {"atom_ff_type", "partial_charge", "formal_charge"}
        ):
            dropped(
                "molecular_mechanics_settings",
                "PDBQT retains AutoDock labels and charges, not general force-field settings.",
                "molecular_mechanics",
            )
    return issues
