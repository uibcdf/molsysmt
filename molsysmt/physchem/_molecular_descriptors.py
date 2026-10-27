"""Sharing complete-molecule admission and provenance for graph descriptors.

The scientific calculators remain explicit branches for the two supported tools.
This module does not prepare chemistry or define a second molecule partition.
"""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError


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
        indices, members = get(
            molecular_system,
            element="molecule",
            selection=selection,
            structure_indices=structure_indices,
            chemical_state=chemical_state,
            syntax=syntax,
            molecule_index=True,
            atom_index=True,
        )
        if indices is None or members is None:
            fail(
                "Molecular descriptors require source molecule indices and atom membership."
            )
        indices = np.asarray(indices, dtype=np.int64)
        if len(members) != len(indices):
            fail(
                "Molecule labels and source atom membership must have matching lengths."
            )
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
                value, charge, charged_atoms = checked[molecule_index]
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
                checked[molecule_index] = value, charge, charged_atoms
            values.append(value)
            charges.append(charge)
            charged_members.append(charged_atoms)
        result = np.asarray(values, dtype=np.float64)
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
            software=software,
            attribution=dict(
                schema="molsysmt.scientific_attribution@1",
                target=caller,
                items=items,
            ),
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
