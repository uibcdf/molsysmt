"""Defining immutable, machine-readable chemical conversion reports."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConversionIssue:
    """Describing one source semantic field not preserved by a conversion.

    Attributes
    ----------
    attribute : str
        Canonical attribute or state concept affected by the issue.
    reason : str
        Human-readable explanation of the detected limitation.
    kind : str
        Machine-readable issue category. The default is ``'unsupported'``.

    .. versionadded:: 1.0.0
    """

    attribute: str
    reason: str
    kind: str = 'unsupported'


@dataclass(frozen=True)
class ConversionReport:
    """Classifying an audited chemical conversion before target creation.

    The report is immutable. It records conservative, instance-aware preflight
    evidence; it does not claim that every semantic exposed by every
    third-party library has already been audited.

    Attributes
    ----------
    from_form : str or tuple of str
        Source form or forms identified by MolSysMT.
    to_form : str
        Canonical target form.
    outcome : {'exact', 'equivalent', 'lossy', 'rejected'}
        Fidelity classification for the audited conversion.
    issues : tuple of ConversionIssue
        Structured semantic limitations detected by the preflight.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=1)
    >>> _, report = msm.convert(
    ...     topology, to_form='molsysmt.Topology', return_report=True
    ... )
    >>> report.outcome
    'exact'
    >>> report.is_lossy
    False

    .. versionadded:: 1.0.0
    """

    from_form: str | tuple[str, ...]
    to_form: str
    outcome: str
    issues: tuple[ConversionIssue, ...] = ()

    @property
    def is_lossy(self):
        """Returning whether supplied semantics would be discarded."""

        return self.outcome == 'lossy'
