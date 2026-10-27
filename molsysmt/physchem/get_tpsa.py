"""Calculating topological polar surface area on complete molecular graphs."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    StructuralInconsistencyError,
)


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_tpsa(
    molecular_system,
    element="molecule",
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="ertl_rohde_selzer",
    include_sulfur_phosphorus=False,
    return_report=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Calculating Ertl topological polar surface areas for complete molecules.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form supplying complete chemistry,
        element symbols, hydrogen inventory and molecular membership.
    element : str, default='molecule'
        Only 'molecule' is supported. No fragment or whole-system sum is inferred.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Molecules to return. Numeric molecule indices preserve order and
        repetitions. String expressions identify whole molecules, never capped
        atom fragments, using the requested syntax.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices for spatial selection and chemical-state resolution.
        No structure axis is added to these graph-derived outputs.
    chemical_state : str or int, default='reference'
        Chemical state supplying charges, bonds and hydrogen counts. 'structure'
        must resolve to one state across the requested structures.
    method : str, default='ertl_rohde_selzer'
        Ertl, Rohde and Selzer (2000), executed through RDKit. No fallback runs.
    include_sulfur_phosphorus : bool, default=False
        Include polar S/P contributions in addition to N/O when True. False
        follows the conventional N/O-only RDKit/reference-program variant.
    return_report : bool, default=False
        Return a dictionary containing tpsa and a detached provenance report.
    syntax : str, default='MolSysMT'
        Selection syntax. External languages require their optional provider.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated arguments.

    Returns
    -------
    quantity or dict
        Area quantity with shape (n_selected_molecules,), standardized through
        PyUnitWizard (nm² by default). Empty selections retain shape (0,).
        With return_report=True, keys are tpsa and report; the report retains
        source molecule/atom indices, state, method, parameters and attribution.

    Raises
    ------
    ArgumentChoiceError
        If element requests a level other than molecule.
    ArgumentError
        If method, selections, state or other arguments are invalid.
    StructuralInconsistencyError
        If required chemistry is missing or contradictory, a selected molecule
        is disconnected, a bond crosses its boundary, or chemistry is outside
        the supported closed-shell organic profile.
    ImportError
        If the explicitly required optional RDKit provider is unavailable.

    Notes
    -----
    TPSA is a fitted topological descriptor, not geometric SASA, an observed
    conformation's exposed polar area or a permeability prediction. The original
    fragment contributions are in angstrom². N/O-only and N/O/S/P definitions
    differ; neither is universally superior. Charged graphs are allowed when
    supported by the model; protonation and tautomer states are never prepared.

    Complete closed-shell H/B/C/N/O/F/Si/P/S/Cl/Se/Br/Te/I graphs are admitted.
    Query/dummy atoms, metals, radicals and dative relationships are excluded.
    Declared indexed and nonindexed hydrogen counts must be available and
    preserved; missing counts are not guessed. Aromaticity is checked using
    the general aromaticity tool on detached selected chemistry. The input's
    atoms, assignments, coordinates and provider caches remain unchanged.

    Molecule membership belongs to the source topology; other chemical states
    cannot silently repartition it. Disconnected salt labels and covalent
    adducts crossing a selected molecule boundary fail. Several independent
    selected molecules produce separate values. Atom-level contributions and
    system-level aggregation are not exposed by this experimental boundary.
    Optional Ackredit credits the original model and actual executed software;
    completed empty selections retain provenance. Default quantity outputs
    carry no report; request return_report=True to retain scientific provenance.

    See Also
    --------
    molsysmt.physchem.get_sasa : Calculating geometric solvent-accessible areas.
    molsysmt.physchem.get_aromaticity : Checking state-specific aromaticity.
    molsysmt.topology.get_covalent_blocks : Finding covalently connected blocks.

    References
    ----------
    Ertl, P., Rohde, B. and Selzer, P. (2000). Fast Calculation of Molecular
    Polar Surface Area as a Sum of Fragment-Based Contributions and Its
    Application to the Prediction of Drug Transport Properties. Journal of
    Medicinal Chemistry 43, 3714–3717. doi:10.1021/jm000942e.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> area = msm.physchem.get_tpsa(Chem.MolFromSmiles('CCO'))
    >>> msm.pyunitwizard.get_value(area, to_unit='angstrom**2').round(2).tolist()
    [20.23]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_tpsa` for molecules, chemical states and units.

    .. versionadded:: 1.0.0
    """
    from copy import deepcopy

    from rdkit import Chem, rdBase
    from rdkit.Chem import rdMolDescriptors

    from molsysmt import __version__, _ackredit
    from molsysmt import pyunitwizard as puw
    from molsysmt._private.scientific_citations import ARTICLES, SOFTWARE
    from molsysmt.basic import convert, get
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        chemical_graph_digest,
        detached_chemical_graph_view,
        validate_chemical_frames,
    )

    caller = "molsysmt.physchem.get_tpsa"
    if element != "molecule":
        raise ArgumentChoiceError(
            argument="element", value=element, choices=["molecule"], caller=caller
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
            fail("TPSA requires source molecule indices and atom membership.")
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
        values, charges, checked = [], [], {}
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
                value, charge = checked[molecule_index]
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
                        fail(f"TPSA requires declared {field} for every selected atom.")
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
                value = float(
                    rdMolDescriptors.CalcTPSA(
                        molecule, force=True, includeSandP=include_sulfur_phosphorus
                    )
                )
                if not np.isfinite(value) or value < 0:
                    fail("The TPSA provider returned an invalid area.")
                charge = Chem.GetFormalCharge(molecule)
                checked[molecule_index] = value, charge
            values.append(value)
            charges.append(charge)
        result = puw.quantity(
            np.asarray(values, dtype=np.float64), "angstrom**2", standardized=True
        )
        software = {"molsysmt": __version__, "rdkit": rdBase.rdkitVersion}
        items = [
            dict(
                id="doi:10.1021/jm000942e",
                type="article",
                **deepcopy(ARTICLES["ertl_2000"]),
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
            return result
        offsets = np.concatenate(
            ([0], np.cumsum([len(atoms) for atoms in members]))
        ).astype(np.int64)
        return dict(
            tpsa=result,
            report=dict(
                schema="molsysmt.tpsa@1",
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
                parameters=dict(
                    include_sulfur_phosphorus=include_sulfur_phosphorus,
                    hydrogen_treatment="preserve_declared_inventory",
                    implementation="rdkit.CalcTPSA",
                ),
                software=software,
                attribution=dict(
                    schema="molsysmt.scientific_attribution@1",
                    target=caller,
                    items=items,
                ),
            ),
        )
