"""Interpret an explicitly selected CCD descriptor with complete mapping consensus."""

from copy import deepcopy

from molsysmt._private.ccd_reference import CALLER
from molsysmt._private.smonitor import (
    FileContentError,
    MemoryBudgetExceededError,
    UnsupportedHeavyOperationError,
)


def interpret(block, atoms, bonds, program, max_matches, *, table_conflicts=False):
    from molsysmt._private.chemical_reference_template import _issue, value

    table = block.getObj("pdbx_chem_comp_descriptor")
    selected = [
        row
        for row in range(0 if table is None else table.getRowCount())
        if value(table, "type", row) == "SMILES_CANONICAL"
        and value(table, "program", row) == program
    ]
    report = dict(
        program=program,
        software={},
        issues=[],
        references=[],
        n_graph_matches=0,
        n_compatible_matches=0,
        search_complete=False,
        assignment_consensus_complete=False,
        stereo_disagreements=[],
    )
    if len(selected) != 1:
        _issue(
            report["issues"],
            "canonical_descriptor_not_found"
            if not selected
            else "canonical_descriptor_ambiguous",
        )
        return None, report
    row = selected[0]
    component_id = value(block.getObj("chem_comp"), "id")
    descriptor_id = value(table, "comp_id", row)
    if (
        descriptor_id is not None
        and descriptor_id.casefold() != component_id.casefold()
    ):
        raise FileContentError(
            "A CCD descriptor belongs to another component", caller=CALLER
        )
    report.update(
        source_row_index=row,
        program_version=value(table, "program_version", row),
        descriptor=value(table, "descriptor", row),
        type="SMILES_CANONICAL",
    )
    if table_conflicts:
        _issue(report["issues"], "conflicting_ccd_declarations", status="conflict")
        return None, report
    if any(bond["aromatic"] is True and bond["order"] in {3, 4} for bond in bonds):
        _issue(report["issues"], "unsupported_descriptor_bond_model")
        return None, report
    if any(
        atom[field] is None
        for atom in atoms
        for field in ("symbol", "charge", "aromatic")
    ) or any(
        bond["aromatic"] is None or bond["order"] is None and bond["fractional"] != 1.5
        for bond in bonds
    ):
        _issue(report["issues"], "incomplete_ccd_graph_for_descriptor_validation")
        return None, report
    from rdkit import Chem, rdBase

    from molsysmt import configure
    from molsysmt._private.stereochemistry import REFERENCE, assign_cip, native_labels

    report["software"] = dict(rdkit=rdBase.rdkitVersion)
    reference = Chem.MolFromSmiles(report["descriptor"] or "")
    if reference is None or reference.GetNumAtoms() == 0:
        _issue(report["issues"], "invalid_canonical_descriptor")
        return None, report
    if reference.GetStereoGroups():
        _issue(report["issues"], "enhanced_descriptor_stereo_not_supported")
        return None, report
    if any(
        atom.GetChiralTag()
        not in {
            Chem.ChiralType.CHI_UNSPECIFIED,
            Chem.ChiralType.CHI_TETRAHEDRAL_CW,
            Chem.ChiralType.CHI_TETRAHEDRAL_CCW,
        }
        for atom in reference.GetAtoms()
    ):
        _issue(report["issues"], "non_tetrahedral_descriptor_stereo_not_supported")
        return None, report
    assign_cip(reference)
    labels, bond_labels = native_labels(reference)
    citation = deepcopy(REFERENCE)
    citation["roles"] = ["scientific_criterion"]
    report["references"].append(citation)
    graph = Chem.RWMol()
    for index, record in enumerate(atoms):
        atom = Chem.Atom(record["symbol"])
        atom.SetFormalCharge(record["charge"])
        atom.SetIsAromatic(record["aromatic"])
        atom.SetIsotope(record["isotope"] or 0)
        atom.SetNoImplicit(True)
        atom.SetIntProp("_CCDRowIndex", index)
        graph.AddAtom(atom)
    order_types = {
        1: Chem.BondType.SINGLE,
        2: Chem.BondType.DOUBLE,
        3: Chem.BondType.TRIPLE,
        4: Chem.BondType.QUADRUPLE,
    }
    for bond in bonds:
        order = (
            Chem.BondType.AROMATIC
            if bond["aromatic"]
            else order_types.get(bond["order"])
        )
        if order is None:
            _issue(report["issues"], "unsupported_descriptor_bond_model")
            return None, report
        graph.AddBond(*bond["pair"], order)
    full = graph.GetMol()
    try:
        Chem.SanitizeMol(full)
        core = Chem.RemoveHs(full)
    except (ValueError, RuntimeError):
        _issue(
            report["issues"],
            "invalid_ccd_valence_for_descriptor_validation",
            status="conflict",
        )
        return None, report
    core_rows = [atom.GetIntProp("_CCDRowIndex") for atom in core.GetAtoms()]
    if (
        core.GetNumAtoms() != reference.GetNumAtoms()
        or core.GetNumBonds() != reference.GetNumBonds()
    ):
        _issue(report["issues"], "descriptor_graph_size_conflict", status="conflict")
        return None, report
    per_match = 256 + 64 * core.GetNumAtoms()
    budget = configure.max_ram_usage // 4
    bound = min(max_matches, budget // per_match)
    if bound < 1:
        raise MemoryBudgetExceededError(
            reason="One descriptor correspondence exceeds the candidate budget.",
            predicted_bytes=per_match,
            available_bytes=budget,
            caller=CALLER,
        )
    matches = core.GetSubstructMatches(
        reference, uniquify=False, useChirality=False, maxMatches=int(bound + 1)
    )
    if len(matches) > bound:
        if bound < max_matches:
            raise MemoryBudgetExceededError(
                reason="Descriptor correspondence search exceeds the candidate budget.",
                predicted_bytes=len(matches) * per_match,
                available_bytes=budget,
                caller=CALLER,
            )
        raise UnsupportedHeavyOperationError(
            operation=CALLER,
            form="CCD/canonical descriptor",
            reason="Search exceeds max_matches; no truncated assignment consensus is returned.",
            caller=CALLER,
        )
    report.update(n_graph_matches=len(matches), search_complete=True)
    bond_indices = {bond["pair"]: index for index, bond in enumerate(bonds)}
    consensus = None
    for mapping in matches:
        source_rows = [core_rows[index] for index in mapping]
        valid = True
        for index, target in enumerate(source_rows):
            reference_atom = reference.GetAtomWithIdx(index)
            source_atom = full.GetAtomWithIdx(target)
            record = atoms[target]
            if (
                reference_atom.GetFormalCharge() != record["charge"]
                or reference_atom.GetIsAromatic() != record["aromatic"]
                or reference_atom.GetIsotope() != (record["isotope"] or 0)
                or reference_atom.GetTotalNumHs(includeNeighbors=True)
                != source_atom.GetTotalNumHs(includeNeighbors=True)
                or reference_atom.GetNumRadicalElectrons()
                != source_atom.GetNumRadicalElectrons()
            ):
                valid = False
                break
        if not valid:
            continue
        # Ordinary removed H is independently present in the CCD graph. Its
        # charge/radicals/aromaticity must be ordinary before count consensus
        # can cover it; isolated or isotopic H remains in the core instead.
        outside = set(range(len(atoms))) - set(source_rows)
        if any(
            atoms[i]["symbol"] != "H"
            or atoms[i]["isotope"] is not None
            or atoms[i]["charge"] != 0
            or atoms[i]["aromatic"]
            or full.GetAtomWithIdx(i).GetNumRadicalElectrons() != 0
            for i in outside
        ):
            continue
        atom_stereo = [None] * len(atoms)
        for index, target in enumerate(source_rows):
            atom_stereo[target] = labels[index]
        bond_assignments = [(None, None, False)] * len(bonds)
        for bond in reference.GetBonds():
            first, second = (
                source_rows[bond.GetBeginAtomIdx()],
                source_rows[bond.GetEndAtomIdx()],
            )
            pair = tuple(sorted((first, second)))
            label, references = bond_labels[bond.GetIdx()]
            endpoints = None
            if label is not None:
                if len(references) != 2:
                    valid = False
                    break
                endpoints = tuple(source_rows[i] for i in references)
                if first > second:
                    endpoints = endpoints[::-1]
            bond_assignments[bond_indices[pair]] = (
                label,
                endpoints,
                bond.GetIsConjugated(),
            )
        if not valid:
            continue
        signature = (tuple(atom_stereo), tuple(bond_assignments))
        report["n_compatible_matches"] += 1
        if consensus is None:
            consensus = signature
        elif signature != consensus:
            _issue(
                report["issues"], "descriptor_assignment_ambiguous", status="conflict"
            )
            return None, report
    if consensus is None:
        _issue(report["issues"], "descriptor_chemistry_conflict", status="conflict")
        return None, report
    atom_stereo, bond_assignments = consensus
    report["assignment_consensus_complete"] = True
    for index, label in enumerate(atom_stereo):
        if atoms[index]["stereo"] in {"R", "S"} and atoms[index]["stereo"] != label:
            report["stereo_disagreements"].append(
                dict(
                    axis="atom",
                    source_index=index,
                    source_atom_id=atoms[index]["name"],
                    ccd_flag=atoms[index]["stereo"],
                    chosen_descriptor_label=label,
                )
            )
    for index, (label, _, _) in enumerate(bond_assignments):
        if bonds[index]["stereo"] in {"E", "Z"} and bonds[index]["stereo"] != label:
            report["stereo_disagreements"].append(
                dict(
                    axis="bond",
                    source_index=index,
                    ccd_flag=bonds[index]["stereo"],
                    chosen_descriptor_label=label,
                )
            )
    potential = list(Chem.FindPotentialStereo(reference))
    if any(item.specified != Chem.StereoSpecified.Specified for item in potential):
        _issue(report["issues"], "unassigned_descriptor_stereochemistry")
    return dict(
        atoms=dict(
            formal_charge=[atom["charge"] for atom in atoms],
            is_aromatic=[atom["aromatic"] for atom in atoms],
            n_unpaired_electrons=[
                atom.GetNumRadicalElectrons() for atom in full.GetAtoms()
            ],
            stereochemistry=list(atom_stereo),
        ),
        bonds=[
            dict(
                stereochemistry=label, stereo_atoms=references, is_conjugated=conjugated
            )
            for label, references, conjugated in bond_assignments
        ],
    ), report
