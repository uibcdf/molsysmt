from .group_names import group_names
from .get_group_db import get_group_db
from .get_standard_name import get_standard_name


def _is_hydrogen(atom_name):
    """Return True if atom_name follows PDB hydrogen naming conventions."""
    if not atom_name:
        return False
    if atom_name[0] == 'H':
        return True
    if len(atom_name) >= 2 and atom_name[0].isdigit() and atom_name[1] == 'H':
        return True
    return False


def get_expected_hydrogens(group_name, present_atom_names=None, pH=7.4,
                           is_n_terminal=False, is_c_terminal=False,
                           is_disulfide=False):
    """Return the list of expected hydrogen atom names for a residue.

    Selects the best-matching topology variant from the amino-acid database,
    then applies pH-dependent protonation rules to decide which H atoms should
    be present.

    Parameters
    ----------
    group_name : str
        Residue name as stored in the topology.
    present_atom_names : list of str or None, default None
        Heavy atoms currently in the residue.  Used to select the best variant
        (tightest-fit strategy, same as :func:`get_expected_heavy_atoms`).
    pH : float, default 7.4
        Approximate pH for protonation-state assignment.
    is_n_terminal : bool, default False
        True if this is the N-terminal residue of a peptide chain.
    is_c_terminal : bool, default False
        True if this is the C-terminal residue of a peptide chain.
    is_disulfide : bool, default False
        True if this CYS is part of a disulfide bridge (removes HG).

    Returns
    -------
    list of str or None
        Hydrogen atom names to be present, or ``None`` if the residue is not
        in the amino-acid database.

    Notes
    -----
    pH rules applied:

    * **ASP**: deprotonated (no HD2) when pH ≥ 4.4
    * **GLU**: deprotonated (no HE2) when pH ≥ 4.4
    * **HIS**: HIP (HD1+HE2) when pH < 6.5; HIE (HE2 only) otherwise
    * **LYS**: deprotonated NZ (no HZ3) when pH ≥ 10.5
    * **CYS**: no HG when *is_disulfide* is True

    .. versionadded:: 1.0.0
    """

    canonical = get_standard_name(group_name)
    lookup_name = canonical if canonical is not None else group_name

    if lookup_name not in group_names:
        return None

    db = get_group_db(lookup_name)

    # --- Select the best variant ---
    # Strategy: choose the variant whose heavy-atom set is a superset of the
    # present heavy atoms, with the fewest extra atoms (tightest fit).
    # Prefer variants that match terminal status.
    if present_atom_names is not None:
        present_heavy = {a for a in present_atom_names if not _is_hydrogen(a)}
        present_h = {a for a in present_atom_names if _is_hydrogen(a)}
        best_variant = None
        best_h_overlap = -1
        best_extra = None
        for variant in db['topology']:
            variant_heavy = {a for a in variant['atoms'] if not _is_hydrogen(a)}
            if present_heavy <= variant_heavy:
                extra = len(variant_heavy) - len(present_heavy)
                variant_hs = {a for a in variant['atoms'] if _is_hydrogen(a)}
                h_overlap = len(present_h & variant_hs)
                if (best_extra is None or
                        h_overlap > best_h_overlap or
                        (h_overlap == best_h_overlap and extra < best_extra)):
                    best_extra = extra
                    best_h_overlap = h_overlap
                    best_variant = variant
        if best_variant is None:
            best_variant = db['topology'][0]
    else:
        best_variant = db['topology'][0]

    # All H names from the chosen variant
    all_hs = [a for a in best_variant['atoms'] if _is_hydrogen(a)]
    all_hs_set = set(all_hs)

    # --- pH / context rules ---
    remove_hs = set()

    # ASP: OD2 is protonated only at low pH (HD2)
    if lookup_name == 'ASP' and pH >= 4.4:
        remove_hs.update(h for h in all_hs_set if h in ('HD2',))

    # GLU: OE2 is protonated only at low pH (HE2)
    if lookup_name == 'GLU' and pH >= 4.4:
        remove_hs.update(h for h in all_hs_set if h in ('HE2',))

    # HIS: at pH >= 6.5 use HIE (NE2-H only), remove HD1
    if lookup_name == 'HIS' and pH >= 6.5:
        remove_hs.update(h for h in all_hs_set if h in ('HD1',))

    # LYS: NZ deprotonated (LYN) at very high pH – remove the third NZ hydrogen
    if lookup_name == 'LYS' and pH >= 10.5:
        # Identify the third H on NZ.  Common names: HZ3, 3HZ
        remove_hs.update(h for h in all_hs_set if h in ('HZ3', '3HZ'))

    # CYS in disulfide: remove HG / HG1
    if lookup_name == 'CYS' and is_disulfide:
        remove_hs.update(h for h in all_hs_set if h in ('HG', 'HG1'))

    # Non-terminal residues: remove OXT-bound hydrogen (HXT) if OXT is absent.
    # If present_atom_names is given and OXT is absent, remove HXT.
    if present_atom_names is not None:
        present_heavy_for_oxt = {a for a in present_atom_names if not _is_hydrogen(a)}
        if 'OXT' not in present_heavy_for_oxt:
            remove_hs.update(h for h in all_hs_set if h in ('HXT',))
    elif not is_c_terminal:
        remove_hs.update(h for h in all_hs_set if h in ('HXT',))

    # Non-N-terminal: remove extra N-terminal Hs (H2, H3, HN2, HT2, HT3, etc.)
    # N-terminal has H + H2 (+H3 in some force fields); mid-chain has only H.
    if not is_n_terminal:
        remove_hs.update(h for h in all_hs_set if h in ('H2', 'H3', 'HN2', 'HT2', 'HT3'))

    # PRO: when not N-terminal, the ring N is tertiary (bonded to C(i-1), CA, CD)
    # — there is no room for a backbone NH.  Remove any H on N that is only
    # present in N-terminal or free-amino PRO variants.
    if lookup_name == 'PRO' and not is_n_terminal:
        remove_hs.update(h for h in all_hs_set if h in ('H', 'HT1'))

    result = [h for h in all_hs if h not in remove_hs]
    return result
