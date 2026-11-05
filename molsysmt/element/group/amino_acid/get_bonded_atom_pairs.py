import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.reference_bonds import DIGEST_OPTIONS

_sorted = sorted


@arg_digest(**DIGEST_OPTIONS)
def get_bonded_atom_pairs(
    group_name,
    atom_names,
    atom_indices=None,
    sorted=True,
    skip_digestion=False,
    *,
    naming_scheme=None,
):
    """Getting reference bond index pairs for an amino-acid group.

    Parameters
    ----------
    group_name : str
        Case-sensitive amino-acid name in the bundled reference catalogue.
    atom_names : str, list of str, tuple of str, or numpy.ndarray
        One-dimensional atom names in caller order. Supply the names for the
        reference layout to query; this is not a molecular-system selection.
        A single atom-name string is accepted as a one-atom query. Repeated
        names retain all supplied occurrences; they are not alternate-location
        filtering instructions.
    atom_indices : int, list of int, tuple of int, or numpy.ndarray, default=None
        One nonnegative integer per supplied name, in the same order. None uses local
        positions 0 through len(atom_names)-1. Explicit indices are mapping
        labels, not positions to select from atom_names or a molecular system.
        A scalar integer is also accepted for a single supplied name.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. False retains template
        bond order. Each pair has its smaller mapped endpoint first.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    naming_scheme : str or none, default=None
        Keyword-only source group vocabulary: sequence, amber, ccd or legacy.
        Ambiguous labels require context. Amber state variants are checked against
        the bundled heavy connectivity and H counts; other meanings cannot reuse them.

    Returns
    -------
    list of list of int or None
        Reference bonds with both names present, mapped to the supplied indices
        or local positions. Explicit maps are normalized to NumPy integer
        scalars. Empty names return an empty list for a recognized group.
        Unknown names and unmatched reference layouts return None.

    Raises
    ------
    ArgumentError
        If the argument digester rejects an input value.

    ArgumentLengthError
        If the explicit map does not contain exactly one index per atom name.

    Notes
    -----
    Maps may contain repeated indices and are not permutations. Values must
    fit int64 and be unit-free and unmasked. Strings, floats, booleans,
    negative indices and nested maps are
    rejected before reference access. An empty name sequence requires an empty
    map or None. Existing skip_digestion=True routes require already valid inputs.

    Matching includes the available terminal reference variants. If names repeat,
    each reference edge expands over the corresponding supplied occurrences.
    This preserves the existing lookup behavior and does not establish which
    alternate locations should coexist. Unmatched layouts retain their legacy
    warning and None result.

    Naming context selects bounded exact-name references, never a sequence parent.
    Standard labels retain their terminal naming layouts; HIS also admits only the
    checked HID/HIE/HIP layouts matching observed H names. Raw unrelated catalogue
    entries are not searched. Reached data are credited through optional Ackredit.
    Unsupported profiles/layouts return None, without a fallback to a parent.

    This queries bundled reference connectivity. It does not inspect coordinates,
    infer the graph of a molecular system, assign a chemical state or add bonds.
    Caller-owned names and index maps are not modified. Supply a flat integer
    map with exactly one entry per name when atom_indices is given.

    See Also
    --------
    molsysmt.chemical_states.get_bondgraph
    molsysmt.build.get_missing_bonds

    Examples
    --------
    >>> from molsysmt.element.group.amino_acid import get_bonded_atom_pairs
    >>> pairs = get_bonded_atom_pairs('ALA', ['N', 'CA', 'C', 'O', 'CB'],
    ...                              atom_indices=[1040, 1009, 1030, 1007, 1012])
    >>> [[int(index) for index in pair] for pair in pairs]
    [[1007, 1030], [1009, 1012], [1009, 1030], [1009, 1040]]
    >>> get_bonded_atom_pairs('ALA', [])
    []

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for local and explicit mapping.

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.amino_acid_templates import (
        _catalogue,
        credit,
        family,
        variants,
    )
    from molsysmt.element.group.amino_acid import group_names

    caller = "molsysmt.element.group.amino_acid.get_bonded_atom_pairs"
    kind = family(group_name, naming_scheme, caller=caller)
    candidates = variants(group_name, naming_scheme, caller=caller)
    if candidates is None:
        return None
    references = [(group_name, kind, candidate) for candidate in candidates]
    if kind == "standard":
        for prefix in ("C", "N"):
            name = prefix + group_name
            if name in group_names:
                references.extend(
                    (name, kind, candidate) for candidate in _catalogue(name)
                )
        if group_name == "HIS":
            # Observed H names may identify an internal histidine layout. Search
            # only checked histidine states, never unrelated catalogue entries.
            for name in ("HID", "HIE", "HIP"):
                references.extend(
                    (name, "amber_state", candidate)
                    for candidate in variants(name, "amber", caller=caller)
                )
    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()
    mapping = {}
    for name, index in zip(atom_names, atom_indices):
        mapping.setdefault(name, []).append(index)
    for reference_name, reference_kind, variant in references:
        if set(atom_names) <= set(variant["atoms"]):
            pairs = []
            for first, second in variant["bonds"]:
                for a in mapping.get(first, ()):
                    for b in mapping.get(second, ()):
                        pairs.append([min(a, b), max(a, b)])
            credit(reference_name, reference_kind, caller)
            return _sorted(pairs) if sorted else pairs
    print(f"Warning! The amino acid {group_name} has no template.")
    print("No bonds were added by element.group.amino_acid.get_bonded_atom_pairs")
    return None
