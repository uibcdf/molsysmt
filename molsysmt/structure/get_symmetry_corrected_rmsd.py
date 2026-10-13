"""Computing chemically constrained pose RMSD in the original Cartesian axes."""

from copy import deepcopy

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    StructuralInconsistencyError,
)
from molsysmt.configure import with_configure_overrides


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
@dep_digest("rdkit")
def get_symmetry_corrected_rmsd(
    molecular_system,
    selection='atom_type!="H"',
    structure_indices="all",
    reference_molecular_system=None,
    reference_selection=None,
    reference_structure_index=0,
    chemical_state="reference",
    reference_chemical_state="reference",
    correspondences=None,
    baseline_atom_correspondence=None,
    method="declared_graph_isomorphism",
    max_matches=100000,
    tie_tolerance="1e-12 nm",
    syntax="MolSysMT",
    heavy_mode="auto",
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """Computing minimum positional RMSD over admitted chemical correspondences.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates and a complete fixed chemical graph.
    selection : str, list, tuple or numpy.ndarray, default='atom_type!="H"'
        Nonempty RMSD population within one complete covalent component.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Query structure indices. Order and repetitions are preserved.
    reference_molecular_system : molecular system or None, default=None
        Reference system sharing the Cartesian coordinate axes; None uses the query.
    reference_selection : str, list, tuple, numpy.ndarray or None, default=None
        Reference RMSD population; None uses selection.
    reference_structure_index : int, default=0
        One reference structure index (0-based), independent of its ID.
    chemical_state : str or int, default='reference'
        Query fixed state; 'structure' requires one resolved state.
    reference_chemical_state : str or int, default='reference'
        Reference fixed state, resolved at reference_structure_index.
    correspondences : dict or None, default=None
        Reusable result from get_atom_correspondences. Graphs, populations,
        axes, witnesses and consistency digest are checked before reuse.
    baseline_atom_correspondence : list, tuple, numpy.ndarray or None, default=None
        Explicit original query/reference source-index pairs, shape (n_selected, 2).
        Produces a separate raw positional RMSD. None reports raw_rmsd=None;
        equal axis sizes or atom IDs do not declare original correspondence.
    method : str, default='declared_graph_isomorphism'
        Exact declared-state graph profile used to admit chemical equivalences.
    max_matches : int, default=100000
        Candidate enumeration bound when constructing correspondences.
    tie_tolerance : quantity or str, default='1e-12 nm'
        Nonnegative absolute length tolerance for counting near-optimal mappings.
        The chosen mapping always attains the actual computed minimum.
    syntax : str, default='MolSysMT'
        Selection syntax for both systems.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Projected coordinate delivery policy; forced streaming requires support.
    parallel : bool or None, default=None
        Whether to override the session's Rust CPU parallelization policy.
    num_threads : int or None, default=None
        Rust worker count, or None for the configured session value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        rmsd and optional raw_rmsd length quantities in the session's standard
        unit, int64 structure_indices, reference_structure_index,
        correspondence_indices selecting rows of the shared correspondence table,
        n_near_optimal_correspondences, graph/result provenance and detached
        bibliography. An empty structure request returns typed empty arrays.

    Raises
    ------
    ArgumentError
        If populations, baseline maps, cached results or indices are invalid.
    StructuralInconsistencyError
        If chemistry is unsupported/incompatible, coordinates are nonfinite,
        or cached correspondences no longer match current chemistry.
    MemoryBudgetExceededError
        If resident results or numeric working estimates exceed configured RAM.
    UnsupportedHeavyOperationError
        If matching exceeds its bound or the form cannot supply forced streaming.

    Notes
    -----
    Experimental MolSysMT implementation inspired by Bell and Zhang (2019) and
    Meli and Biggin (2020); neither external algorithm is reproduced faithfully.
    RDKit executes graph matching; the bundled Rust positional RMSD kernels
    evaluate admitted maps. Coordinates are never rotated, translated, centered,
    reflected or periodically imaged. Prepare whole periodic molecules explicitly
    and retain a common receptor coordinate frame before comparison.
    Exact ties choose the lexically first source-index mapping. Near ties are
    reported without replacing the actual minimum. Complete chemical context is
    retained when H or other atoms are omitted from the RMSD population.
    Both graphs require the same indexed-H representation; H materialization
    and implicit-H policy normalization are separate preparation operations.
    Candidate construction and coordinate chunks are bounded separately; chemistry
    objects and total process RSS are outside numeric working estimates. No
    coordinate-by-mapping tensor or disk-backed output is created. Reading a saved
    dictionary preserves its original producer attribution without recording new use.

    Assigned stereo uses RDKit's implementation of the Hanson et al. (2018) CIP
    algorithm, DOI 10.1021/acs.jcim.8b00324, through the shared stereo helper.
    This executed scientific criterion is credited separately from RMSD inspiration.

    See Also
    --------
    molsysmt.topology.get_atom_correspondences
        Build reusable correspondences without coordinates.
    get_rmsd
        Compute positional RMSD for the given atom ordering.
    get_least_rmsd
        Compute RMSD after optimal superposition.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molsys = Chem.MolFromMolFile(msm.systems['caffeine']['caffeine.sdf'])
    >>> result = msm.structure.get_symmetry_corrected_rmsd(molsys)
    >>> result['rmsd'].shape
    (1,)

    .. admonition:: User guide

       See :ref:`Tutorial_Get_symmetry_corrected_rmsd`.

    .. versionadded:: 1.0.0
    """
    from rdkit import rdBase

    from molsysmt import __version__, configure
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.scientific_attribution import attach_graph_attribution
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get
    from molsysmt.topology import get_atom_correspondences
    from molsysmt.topology._atom_correspondences import (
        ChemicalGraph,
        validate_correspondence_result,
    )

    from ._symmetry_rmsd import SymmetryRMSDReducer

    caller = "molsysmt.structure.get_symmetry_corrected_rmsd"
    reference = (
        molecular_system
        if reference_molecular_system is None
        else reference_molecular_system
    )
    reference_selection = (
        selection if reference_selection is None else reference_selection
    )
    dimensions = modular_h5msm_dimensions(molecular_system)
    n_structures = int(
        dimensions[1]
        if dimensions is not None
        else get(molecular_system, n_structures=True)
    )
    frames = (
        np.arange(n_structures, dtype=np.int64)
        if structure_indices is None or is_all(structure_indices)
        else np.asarray(structure_indices, dtype=np.int64)
    )
    if frames.ndim != 1 or np.any((frames < 0) | (frames >= n_structures)):
        raise ArgumentError("structure_indices", caller=caller)
    reference_count = int(get(reference, n_structures=True))
    if (
        isinstance(reference_structure_index, (bool, np.bool_))
        or not 0 <= reference_structure_index < reference_count
    ):
        raise ArgumentError("reference_structure_index", caller=caller)
    if correspondences is None:
        correspondences = get_atom_correspondences(
            molecular_system,
            selection=selection,
            structure_indices=frames,
            reference_molecular_system=reference,
            reference_selection=reference_selection,
            reference_structure_indices=[reference_structure_index],
            chemical_state=chemical_state,
            reference_chemical_state=reference_chemical_state,
            method=method,
            max_matches=max_matches,
            syntax=syntax,
        )
    else:
        first = ChemicalGraph(
            molecular_system, selection, frames, chemical_state, syntax, caller
        )
        second = ChemicalGraph(
            reference,
            reference_selection,
            [reference_structure_index],
            reference_chemical_state,
            syntax,
            caller,
        )
        validate_correspondence_result(correspondences, first, second, method, caller)
    table = np.asarray(correspondences["atom_correspondences"], dtype=np.int64)
    atoms = np.asarray(correspondences["selection_atom_indices"], dtype=np.int64)
    reference_atoms = np.asarray(
        correspondences["reference_selection_atom_indices"], dtype=np.int64
    )
    if not len(table):
        raise StructuralInconsistencyError(
            reason="No correspondence satisfies the declared chemical-state profile.",
            caller=caller,
        )
    baseline = None
    if baseline_atom_correspondence is not None:
        baseline = np.asarray(baseline_atom_correspondence)
        if (
            baseline.shape != (len(atoms), 2)
            or not np.array_equal(np.sort(baseline[:, 0]), atoms)
            or not np.array_equal(np.sort(baseline[:, 1]), reference_atoms)
        ):
            raise ArgumentError("baseline_atom_correspondence", caller=caller)
        baseline = np.searchsorted(
            reference_atoms, baseline[np.argsort(baseline[:, 0]), 1]
        )
    numeric_bytes = (
        2
        * sum(
            np.asarray(correspondences[name]).nbytes
            for name in ("atom_correspondences", "context_atom_correspondences")
        )
        + 64 * len(frames)
        + 96 * len(reference_atoms)
        + 8 * table.shape[0] * table.shape[1]
    )
    if numeric_bytes > configure.max_ram_usage // 2:
        raise MemoryBudgetExceededError(
            reason="Resident RMSD results and correspondence tables exceed their working budget.",
            predicted_bytes=numeric_bytes,
            available_bytes=configure.max_ram_usage // 2,
            caller=caller,
        )
    coordinates = np.asarray(
        puw.get_value(
            get(
                reference,
                selection=reference_atoms,
                structure_indices=[reference_structure_index],
                coordinates=True,
            ),
            to_unit="nm",
        ),
        dtype=np.float64,
    )
    if (
        coordinates.shape != (1, len(reference_atoms), 3)
        or not np.isfinite(coordinates).all()
    ):
        raise StructuralInconsistencyError(
            reason="Reference coordinates must be finite and aligned to selected atoms.",
            caller=caller,
        )
    tolerance = float(puw.get_value(tie_tolerance, to_unit="nm"))
    maps = np.searchsorted(reference_atoms, table[:, :, 1])
    reducer = SymmetryRMSDReducer(
        frames,
        coordinates[0],
        maps,
        baseline,
        tolerance,
        caller,
    )
    if len(frames):
        execute_projected_geometry(
            molecular_system,
            universe=atoms,
            frames=frames,
            reducer=reducer,
            per_frame_bytes=4096 + 96 * len(atoms) + 32 * len(table),
            pbc=False,
            heavy_mode=heavy_mode,
            caller=caller,
        )
    else:
        reducer.initialize({})
        reducer.finalize()
        reducer.metadata["execution"]["execution"] = "empty"
    result = dict(
        schema="molsysmt.symmetry_corrected_rmsd@1",
        rmsd=puw.standardize(puw.quantity(reducer.rmsd, "nm")),
        raw_rmsd=None
        if reducer.raw is None
        else puw.standardize(puw.quantity(reducer.raw, "nm")),
        structure_indices=frames.copy(),
        reference_structure_index=int(reference_structure_index),
        correspondence_indices=reducer.winners,
        n_near_optimal_correspondences=reducer.tie_counts,
        correspondences=deepcopy(correspondences),
        baseline_atom_correspondence=None
        if baseline_atom_correspondence is None
        else np.array(baseline_atom_correspondence, dtype=np.int64, copy=True),
        method=method,
        alignment="none",
        periodic_imaging="none",
        tie_tolerance=puw.standardize(puw.quantity(tolerance, "nm")),
        execution=reducer.metadata["execution"],
        software=dict(molsysmt=__version__, rdkit=rdBase.rdkitVersion),
    )
    attach_graph_attribution(result, caller)
    return result
