"""Reading graphics bond encodings without inferring chemical-state identity."""

from molsysmt._private.smonitor import FormatError

_ENDPOINT_FIELDS = ("atom_pairs", "indexA", "indexB")


def _single_bond_block(value):
    """Resolving an absent, flat or uniquely wrapped bond definition."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise FormatError(reason="ViewerJSON bonds must be a dictionary.")
    if "sets" not in value:
        return value
    sets = value["sets"]
    if not isinstance(sets, list):
        raise FormatError(reason="ViewerJSON bond sets must be a list.")
    if len(sets) > 1:
        raise FormatError(
            reason="Multiple bond sets are ambiguous for native chemistry and bond queries. "
            "Copy the payload and assign the desired set to data['bonds'] explicitly."
        )
    if any(
        value.get(field) not in (None, [])
        for field in (*_ENDPOINT_FIELDS, "order", "type")
    ):
        raise FormatError(
            reason="ViewerJSON bonds mix a populated flat definition with bond sets."
        )
    return _single_bond_block(sets[0]) if sets else {}


def _decode_bond_block(value, n_atoms=None):
    """Validating one flat block and providing canonical endpoint pairs."""
    if not isinstance(value, dict):
        raise FormatError(reason="ViewerJSON bonds must be a dictionary.")
    result = dict(value)
    pairs = value.get("atom_pairs")
    a, b = value.get("indexA"), value.get("indexB")
    has_aliases = "indexA" in value or "indexB" in value
    if has_aliases:
        if not isinstance(a, list) or not isinstance(b, list) or len(a) != len(b):
            raise FormatError(
                reason="ViewerJSON bond indexA and indexB must be aligned lists."
            )
        if pairs is None:
            pairs = [list(pair) for pair in zip(a, b)]
    if pairs is None:
        pairs = []
    if not isinstance(pairs, list):
        raise FormatError(reason="ViewerJSON bond atom_pairs must be a list.")
    for row, pair in enumerate(pairs):
        if (
            not isinstance(pair, list)
            or len(pair) != 2
            or any(
                type(index) is not int
                or index < 0
                or (n_atoms is not None and index >= n_atoms)
                for index in pair
            )
        ):
            raise FormatError(
                reason="ViewerJSON bond atom_pairs must contain valid pairs of atom indices."
            )
        if has_aliases and (
            len(a) != len(pairs)
            or a[row] != pair[0]
            or b[row] != pair[1]
            or type(a[row]) is not int
            or type(b[row]) is not int
        ):
            raise FormatError(reason="ViewerJSON bond endpoint encodings disagree.")
    if has_aliases and len(a) != len(pairs):
        raise FormatError(reason="ViewerJSON bond endpoint encodings disagree.")
    for field, values in value.items():
        if field in (*_ENDPOINT_FIELDS, "sets") or values is None:
            continue
        if isinstance(values, list):
            if len(values) not in (0, len(pairs)):
                raise FormatError(
                    reason=f"ViewerJSON bond {field} must align with {len(pairs)} bond rows."
                )
        elif field in ("order", "type"):
            raise FormatError(
                reason=f"ViewerJSON bond {field} must be an aligned list or null."
            )
    result["atom_pairs"] = pairs
    return result


def _read_bonds(value, n_atoms=None):
    """Reading one unambiguous graphics bond population."""
    return _decode_bond_block(_single_bond_block(value), n_atoms=n_atoms)
