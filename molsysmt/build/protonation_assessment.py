"""Expose process-local, geometry-independent protonation decisions."""

from copy import deepcopy
from threading import Lock

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.protonation import DIGEST_OPTIONS


class ProtonationAssessment:
    """Preparing a read-only protonation-removal decision for one source.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form providing stable atom/group inventory and
        a resolved reference chemical state. Coordinates are not required.
    pH : float, default=7.4
        Finite dimensionless pH for the existing fixed-pKa name-inventory rules.
    engine : str, default='MolSysMT'
        Reference-rule engine. Only MolSysMT is implemented.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.

    Notes
    -----
    This is an operation result, not a molecular-system form or chemical store.
    Use to_dict() to inspect detached coverage and positional atom maps. Use
    apply() to execute the same decision once without repeating reference queries.
    Report data can be preserved independently; an executable assessment is
    process-local and is not a portable authorization token.

    Assessment never rebuilds stored components or copies/hashes coordinate
    trajectories. Prepared maps remain valid after coordinate edits on unchanged
    axes. Replacing native domains or changing inventory, naming, chemistry or
    the structure count requires a new assessment. Callers must serialize source
    access; there is no general lock over arbitrary external mutation.

    Standard names retain the fixed-pKa approximation; supported explicit Amber
    states retain their name-constrained side chains. Unsupported groups and
    named-state termini remain explicitly unassessed. The operation removes
    atoms; it does not add H, assign charges, choose a stored state or certify
    protonation, force-field compatibility or readiness for docking.

    See Also
    --------
    assess_protonation
        Prepare the same result through the public factory.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import MolSys
    >>> molsys = MolSys()
    >>> assessment = msm.build.ProtonationAssessment(molsys)
    >>> assessment.to_dict()['source']['n_atoms']
    0
    >>> assessment.apply(molsys) is molsys
    False

    .. admonition:: User guide

       See :ref:`Tutorial_Protonation_Assessment` for coverage and atom maps.

    .. versionadded:: 1.0.0
    """

    __slots__ = ("_decision", "_execution", "_lock")

    @arg_digest(**DIGEST_OPTIONS)
    def __init__(
        self, molecular_system, pH=7.4, engine="MolSysMT", skip_digestion=False
    ):
        """Initializing one validated source-bound assessment."""
        from molsysmt._private.protonation_preparation import prepare

        self._decision = prepare(molecular_system, pH, engine)
        self._execution = dict(status="prepared")
        self._lock = Lock()

    @arg_digest(**DIGEST_OPTIONS)
    def to_dict(self, skip_digestion=False):
        """Returning a detached report and the current execution state.

        Parameters
        ----------
        skip_digestion : bool, default=False
            Skip argument digestion only for already validated inputs.

        Returns
        -------
        dict
            molsysmt.protonation_assessment@1 data. source_to_output_atom_indices is an int64
            vector over original atoms, with -1 for removed atoms.
            output_to_source_atom_indices lists retained original indices in target order.
            structure_indices is the unchanged full source structure axis.
            Coverage distinguishes assessed, unassessed and unassigned atoms;
            labels and IDs are descriptive and never establish correspondence.
            group_contexts keeps every group's actual name, naming declaration,
            assessment status/reason and available terminal/disulfide context.
            Arrays and nested records are independently owned by the caller.

        Notes
        -----
        The report keeps its original source universe after execution. A no-change
        assessment with unassessed groups is partial_no_change or unassessed,
        rather than a claim of complete protonation correctness.

        .. versionadded:: 1.0.0
        """
        with self._lock:
            report = deepcopy(self._decision.report)
            report["execution"] = deepcopy(self._execution)
            return report

    @signal(tags=["api", "build", "preparation"])
    @arg_digest(**DIGEST_OPTIONS)
    def apply(self, molecular_system, in_place=False, skip_digestion=False):
        """Applying the prepared atom-removal decision without repeating science.

        Parameters
        ----------
        molecular_system : molecular system
            The original object/resource assessed by this result. Native domain
            identities and the chemical/inventory/axis fingerprint must match.
        in_place : bool, default=False
            False returns an independent native MolSys, including for no-op,
            file and complementary inputs. True publishes on the original native
            MolSys and returns None. Other in-place forms are refused.
        skip_digestion : bool, default=False
            Skip argument digestion only for already validated inputs. Source
            staleness and publication guards are always checked.

        Returns
        -------
        molsysmt.MolSys or None
            An independent native subset, or None after native in-place execution.

        Raises
        ------
        ArgumentConflictError
            If the assessment was consumed or source identity/contents changed.
        ArgumentError
            If in-place mutation is unsupported for the supplied source.
        StructuralInconsistencyError
            If the prepared subset violates the retained atom or structure axes.

        Notes
        -----
        Successful execution consumes the assessment once, including a true no-op.
        Candidate-preparation failure leaves the source and plan unmodified.
        The complete candidate is prepared before native publication. In-place
        no-ops preserve native domain identities; independent no-ops copy data.
        Normal removal projects all stored chemical states, mechanics and named
        analyses; removed participants lose observations without recalculation.
        Surviving observations retain their historical evaluated scope. Old native
        domain/result references remain detached snapshots after publication.

        Current coordinates, mechanics, analyses and preparation history are
        projected at execution, not copied into the assessment. Coordinate edits
        on unchanged axes do not trigger another pH decision. The source must be
        exclusively owned during the call; this does not observe external edits.

        .. versionadded:: 1.0.0
        """
        from molsysmt._private.protonation_preparation import stage
        from molsysmt._private.smonitor import ArgumentConflictError

        with self._lock:
            if self._execution["status"] != "prepared":
                raise ArgumentConflictError(
                    "assessment",
                    "execution",
                    reason="This assessment has already been consumed.",
                    caller="molsysmt.build.ProtonationAssessment.apply",
                )
            execution = stage(self._decision, molecular_system, in_place)
            if execution.publish is not None:
                execution.publish()
            self._execution = execution.report
            return execution.output
