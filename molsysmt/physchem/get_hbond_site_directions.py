"""Derive explicit local direction hypotheses from declared hydrogen-bond sites."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed


@signal(tags=["api", "physchem"])
@arg_digest()
@dep_digest("rdkit")
@attributed("hbond_site_directions")
def get_hbond_site_directions(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    method="ideal_local_geometry",
    site_method="smarts_donor_acceptor",
    assume_complete_connectivity=False,
    pbc=True,
    syntax="MolSysMT",
    heavy_mode="auto",
    skip_digestion=False,
    *,
    max_matches=100000,
):
    """Getting observed donor directions and bounded ideal acceptor hypotheses.

    Recognition and geometry are separate: sites retains the chemical rule,
    while method names the directional model. No source domain is modified.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates, elements, complete covalent
        connectivity, formal charges, bond orders and aromatic atom/bond flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Both donor and indexed hydrogen must be selected;
        an acceptor anchor must be selected. Supporting neighbors can lie outside
        selection because recognition uses the complete source graph.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source structure indices (0-based). Preserve order and repetitions;
        direction_structure_positions distinguishes repeated indices.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        Declared state used for recognition. Structure-assigned states must
        resolve to one state across the selected structures.
    method : str, default='ideal_local_geometry'
        Observed donor-to-H vectors; two ideal trigonal directions for ordinary
        aldehyde/ketone/amide carbonyl O; opposite neighbor bisector for
        pyridine-like N; opposite N-to-C vector for neutral nitrile N.
    site_method : str, default='smarts_donor_acceptor'
        Recognition rule accepted by get_hbond_sites. Elemental rules can
        recognize additional unsuitable atoms; they do not expand geometry
        coverage. RDKit is required for this profile's environment matching.
    assume_complete_connectivity : bool, default=False
        Explicitly assume supplied connectivity complete when metadata is
        insufficient, without changing the declared source chemistry.
    pbc : bool, default=True
        Apply minimum-image bond vectors when a source box is present. Support
        images use row-vector boxes and reference the site anchor (image zero).
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Execute projected geometry in bounded blocks, force streaming, or use
        bounded eager delivery. Resident output must fit the RAM estimate.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum matches per chemical SMARTS query, before selection.
        Exceeding the limit raises instead of returning truncated sites.

    Returns
    -------
    dict
        Static site_atom_indices, site_roles, site_models and CSR support atoms;
        evaluated_structure_indices and uint8 status (n_structures, n_sites);
        sparse directions (n_directions, 3), dimensionless and normalized;
        origins with configured length units; aligned direction_site_indices,
        direction_structure_indices, direction_structure_positions and local
        direction_indices. image_offsets indexes packed int32 image_vectors for
        each direction's support atoms. Metadata defines all codes, geometry,
        source axes, selected chemistry, evidence, versions and attribution.
        Empty directions have shape (0, 3). Unsupported or undefined sites
        contribute status entries but no finite directional records.

    Raises
    ------
    ArgumentError
        If the method, recognition rule, selection, state or indices are invalid.
    StructuralInconsistencyError
        If required chemistry/coordinates are missing, nonfinite or inconsistent,
        or a periodic box is singular.
    MemoryBudgetExceededError
        If estimated resident numeric output or eager work exceeds the budget.
    UnsupportedHeavyOperationError
        If streaming is unavailable, a block cannot fit, or a match limit is exceeded.

    Notes
    -----
    Experimental geometric hypotheses, not electronic orbitals or an optimized
    hydrogen network. Unsupported acceptors include esters, acids/carboxylates,
    amines, ether/alcohol/water O, sulfur/phosphorus and metal-bound atoms.
    Missing indexed plane references and coincident/collinear supporting atoms
    are undefined geometry. No arbitrary axis or virtual hydrogen is invented.
    The carbonyl reference is the lowest-index heavy covalent substituent of C,
    otherwise its lowest-index indexed hydrogen. Its projected bond sets local
    direction 0; direction 1 uses the opposite transverse sign.

    Finite status is per site and structure, not a claim of chemical validity
    beyond the declared recognition rule. Numerical degeneracy uses a 1e-12
    dimensionless vector-sum/projection threshold. Images are those actually
    used by the shared get_vectors kernel, composed along carbonyl O-C-substituent bonds.
    Execution estimates include status, sparse packing and unit presentation;
    source graphs/Python overhead are outside the estimate, which is not an RSS
    guarantee. Results are detached dictionaries, never attached automatically
    to MolSys.interactions. Optional Ackredit records completed calculations.

    See Also
    --------
    molsysmt.physchem.get_hbond_sites
        Recognizing sites without requiring coordinates.
    molsysmt.structure.get_vectors
        Calculating general vectors and their observed periodic images.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molecule = Chem.MolFromSmiles('C#N')
    >>> conformer = Chem.Conformer(2)
    >>> conformer.SetAtomPosition(0, (0, 0, 0))
    >>> conformer.SetAtomPosition(1, (1, 0, 0))
    >>> _ = molecule.AddConformer(conformer)
    >>> result = msm.physchem.get_hbond_site_directions(molecule, pbc=False)
    >>> result['directions'].tolist()
    [[1.0, -0.0, -0.0]]

    .. admonition:: User guide

       See :ref:`Getting hydrogen-bond site directions <Tutorial_Get_hbond_site_directions>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import configure
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get
    from molsysmt.physchem import get_hbond_sites
    from molsysmt.physchem._hbond_directions import DirectionReducer, build_site_plan
    from molsysmt.topology._chemical_graph import validate_chemical_frames

    caller = "molsysmt.physchem.get_hbond_site_directions"
    structure_indices = validate_chemical_frames(
        molecular_system, structure_indices, caller
    )
    dimensions = modular_h5msm_dimensions(molecular_system)
    frames = (
        np.arange(
            dimensions[1]
            if dimensions is not None
            else get(molecular_system, n_structures=True),
            dtype=np.int64,
        )
        if structure_indices is None or is_all(structure_indices)
        else np.asarray(structure_indices, dtype=np.int64)
    )
    sites = get_hbond_sites(
        molecular_system,
        selection=selection,
        structure_indices=frames,
        chemical_state=chemical_state,
        method=site_method,
        assume_complete_connectivity=assume_complete_connectivity,
        syntax=syntax,
        max_matches=max_matches,
    )
    plan = build_site_plan(
        molecular_system, sites, assume_complete_connectivity, max_matches
    )
    periodic = pbc
    reducer = DirectionReducer(plan, sites, frames, periodic, configure.max_ram_usage)
    if not len(frames) or not len(plan["edges"]):
        return reducer.finalize()
    per_frame_bytes = max(
        1,
        len(plan["universe"]) * 96
        + len(plan["edges"]) * 192
        + len(plan["slot_sites"]) * 384
        + 1024,
    )
    return execute_projected_geometry(
        molecular_system,
        universe=plan["universe"],
        frames=frames,
        reducer=reducer,
        per_frame_bytes=per_frame_bytes,
        pbc=periodic,
        heavy_mode=heavy_mode,
        caller=caller,
    )
