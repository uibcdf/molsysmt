"""Prepare and compare fixed chemical graphs without consulting coordinates."""

import hashlib
import json

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

from ._chemical_graph import (
    chemical_graph_context,
    detached_chemical_graph_view,
    select_chemical_atoms,
    validate_chemical_frames,
)


class ChemicalGraph:
    """Keep one complete covalent component and its original positional axis."""

    def __init__(self, source, selection, frames, state_index, syntax, caller):
        from rdkit import Chem

        from molsysmt._private import rust_backend as kernels
        from molsysmt._private.stereochemistry import assign_cip
        from molsysmt._private.variables import is_all
        from molsysmt.basic import convert

        if hasattr(source, "GetStereoGroups") and source.GetStereoGroups():
            raise StructuralInconsistencyError(
                reason="Enhanced stereo groups are outside this correspondence profile.",
                caller=caller,
            )
        rich = isinstance(selection, str) and not is_all(selection)
        if rich:
            frames = validate_chemical_frames(source, frames, caller)
        source, states, state, index, _, pairs, frames = chemical_graph_context(
            source,
            state_index,
            frames,
            False,
            caller,
            with_structures=rich,
        )
        self.n_atoms, self.state_index = states.n_atoms, index
        self.state_id = state.state_id
        self.provenance_index = state.provenance_index
        self.selected = select_chemical_atoms(
            source,
            states,
            index,
            selection,
            frames,
            syntax,
            reference_request=state_index in (None, "reference"),
        )
        if not len(self.selected):
            raise ArgumentError(
                "selection", caller=caller, message="Select at least one atom."
            )
        if np.any((self.selected < 0) | (self.selected >= states.n_atoms)):
            raise ArgumentError("selection", caller=caller)
        components = kernels.get_component_index_from_bonded_atom_pairs(
            pairs, states.n_atoms
        )
        self.atoms = np.flatnonzero(components == components[self.selected[0]]).astype(
            np.int64
        )
        if not np.isin(self.selected, self.atoms).all():
            raise StructuralInconsistencyError(
                reason="Select atoms from one complete covalent component.",
                caller=caller,
            )
        bonds = state.bonds
        scoped = (
            bonds.loc[
                bonds["atom1_index"].isin(self.atoms)
                | bonds["atom2_index"].isin(self.atoms)
            ]
            if len(bonds)
            else bonds
        )
        if len(scoped) and not scoped["bond_type"].eq("covalent").all():
            raise StructuralInconsistencyError(
                reason="Dative chemistry is outside the declared-graph correspondence profile.",
                caller=caller,
            )
        inventory = state.atom_attributes.reindex(self.atoms)
        required = (
            "formal_charge",
            "is_aromatic",
            "n_unpaired_electrons",
            "n_implicit_hydrogens",
            "n_explicit_hydrogens",
            "allows_implicit_hydrogens",
            "stereochemistry",
        )
        for name in required:
            if name not in inventory or inventory[name].isna().any():
                raise StructuralInconsistencyError(
                    reason=f"Every context atom requires declared {name} metadata.",
                    caller=caller,
                )
        for name in (
            "formal_charge",
            "n_unpaired_electrons",
            "n_implicit_hydrogens",
            "n_explicit_hydrogens",
        ):
            values = inventory[name].to_numpy(dtype=np.float64)
            if (
                any(isinstance(value, (bool, np.bool_)) for value in inventory[name])
                or not np.isfinite(values).all()
                or not np.equal(values, np.trunc(values)).all()
                or (name != "formal_charge" and np.any(values < 0))
            ):
                raise StructuralInconsistencyError(
                    reason=f"Declared {name} values must be integer counts; H/radical counts must be nonnegative.",
                    caller=caller,
                )
        for name in ("is_aromatic", "allows_implicit_hydrogens"):
            if not all(
                isinstance(value, (bool, np.bool_)) for value in inventory[name]
            ):
                raise StructuralInconsistencyError(
                    reason=f"Declared {name} values must be boolean.", caller=caller
                )
        if (
            not inventory["stereochemistry"]
            .isin(["unspecified", "R", "S", "r", "s"])
            .all()
        ):
            raise StructuralInconsistencyError(
                reason="Unsupported declared atom stereochemistry.", caller=caller
            )
        view = detached_chemical_graph_view(source, states, index, caller)
        symbols = view.topology.atoms.loc[self.atoms, "atom_type"].tolist()
        from molsysmt.physchem.atoms.mass import physical as elements

        if any(pd.isna(symbol) or symbol not in elements for symbol in symbols):
            raise StructuralInconsistencyError(
                reason="Every context atom requires an explicit element symbol.",
                caller=caller,
            )
        isotopes = (
            view.topology.atoms.loc[self.atoms, "isotope"]
            .fillna(0)
            .astype(int)
            .tolist()
        )
        self.labels = [
            (
                symbol,
                isotope,
                int(row.formal_charge),
                bool(row.is_aromatic),
                int(row.n_unpaired_electrons),
                int(row.n_implicit_hydrogens),
                int(row.n_explicit_hydrogens),
                bool(row.allows_implicit_hydrogens),
                row.stereochemistry,
            )
            for symbol, isotope, row in zip(symbols, isotopes, inventory.itertuples())
        ]
        self.molecule = convert(view, selection=self.atoms, to_form="rdkit.Mol")
        self.molecule.RemoveAllConformers()
        assign_cip(self.molecule)
        actual = [
            (
                atom.GetSymbol(),
                atom.GetIsotope(),
                atom.GetFormalCharge(),
                atom.GetIsAromatic(),
                atom.GetNumRadicalElectrons(),
                atom.GetNumImplicitHs(),
                atom.GetNumExplicitHs(),
                not atom.GetNoImplicit(),
                atom.GetProp("_CIPCode") if atom.HasProp("_CIPCode") else "unspecified",
            )
            for atom in self.molecule.GetAtoms()
        ]
        if actual != self.labels:
            raise StructuralInconsistencyError(
                reason="RDKit changed declared atom chemistry or stereochemistry.",
                caller=caller,
            )
        for site in Chem.FindPotentialStereo(self.molecule):
            if (
                site.type
                not in (Chem.StereoType.Atom_Tetrahedral, Chem.StereoType.Bond_Double)
                or site.specified != Chem.StereoSpecified.Specified
            ):
                raise StructuralInconsistencyError(
                    reason="Potential stereochemistry must be explicitly assigned; unsupported stereo cannot certify correspondence.",
                    caller=caller,
                )
        if self.molecule.GetStereoGroups():
            raise StructuralInconsistencyError(
                reason="Enhanced stereo groups are outside this correspondence profile.",
                caller=caller,
            )
        self.edges = {}
        for row in scoped.itertuples():
            left, right = np.searchsorted(
                self.atoms, [row.atom1_index, row.atom2_index]
            )
            aromatic = getattr(row, "is_aromatic", pd.NA)
            order, fractional = (
                getattr(row, "bond_order", pd.NA),
                getattr(row, "fractional_bond_order", pd.NA),
            )
            value = (
                float(order)
                if pd.notna(order)
                else float(fractional)
                if pd.notna(fractional)
                else np.nan
            )
            if not isinstance(aromatic, (bool, np.bool_)) or value not in (
                1,
                1.5,
                2,
                3,
            ):
                raise StructuralInconsistencyError(
                    reason="Every context bond requires explicit aromaticity and a supported order (1, 1.5, 2 or 3).",
                    caller=caller,
                )
            bond = self.molecule.GetBondBetweenAtoms(int(left), int(right))
            if (
                bond is None
                or bond.GetIsAromatic() != bool(aromatic)
                or bond.GetBondTypeAsDouble() != value
            ):
                raise StructuralInconsistencyError(
                    reason="RDKit changed declared connectivity, orders or aromaticity.",
                    caller=caller,
                )
            stereo = getattr(row, "stereochemistry", pd.NA)
            if pd.notna(stereo) and stereo not in ("E", "Z", "cis", "trans"):
                raise StructuralInconsistencyError(
                    reason="Unsupported declared bond stereochemistry.", caller=caller
                )
            cip = bond.GetProp("_CIPCode") if bond.HasProp("_CIPCode") else None
            if pd.notna(stereo) and cip is None:
                raise StructuralInconsistencyError(
                    reason="Declared bond stereochemistry was not preserved.",
                    caller=caller,
                )
            self.edges[tuple(sorted((int(left), int(right))))] = (
                value,
                bool(aromatic),
                cip,
            )
        self.selected_positions = np.searchsorted(self.atoms, self.selected)
        self.uses_cip = any(label[-1] != "unspecified" for label in self.labels) or any(
            label[-1] is not None for label in self.edges.values()
        )
        payload = dict(
            n_atoms=self.n_atoms,
            atoms=self.atoms.tolist(),
            selected=self.selected.tolist(),
            labels=self.labels,
            edges=sorted(self.edges.items()),
            state_index=index,
        )
        self.digest = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

    def admits(self, other, mapping):
        """Check exact labels and bonds after the compiled stereochemical search."""
        if len(mapping) != len(self.atoms) or len(set(mapping)) != len(mapping):
            return False
        if len(self.edges) != len(other.edges):
            return False
        if not np.array_equal(
            np.sort(other.atoms[np.asarray(mapping)[self.selected_positions]]),
            other.selected,
        ):
            return False
        if any(self.labels[i] != other.labels[j] for i, j in enumerate(mapping)):
            return False
        return all(
            other.edges.get(tuple(sorted((mapping[a], mapping[b])))) == label
            for (a, b), label in self.edges.items()
        )


