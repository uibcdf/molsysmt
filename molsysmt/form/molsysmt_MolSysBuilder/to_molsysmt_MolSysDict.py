from molsysmt._private.argdigest import arg_digest
from molsysmt.form._serialization import normalize_scalar as _normalize_scalar


def _matches_index(value, index):
    normalized = _normalize_scalar(value)
    return normalized is not None and int(normalized) == index


@arg_digest(form="molsysmt.MolSysBuilder")
def to_molsysmt_MolSysDict(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
):
    """
    Converting from molsysmt.MolSysBuilder to molsysmt.MolSysDict.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSysDict
        Resulting object in molsysmt.MolSysDict form.


    Notes
    -----
    Nullable table fields become Python scalars or None, including typed isotope
    and bond-order numbers. The emitted record schema is 0.2 and retains independent stable inventory,
    chemical states, structures and their explicit associations.

    Examples
    --------
    >>> import json
    >>> import molsysmt as msm
    >>> molsys = msm.MolSysBuilder()
    >>> _ = molsys.add_atom(atom_name="C", atom_type="C")
    >>> molsys.topology.atoms.loc[0, "isotope"] = 13
    >>> records = msm.convert(molsys, to_form="molsysmt.MolSysDict").to_dict()
    >>> json.loads(json.dumps(records))["topology"]["atoms"][0]["isotope"]
    13

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSysDict import (
        to_molsysmt_MolSysDict as encode,
    )

    return encode(
        item._query_view(),
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
