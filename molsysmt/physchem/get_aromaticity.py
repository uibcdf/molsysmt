"""Perceiving aromatic atom and bond flags without changing stored chemistry."""

import numpy as np
import pandas as pd
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_aromaticity(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="fused_ring_electron_count",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Perceiving aromatic flags on a complete graph before filtering source indices.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying elements, complete covalent connectivity,
        formal charges, closed-shell radical counts and supported bond orders.
        Missing aromatic flags may be perceived; known contradictions fail.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to return. Only bonds with both endpoints selected are included;
        perception uses the full chemical graph before selection.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selection.
        Perception uses chemical evidence, without coordinates.
    chemical_state : str or int, default='reference'
        Selected chemical state; 'structure' must resolve unambiguously.
    method : str, default='fused_ring_electron_count'
        RDKit's AROMATICITY_RDKIT model: environment-dependent electron
        contributions in rings and fused systems, evaluated against 4N+2.
        RDKit is an optional explicit implementation, not a fallback.
    syntax : str, default='MolSysMT'
        Syntax used to evaluate selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Source atom_indices, bond_indices, bonded_atom_pairs and aligned bool
        atom_is_aromatic and bond_is_aromatic arrays. Empty arrays have shapes
        (0,) and (0, 2). Metadata records the full evaluated source, state, model,
        chemical evidence, references and original producer versions. No units
        apply to indices or flags. No chemical assignments are attached.

    Raises
    ------
    ArgumentError
        If a method, atom selection, structure index or state is invalid.
    StructuralInconsistencyError
        If required chemistry is missing, unsupported or contradictory, provider
        perception fails, or the provider changes the source atom/bond inventory.

    Notes
    -----
    This experimental route supports closed-shell H/B/C/N/O/F/Si/P/S/Cl/Se/Br/Te/I
    graphs. It rejects query/dummy atoms, metals, dative relationships, radicals
    and missing formal charges or bond orders. Valence interpretation can use
    declared/provider implicit H; it never adds indexed atoms or changes the
    stored hydrogen inventory. Known formal charges, radicals and aromatic flags
    must survive perception. A bond joining two aromatic atoms need not be aromatic.
    Ring planarity and atom names are not evidence. The provider model is defined
    in the RDKit Book; it is not a universal definition of chemical aromaticity.
    Numeric H5MSM queries read chemistry without coordinates. Rich spatial
    selections can load coordinates. Optional Ackredit failures preserve results.

    See Also
    --------
    molsysmt.physchem.get_aromatic_rings : Get rings from stored aromatic flags.
    molsysmt.topology.get_substructure_matches : Match declared chemical graphs.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> result = msm.physchem.get_aromaticity(Chem.MolFromSmiles('c1ccccc1'))
    >>> result['atom_is_aromatic'].tolist()
    [True, True, True, True, True, True]
    >>> bool(result['bond_is_aromatic'].all())
    True

    .. admonition:: User guide

       See :ref:`Tutorial_Get_Aromaticity` for model evidence and scope.

    .. versionadded:: 1.0.0
    """
    from copy import deepcopy

    from rdkit import Chem, rdBase

    from molsysmt import __version__, _ackredit
    from molsysmt._private.atom_types import CHEMICAL_ATOM_TYPES
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get_form
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        detached_chemical_graph_view,
        select_chemical_atoms,
        validate_chemical_frames,
    )

    caller = "molsysmt.physchem.get_aromaticity"

    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=caller)

    def fail(reason):
        raise StructuralInconsistencyError(reason=reason, caller=caller)

    if method != "fused_ring_electron_count":
        raise ArgumentError("method", value=method, caller=caller)
    original, original_frames = molecular_system, structure_indices
    if get_form(molecular_system) == "rdkit.Mol":
        if any(atom.HasQuery() for atom in molecular_system.GetAtoms()) or any(
            bond.HasQuery() for bond in molecular_system.GetBonds()
        ):
            fail(
                "Aromaticity requires a concrete chemical graph, not query atoms or bonds."
            )
        molecular_system = Chem.Mol(molecular_system)
        original = molecular_system
    source, states, state, state_index, _, pairs, frames = chemical_graph_context(
        molecular_system, chemical_state, structure_indices, False, caller
    )
    frames = validate_chemical_frames(source, frames, caller)
    view = detached_chemical_graph_view(source, states, state_index, caller)
    symbols = view.topology.atoms["atom_type"]
    allowed = {
        "H",
        "B",
        "C",
        "N",
        "O",
        "F",
        "Si",
        "P",
        "S",
        "Cl",
        "Se",
        "Br",
        "Te",
        "I",
    }
    if not symbols.isin(CHEMICAL_ATOM_TYPES).all() or not symbols.isin(allowed).all():
        fail(
            "Aromaticity requires supported explicit element symbols; query atoms and metals are outside this route."
        )
    attrs, bonds = state.atom_attributes, state.bonds
    for field in ("formal_charge", "n_unpaired_electrons"):
        if states.n_atoms and (field not in attrs or attrs[field].isna().any()):
            fail(f"Aromaticity requires explicit {field} on every atom.")
    if states.n_atoms and attrs["n_unpaired_electrons"].ne(0).any():
        fail("Radical aromaticity is outside this closed-shell route.")
    if len(bonds) and (
        not bonds["bond_type"].eq("covalent").all()
        or not (
            bonds.get("bond_order", pd.Series(np.nan, index=bonds.index)).isin(
                [1, 2, 3]
            )
            | bonds.get("is_aromatic", pd.Series(False, index=bonds.index)).fillna(
                False
            )
        ).all()
    ):
        fail(
            "Aromaticity requires complete supported covalent bond orders; dative chemistry is outside this route."
        )
    try:
        molecule = convert(view, to_form="rdkit.Mol")
        Chem.Kekulize(molecule, clearAromaticFlags=True)
        Chem.SetAromaticity(molecule, Chem.AromaticityModel.AROMATICITY_RDKIT)
    except Exception as error:
        fail(f"Aromaticity perception failed on the unchanged source graph: {error}")
    if molecule.GetNumAtoms() != states.n_atoms or molecule.GetNumBonds() != len(bonds):
        fail("Aromaticity provider changed the source atom or bond inventory.")
    atom_flags = np.asarray(
        [atom.GetIsAromatic() for atom in molecule.GetAtoms()], dtype=bool
    )
    if any(
        atom.GetFormalCharge() != int(attrs["formal_charge"].iloc[i])
        or atom.GetNumRadicalElectrons() != 0
        for i, atom in enumerate(molecule.GetAtoms())
    ):
        fail(
            "Aromaticity provider changed declared formal charge or closed-shell chemistry."
        )
    bond_flags = []
    for left, right in pairs:
        bond = molecule.GetBondBetweenAtoms(int(left), int(right))
        if bond is None:
            fail("Aromaticity provider changed source connectivity.")
        bond_flags.append(bond.GetIsAromatic())
    bond_flags = np.asarray(bond_flags, dtype=bool)
    for frame, field, observed in [
        (attrs, "is_aromatic", atom_flags),
        (bonds, "is_aromatic", bond_flags),
    ]:
        if field in frame:
            known = frame[field].notna().to_numpy()
            if np.any(frame.loc[known, field].to_numpy(dtype=bool) != observed[known]):
                fail(
                    "Perceived aromaticity conflicts with known source aromatic flags."
                )
    rich = isinstance(selection, str) and not is_all(selection)
    selected = select_chemical_atoms(
        original if rich else source,
        states,
        state_index,
        selection,
        original_frames if rich else frames,
        syntax,
    )
    chosen_bonds = np.flatnonzero(np.isin(pairs, selected).all(axis=1))
    software = {"molsysmt": __version__, "rdkit": rdBase.rdkitVersion}
    reference = dict(
        id="rdkit-aromaticity-model",
        type="webpage",
        title="The RDKit Book: The RDKit Aromaticity Model",
        url="https://www.rdkit.org/docs/RDKit_Book.html#aromaticity",
        roles=["scientific_criterion"],
    )
    items = [reference] + [
        dict(
            id=f"software:{name}:{version}",
            type="software",
            **deepcopy(SOFTWARE[name]),
            version=version,
            roles=["executed_software"],
        )
        for name, version in software.items()
    ]
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    return dict(
        atom_indices=selected,
        bond_indices=chosen_bonds,
        bonded_atom_pairs=pairs[chosen_bonds],
        atom_is_aromatic=atom_flags[selected],
        bond_is_aromatic=bond_flags[chosen_bonds],
        evaluated_atom_indices=np.arange(states.n_atoms, dtype=np.int64),
        chemical_state_index=state_index,
        chemical_state_id=state.state_id,
        method=method,
        implementation="rdkit.AROMATICITY_RDKIT",
        evidence="declared_chemical_graph_with_provider_perception",
        software=software,
        references=[reference],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
