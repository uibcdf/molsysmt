"""Which hydrogens a system carries that the requested pH does not call for.

`add_missing_hydrogens` compares expected against present in one direction only: it
adds what is absent and never looks at what is present and unwanted. That asymmetry is
`uibcdf/molsysmt#178`, and this module holds the other half of the comparison so the two
functions cannot drift apart — `reconcile_protonation` removes what it reports, and
`add_missing_hydrogens` warns about it.

Detection lives here rather than in either caller because the rule that decides is the
same one: `get_expected_hydrogens`, with the same terminal and disulfide context. Two
implementations of "which hydrogens belong here" would eventually disagree, and the
disagreement would be silent.
"""

from molsysmt._private.amino_acid_templates import family
from molsysmt._private.amino_acid_templates import is_hydrogen as _is_hydrogen
from molsysmt.element.group.amino_acid.get_expected_hydrogens import (
    get_expected_hydrogens,
)


def assess(native_molsys, pH, *, n_structures=None):
    """Evaluate reference inventories on detached graph labels, without rebuilding."""
    import numpy as np

    from molsysmt import __version__
    from molsysmt._private.amino_acid_templates import references
    from molsysmt.native._chemical_components import indices_from_bonds

    topology = native_molsys.topology
    schemes = topology.group_naming_schemes
    kinds = [
        family(
            group_name,
            schemes[group_index],
            caller="molsysmt.build.reconcile_protonation",
        )
        for group_index, group_name in enumerate(topology.groups["group_name"])
    ]

    n_groups = topology.n_groups
    n_atoms = topology.n_atoms
    states = native_molsys.chemical_states
    bonds = states._get_chemical_state_bonds()
    component_indices = indices_from_bonds(n_atoms, bonds)
    grouped = topology.atoms.groupby("group_index", sort=False).indices

    first_group_of_component = {}
    last_group_of_component = {}
    for group_index in range(n_groups):
        positions = grouped.get(group_index, [])
        if not len(positions):
            continue
        component_index = int(component_indices[positions[0]])
        if component_index not in first_group_of_component:
            first_group_of_component[component_index] = group_index
        last_group_of_component[component_index] = group_index

    disulfide_groups = set()
    if bonds is not None and len(bonds) > 0:
        for _, bond in bonds.iterrows():
            first = topology.atoms.loc[int(bond["atom1_index"])]
            second = topology.atoms.loc[int(bond["atom2_index"])]
            if first["atom_name"] == "SG" and second["atom_name"] == "SG":
                disulfide_groups.add(int(first["group_index"]))
                disulfide_groups.add(int(second["group_index"]))

    unexpected, assessed, unassessed, reasons, contexts = [], [], [], [], []
    items = {}
    assigned = np.zeros(n_atoms, dtype=bool)

    for group_index in range(n_groups):
        positions = grouped.get(group_index, [])
        group_atoms = topology.atoms.iloc[positions]
        assigned[positions] = True
        group_name = topology.groups.loc[group_index, "group_name"]
        context = dict(
            group_index=group_index,
            naming_scheme=schemes[group_index],
            group_name=str(group_name),
            reference_kind=kinds[group_index],
            is_n_terminal=None,
            is_c_terminal=None,
            is_disulfide=None,
            status="unassessed",
            reason="empty_group",
        )
        contexts.append(context)
        if group_atoms.empty:
            unassessed.append(group_index)
            reasons.append("empty_group")
            continue

        component_index = int(component_indices[positions[0]])
        n_terminal = first_group_of_component.get(component_index) == group_index
        c_terminal = last_group_of_component.get(component_index) == group_index
        disulfide = group_index in disulfide_groups
        context.update(
            is_n_terminal=n_terminal,
            is_c_terminal=c_terminal,
            is_disulfide=disulfide,
        )

        present_names = group_atoms["atom_name"].tolist()
        expected = get_expected_hydrogens(
            group_name,
            naming_scheme=schemes[group_index],
            present_atom_names=present_names,
            pH=pH,
            is_n_terminal=n_terminal,
            is_c_terminal=c_terminal,
            is_disulfide=disulfide,
        )
        if expected is None:
            unassessed.append(group_index)
            reason = "unsupported_reference"
            if kinds[group_index] == "amber_state" and (n_terminal or c_terminal):
                reason = "named_state_terminal_reference_unavailable"
            elif kinds[group_index] in {"standard", "amber_state"}:
                reason = "incompatible_atom_layout"
            context["reason"] = reason
            reasons.append(reason)
            continue

        assessed.append(group_index)
        context.update(status="assessed", reason=None)
        for reference in references(group_name, kinds[group_index]):
            items.setdefault(reference["id"], reference)
        expected_set = set(expected)
        for atom_index, atom_name in zip(group_atoms.index.tolist(), present_names):
            if _is_hydrogen(atom_name) and atom_name not in expected_set:
                unexpected.append(
                    (int(atom_index), str(atom_name), int(group_index), str(group_name))
                )

    unexpected.sort()
    removed = np.asarray([entry[0] for entry in unexpected], dtype=np.int64)
    retained_mask = np.ones(n_atoms, dtype=bool)
    retained_mask[removed] = False
    retained = np.flatnonzero(retained_mask)
    source_to_output_atom_indices = np.full(n_atoms, -1, dtype=np.int64)
    source_to_output_atom_indices[retained] = np.arange(len(retained), dtype=np.int64)
    unassigned = np.flatnonzero(~assigned)
    reference_state = states.reference_chemical_state_index
    other_states = np.asarray(
        [
            index
            for index in range(states.n_chemical_states)
            if index != reference_state
        ],
        dtype=np.int64,
    )
    complete = not unassessed and not len(unassigned) and not len(other_states)
    status = (
        "removal_required"
        if len(removed)
        else (
            "no_change"
            if complete
            else ("partial_no_change" if assessed else "unassessed")
        )
    )
    if n_structures is None:
        n_structures = (
            0
            if native_molsys.structures is None
            else native_molsys.structures.n_structures
        )
    return dict(
        schema="molsysmt.protonation_assessment@1",
        status=status,
        source=dict(
            n_atoms=n_atoms,
            n_groups=n_groups,
            n_structures=n_structures,
            reference_chemical_state_index=states.reference_chemical_state_index,
            n_chemical_states=states.n_chemical_states,
        ),
        parameters=dict(
            pH=float(pH),
            engine="MolSysMT",
            method="fixed_pka_name_inventory",
            method_version=1,
            component_context="stored_joins_components",
            chemical_state="reference",
        ),
        coverage=dict(
            assessed_chemical_state_indices=np.asarray(
                [reference_state], dtype=np.int64
            ),
            unassessed_chemical_state_indices=other_states,
            assessed_group_indices=np.asarray(assessed, dtype=np.int64),
            unassessed_group_indices=np.asarray(unassessed, dtype=np.int64),
            unassessed_reasons=reasons,
            unassigned_atom_indices=unassigned,
            complete=complete,
        ),
        group_contexts=contexts,
        removed_atoms=unexpected,
        removed_atom_indices=removed,
        atom_map=dict(
            schema="molsysmt.atom_map@1",
            n_source_atoms=n_atoms,
            n_output_atoms=len(retained),
            source_to_output_atom_indices=source_to_output_atom_indices,
            output_to_source_atom_indices=retained,
        ),
        structure_indices=np.arange(n_structures, dtype=np.int64),
        software=dict(molsysmt=__version__),
        attribution=dict(items=list(items.values())),
        execution=dict(status="prepared"),
    )


def unexpected_hydrogens(native_molsys, pH):
    """Return sorted unwanted-H tuples without changing any stored component data."""
    return assess(native_molsys, pH)["removed_atoms"]
