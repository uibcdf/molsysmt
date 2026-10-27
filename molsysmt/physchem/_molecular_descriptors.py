"""Sharing complete-molecule admission and provenance for graph descriptors.

The scientific calculators remain explicit branches for the two supported tools.
This module does not prepare chemistry or define a second molecule partition.
"""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError


def _flat_members(members):
    """Flattening atom views or ragged hierarchical membership without objects per atom."""
    if isinstance(members, np.ndarray):
        return members.reshape(-1)
    return (
        np.concatenate(members).astype(np.int64)
        if len(members)
        else np.empty(0, dtype=np.int64)
    )


def calculate_molecular_descriptor(
    molecular_system,
    selection,
    structure_indices,
    chemical_state,
    syntax,
    *,
    descriptor,
    method,
    parameters,
    article_key,
    caller,
    return_report,
    element="molecule",
):
    """Evaluating already validated public descriptor requests on detached graphs."""
    from copy import deepcopy

    from rdkit import Chem, rdBase
    from rdkit.Chem import rdMolDescriptors

    from molsysmt import __version__, _ackredit
    from molsysmt._private.scientific_citations import ARTICLES, SOFTWARE
    from molsysmt.basic import convert, get
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        chemical_graph_digest,
        detached_chemical_graph_view,
        validate_chemical_frames,
    )

    def fail(reason):
        raise StructuralInconsistencyError(reason=reason, caller=caller)

    with _ackredit.scope(caller) as provider:
        population_args = dict(
            selection=selection,
            structure_indices=structure_indices,
            chemical_state=chemical_state,
            syntax=syntax,
        )
        if element == "system":
            selected_atoms = get(
                molecular_system, element="atom", atom_index=True, **population_args
            )
            output_indices = np.asarray([0], dtype=np.int64)
            output_members = [np.asarray(selected_atoms, dtype=np.int64)]
        elif element == "atom":
            output_indices = np.asarray(
                get(
                    molecular_system,
                    element="atom",
                    atom_index=True,
                    **population_args,
                ),
                dtype=np.int64,
            )
            output_members = output_indices.reshape(-1, 1)
        else:
            output_indices, output_members = get(
                molecular_system,
                element=element,
                **{f"{element}_index": True, "atom_index": True},
                **population_args,
            )
            if output_indices is None or output_members is None:
                fail(
                    "Molecular descriptors require source element indices and atom membership."
                )
            output_indices = np.asarray(output_indices, dtype=np.int64)
        if len(output_members) != len(output_indices):
            fail(
                "Element labels and source atom membership must have matching lengths."
            )
        if element == "molecule":
            indices, members = output_indices, output_members
        else:
            selected_atoms = np.unique(_flat_members(output_members))
            if len(selected_atoms):
                parents = get(
                    molecular_system,
                    element="atom",
                    selection=selected_atoms,
                    molecule_index=True,
                    structure_indices=structure_indices,
                    chemical_state=chemical_state,
                    syntax=syntax,
                )
                if parents is None or any(i is None for i in parents):
                    fail("Every selected atom requires source molecule membership.")
                parent_indices = np.unique(np.asarray(parents, dtype=np.int64))
            else:
                parent_indices = np.empty(0, dtype=np.int64)
            indices, members = get(
                molecular_system,
                element="molecule",
                selection=parent_indices,
                molecule_index=True,
                atom_index=True,
                structure_indices=structure_indices,
                chemical_state=chemical_state,
                syntax=syntax,
            )
            if indices is None or members is None:
                fail(
                    "Molecular contributions require complete source molecule membership."
                )
            indices = np.asarray(indices, dtype=np.int64)
        source, states, state, state_index, _, pairs, frames = chemical_graph_context(
            molecular_system, chemical_state, structure_indices, False, caller
        )
        validate_chemical_frames(source, frames, caller)
        from .get_aromaticity import get_aromaticity

        # Check all selected boundaries in one pass over the source bonds.
        # Repeating the full bond scan per molecule would scale poorly in mixtures.
        labels = np.full(states.n_atoms, -1, dtype=np.int64)
        for molecule_index, atoms in zip(indices, members):
            labels[np.asarray(atoms, dtype=np.int64)] = molecule_index
        if len(pairs):
            left, right = labels[pairs[:, 0]], labels[pairs[:, 1]]
            if np.any((left != right) & ((left >= 0) | (right >= 0))):
                fail("A covalent bond crosses the selected molecule boundary.")
        values, charges, charged_members, checked = [], [], [], {}
        atomic_values = []
        child_items = {}
        # One detached inventory is shared by the selected calculations; structures
        # are deliberately absent from this chemistry view.
        view = (
            detached_chemical_graph_view(source, states, state_index, caller)
            if len(indices) or return_report
            else None
        )
        for molecule_index, atoms in zip(indices, members):
            atoms = np.asarray(atoms, dtype=np.int64)
            if molecule_index in checked:
                value, charge, charged_atoms, contributions = checked[molecule_index]
            else:
                if not len(atoms):
                    fail("Selected molecules require nonempty source atom membership.")
                attrs = state.atom_attributes
                for field in (
                    "n_implicit_hydrogens",
                    "n_explicit_hydrogens",
                    "allows_implicit_hydrogens",
                ):
                    if field not in attrs or attrs[field].iloc[atoms].isna().any():
                        fail(
                            f"Molecular descriptors require declared {field} for every selected atom."
                        )
                selected = convert(view, to_form="molsysmt.MolSys", selection=atoms)
                aromaticity = get_aromaticity(selected)
                for item in aromaticity["attribution"]["items"]:
                    child_items[item["id"]] = item
                molecule = convert(selected, to_form="rdkit.Mol")
                if (
                    molecule.GetNumAtoms() != len(atoms)
                    or len(Chem.GetMolFrags(molecule)) != 1
                ):
                    fail(
                        "Each selected molecule must be one complete connected covalent graph."
                    )
                for i, atom in enumerate(molecule.GetAtoms()):
                    original = int(atoms[i])
                    if atom.GetNumImplicitHs() != int(
                        attrs["n_implicit_hydrogens"].iloc[original]
                    ) or atom.GetNumExplicitHs() != int(
                        attrs["n_explicit_hydrogens"].iloc[original]
                    ):
                        fail(
                            "The provider changed the declared nonindexed hydrogen inventory."
                        )
                contributions = None
                if element != "molecule":
                    if descriptor == "tpsa":
                        contributions = np.asarray(
                            rdMolDescriptors._CalcTPSAContribs(
                                molecule,
                                force=True,
                                includeSandP=parameters["include_sulfur_phosphorus"],
                            ),
                            dtype=np.float64,
                        )
                    else:
                        # RDKit's atom kernel does not add nonindexed H atoms.
                        # Materialize only the declared inventory and fold its
                        # contributions back to the retained attachment atom.
                        expanded = Chem.AddHs(molecule)
                        raw = np.asarray(
                            rdMolDescriptors._CalcCrippenContribs(
                                expanded,
                                force=True,
                            ),
                            dtype=np.float64,
                        )[:, 0]
                        owners = np.arange(expanded.GetNumAtoms(), dtype=np.int64)
                        for i in range(len(atoms), len(owners)):
                            hydrogen = expanded.GetAtomWithIdx(i)
                            neighbors = list(hydrogen.GetNeighbors())
                            if (
                                hydrogen.GetAtomicNum() != 1
                                or len(neighbors) != 1
                                or neighbors[0].GetIdx() >= len(atoms)
                            ):
                                fail(
                                    "Materialized hydrogen requires one retained attachment atom."
                                )
                            owners[i] = neighbors[0].GetIdx()
                        contributions = np.bincount(
                            owners, weights=raw, minlength=len(atoms)
                        )
                    if contributions.shape != (len(atoms),) or not np.all(
                        np.isfinite(contributions)
                    ):
                        fail("The provider returned invalid atomic contributions.")
                    value = float(np.sum(contributions))
                else:
                    if descriptor == "tpsa":
                        value = float(
                            rdMolDescriptors.CalcTPSA(
                                molecule,
                                force=True,
                                includeSandP=parameters["include_sulfur_phosphorus"],
                            )
                        )
                    else:
                        value = float(
                            rdMolDescriptors.CalcCrippenDescriptors(
                                molecule,
                                includeHs=True,
                                force=True,
                            )[0]
                        )
                if not np.isfinite(value) or (descriptor == "tpsa" and value < 0):
                    fail("The molecular descriptor provider returned an invalid value.")
                charge = Chem.GetFormalCharge(molecule)
                charged_atoms = atoms[
                    np.asarray(
                        [atom.GetFormalCharge() != 0 for atom in molecule.GetAtoms()],
                        dtype=bool,
                    )
                ]
                checked[molecule_index] = value, charge, charged_atoms, contributions
            values.append(value)
            charges.append(charge)
            charged_members.append(charged_atoms)
            if contributions is not None:
                atomic_values.append(contributions)
        result = np.asarray(values, dtype=np.float64)
        if element != "molecule":
            if atomic_values:
                source_atoms = np.concatenate(members).astype(np.int64)
                order = np.argsort(source_atoms)
                source_atoms = source_atoms[order]
                source_values = np.concatenate(atomic_values)[order]
                if element == "atom":
                    result = source_values[
                        np.searchsorted(source_atoms, output_indices)
                    ]
                else:
                    result = np.asarray(
                        [
                            np.sum(source_values[np.searchsorted(source_atoms, atoms)])
                            for atoms in output_members
                        ],
                        dtype=np.float64,
                    )
            else:
                result = np.zeros(len(output_members), dtype=np.float64)
            if element == "system":
                result = result[0]

        software = {"molsysmt": __version__, "rdkit": rdBase.rdkitVersion}
        items = [
            dict(
                id=f"doi:{ARTICLES[article_key]['doi']}",
                type="article",
                **deepcopy(ARTICLES[article_key]),
                roles=["scientific_criterion"],
            )
        ]
        items.extend(
            dict(
                id=f"software:{name}:{version}",
                type="software",
                **deepcopy(SOFTWARE[name]),
                version=version,
                roles=["executed_software"],
            )
            for name, version in software.items()
        )
        items = list(
            {item["id"]: item for item in [*child_items.values(), *items]}.values()
        )
        _ackredit.credit(provider, items, caller)
        if not return_report:
            return result, None
        offsets = np.concatenate(
            ([0], np.cumsum([len(atoms) for atoms in members]))
        ).astype(np.int64)
        report = dict(
            schema=f"molsysmt.{descriptor}@1",
            molecule_indices=indices.copy(),
            atom_offsets=offsets,
            atom_indices=np.concatenate(members).astype(np.int64)
            if members
            else np.empty(0, dtype=np.int64),
            chemical_state_index=state_index,
            chemical_state_id=state.state_id,
            chemical_graph_digest=chemical_graph_digest(view, state_index),
            formal_charges=np.asarray(charges, dtype=np.int64),
            formal_charge_unit="elementary_charge",
            method=method,
            parameters=deepcopy(parameters),
            element=element,
            element_indices=output_indices.copy(),
            element_atom_offsets=np.arange(len(output_indices) + 1, dtype=np.int64)
            if element == "atom"
            else np.concatenate(
                ([0], np.cumsum([len(a) for a in output_members]))
            ).astype(np.int64),
            element_atom_indices=_flat_members(output_members).copy(),
            output_kind="molecular_descriptor"
            if element == "molecule"
            else "atomic_contribution_sum",
            software=software,
            attribution=dict(
                schema="molsysmt.scientific_attribution@1",
                target=caller,
                items=items,
            ),
        )
        if element != "molecule":
            report["parameters"].update(
                implementation="rdkit._CalcTPSAContribs"
                if descriptor == "tpsa"
                else "rdkit._CalcCrippenContribs",
                contribution_context="complete_source_molecules",
                nonindexed_hydrogen_attribution="attached_source_atom",
                indexed_hydrogen_attribution="own_source_atom",
            )
        if descriptor == "lipophilicity":
            report.update(
                value_kind="wildman_crippen_model_score",
                value_unit="dimensionless",
                charged_atom_offsets=np.concatenate(
                    ([0], np.cumsum([len(atoms) for atoms in charged_members]))
                ).astype(np.int64),
                charged_atom_indices=np.concatenate(charged_members).astype(np.int64)
                if charged_members
                else np.empty(0, dtype=np.int64),
            )
        return result, report
