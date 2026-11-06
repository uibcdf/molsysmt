"""Prepare public atom-removal correspondence without changing the source."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.protonation import DIGEST_OPTIONS


@signal(tags=["api", "build", "preparation"])
@arg_digest(**DIGEST_OPTIONS)
def assess_protonation(
    molecular_system, pH=7.4, engine="MolSysMT", skip_digestion=False
):
    """Assessing reference-rule protonation removal without modifying the source.

    Parameters
    ----------
    molecular_system : molecular system
        Source in any supported form supplying stable atoms/groups and a resolved
        reference chemical state. Coordinates are not needed for the decision.
    pH : float, default=7.4
        Finite dimensionless pH for the existing fixed-pKa name-inventory rules.
    engine : str, default='MolSysMT'
        Reference-rule engine. Only MolSysMT is implemented.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated internal inputs.

    Returns
    -------
    molsysmt.build.ProtonationAssessment
        Source-bound, single-use decision. to_dict() exposes detached coverage,
        actual pH/naming/reference scope, both directions of the positional atom
        map and the unchanged structure axis. apply() executes that same decision
        without repeating scientific reference queries.

    Raises
    ------
    ArgumentError
        If pH is nonfinite or arguments/naming declarations are invalid.
    NotImplementedMethodError
        If the requested reference-rule engine is unsupported.
    NotWithThisFormError
        If required stable inventory or chemistry is absent.
    StructuralInconsistencyError
        If no reference chemical state can be resolved.

    Notes
    -----
    The assessment uses stored connectivity for detached component context. It
    never rebuilds source components or copies/hashes native coordinate series.
    Source identity and chemical/inventory/axis fingerprints are rechecked before
    publication. Callers serialize source access; fingerprints are not authentication.

    Standard labels use the existing fixed-pKa approximation.
    Explicit supported Amber-state side chains are name-constrained. Unsupported
    groups, layouts and named-state termini remain unassessed, including when no
    atoms would be removed. No environmental pKa, hydrogen addition, formal-charge
    assignment, chemical-state choice or docking certification is performed.
    Optional Ackredit tracking records the consulted reference datasets; detached
    reference data remains available without that provider.

    See Also
    --------
    reconcile_protonation
        Assess and execute in one call.
    ProtonationAssessment
        Inspect and apply one prepared decision.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['chicken villin HP35']['1vii.pdb']
    >>> molsys = msm.convert(source, structure_indices=0)
    >>> assessment = msm.build.assess_protonation(molsys, pH=12.0)
    >>> len(assessment.to_dict()['removed_atom_indices'])
    6
    >>> result = assessment.apply(molsys)
    >>> (molsys.get(n_atoms=True), result.get(n_atoms=True))
    (596, 590)

    .. admonition:: User guide

       See :ref:`Tutorial_Protonation_Assessment` for maps and publication limits.

    .. versionadded:: 1.0.0
    """
    from .protonation_assessment import ProtonationAssessment

    return ProtonationAssessment(
        molecular_system, pH=pH, engine=engine, skip_digestion=True
    )
