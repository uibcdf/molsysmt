from copy import deepcopy

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, FormatError
from molsysmt._private.variables import is_all


def _subset_column(values, indices, length, field):
    """Selecting an aligned JSON column without NumPy scalar coercion."""
    if values is None:
        return None
    if not isinstance(values, list) or len(values) not in (0, length):
        raise FormatError(
            reason=f"ViewerJSON {field} must be empty or aligned with its axis of length {length}."
        )
    return [values[index] for index in indices] if values else []


def _subset_bonds(bonds, atom_map, n_atoms):
    """Filtering graphics bond rows and translating their endpoint encodings."""
    if not isinstance(bonds, dict):
        raise FormatError(reason="ViewerJSON bonds must be a dictionary.")
    result = dict(bonds)
    if "sets" in bonds:
        if not isinstance(bonds["sets"], list):
            raise FormatError(reason="ViewerJSON bond sets must be a list.")
        result["sets"] = [
            _subset_bonds(block, atom_map, n_atoms) for block in bonds["sets"]
        ]
    has_aliases = "indexA" in bonds or "indexB" in bonds
    if has_aliases:
        a, b = bonds.get("indexA"), bonds.get("indexB")
        if not isinstance(a, list) or not isinstance(b, list) or len(a) != len(b):
            raise FormatError(
                reason="ViewerJSON bond indexA and indexB must be aligned lists."
            )
        alias_pairs = [list(pair) for pair in zip(a, b)]
    pairs = bonds.get("atom_pairs", alias_pairs if has_aliases else None)
    if pairs is None:
        return result
    if not isinstance(pairs, list) or any(
        not isinstance(pair, list)
        or len(pair) != 2
        or any(type(index) is not int or not 0 <= index < n_atoms for index in pair)
        for pair in pairs
    ):
        raise FormatError(
            reason="ViewerJSON bond atom_pairs must contain valid pairs of atom indices."
        )
    if has_aliases and alias_pairs != pairs:
        raise FormatError(reason="ViewerJSON bond endpoint encodings disagree.")
    rows = [i for i, (a, b) in enumerate(pairs) if a in atom_map and b in atom_map]
    for field, values in bonds.items():
        if field not in ("atom_pairs", "indexA", "indexB", "sets") and isinstance(
            values, list
        ):
            result[field] = _subset_column(values, rows, len(pairs), f"bond {field}")
    result["atom_pairs"] = [
        [atom_map[pairs[i][0]], atom_map[pairs[i][1]]] for i in rows
    ]
    if has_aliases:
        result["indexA"] = [pair[0] for pair in result["atom_pairs"]]
        result["indexB"] = [pair[1] for pair in result["atom_pairs"]]
    return result


@arg_digest(form="molsysmt.ViewerJSON")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting aligned atoms, bonds and structures from ViewerJSON.

    Parameters
    ----------
    item : molecular system
        Molecular system in molsysmt.ViewerJSON form.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Unique atom indices (0-based) in the requested output order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) in the requested order, including repetitions.
    copy_if_all : bool, default=True
        Whether unrestricted extraction copies the payload instead of returning it.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Independent graphics subset with positional bond endpoints remapped and
        bond columns aligned. Coordinates remain in nm, time in ps and box
        vectors in nm. Unrestricted copy_if_all=False returns the original.

    Raises
    ------
    ArgumentError
        If an index is out of range or atom indices repeat.
    FormatError
        If selected atom/bond columns or bond endpoint encodings are inconsistent.

    Notes
    -----
    Bonds survive only when both endpoints are selected. Repeated atom indices
    are rejected because extraction does not define cloning atoms and their bonds.
    Optional empty columns remain absent. Legacy indexA/indexB fields and bond
    sets are filtered with the same atom map; legacy endpoints gain atom_pairs.
    List-valued fields in a bond block are aligned bond columns. Structure aliases
    frames/estructures normalize to structures on subset extraction. Group, chain
    and entity indices remain source positions for native recovery to compact.
    Only selected structures and atom rows are copied; this is resident JSON
    extraction, not an on-disk query or a full native-domain persistence route.

    Examples
    --------
    >>> from molsysmt.native import ViewerJSON
    >>> payload = ViewerJSON(data={"atoms": {"atom_id": ["A", "B", "C"]},
    ...     "bonds": {"atom_pairs": [[0, 1], [1, 2]], "order": [1, 2]}})
    >>> subset = extract(payload, atom_indices=[2, 1])
    >>> subset.data["bonds"]
    {'atom_pairs': [[1, 0]], 'order': [2]}

    .. admonition:: User guide

       See :ref:`user-foundations-native-world-classes-molsysmt-viewerjson`.

    .. versionadded:: 1.0.0
    """
    if is_all(atom_indices) and is_all(structure_indices):
        return deepcopy(item) if copy_if_all else item

    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )

    from .get_topological_attributes import get_n_atoms_from_system

    n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    structures = (
        item.data.get(
            "structures", item.data.get("estructures", item.data.get("frames", []))
        )
        or []
    )
    caller = "molsysmt.form.molsysmt_ViewerJSON.extract"
    atom_indices = validate_element_indices(
        item,
        atom_indices,
        "atom",
        "atom_indices",
        caller,
        count_getter=lambda _: n_atoms,
    )
    structure_indices = validate_structure_indices(
        item, structure_indices, caller, count_getter=lambda _: len(structures)
    )
    data = dict(item.data)
    if atom_indices is not None and not is_all(atom_indices):
        if len(set(atom_indices)) != len(atom_indices):
            raise ArgumentError(
                argument="atom_indices",
                value=atom_indices,
                caller=caller,
                message="ViewerJSON extraction requires unique atom indices; duplicates are ambiguous.",
            )
        data["atoms"] = {
            field: _subset_column(values, atom_indices, n_atoms, f"atom {field}")
            for field, values in (item.data.get("atoms") or {}).items()
        }
        data["bonds"] = _subset_bonds(
            item.data.get("bonds") or {},
            {old: new for new, old in enumerate(atom_indices)},
            n_atoms,
        )
    selected_structures = (
        range(len(structures))
        if structure_indices is None or is_all(structure_indices)
        else structure_indices
    )
    data["structures"] = []
    for index in selected_structures:
        structure = dict(structures[index])
        if (
            atom_indices is not None
            and not is_all(atom_indices)
            and structure.get("coordinates") is not None
        ):
            structure["coordinates"] = _subset_column(
                structure["coordinates"], atom_indices, n_atoms, "structure coordinates"
            )
        data["structures"].append(structure)
    data.pop("frames", None)
    data.pop("estructures", None)
    # Copy the selected data first, then retain wrapper/subclass metadata through
    # its normal memo-aware protocol without copying the discarded trajectory.
    memo = {}
    copied_data = deepcopy(data, memo)
    memo[id(item.data)] = copied_data
    return deepcopy(item, memo)
