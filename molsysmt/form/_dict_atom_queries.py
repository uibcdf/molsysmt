"""Reading stored atom inventory without finalizing a declarative topology.

Only fields already in native string form take the direct path. Missing/defaulted
fields retain the converter's normalization and chemistry inference. Hierarchy
counts are deliberately excluded: builder finalization can add missing parents.
"""

from numbers import Integral

from molsysmt._private.variables import is_all

_ATOM_FIELDS = frozenset(("atom_id", "atom_name", "atom_type"))


def supports(attribute, element):
    return (attribute == "n_atoms" and element in ("system", "atom")) or (
        element == "atom" and attribute in _ATOM_FIELDS | {"atom_index"}
    )


def _atoms(item, *, nested):
    data = item.data
    if nested:
        data = data.get("topology", {}) or {}
    records = data.get("atoms", [])
    if records is None:
        return []
    return records if isinstance(records, list) else None


def can_read(item, attribute, element, indices="all", *, nested):
    """Check only the fields needed by the requested stored-atom query."""
    if not supports(attribute, element):
        return False
    atoms = _atoms(item, nested=nested)
    if atoms is None:
        return False
    if not is_all(indices) and (
        indices is None or any(not isinstance(index, Integral) for index in indices)
    ):
        return False
    if attribute not in _ATOM_FIELDS:
        return True
    positions = range(len(atoms)) if is_all(indices) else indices
    return all(
        isinstance(atoms[index], dict) and isinstance(atoms[index].get(attribute), str)
        for index in positions
    )


def read(item, attribute, element, indices="all", *, nested):
    """Return a detached result, or request the existing native conversion."""
    if not can_read(item, attribute, element, indices, nested=nested):
        return NotImplemented
    atoms = _atoms(item, nested=nested)
    positions = range(len(atoms)) if is_all(indices) else indices
    if attribute == "n_atoms":
        return len(atoms) if element == "system" else len(positions)
    if attribute == "atom_index":
        return list(positions)
    return [atoms[index][attribute] for index in positions]


def can_query(item, element, attributes, indices="all", *, nested):
    """Keep bulk conversion unless every requested value has a direct route."""
    return all(
        can_read(item, attribute, element, indices, nested=nested)
        for attribute in attributes
    )


def query_docstring(attribute, element, form):
    """Describe the existing adapter boundary and its bounded direct route."""
    description = {
        "n_atoms": "Number of atoms, counting repeated selected positions.",
        "atom_index": "Atom positions in selection order, preserving repetitions.",
        "atom_id": "Atom ID labels as strings, in selection order.",
        "atom_name": "Atom names in selection order.",
        "atom_type": "Element symbols in selection order; these are not force-field types.",
    }[attribute]
    indices_doc = (
        ""
        if element == "system"
        else """    indices : str or list of int, default='all'
        Atom positions to read. The default includes every atom.
"""
    )
    result_type = "int" if attribute == "n_atoms" else "list"
    query = (
        "n_atoms=True"
        if attribute == "n_atoms"
        else f'element="atom", {attribute}=True'
    )
    expected = (
        "1"
        if attribute == "n_atoms"
        else {
            "atom_index": "[0]",
            "atom_id": "['10']",
            "atom_name": "['N']",
            "atom_type": "['N']",
        }[attribute]
    )
    nested = form == "molsysmt.MolSysDict"
    data = '{"atoms": [{"atom_id": "10", "atom_name": "N", "atom_type": "N"}]}'
    if nested:
        data = '{"topology": ' + data + "}"
    return f"""Reading {attribute} from {element} in {form}.

    Parameters
    ----------
    item : {form}
        Declarative molecular data containing the atom inventory.
{indices_doc}    skip_digestion : bool, default=False
        Whether to skip argument digestion for an already normalized internal call.

    Returns
    -------
    {result_type}
        {description}

    Notes
    -----
    Counts and indices read the stored atom inventory. ID/name/type fields read
    stored strings directly; fields requiring defaults or normalization retain
    the native converter. Public basic queries validate selection indices.
    Reading this inventory does not validate unrelated serialized domains.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.{form.split(".")[-1]}(data={data})
    >>> msm.get(molsys, {query})
    {expected}

    .. versionadded:: 1.0.0
    """
