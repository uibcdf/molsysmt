from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import FormatError

from . import attributes
from . import get_topological_attributes as get_topo


@arg_digest(form="molsysmt.ViewerJSON")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """
    Checking if form molsysmt.ViewerJSON supports a specific attribute.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    attribute : object
        Argument attribute.
    include_none : object, default=False
        Argument include_none.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    Notes
    -----
    With include_none=False, ambiguous or malformed bond definitions raise
    FormatError rather than being reported as an absent attribute. The
    include_none=True capability query does not validate stored bond data.

    .. versionadded:: 1.0.0
    """

    if not attributes[attribute]:
        return False

    if include_none:
        return True

    atoms = molecular_system.data.get("atoms", {}) or {}
    structures = (
        molecular_system.data.get(
            "structures",
            molecular_system.data.get(
                "estructures", molecular_system.data.get("frames", [])
            ),
        )
        or []
    )

    checkers = {
        "atom_index": lambda: range(
            get_topo.get_n_atoms_from_system(molecular_system, skip_digestion=True)
        ),
        "atom_id": lambda: atoms.get("atom_id", None),
        "atom_name": lambda: atoms.get("atom_name", None),
        "group_id": lambda: atoms.get("group_id", atoms.get("group_ig", None)),
        "group_name": lambda: atoms.get("group_name", None),
        "chain_id": lambda: atoms.get("chain_id", None),
        "entity_id": lambda: atoms.get("entity_id", None),
        "formal_charge": lambda: get_topo.get_formal_charge_from_atom(
            molecular_system, skip_digestion=True
        ),
        "partial_charge": lambda: get_topo.get_partial_charge_from_atom(
            molecular_system, skip_digestion=True
        ),
        "n_atoms": lambda: get_topo.get_n_atoms_from_system(
            molecular_system, skip_digestion=True
        ),
        "n_bonds": lambda: get_topo.get_n_bonds_from_system(
            molecular_system, skip_digestion=True
        ),
        "bond_index": lambda: get_topo.get_bond_index_from_bond(
            molecular_system, skip_digestion=True
        ),
        "bond_order": lambda: get_topo.get_bond_order_from_bond(
            molecular_system, skip_digestion=True
        ),
        "bond_type": lambda: get_topo.get_bond_type_from_bond(
            molecular_system, skip_digestion=True
        ),
        "bonded_atoms": lambda: get_topo._bonds_dict(molecular_system)["atom_pairs"],
        "coordinates": lambda: [
            frame.get("coordinates")
            for frame in structures
            if frame.get("coordinates") is not None
        ],
        "time": lambda: [
            frame.get("time") for frame in structures if frame.get("time") is not None
        ],
        "n_structures": lambda: structures,
    }

    try:
        value = checkers[attribute]()
    except FormatError:
        raise
    except Exception:
        return False

    if value is None:
        return False

    import numpy as np

    if isinstance(value, (list, tuple, np.ndarray)):
        return len(value) > 0

    return True
