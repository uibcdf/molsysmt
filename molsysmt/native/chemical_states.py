"""Native collection of discrete chemical states."""

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError


class ChemicalStates:
    """Holding chemical states over one stable atom-index domain.

    The collection owns the state records. A state contains covalent bonds,
    atom-level chemical assignments, and state-local components. Topology
    compatibility access may refer to this collection, but it must not store
    a second copy of those records.

    Parameters
    ----------
    n_atoms : int, default=0
        Number of atoms in the collection's local index space.
    skip_digestion : bool, default=False
        Whether to skip internal argument validation.

    Notes
    -----
    A new standalone collection has no states. An ordinary native Topology
    creates one reference state for its historical compatibility behavior.

    Examples
    --------
    >>> import molsysmt as msm
    >>> states = msm.ChemicalStates(n_atoms=2)
    >>> states.n_chemical_states
    0
    >>> states.append_state()
    0
    >>> states.get_bonds().empty
    True

    .. versionadded:: 1.0.0
    """

    @arg_digest()
    def __init__(self, n_atoms=0, skip_digestion=False):
        self._n_atoms = int(n_atoms)
        if self._n_atoms < 0:
            raise StructuralInconsistencyError(
                reason="The chemical-state atom count must be nonnegative.",
                caller="molsysmt.native.ChemicalStates",
            )
        self._states = []
        self._reference_index = None

    @property
    def n_atoms(self):
        """Returning the cardinality of the local atom-index domain."""

        return self._n_atoms

    @property
    def n_chemical_states(self):
        """Returning the number of stored chemical states."""

        return len(self._states)

    @property
    def reference_chemical_state_index(self):
        """Returning the explicit or implicit reference-state index."""

        if len(self._states) == 1:
            return 0
        return self._reference_index

    def _resolve_index(self, state_index=None):
        if not self._states:
            raise StructuralInconsistencyError(
                reason="Chemical states are unavailable.",
                caller="molsysmt.native.ChemicalStates",
            )
        if state_index is None:
            state_index = self.reference_chemical_state_index
            if state_index is None:
                raise StructuralInconsistencyError(
                    reason=(
                        f"The collection has {len(self._states)} chemical states "
                        "and no reference state."
                    ),
                    caller="molsysmt.native.ChemicalStates",
                )
        if isinstance(state_index, (bool, np.bool_)) or not isinstance(
            state_index, (int, np.integer)
        ):
            raise StructuralInconsistencyError(
                reason="Chemical-state index must be an integer.",
                caller="molsysmt.native.ChemicalStates",
            )
        state_index = int(state_index)
        if not 0 <= state_index < len(self._states):
            raise StructuralInconsistencyError(
                reason=(
                    f"Chemical-state index {state_index} is invalid for "
                    f"{len(self._states)} states."
                ),
                caller="molsysmt.native.ChemicalStates",
            )
        return state_index

    def _replace_states(self, states, reference_index=None):
        """Replace state records after validating their shared atom domain."""

        states = list(states)
        for state in states:
            state._ensure_compatibility(self._n_atoms)
        if reference_index is not None:
            if isinstance(reference_index, (bool, np.bool_)) or not isinstance(
                reference_index, (int, np.integer)
            ):
                raise StructuralInconsistencyError(
                    reason="Reference chemical-state index must be an integer or None.",
                    caller="molsysmt.native.ChemicalStates",
                )
            reference_index = int(reference_index)
            if not 0 <= reference_index < len(states):
                raise StructuralInconsistencyError(
                    reason="Reference chemical-state index is outside the collection.",
                    caller="molsysmt.native.ChemicalStates",
                )
        self._states = states
        self._reference_index = reference_index

    def _append_state(self, state, set_as_reference=False):
        """Append one validated record and return its positional index."""

        state._ensure_compatibility(self._n_atoms)
        self._states.append(state)
        index = len(self._states) - 1
        if len(self._states) == 1 or set_as_reference:
            self._reference_index = index
        return index

    def _set_reference_index(self, state_index):
        """Select a reference state without changing the state inventory."""

        if state_index is not None:
            state_index = self._resolve_index(state_index)
        self._reference_index = state_index

    def _resize_atom_domain(self, n_atoms):
        """Update the atom domain after aligned state records have changed."""

        n_atoms = int(n_atoms)
        for state in self._states:
            state._ensure_compatibility(n_atoms)
        self._n_atoms = n_atoms

    @arg_digest()
    def append_state(self, skip_digestion=False):
        """Appending an empty chemical state to the collection.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Whether to skip internal argument validation.

        Returns
        -------
        int
            Index of the appended chemical state.

        Notes
        -----
        A state added to an empty collection becomes the reference state.
        Later states leave the current reference unchanged.

        .. versionadded:: 1.0.0
        """

        from .topology import _ChemicalStateStorage

        return self._append_state(_ChemicalStateStorage(n_atoms=self._n_atoms))

    @arg_digest()
    def get_bonds(self, chemical_state="reference", skip_digestion=False):
        """Returning covalent bonds from one chemical state.

        Parameters
        ----------
        chemical_state : int or {'reference'}, default='reference'
            State index or the reference state.
        skip_digestion : bool, default=False
            Whether to skip internal argument validation.

        Returns
        -------
        pandas.DataFrame
            Bond table owned by the selected state.

        .. versionadded:: 1.0.0
        """

        state_index = None if chemical_state == "reference" else chemical_state
        return self._states[self._resolve_index(state_index)].bonds

    @arg_digest()
    def get_preparation_history(self, chemical_state="reference", skip_digestion=False):
        """Returning historical preparation evidence from one chemical state.

        Parameters
        ----------
        chemical_state : int or {'reference'}, default='reference'
            State index or the reference state.
        skip_digestion : bool, default=False
            Whether to skip internal argument validation.

        Returns
        -------
        tuple of dict
            Independent records in append order, empty if none were recorded.
            Each envelope declares ``index_scope='operation'`` and original
            output dimensions. Its report retains original indices, units,
            template declarations and producer versions.

        Notes
        -----
        These records describe past operations. Extraction, reordering, merging
        and later edits retain their original index domains; they do not remap
        report indices or certify current assignments. Do not use a historical
        report index directly to address the current system. Successful template
        application, fixed-state H generation and terminal attachment record
        evidence automatically, including successful no-addition operations.
        Geometry reports declare their original structure indices and counts.

        Examples
        --------
        >>> import molsysmt as msm
        >>> states = msm.ChemicalStates(n_atoms=2)
        >>> states.append_state()
        0
        >>> states.get_preparation_history()
        ()

        .. versionadded:: 1.0.0
        """
        from copy import deepcopy

        state_index = None if chemical_state == "reference" else chemical_state
        state = self._states[self._resolve_index(state_index)]
        return tuple(deepcopy(getattr(state, "_preparation_history", [])))

    @arg_digest()
    def append_preparation_history(
        self, preparation_history, chemical_state="reference", skip_digestion=False
    ):
        """Appending caller-declared historical records to one chemical state.

        Parameters
        ----------
        preparation_history : list or tuple of dict
            Versioned operation envelopes returned by get_preparation_history.
            Records must use supported scalar, mapping, sequence and typed-array
            values. Their original output dimensions need not match this state.
        chemical_state : int or {'reference'}, default='reference'
            Destination state index or the reference state.
        skip_digestion : bool, default=False
            Whether to skip internal argument validation.

        Returns
        -------
        tuple of int
            Positional indices of the appended records, empty for empty input.

        Raises
        ------
        ArgumentError
            If envelopes or serialized value types are unsupported.
        StructuralInconsistencyError
            If the destination state is unavailable or ambiguous.

        Notes
        -----
        This archives independent copies of declared evidence. It does not apply
        chemistry, align atoms or structures, verify source authenticity, or credit
        a new calculation. Retain intervening maps separately. Records keep their
        original operation indices; repeated records are appended in input order.
        Invalid input leaves the history unchanged. H5MSM and ChemicalStatesDict
        preserve the imported records. The supported template, H-generation and
        attachment reports contain no coordinate snapshots.

        See Also
        --------
        get_preparation_history : Retrieve independent historical records.

        Examples
        --------
        >>> import molsysmt as msm
        >>> states = msm.ChemicalStates(n_atoms=1)
        >>> states.append_state()
        0
        >>> states.append_preparation_history(())
        ()

        .. admonition:: User guide

           See :ref:`Tutorial_Chemical_Templates` and
           :ref:`Tutorial_Fixed_State_Hydrogens` for historical evidence and scope.

        .. versionadded:: 1.0.0
        """
        from copy import deepcopy

        state_index = None if chemical_state == "reference" else chemical_state
        state = self._states[self._resolve_index(state_index)]
        records = deepcopy(list(preparation_history))
        start = len(state._preparation_history)
        state._preparation_history.extend(records)
        return tuple(range(start, start + len(records)))

    def copy(self):
        """Returning an independent copy of the collection."""

        clone = ChemicalStates(n_atoms=self._n_atoms, skip_digestion=True)
        clone._replace_states(
            [state.copy() for state in self._states], self._reference_index
        )
        return clone

    def _extract_atoms(self, atom_indices):
        """Return states remapped to one ordered subset of the atom axis."""

        from .topology import Topology, _ChemicalStateStorage

        atoms = np.asarray(atom_indices)
        if atoms.size == 0:
            atoms = np.asarray(atom_indices, dtype=np.int64)
        if (
            atoms.ndim != 1
            or atoms.dtype.kind not in "iu"
            or np.any(atoms < 0)
            or np.any(atoms >= self._n_atoms)
            or np.unique(atoms).size != atoms.size
        ):
            raise ValueError("atom_indices must be unique valid integer indices.")
        atoms = atoms.astype(np.int64, copy=False)
        atom_map = {int(old): new for new, old in enumerate(atoms)}
        extracted_states = []
        for source_state in self._states:
            source_state._ensure_compatibility(self._n_atoms)
            membership = source_state.component_indices.iloc[atoms].copy()
            old_components = membership.dropna().unique().tolist()
            component_map = {old: new for new, old in enumerate(old_components)}
            components = source_state.components.iloc[old_components].copy()
            components.reset_index(drop=True, inplace=True)
            membership = membership.map(component_map).astype("Int64")
            membership.reset_index(drop=True, inplace=True)

            bonds = source_state.bonds
            kept = np.isin(bonds["atom1_index"], atoms) & np.isin(
                bonds["atom2_index"], atoms
            )
            bonds = bonds[kept].copy()
            bonds.reset_index(drop=True, inplace=True)
            bonds = Topology._remap_bond_atom_indices(bonds, atom_map)
            state = _ChemicalStateStorage(
                n_atoms=len(atoms),
                bonds=Topology._coerce_bond_table(bonds, n_atoms=len(atoms)),
                components=components,
                component_indices=membership,
                state_id=source_state.state_id,
                connectivity_completeness=source_state.connectivity_completeness,
                component_completeness=source_state.component_completeness,
                component_evidence=source_state.component_evidence,
                provenance_index=source_state.provenance_index,
                preparation_history=source_state._preparation_history,
            )
            state.atom_attributes = source_state.atom_attributes.iloc[atoms].copy()
            state.atom_attributes.reset_index(drop=True, inplace=True)
            state._normalize_atom_attribute_columns()
            extracted_states.append(state)

        result = ChemicalStates(n_atoms=len(atoms), skip_digestion=True)
        result._replace_states(extracted_states, self._reference_index)
        return result
