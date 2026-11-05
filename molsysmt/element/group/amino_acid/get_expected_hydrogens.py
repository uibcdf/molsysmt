"""Querying bounded hydrogen references under explicit group naming context."""

from smonitor import signal

from molsysmt._private.amino_acid_templates import is_hydrogen as _is_hydrogen
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.atom_expectations import DIGEST_OPTIONS


@signal(tags=["api", "element", "preparation", "naming"])
@arg_digest(**DIGEST_OPTIONS)
def get_expected_hydrogens(
    group_name,
    present_atom_names=None,
    pH=7.4,
    is_n_terminal=False,
    is_c_terminal=False,
    is_disulfide=False,
    skip_digestion=False,
    *,
    naming_scheme=None,
):
    """
    Getting supported hydrogen names under a group naming convention.

    Standard amino-acid names retain the existing approximate pH model. Named
    Amber states constrain their side-chain hydrogen inventory; a reporting
    parent is never used as the chemical reference.


    Parameters
    ----------
    group_name : str
        Name of the chemical group (residue).
    present_atom_names : list, tuple, numpy.ndarray or none, default=None
        Flat atom-name strings selecting a compatible heavy-atom reference with
        maximal overlap of existing H names, then minimal extra heavy atoms.
        None selects the first supported variant.
    pH : float, default=7.4
        Finite dimensionless pH for the existing standard-group approximation.
    is_n_terminal : bool, default=False
        Whether the group occupies an amino terminus.
    is_c_terminal : bool, default=False
        Whether the group occupies a carboxyl terminus.
    is_disulfide : bool, default=False
        Whether cysteine participates in a declared disulfide bond.

    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs.
    naming_scheme : str or none, default=None
        Keyword-only group vocabulary: sequence, amber, ccd or legacy. None
        uses supported unambiguous names; ambiguous labels require context.

    Returns
    -------
    list of str or None
        Hydrogen atom names to be present, or ``None`` if the residue is not
        supported by the exact-name reference. Modified heavy-only references,
        incompatible atom layouts and named-state terminal completion return None.

    Raises
    ------
    ArgumentError
        If arguments are invalid or an ambiguous label lacks source context.
    ArgumentChoiceError
        If naming_scheme is unsupported.
    StructuralInconsistencyError
        If a bundled state variant fails chemical-reference verification.


    Notes
    -----
    Explicit Amber GLH, HID, HIE, HIP, ASH, CYM, CYX and LYN select only
    catalogue variants whose heavy connectivity and per-parent H counts match
    the bundled Meeko-derived state fragment. Their side chains are not reset
    by pH. These variants represent internal peptide groups; named-state terminal
    H completion remains unassessed. CCD/legacy interpretations cannot reuse the
    Amber variants. No parent substitution, chemical-state selection or geometry
    calculation occurs. Optional Ackredit credits the actual reference datasets.

    The following approximate rules remain for standard labels:

    * **ASP**: deprotonated (no HD2) when pH ≥ 4.4
    * **GLU**: deprotonated (no HE2) when pH ≥ 4.4
    * **HIS**: HIP (HD1+HE2) when pH < 6.5; HIE (HE2 only) otherwise
    * **LYS**: deprotonated NZ (no HZ3) when pH ≥ 10.5
    * **CYS**: no HG when *is_disulfide* is True
    * **C-terminus**: carboxylate (no HXT/HO2) when pH ≥ 3.2
    * **N-terminus**: neutral amine (no H3) when pH ≥ 9.6

    These are fixed thresholds taken from free-amino-acid pKa values. They do not
    model the pKa shifts a residue's environment produces, which is what a
    PROPKA-style calculation would do; see `devguide/structure_preparation_pipeline.md`.


    Examples
    --------
    >>> 'HE2' in get_expected_hydrogens('GLH', naming_scheme='amber', pH=12.0)
    True
    >>> get_expected_hydrogens('MSE') is None
    True
    >>> get_expected_hydrogens('HIP', naming_scheme='ccd') is None
    True

    .. admonition:: User guide

       See :ref:`user-foundations-group-naming-schemes` and
       :ref:`Tutorial_Get_expected_hydrogens` for model limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.amino_acid_templates import (
        choose_variant,
        credit,
        family,
        variants,
    )

    caller = "molsysmt.element.group.amino_acid.get_expected_hydrogens"
    kind = family(group_name, naming_scheme, caller=caller)
    candidates = variants(group_name, naming_scheme, caller=caller)
    if candidates is None:
        return None
    if kind == "amber_state" and (is_n_terminal or is_c_terminal):
        return None
    best_variant = choose_variant(candidates, present_atom_names)
    if best_variant is None:
        return None
    lookup_name = group_name

    # All H names from the chosen variant
    all_hs = [a for a in best_variant["atoms"] if _is_hydrogen(a)]
    all_hs_set = set(all_hs)

    # --- pH / context rules ---
    remove_hs = set()

    # ASP: OD2 is protonated only at low pH (HD2)
    if lookup_name == "ASP" and pH >= 4.4:
        remove_hs.update(h for h in all_hs_set if h in ("HD2",))

    # GLU: OE2 is protonated only at low pH (HE2)
    if lookup_name == "GLU" and pH >= 4.4:
        remove_hs.update(h for h in all_hs_set if h in ("HE2",))

    # HIS: at pH >= 6.5 use HIE (NE2-H only), remove HD1
    if lookup_name == "HIS" and pH >= 6.5:
        remove_hs.update(h for h in all_hs_set if h in ("HD1",))

    # LYS: NZ deprotonated (LYN) at very high pH – remove the third NZ hydrogen
    if lookup_name == "LYS" and pH >= 10.5:
        # Identify the third H on NZ.  Common names: HZ3, 3HZ
        remove_hs.update(h for h in all_hs_set if h in ("HZ3", "3HZ"))

    # CYS in disulfide: remove HG / HG1
    if lookup_name == "CYS" and is_disulfide:
        remove_hs.update(h for h in all_hs_set if h in ("HG", "HG1"))

    # C-terminal carboxylate: pKa is 2.0-3.5 across the residues, so above the
    # threshold the group is a carboxylate and carries no proton. The rule below asks
    # only whether OXT exists, which is a topology question; this one asks whether it
    # should be protonated, which is the chemistry question, and both are needed.
    # Without this the terminus stays COOH at every pH and no standard force field has
    # a template for it (uibcdf/molsysmt#176).
    if is_c_terminal and pH >= 3.2:
        remove_hs.update(h for h in all_hs_set if h in ("HXT", "HO2"))

    # N-terminal amine: pKa around 9.6. Above it the amine is neutral and loses its
    # third proton. This one never raises downstream, since NH3+ has a template
    # everywhere, so it has to be asserted directly rather than through a force field.
    if is_n_terminal and pH >= 9.6:
        remove_hs.update(h for h in all_hs_set if h in ("H3",))

    # Non-terminal residues: remove OXT-bound hydrogen (HXT) if OXT is absent.
    # If present_atom_names is given and OXT is absent, remove HXT.
    if present_atom_names is not None:
        present_heavy_for_oxt = {a for a in present_atom_names if not _is_hydrogen(a)}
        if "OXT" not in present_heavy_for_oxt:
            remove_hs.update(h for h in all_hs_set if h in ("HXT",))
    elif not is_c_terminal:
        remove_hs.update(h for h in all_hs_set if h in ("HXT",))

    # Non-N-terminal: remove extra N-terminal Hs (H2, H3, HN2, HT2, HT3, etc.)
    # N-terminal has H + H2 (+H3 in some force fields); mid-chain has only H.
    if not is_n_terminal:
        remove_hs.update(
            h for h in all_hs_set if h in ("H2", "H3", "HN2", "HT2", "HT3")
        )

    # PRO: when not N-terminal, the ring N is tertiary (bonded to C(i-1), CA, CD)
    # — there is no room for a backbone NH.  Remove any H on N that is only
    # present in N-terminal or free-amino PRO variants.
    if lookup_name == "PRO" and not is_n_terminal:
        remove_hs.update(h for h in all_hs_set if h in ("H", "HT1"))

    result = [h for h in all_hs if h not in remove_hs]
    credit(group_name, kind, caller)
    return result
