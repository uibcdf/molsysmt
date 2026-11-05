"""Projecting explicit group-name meanings to an amino-acid alphabet."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.name_resolution import DIGEST_OPTIONS


@signal(tags=["api", "element", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def get_1_letter_code_from_name(name, naming_scheme=None, skip_digestion=False):
    """Getting an amino-acid letter under a declared group naming scheme.

    Parameters
    ----------
    name : str
        Case-sensitive uppercase group label. The original label is preserved.
    naming_scheme : str or none, default=None
        Source vocabulary: 'sequence', 'amber', 'ccd' or 'legacy'. None accepts
        only the assessed unambiguous subset; context-dependent labels require
        an explicit convention. This scalar helper has no stored system context.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.

    Returns
    -------
    str
        One amino-acid letter, including supported sequence ambiguity symbols.
        Modified groups project to their declared parent without replacement.

    Raises
    ------
    ArgumentError
        If context is required, the name is unsupported in that profile or the
        declared component has no amino-acid projection.
    ArgumentChoiceError
        If naming_scheme is unsupported.

    Notes
    -----
    The sequence profile uses the shared DDBJ alphabet. The Amber profile is
    bounded to the standard twenty names and eight reviewed state labels. CCD
    uses the bundled 2026-11-04 metadata snapshot, not an online lookup. Legacy
    explicitly selects the historical MDTraj-derived parent table; it is not
    a certified CCD snapshot. There is no fallback between declared profiles.
    For example, XLE is a sequence ambiguity symbol but a non-peptide component
    in CCD. Neither a chemical state nor coordinates are selected or changed.

    Reached reference datasets are credited through optional Ackredit. No
    Amber or MDTraj engine is executed. Provider absence/failure preserves
    the computed letter. Source revisions and bounded coverage are documented
    in the group naming guide and bundled profile receipt.

    Examples
    --------
    >>> get_1_letter_code_from_name('ALA')
    'A'
    >>> get_1_letter_code_from_name('GLH', naming_scheme='amber')
    'E'
    >>> get_1_letter_code_from_name('GLH', naming_scheme='legacy')
    'Q'
    >>> get_1_letter_code_from_name('XLE', naming_scheme='sequence')
    'J'
    >>> get_1_letter_code_from_name('MSE', naming_scheme='ccd')
    'M'

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` for conventions and
       :ref:`Tutorial_Group_Name_Code` for bounded examples.

    .. versionadded:: 1.0.0
    """
    from molsysmt import _ackredit
    from molsysmt._private.name_resolution import one_letter, references

    caller = "molsysmt.element.group.get_1_letter_code_from_name"
    letter, profile = one_letter(name, naming_scheme, caller=caller)
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, references(profile), caller, contextual=True)
    return letter
