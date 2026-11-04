from molsysmt._private.argdigest import arg_digest
from molsysmt._private.argdigest.reference_bonds import DIGEST_OPTIONS


@arg_digest(**DIGEST_OPTIONS)
def get_bonded_atom_pairs(group_name, atom_names, atom_indices=None, sorted=True):
    """Getting reference bond index pairs for a named group.

    Parameters
    ----------
    group_name : str
        Case-sensitive group name used to choose its bundled reference family.
    atom_names : str, list of str, tuple of str, or numpy.ndarray
        One-dimensional atom names in caller order. Supply the names for the
        reference layout to query; this is not a molecular-system selection.
    atom_indices : int, list of int, tuple of int, or numpy.ndarray, default=None
        One nonnegative integer per supplied name, in the same order. None uses local
        positions 0 through len(atom_names)-1. Explicit indices are mapping
        labels, not positions to select from atom_names or a molecular system.
        Amino-acid and ion routes also accept a scalar for one supplied name.
    sorted : bool, default=True
        Whether to sort pair rows lexicographically. Family conventions for
        endpoint orientation and unsorted row order are described below.

    Returns
    -------
    list of list of int or None
        Bond pairs mapped to local positions or the supplied integer indices.
        NumPy integer scalars can be retained. An empty list means the chosen
        lookup returned no bonds; None means no supported result was found.

    Raises
    ------
    ArgumentError
        If a delegated family rejects an argument during validation.
    ArgumentLengthError
        If the explicit map does not contain exactly one index per atom name.
    InternalAlgorithmError
        If a delegated family reports an unknown group or unmatched layout.

    Notes
    -----
    Maps may contain repeated indices and are not permutations. Values must
    fit int64 and be unit-free and unmasked. Strings, floats, booleans,
    negative indices and nested maps are
    rejected before reference access. An empty name sequence requires an empty
    map or None.

    Amino-acid, ion, saccharide, small-molecule, terminal-capping and water
    lookups are supported. Lipid, nucleotide and polysaccharide routes return
    None. Unknown group names also return None with the legacy warning.

    The five stored-template families orient each pair with its smaller mapped
    index first. Water keeps oxygen first, even when its index is larger.
    sorted=True sorts rows; False retains template order, or hydrogen encounter
    order for water. Repeated-name handling and unknown/layout outcomes remain
    family-specific: consult the family helper for those details.

    Amino-acid and ion lookups also accept a single atom-name string. The other
    families require a flat sequence of strings. Atom indices are unrelated to
    atom IDs, which are labels in a molecular system.

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
    >>> from molsysmt.element.group import get_bonded_atom_pairs
    >>> get_bonded_atom_pairs('ALA', ['N', 'CA'])
    [[0, 1]]
    >>> pairs = get_bonded_atom_pairs('ALA', ['N', 'CA'], atom_indices=[20, 10])
    >>> [[int(index) for index in pair] for pair in pairs]
    [[10, 20]]
    >>> get_bonded_atom_pairs('DA', []) is None
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_bonded_atom_pairs` for local and explicit mapping.

    .. versionadded:: 1.0.0
    """

    from .amino_acid import (
        get_bonded_atom_pairs as get_bonded_atom_pairs_from_amino_acid,
    )
    from .get_group_type import get_group_type_from_group_name
    from .ion import get_bonded_atom_pairs as get_bonded_atom_pairs_from_ion
    from .saccharide import (
        get_bonded_atom_pairs as get_bonded_atom_pairs_from_saccharide,
    )
    from .small_molecule import (
        get_bonded_atom_pairs as get_bonded_atom_pairs_from_small_molecule,
    )
    from .terminal_capping import (
        get_bonded_atom_pairs as get_bonded_atom_pairs_from_terminal_capping,
    )
    from .water import get_bonded_atom_pairs as get_bonded_atom_pairs_from_water

    group_type = get_group_type_from_group_name(group_name)

    bonds = None

    match group_type:
        case "amino acid":
            bonds = get_bonded_atom_pairs_from_amino_acid(
                group_name, atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case "ion":
            bonds = get_bonded_atom_pairs_from_ion(
                group_name, atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case "lipid":
            pass

        case "nucleotide":
            pass

        case "polysaccharide":
            pass

        case "saccharide":
            bonds = get_bonded_atom_pairs_from_saccharide(
                group_name, atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case "small molecule":
            bonds = get_bonded_atom_pairs_from_small_molecule(
                group_name, atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case "terminal capping":
            bonds = get_bonded_atom_pairs_from_terminal_capping(
                group_name, atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case "water":
            bonds = get_bonded_atom_pairs_from_water(
                atom_names, atom_indices=atom_indices, sorted=sorted
            )

        case _:
            print(f"Warning! The amino acid {group_name} has no template.")

    return bonds
