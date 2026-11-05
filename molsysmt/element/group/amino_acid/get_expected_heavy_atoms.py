"""Querying name-scoped heavy-atom references without parent substitution."""

from smonitor import signal

from molsysmt._private.amino_acid_templates import is_hydrogen as _is_hydrogen
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.atom_expectations import DIGEST_OPTIONS


@signal(tags=["api", "element", "preparation", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def get_expected_heavy_atoms(
    group_name, present_atom_names=None, skip_digestion=False, *, naming_scheme=None
):
    """Getting supported reference heavy-atom names for a group.

    Parameters
    ----------
    group_name : str or none
        Case-sensitive uppercase group label. Missing names remain unassessed.
    present_atom_names : list, tuple, numpy.ndarray or none, default=None
        Flat atom-name strings used to select a compatible reference variant.
        Hydrogen names do not constrain the heavy-atom match. None selects the
        first supported reference; an empty list requests the smallest variant.
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.
    naming_scheme : str or none, default=None
        Keyword-only source group vocabulary: sequence, amber, ccd or legacy.
        None uses supported unambiguous names. Ambiguous labels require context.

    Returns
    -------
    set of str or none
        Detached heavy-atom names, or None when no chemical reference or no
        compatible heavy-atom variant is supported. A terminal OXT can be included;
        molecular missing-atom assessment handles terminal atoms separately.

    Raises
    ------
    ArgumentError
        If the name/atom list is invalid or an ambiguous label lacks context.
    ArgumentChoiceError
        If naming_scheme is unsupported.
    StructuralInconsistencyError
        If a bundled state variant disagrees with its verification reference.

    Notes
    -----
    Standard twenty amino-acid labels use the existing atom/bond catalogue.
    Explicit Amber GLH, HID, HIE, HIP, ASH, CYM, CYX and LYN use only variants
    whose heavy connectivity and per-parent H counts agree with the bundled
    Meeko-derived state fragments. Identical labels in CCD or legacy do not
    authorize those Amber variants. CCD-derived MSE, SEP, TPO and MLY references
    are supported under ccd or the unambiguous default. No parent fallback occurs.
    These are bounded reference inventories, not a validation of stored chemical
    states, bond orders, stereochemistry or coordinate-placement support.
    Reached reference data are credited through optional Ackredit.

    Examples
    --------
    >>> sorted(get_expected_heavy_atoms('ALA'))
    ['C', 'CA', 'CB', 'N', 'O', 'OXT']
    >>> sorted(get_expected_heavy_atoms('ALA', ['N', 'CA', 'C', 'O', 'CB']))
    ['C', 'CA', 'CB', 'N', 'O']
    >>> 'SE' in get_expected_heavy_atoms('MSE')
    True
    >>> 'OE2' in get_expected_heavy_atoms('GLH', naming_scheme='amber')
    True
    >>> get_expected_heavy_atoms('HID', naming_scheme='ccd') is None
    True
    >>> get_expected_heavy_atoms('PTR') is None
    True

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Get_expected_heavy_atoms` for reference limits.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.amino_acid_templates import (
        choose_variant,
        credit,
        family,
        variants,
    )
    from molsysmt._private.residue_templates import load_residue_template

    caller = "molsysmt.element.group.amino_acid.get_expected_heavy_atoms"
    kind = family(group_name, naming_scheme, caller=caller)
    if kind == "curated_ccd":
        expected = set(load_residue_template(group_name)["atoms"])
        if present_atom_names is not None:
            present = {a for a in present_atom_names if not _is_hydrogen(a)}
            if not present <= expected:
                return None
    else:
        candidates = variants(group_name, naming_scheme, caller=caller)
        if candidates is None:
            return None
        variant = choose_variant(candidates, present_atom_names, match_hydrogens=False)
        if variant is None:
            return None
        expected = {a for a in variant["atoms"] if not _is_hydrogen(a)}
    credit(group_name, kind, caller)
    return expected