def correspondence_digest(result):
    """Detect accidental changes to a detached correspondence result, not authenticate it."""
    digest = hashlib.sha256()
    for name in (
        "atom_correspondences",
        "context_atom_correspondences",
        "selection_atom_indices",
        "reference_selection_atom_indices",
    ):
        values = np.asarray(result[name], dtype=np.int64)
        digest.update(str(values.shape).encode())
        digest.update(values.tobytes())
    digest.update(
        json.dumps(
            [
                result["source_graph_digest"],
                result["reference_graph_digest"],
                result["method"],
                result["rule_version"],
                result["n_atoms"],
                result["reference_n_atoms"],
                result["chemical_state_index"],
                result["reference_chemical_state_index"],
                result["search_complete"],
            ]
        ).encode()
    )
    if "search_scope" in result:
        digest.update(result["search_scope"].encode())
        for name in ("fixed_atom_correspondence", "candidate_atom_correspondences"):
            value = result[name]
            if value is None:
                digest.update(b"None")
            else:
                values = np.asarray(value, dtype=np.int64)
                digest.update(str(values.shape).encode())
                digest.update(values.tobytes())
    return digest.hexdigest()


def validate_correspondence_result(result, first, second, method, caller):
    """Check a detached result against current graphs without enumerating them again."""
    try:
        from ._correspondence_constraints import prepare_constraints

        if (
            result["source_graph_digest"] != first.digest
            or result["reference_graph_digest"] != second.digest
        ):
            raise StructuralInconsistencyError(
                reason="Cached correspondence chemistry, population or axes changed; recalculate correspondences.",
                caller=caller,
            )
        if (
            result["method"] != method
            or result["rule_version"] != "declared_graph_isomorphism@1"
            or result["search_complete"] is not True
            or correspondence_digest(result) != result["correspondence_digest"]
        ):
            raise ArgumentError("correspondences", caller=caller)
        table = np.asarray(result["atom_correspondences"])
        witnesses = np.asarray(result["context_atom_correspondences"])
        if (
            table.ndim != 3
            or table.shape[1:] != (len(first.selected), 2)
            or witnesses.shape != (len(table), len(first.atoms), 2)
            or table.dtype.kind not in "iu"
            or witnesses.dtype.kind not in "iu"
        ):
            raise ArgumentError("correspondences", caller=caller)
        if not np.array_equal(
            result["selection_atom_indices"], first.selected
        ) or not np.array_equal(
            result["reference_selection_atom_indices"], second.selected
        ):
            raise ArgumentError("correspondences", caller=caller)
        rows = [tuple(row) for row in table[:, :, 1]]
        if rows != sorted(set(rows)):
            raise ArgumentError("correspondences", caller=caller)
        fixed = np.empty((0, 2), dtype=np.int64)
        if "search_scope" in result:
            fixed, candidates = prepare_constraints(
                first,
                second,
                result["fixed_atom_correspondence"],
                result["candidate_atom_correspondences"],
                caller,
            )
            expected_scope = (
                "supplied_atom_correspondences"
                if candidates is not None
                else "anchored_chemical_correspondences"
                if len(fixed)
                else "all_chemical_correspondences"
            )
            if result["search_scope"] != expected_scope or (
                candidates is not None and not np.array_equal(table, candidates)
            ):
                raise ArgumentError("correspondences", caller=caller)
        for projected, witness in zip(table, witnesses):
            if not np.array_equal(witness[:, 0], first.atoms) or not np.array_equal(
                projected, witness[first.selected_positions]
            ):
                raise ArgumentError("correspondences", caller=caller)
            if len(fixed) and not np.array_equal(
                witness[np.searchsorted(first.atoms, fixed[:, 0]), 1], fixed[:, 1]
            ):
                raise ArgumentError("correspondences", caller=caller)
            positions = np.searchsorted(second.atoms, witness[:, 1])
            if (
                np.any(positions >= len(second.atoms))
                or not np.array_equal(second.atoms[positions], witness[:, 1])
                or not first.admits(second, positions.tolist())
            ):
                raise ArgumentError("correspondences", caller=caller)
    except (KeyError, TypeError, ValueError, IndexError) as error:
        raise ArgumentError("correspondences", caller=caller) from error
