"""Recognizing amino-acid labels under explicit source vocabularies."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.name_resolution import DIGEST_OPTIONS


@signal(tags=["api", "element", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def is_amino_acid(name, naming_scheme=None, skip_digestion=False):
    """Checking whether a name is recognized as an amino-acid group.

    Parameters
    ----------
    name : str
        Case-sensitive uppercase group label.
    naming_scheme : str or none, default=None
        Source vocabulary: 'sequence', 'amber', 'ccd' or 'legacy'. None uses
        the assessed unambiguous subset, never an implicit legacy convention.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.

    Returns
    -------
    bool
        True for an assessed amino-acid interpretation. False means either
        a recognized non-peptide component or no assessment in this profile;
        it is not proof that the unknown compound cannot be an amino acid.

    Raises
    ------
    ArgumentError
        If a context-dependent label has no naming_scheme, or name is invalid.
    ArgumentChoiceError
        If naming_scheme is unsupported.

    Notes
    -----
    Recognition does not establish that an exact chemical template is available.
    Amber and CCD support is bounded to the bundled naming-profile receipt.
    Optional Ackredit records only the reference data reached by recognition.

    Examples
    --------
    >>> is_amino_acid('ALA')
    True
    >>> is_amino_acid('HID', naming_scheme='amber')
    True
    >>> is_amino_acid('HID', naming_scheme='ccd')
    False
    >>> is_amino_acid('papa')
    False

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Group_Name_Code` for supported conventions.

    .. versionadded:: 1.0.0
    """
    from molsysmt import _ackredit
    from molsysmt._private.name_resolution import assessed, references

    caller = "molsysmt.element.group.amino_acid.is_amino_acid"
    result = assessed(name, naming_scheme, caller=caller, require_context=True)
    if result is None:
        return False
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(
            provider,
            references(result.profile, alphabet=False),
            caller,
            contextual=True,
        )
    return result.group_type == "amino acid"
