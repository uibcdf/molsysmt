"""Observed DSSP assignments through the declared MDTraj implementation."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.execution import ChunkedExecutor, Reducer
from molsysmt._private.smonitor import (
    MemoryBudgetExceededError,
    NotImplementedMethodError,
)


class _SecondaryStructureReducer(Reducer):
    def __init__(self, topology, groups, simplified):
        self.topology = topology
        self.groups = groups
        self.simplified = simplified

    def initialize(self, metadata):
        self.values = np.empty((metadata["n_structures"], len(self.groups)), dtype="U2")
        self.position = 0

    def consume(self, chunk):
        import mdtraj as md

        trajectory = md.Trajectory(chunk["coordinates"], self.topology)
        assignments = np.asarray(
            md.compute_dssp(trajectory, simplified=self.simplified), dtype="U2"
        )
        count = trajectory.n_frames
        if assignments.shape != (count, self.topology.n_residues):
            raise ValueError(
                "MDTraj DSSP returned an incompatible structure/group axis."
            )
        self.values[self.position : self.position + count] = assignments[:, self.groups]
        self.position += count

    def finalize(self):
        if self.position != len(self.values):
            raise ValueError("DSSP did not receive every requested structure.")
        return self.values


@signal(tags=["api", "structure"])
@arg_digest()
@dep_digest("mdtraj", when={"engine": "MDTraj"})
def get_secondary_structure(
    molecular_system,
    selection="all",
    structure_indices="all",
    simplified=True,
    syntax="MolSysMT",
    engine="MDTraj",
    skip_digestion=False,
    *,
    heavy_mode="auto",
):
    """Assigning observed secondary structure to selected molecular groups.

    Evaluate MDTraj's DSSP implementation on the complete molecular context,
    then project the requested groups. Selecting output groups never cuts
    backbone or hydrogen-bond context before assignment.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form with group/atom inventory and
        coordinates. Conversion supplies MDTraj's named backbone context.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Selection of groups. Numeric group indices retain order and repetitions;
        expressions use the requested syntax. These are not atom indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Zero-based structure indices. Order and repetitions are retained.
    simplified : bool, default=True
        True combines DSSP classes into H (helix), E (strand) and C (coil).
        False retains the eight DSSP codes H, G, I, E, B, T, S and a space.
        Both modes preserve NA for groups without MDTraj's backbone quartet.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate the group selection.
    engine : str, default='MDTraj'
        Assignment implementation. Only MDTraj is supported.
    skip_digestion : bool, default=False
        If True, the input arguments are not digested.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Coordinate execution policy. Auto uses bounded chunks when the
        estimated working arrays exceed the numerical allowance; force
        requires a source form with registered coordinate iteration. Off
        admits only an eager calculation within that allowance.

    Returns
    -------
    numpy.ndarray
        Detached dimensionless Unicode array, dtype U2, with shape
        (n_selected_structures, n_selected_groups). Empty axes have defined
        shapes. A blank full-code assignment is an actual DSSP loop code;
        NA does not certify a group's chemical identity or readiness.

    Raises
    ------
    ArgumentError
        If an input, group index or structure index is invalid.
    LibraryNotFoundError
        If the explicitly selected optional MDTraj provider is unavailable.
    NotImplementedMethodError
        If an assignment engine other than MDTraj is requested.
    MemoryBudgetExceededError
        If resident labels and the minimum coordinate working block exceed
        the configured numerical allowance, or eager execution cannot fit.
    UnsupportedHeavyOperationError
        If chunking is required but the source form cannot deliver it.

    Notes
    -----
    This calls MDTraj's implementation based on DSSP 2.2.0, following Kabsch
    and Sander (1983); it does not implement a new MolSysMT criterion, run an
    external DSSP executable, predict from sequence, or use reference
    secondary-structure propensities. The backend recognizes backbone atom
    names N, CA, C and O. Missing quartets retain its NA result. No hydrogens,
    atom names, chemistry, alignment or periodic reconstruction are repaired.

    Stored coordinates are used as supplied. Reconstruct periodic molecules
    explicitly when scientifically intended. Heavy coordinate blocks are staged
    in nm through ChunkedExecutor; MDTraj uses its normal float32 coordinate
    representation. Changing the PyUnitWizard presentation standard does not
    change the dimensionless codes. The output stays resident; topology/source
    and foreign-runtime memory are separate from the numerical estimate, which
    is neither process RSS nor an operating-system reservation.

    Successful nonempty calculations optionally credit the DSSP criterion and
    actual MDTraj version through Ackredit. Empty axes do not run or credit
    DSSP. Backend parity and vocabulary guards are not independent validation
    of DSSP accuracy; that scientific-evidence gap remains explicit.

    See Also
    --------
    molsysmt.physchem.get_secondary_structure_propensity : Looking up reference propensities.
    molsysmt.pbc.wrap_to_mic : Reconstructing periodic molecular coordinates.

    References
    ----------
    Kabsch, W. and Sander, C. (1983). Dictionary of protein secondary
    structure: pattern recognition of hydrogen-bonded and geometrical
    features. Biopolymers 22, 2577–2637. doi:10.1002/bip.360221211.
    MDTraj compute_dssp documentation: https://mdtraj.org/1.11.0/api/generated/mdtraj.compute_dssp.html

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0, 8, 2])
    >>> msm.structure.get_secondary_structure(
    ...     molsys, selection=[3, 1, 3], structure_indices=[2, 0, 2]).shape
    (3, 3)

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_secondary_structure` for full and simplified
       assignments, selections, provider conventions and their limitations.

    .. versionadded:: 1.0.0
    """
    if engine != "MDTraj":
        raise NotImplementedMethodError()

    from molsysmt import configure
    from molsysmt._private.variables import is_all
    from molsysmt.basic import convert, get, get_form, select
    from molsysmt.basic._index_validation import validate_structure_indices

    caller = "molsysmt.structure.get_secondary_structure"
    groups = np.asarray(
        select(molecular_system, element="group", selection=selection, syntax=syntax),
        dtype=np.int64,
    )
    n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
    frames = validate_structure_indices(molecular_system, structure_indices, caller)
    frames = (
        list(range(int(n_structures or 0)))
        if frames is None or is_all(frames)
        else frames
    )
    shape = (len(frames), len(groups))
    if not all(shape):
        return np.empty(shape, dtype="U2")

    output_bytes = shape[0] * shape[1] * np.dtype("U2").itemsize
    frame_bytes = max(1, int(n_atoms) * 64)
    allowance = int(configure.max_ram_usage)
    available = allowance - output_bytes
    if available < frame_bytes or (
        heavy_mode == "off" and available < frame_bytes * len(frames)
    ):
        raise MemoryBudgetExceededError(
            reason="DSSP labels and coordinate working blocks exceed the numerical allowance",
            predicted_bytes=output_bytes
            + frame_bytes * (len(frames) if heavy_mode == "off" else 1),
            available_bytes=allowance,
            caller=caller,
        )
    mode = (
        "force"
        if heavy_mode == "auto" and available < frame_bytes * len(frames)
        else heavy_mode
    )

    import mdtraj as md

    from molsysmt._private.scientific_attribution import credit_secondary_structure

    if mode != "force":
        # The public converter owns eager foreign-form extraction and units.
        # Foreign iterators do not all implement ChunkedExecutor's dictionary API.
        trajectory = convert(
            molecular_system, to_form="mdtraj.Trajectory", structure_indices=frames
        )
        output = np.asarray(
            md.compute_dssp(trajectory, simplified=simplified), dtype="U2"
        )[:, groups].copy()
    else:
        # Construct provider topology with only one complete source structure;
        # the registered iterator then delivers complete coordinate contexts.
        form = get_form(molecular_system)
        from molsysmt._private.smonitor import UnsupportedHeavyOperationError
        from molsysmt.form import _dict_modules

        if not isinstance(form, str) or not getattr(
            _dict_modules.get(form), "_heavy_support", {}
        ).get("coordinates", False):
            raise UnsupportedHeavyOperationError(
                operation=caller,
                form=str(form),
                reason="Source form has no registered chunked-coordinate contract",
            )
        context = convert(
            molecular_system, to_form="molsysmt.MolSys", structure_indices=[frames[0]]
        )
        topology = convert(context, to_form="mdtraj.Topology")
        del context
        reducer = _SecondaryStructureReducer(topology, groups, simplified)
        output = ChunkedExecutor(
            molecular_system,
            form=form,
            operation="get_secondary_structure",
            reducer=reducer,
            atom_indices="all",
            structure_indices=frames,
            heavy_mode="force",
            attributes=["coordinates"],
            max_chunk_size=max(1, available // frame_bytes),
        ).execute()

    credit_secondary_structure(str(md.__version__), caller, simplified=simplified)
    return output
