from .group_names import group_names
from .get_group_db import get_group_db
from .get_standard_name import get_standard_name


def _is_hydrogen(atom_name):
    """Return True if atom_name follows PDB hydrogen naming conventions."""
    if not atom_name:
        return False
    if atom_name[0] == 'H':
        return True
    # Legacy PDB format: digit-first names like '1HB', '2HB', '3H'
    if len(atom_name) >= 2 and atom_name[0].isdigit() and atom_name[1] == 'H':
        return True
    return False


def get_expected_heavy_atoms(group_name, present_atom_names=None):
    """
    Return the set of expected heavy (non-hydrogen) atom names for a residue.

    Looks up the residue in MolSysMT's amino-acid topology database.  When
    ``present_atom_names`` is supplied the function selects the topology
    variant whose atom set is a superset of the given heavy atoms (matching
    PDBFixer's template-selection strategy).  When no variant matches, or when
    ``present_atom_names`` is ``None``, the first (CCD canonical) variant is
    used.

    Parameters
    ----------
    group_name : str
        Residue name as stored in the topology.  Non-standard names are
        canonicalized via :func:`get_standard_name` before the database look-up.
    present_atom_names : list of str or None, default None
        Atom names already present in the residue.  Used to select the best
        matching topology variant.

    Returns
    -------
    set of str or None
        Set of heavy-atom names expected for the residue, or ``None`` when the
        residue is not found in the amino-acid database.

    Examples
    --------
    >>> get_expected_heavy_atoms('ALA')
    {'N', 'CA', 'C', 'O', 'CB', 'OXT'}
    >>> get_expected_heavy_atoms('ALA', present_atom_names=['N', 'CA', 'C', 'O', 'CB'])
    {'N', 'CA', 'C', 'O', 'CB', 'OXT'}
    >>> get_expected_heavy_atoms('MSE')   # selenomethionine → look up MET
    {'N', 'CA', 'C', 'O', 'CB', 'CG', 'SD', 'CE', 'OXT'}

    Notes
    -----
    Heavy atoms are identified by PDB naming convention: a name is a hydrogen
    if it starts with ``'H'`` or with a digit followed by ``'H'`` (e.g.
    ``'1HB'``).

    .. versionadded:: 1.0.0
    """

    # Canonicalize: if group_name is a known non-standard amino acid, use its
    # standard equivalent for the topology look-up.
    canonical = get_standard_name(group_name)
    lookup_name = canonical if canonical is not None else group_name

    if lookup_name not in group_names:
        return None

    db = get_group_db(lookup_name)

    if present_atom_names is not None:
        present_heavy = {a for a in present_atom_names if not _is_hydrogen(a)}
        # Among all variants that contain the present heavy atoms, pick the one
        # with the fewest extra (unexpected) heavy atoms — the tightest fit.
        # This avoids falsely reporting terminal-only atoms (e.g. OXT) as
        # missing for internal residues.
        best_heavy = None
        best_extra = None
        for variant in db['topology']:
            variant_heavy = {a for a in variant['atoms'] if not _is_hydrogen(a)}
            if present_heavy <= variant_heavy:
                extra = len(variant_heavy) - len(present_heavy)
                if best_extra is None or extra < best_extra:
                    best_extra = extra
                    best_heavy = variant_heavy
        if best_heavy is not None:
            return best_heavy

    # Fallback: first (CCD canonical) variant.
    return {a for a in db['topology'][0]['atoms'] if not _is_hydrogen(a)}
