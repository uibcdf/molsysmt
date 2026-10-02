"""Providing state-specific formal-charge centers for general molecular workflows."""

import numpy as np
import pandas as pd
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.chemical_state import resolve_chemical_state
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.sparse_membership import pack_membership

from ._charge_centers import formal_charge_centers

_CALLER = "molsysmt.physchem.get_charge_centers"


@signal(tags=["api", "physchem"])
@arg_digest()
@resolve_chemical_state
def get_charge_centers(
    molecular_system,
    selection="all",
    definition="formal_charge",
    chemical_state="reference",
    structure_indices="all",
    assume_complete_connectivity=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Identifying formal-charge centers in a selected chemical state.

    Recognize carboxyl and guanidine motifs and combine directly covalently
    connected charged atoms. Omit groups whose formal charges sum to zero.
    Other nonzero formal charges remain explicitly labeled atomic centers.
    This bounded definition does not infer protonation, partial charges,
    aromatic delocalization, or every possible ionic functional group.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in a supported MolSysMT format with atom elements,
        complete declared connectivity, bond orders, and formal charges.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or integer array specifying atoms. A selection
        intersecting a center must include all its participant atoms.
    definition : str, default='formal_charge'
        Named recognition definition; only 'formal_charge' is supported.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        Chemical state used to resolve state-dependent attributes. Explicit
        states follow the native MolSysMT basic-query contract.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices used to resolve chemical_state='structure'; all
        requested structures must have the same assigned chemical state.
        Recognition computes chemistry once. Coordinate-based selections
        may read coordinates through the standard selection API.
    assume_complete_connectivity : bool, default=False
        Explicitly declare the supplied connectivity complete when the
        stored completeness metadata is unavailable or partial. This
        assumption is recorded and does not fill bonds or change the source.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Typed sparse membership: atom_indices and atom_offsets describe
        whole centers; geometry_atom_indices and geometry_atom_offsets
        describe distance-reference atoms. Carboxylate references are its
        oxygens, guanidinium references its nitrogens. charges is a quantity
        of shape (n_centers,) in elementary charge units. center_types labels
        the recognition rules. Metadata includes n_atoms, source_atom_indices,
        selection_atom_indices, examined_atom_indices, chemical_state_index,
        charge_source, definition, rule_version, evidence, and software.
        Indices are zero-based indices in the full source system, never IDs.
        Centers and their memberships are ordered by atom indices. Empty
        results have int64 membership arrays, offsets [0], and charges (0,).

    Raises
    ------
    ArgumentError
        If the definition or selection is invalid, including a cut center.
    StructuralInconsistencyError
        If chemistry is missing, connectivity is not declared complete,
        bond relationships/orders are unsupported, or no state is resolved.

    Notes
    -----
    Recognition examines the full state before selecting complete centers.
    Source charges are not modified or parameterized. Atomic/cluster labels
    are formal-charge evidence, not proof of a particular ionic interaction.
    The current rules do not group phosphate, sulfate, or aromatic ions.
    Coordinate geometry and periodic images belong to a subsequent detector.
    The returned dictionary is a chemical-feature result, not InteractionsDict.

    See Also
    --------
    molsysmt.basic.get
        Querying stored formal or partial charges.
    molsysmt.physchem.get_charge
        Getting named residue descriptors or OpenMM partial charges.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> from molsysmt.native import Topology
    >>> from molsysmt.physchem.get_charge_centers import get_charge_centers
    >>> molsys = Topology(n_atoms=2)
    >>> molsys.atoms['atom_type'] = ['Na', 'Cl']
    >>> msm.set(molsys, element='atom', formal_charge=[1, -1])
    >>> centers = get_charge_centers(
    ...     molsys, assume_complete_connectivity=True)
    >>> centers['atom_indices'].tolist()
    [0, 1]
    >>> puw.get_value(centers['charges'], to_unit='e').tolist()
    [1.0, -1.0]

    .. admonition:: User guide

       See :ref:`Getting charge centers <Tutorial_Get_charge_centers>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__
    from molsysmt.basic import convert, select
    from molsysmt.native import MolSys, Topology
    from molsysmt.physchem.atoms.mass import physical as elements

    if definition != "formal_charge":
        raise ArgumentError(argument="definition", value=definition, caller=_CALLER)
    if isinstance(molecular_system, MolSys):
        topology = molecular_system.topology
        if topology is None:
            raise StructuralInconsistencyError(
                reason="A topology domain is required.", caller=_CALLER
            )
    elif isinstance(molecular_system, Topology):
        topology = molecular_system
    else:
        topology = convert(molecular_system, to_form="molsysmt.Topology")

    state = topology._resolve_chemical_state()
    state_index = next(
        index for index, item in enumerate(topology._chemical_states) if item is state
    )
    n_atoms = len(topology.atoms)
    if (
        n_atoms
        and state.connectivity_completeness != "complete"
        and not assume_complete_connectivity
    ):
        raise StructuralInconsistencyError(
            reason="Charge-center recognition requires connectivity declared complete.",
            caller=_CALLER,
        )
    atom_elements = topology.atoms["atom_type"].to_numpy(dtype=object)
    if any(pd.isna(value) or value not in elements for value in atom_elements):
        raise StructuralInconsistencyError(
            reason="Every atom requires an explicit element symbol.", caller=_CALLER
        )
    if n_atoms and not topology._has_chemical_state_atom_attribute("formal_charge"):
        raise StructuralInconsistencyError(
            reason="Every atom requires an explicit formal charge.", caller=_CALLER
        )
    values = (
        topology._get_chemical_state_atom_attribute("formal_charge") if n_atoms else []
    )
    if any(pd.isna(value) for value in values):
        raise StructuralInconsistencyError(
            reason="Every atom requires an explicit formal charge.", caller=_CALLER
        )
    charges = np.asarray(values, dtype=np.int64)

    bonds = state.bonds
    if not len(bonds):
        bonds = bonds.reindex(
            columns=["bond_type", "bond_order", "atom1_index", "atom2_index"]
        )
    elif not {"bond_type", "atom1_index", "atom2_index"} <= set(bonds.columns):
        raise StructuralInconsistencyError(
            reason="Bond chemistry columns are missing.", caller=_CALLER
        )
    relationships = bonds["bond_type"]
    if (
        relationships.isna().any()
        or not relationships.isin(["covalent", "dative"]).all()
    ):
        raise StructuralInconsistencyError(
            reason="Every bond requires a covalent or dative relationship.",
            caller=_CALLER,
        )
    covalent = bonds.loc[relationships == "covalent"]
    pairs = covalent[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    orders = covalent.reindex(columns=["bond_order", "fractional_bond_order"])
    bond_orders = orders["bond_order"].to_numpy(
        dtype=np.float64, na_value=np.nan, copy=True
    )
    fractional = orders["fractional_bond_order"].to_numpy(
        dtype=np.float64, na_value=np.nan
    )
    missing_order = np.isnan(bond_orders)
    bond_orders[missing_order] = fractional[missing_order]
    if "is_aromatic" in covalent:
        bond_orders[covalent["is_aromatic"].fillna(False).to_numpy(dtype=bool)] = 1.5
    if not np.isfinite(bond_orders).all():
        raise StructuralInconsistencyError(
            reason="Every covalent bond requires an explicit bond order.",
            caller=_CALLER,
        )
    if np.any((bond_orders < 1) | (bond_orders > 6)):
        raise StructuralInconsistencyError(
            reason="Supported covalent bond orders range from 1 to 6.",
            caller=_CALLER,
        )
    if (
        np.any(pairs < 0)
        or np.any(pairs >= n_atoms)
        or np.any(pairs[:, 0] == pairs[:, 1])
    ):
        raise StructuralInconsistencyError(
            reason="Covalent bond endpoints must be distinct valid atom indices.",
            caller=_CALLER,
        )
    if len(np.unique(np.sort(pairs, axis=1), axis=0)) != len(pairs):
        raise StructuralInconsistencyError(
            reason="Duplicate covalent bond pairs are not supported.", caller=_CALLER
        )

    selected = np.unique(
        select(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
    )
    selected_set = set(selected.tolist())
    retained = []
    for center in formal_charge_centers(atom_elements, charges, pairs, bond_orders):
        members = set(center[0])
        if members & selected_set:
            if not members <= selected_set:
                raise ArgumentError(
                    argument="selection",
                    value=selection,
                    caller=_CALLER,
                    message="The selection cuts a compound charge center; include all participant atoms.",
                )
            retained.append(center)
    atom_indices, atom_offsets = pack_membership([center[0] for center in retained])
    geometry_indices, geometry_offsets = pack_membership(
        [center[1] for center in retained]
    )
    source_indices = np.arange(n_atoms, dtype=np.int64)
    return {
        "atom_indices": atom_indices,
        "atom_offsets": atom_offsets,
        "geometry_atom_indices": geometry_indices,
        "geometry_atom_offsets": geometry_offsets,
        "charges": puw.quantity(
            np.asarray([center[2] for center in retained], dtype=np.float64), "e"
        ),
        "center_types": np.asarray([center[3] for center in retained], dtype="U24"),
        "n_atoms": n_atoms,
        "source_atom_indices": source_indices,
        "selection_atom_indices": selected.astype(np.int64),
        "examined_atom_indices": source_indices.copy(),
        "chemical_state_index": state_index,
        "charge_source": "chemical_states.formal_charge",
        "definition": "formal_charge",
        "rule_version": "formal_charge_centers@1",
        "evidence": {
            "kind": "formal_charge",
            "connectivity_completeness": state.connectivity_completeness,
            "assume_complete_connectivity": assume_complete_connectivity,
            "chemical_state_provenance_index": state.provenance_index,
        },
        "software": {"molsysmt": __version__},
    }
