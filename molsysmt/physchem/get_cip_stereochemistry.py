"""Analyzing tetrahedral and double-bond stereochemistry through explicit CIP rules."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
def get_cip_stereochemistry(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    engine="rdkit",
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    from_coordinates=False,
):
    """Getting accurate CIP labels from declared stereo or one selected 3D structure.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying chemical elements, complete connectivity,
        explicit charges and bond orders. SDF source hydrogen atoms are retained.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atoms to include in the result. The full graph is analyzed first;
        only bonds with both endpoints in the selection are returned.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based) for state resolution and spatial selections.
        Coordinate inference requires exactly one selected structure.
    chemical_state : str or int, default='reference'
        Selected chemical state; 'structure' must resolve to one state.
    engine : str, default='rdkit'
        Explicit optional provider implementing the Hanson et al. 2018 CIP
        algorithm. Missing RDKit raises; no alternative engine is selected.
    syntax : str, default='MolSysMT'
        Syntax used for selection.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.
    from_coordinates : bool, default=False
        Keyword-only flag to infer tetrahedral and double-bond stereo from
        exactly one nonperiodic 3D conformer, replacing its declared tags on a copy.

    Returns
    -------
    dict
        Source atom_indices, bond_indices, bonded_atom_pairs and aligned
        atom_stereochemistry/bond_stereochemistry arrays. None means no assigned
        CIP label. bond_stereo_atom_indices contains RDKit reference atoms,
        with [-1, -1] for unassigned bonds. It is not a priority-ranking table.
        bond_reference_stereochemistry gives cis/trans relative to those atoms,
        independently of the absolute E/Z labels.
        Empty arrays retain (0,), (0, 2) shapes. Metadata identifies method,
        provider/software versions, selected state, evidence and references.

    Raises
    ------
    ArgumentError
        If a provider, selection or structure request is invalid.
    StructuralInconsistencyError
        If chemistry is incomplete, assignment fails, a non-tetrahedral
        descriptor is encountered or coordinate inference lacks one conformer.
    FormatError
        If an SDF source uses unsupported query or enhanced stereo encodings.

    Notes
    -----
    Uses rdCIPLabeler.AssignCIPLabels, implementing Hanson et al. (2018),
    DOI 10.1021/acs.jcim.8b00324. The scientific method is distinct from the
    optional RDKit provider. The function changes neither source labels,
    reference state, hydrogens nor coordinates. Full-graph CIP assignment
    precedes selection. It does not reconstruct periodic molecules: supply
    compatible compact coordinates before requesting geometry inference.
    Explicit SDF directions are interpreted by the provider; query, enhanced
    stereo and unsupported relative-only encodings remain rejected.

    See Also
    --------
    molsysmt.topology.get_substructure_matches : Query a complete chemical graph.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> result = msm.physchem.get_cip_stereochemistry(Chem.MolFromSmiles('N[C@@H](C)C(=O)O'))
    >>> result['atom_stereochemistry'].tolist()
    [None, 'S', None, None, None, None]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_CIP_stereochemistry` for evidence and selection rules.

    .. versionadded:: 1.0.0
    """
    from rdkit import Chem, rdBase

    from molsysmt import __version__
    from molsysmt._private.stereochemistry import (
        REFERENCE,
        assign_cip,
        molecule_from_sdf,
        native_labels,
    )
    from molsysmt.basic import convert, get_form
    from molsysmt.native import MolSys, Topology
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    caller = "molsysmt.physchem.get_cip_stereochemistry"
    original_source, original_frames = molecular_system, structure_indices
    if engine != "rdkit":
        raise ArgumentError("engine", value=engine, caller=caller)
    form = get_form(molecular_system)
    if form == "file:sdf":
        if chemical_state != "reference" and chemical_state != 0:
            raise ArgumentError("chemical_state", value=chemical_state, caller=caller)
        from molsysmt.form.file_sdf._native import to_native

        record, molecule = molecule_from_sdf(molecular_system)
        source = to_native(record, discard_properties=True)
        state_index = 0
        states, state = source.chemical_states, source.chemical_states._states[0]
        frames = structure_indices
    else:
        # Existing RDKit-to-native adapters assign properties. Use a detached
        # molecule before any dispatch so the public analysis remains read-only.
        source_input = (
            Chem.Mol(molecular_system) if form == "rdkit.Mol" else molecular_system
        )
        source, states, state, state_index, _, _, frames = chemical_graph_context(
            source_input, chemical_state, structure_indices, False, caller
        )
        if form == "rdkit.Mol":
            molecule = Chem.Mol(source_input)
        else:
            topology = (
                source.topology
                if isinstance(source, MolSys)
                else source
                if isinstance(source, Topology)
                else convert(source, to_form="molsysmt.Topology")
            )
            if topology is None:
                raise StructuralInconsistencyError(
                    reason="CIP analysis needs a chemical element inventory.",
                    caller=caller,
                )
            if states.n_atoms and (
                "formal_charge" not in state.atom_attributes
                or state.atom_attributes["formal_charge"].isna().any()
            ):
                raise StructuralInconsistencyError(
                    reason="CIP analysis needs explicit formal charges.", caller=caller
                )
            from molsysmt._private.atom_types import CHEMICAL_ATOM_TYPES

            if not topology.atoms["atom_type"].isin(CHEMICAL_ATOM_TYPES).all():
                raise StructuralInconsistencyError(
                    reason="CIP analysis needs explicit chemical element symbols, not force-field types or guessed atom names.",
                    caller=caller,
                )
            covalent = state.bonds.loc[state.bonds["bond_type"].eq("covalent")]
            import pandas as pd

            known_order = covalent["bond_order"].isin([1, 2, 3]) | covalent.get(
                "is_aromatic", pd.Series(False, index=covalent.index)
            ).fillna(False)
            if not known_order.all():
                raise StructuralInconsistencyError(
                    reason="CIP analysis needs explicit supported covalent bond orders.",
                    caller=caller,
                )
            view = object.__new__(type(topology))
            view.__dict__ = topology.__getstate__()
            state_view = states.copy()
            state_view._reference_index = state_index
            view._chemical_states_domain = state_view
            chemical_source = MolSys._from_partial_domains(
                topology=view, chemical_states=state_view
            )
            molecule = convert(chemical_source, to_form="rdkit.Mol")
    if any(
        atom.HasQuery() or atom.GetAtomicNum() == 0 for atom in molecule.GetAtoms()
    ) or any(bond.HasQuery() for bond in molecule.GetBonds()):
        raise StructuralInconsistencyError(
            reason="CIP analysis requires a concrete chemical graph, not query or dummy atoms/bonds.",
            caller=caller,
        )
    if any(
        atom.GetChiralTag()
        not in {
            Chem.ChiralType.CHI_UNSPECIFIED,
            Chem.ChiralType.CHI_TETRAHEDRAL_CW,
            Chem.ChiralType.CHI_TETRAHEDRAL_CCW,
        }
        for atom in molecule.GetAtoms()
    ):
        raise StructuralInconsistencyError(
            reason="Only tetrahedral atom stereo is supported by this analysis.",
            caller=caller,
        )
    from molsysmt.basic._index_validation import validate_structure_indices

    frames = validate_structure_indices(source, frames, caller)
    structure_index = None
    if from_coordinates:
        coordinate_source = convert(
            source if form == "file:sdf" else original_source,
            to_form="molsysmt.Structures",
            structure_indices=original_frames,
        )
        coordinates = coordinate_source.coordinates
        if coordinates is None or coordinates.shape[0] != 1:
            raise StructuralInconsistencyError(
                reason="Coordinate stereo inference requires exactly one selected structure.",
                caller=caller,
            )
        from molsysmt import pyunitwizard as puw

        values = np.asarray(puw.get_value(coordinates, to_unit="angstrom"), dtype=float)
        if (
            values.shape != (1, molecule.GetNumAtoms(), 3)
            or not np.isfinite(values).all()
        ):
            raise StructuralInconsistencyError(
                reason="Stereo inference needs finite coordinates.", caller=caller
            )
        molecule.RemoveAllConformers()
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(values[0])
        conformer.Set3D(True)
        molecule.AddConformer(conformer)
        Chem.AssignStereochemistryFrom3D(molecule, confId=0, replaceExistingTags=True)
        structure_index = (
            0
            if original_frames is None or isinstance(original_frames, str)
            else int(np.asarray(original_frames).reshape(-1)[0])
        )
    assign_cip(molecule)
    atom_labels, _ = native_labels(molecule)
    indices = select_chemical_atoms(
        source, states, state_index, selection, frames, syntax
    )
    bonds = state.bonds
    pairs = (
        bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
        if len(bonds)
        else np.empty((0, 2), dtype=np.int64)
    )
    bond_indices = np.flatnonzero(np.isin(pairs, indices).all(axis=1))
    labels, references, relative_labels = [], [], []
    for left, right in pairs[bond_indices]:
        bond = molecule.GetBondBetweenAtoms(int(left), int(right))
        if bond is None:
            raise StructuralInconsistencyError(
                reason="Stereo provider connectivity differs from the source graph.",
                caller=caller,
            )
        label = bond.GetProp("_CIPCode") if bond.HasProp("_CIPCode") else None
        reference = list(bond.GetStereoAtoms()) if label is not None else [-1, -1]
        if label is not None and len(reference) != 2:
            raise StructuralInconsistencyError(
                reason="A labeled double bond needs two reference atoms.", caller=caller
            )
        if bond.GetBeginAtomIdx() != left:
            reference.reverse()
        labels.append(label)
        references.append(reference)
        relative_labels.append(
            {
                Chem.BondStereo.STEREOCIS: "cis",
                Chem.BondStereo.STEREOTRANS: "trans",
                Chem.BondStereo.STEREOE: "trans",
                Chem.BondStereo.STEREOZ: "cis",
            }.get(bond.GetStereo())
            if label is not None
            else None
        )
    result = {
        "atom_indices": indices,
        "bond_indices": bond_indices,
        "bonded_atom_pairs": pairs[bond_indices],
        "atom_stereochemistry": np.asarray(atom_labels, dtype=object)[indices],
        "bond_stereochemistry": np.asarray(labels, dtype=object),
        "bond_reference_stereochemistry": np.asarray(relative_labels, dtype=object),
        "bond_stereo_atom_indices": np.asarray(references, dtype=np.int64).reshape(
            -1, 2
        ),
        "n_atoms": molecule.GetNumAtoms(),
        "chemical_state_index": state_index,
        "structure_index": structure_index,
        "method": "hanson_2018",
        "engine": engine,
        "evidence": "coordinates" if from_coordinates else "declared_stereochemistry",
        "software": {"molsysmt": __version__, "rdkit": rdBase.rdkitVersion},
        "references": [dict(REFERENCE)],
    }
    from copy import deepcopy

    from molsysmt import _ackredit
    from molsysmt._private.scientific_citations import SOFTWARE

    items = [dict(REFERENCE, roles=["scientific_criterion"])]
    for name, version in result["software"].items():
        items.append(
            dict(
                id=f"software:{name}:{version}",
                type="software",
                **deepcopy(SOFTWARE.get(name, dict(title=name))),
                version=version,
                roles=["executed_software"],
            )
        )
    result["attribution"] = dict(
        schema="molsysmt.scientific_attribution@1", target=caller, items=items
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    return result
