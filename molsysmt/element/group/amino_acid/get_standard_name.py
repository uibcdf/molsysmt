"""Reporting reference names independently of chemical templates."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.name_resolution import DIGEST_OPTIONS


@signal(tags=["api", "element", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def get_standard_name(group_name, naming_scheme=None, skip_digestion=False):
    """Getting a non-canonical group's reference amino-acid name.

    Parameters
    ----------
    group_name : str or none
        Case-sensitive uppercase group label. Missing labels are not inferred.
    naming_scheme : str or none, default=None
        Source vocabulary: 'sequence', 'amber', 'ccd' or 'legacy'. None uses
        only assessed unambiguous names. Context-dependent labels require an
        explicit convention; this scalar helper has no stored system context.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.

    Returns
    -------
    str or none
        Reference three-letter name for an assessed modified amino acid.
        None for an already canonical name, a non-peptide component, an
        unknown parent (XAA), or a missing/unassessed default label.

    Raises
    ------
    ArgumentError
        If an ambiguous label has no convention, or an explicit profile does
        not support an amino-acid candidate or unclassified name.
    ArgumentChoiceError
        If naming_scheme is unsupported.

    Notes
    -----
    This is a reporting projection, not a chemical equivalence or permission
    to replace a group or use its parent's chemical template. The bounded
    profiles and their reference datasets are shared with the group one-letter
    helper. Legacy explicitly selects the historical MDTraj-derived table.
    Reached datasets are credited through optional Ackredit; no external
    molecular engine is executed. Names, assignments and coordinates stay intact.

    Examples
    --------
    >>> get_standard_name('MSE')
    'MET'
    >>> get_standard_name('SEP')
    'SER'
    >>> print(get_standard_name('ALA'))
    None
    >>> print(get_standard_name('HOH'))
    None
    >>> get_standard_name('GLH', naming_scheme='amber')
    'GLU'
    >>> get_standard_name('GLH', naming_scheme='legacy')
    'GLN'
    >>> print(get_standard_name('CYX', naming_scheme='ccd'))
    None

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Group_Name_Code` for conventions and examples.

    .. versionadded:: 1.0.0
    """
    from molsysmt import _ackredit
    from molsysmt._private.name_resolution import (
        assessed,
        classify_group_name,
        references,
        resolve,
    )

    caller = "molsysmt.element.group.amino_acid.get_standard_name"
    if not isinstance(group_name, str):
        return None
    result = assessed(group_name, naming_scheme, caller=caller, require_context=True)
    if result is None and naming_scheme is not None:
        if classify_group_name(group_name, naming_scheme) not in {
            "unknown",
            "amino acid",
        }:
            return None
        result = resolve(group_name, naming_scheme, caller=caller)
    if result is None:
        return None
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            references(result.profile, alphabet=False),
            caller,
            contextual=True,
        )
    return (
        result.parent
        if result.group_type == "amino acid"
        and result.parent not in (None, "XAA", group_name)
        else None
    )
