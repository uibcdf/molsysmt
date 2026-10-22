import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import FormatError
from molsysmt.native import MolSys, Structures, Topology
from molsysmt.pbc import get_box_from_lengths_and_angles

from ._bonds import _read_bonds


def _safe_array(values, length, dtype=object):
    arr = np.array(values if values is not None else [], dtype=dtype)
    if length is None:
        return arr
    if arr.shape[0] < length:
        pad_width = [(0, length - arr.shape[0])]
        arr = np.pad(arr, pad_width, constant_values=None)
    elif arr.shape[0] > length:
        arr = arr[:length]
    return arr


def _labels(values, n_atoms):
    """Normalizing labels without interpreting them as positions."""
    return [
        None if pd.isna(value) else str(value) for value in _safe_array(values, n_atoms)
    ]


def _axis(atoms, name, n_atoms, scope=None):
    """Decoding positional identity, with a declared legacy label fallback."""
    label_name, index_name = f"{name}_id", f"{name}_index"
    labels = _labels(atoms.get(label_name), n_atoms)
    if index_name in atoms:
        keys = atoms[index_name]
        if (
            not isinstance(keys, list)
            or len(keys) != n_atoms
            or any(
                value is not None and (type(value) is not int or value < 0)
                for value in keys
            )
        ):
            raise FormatError(
                reason=f"ViewerJSON {index_name} must contain one nonnegative integer or null per atom."
            )
        # Keep the source axis order even when the first atom belongs to a later element.
        unique = sorted({value for value in keys if value is not None})
    else:
        keys = [
            None if label is None else (scope[i], label) if scope is not None else label
            for i, label in enumerate(labels)
        ]
        unique = list(dict.fromkeys(value for value in keys if value is not None))
    mapping = {key: i for i, key in enumerate(unique)}
    indices = [mapping.get(key) for key in keys]
    rows = {}
    for row, index in enumerate(indices):
        if index is None:
            continue
        first = rows.setdefault(index, row)
        if labels[row] != labels[first]:
            raise FormatError(
                reason=f"ViewerJSON {label_name} disagrees within one {index_name}."
            )
    first_rows = [rows[index] for index in range(len(unique))]
    return indices, [labels[row] for row in first_rows], first_rows


def _per_group(values, group_indices, first_rows, field):
    """Checking that an atom-aligned value is well defined for each group."""
    for row, group in enumerate(group_indices):
        if group is not None and values[row] != values[first_rows[group]]:
            raise FormatError(
                reason=f"ViewerJSON {field} disagrees within one group_index."
            )
    return [values[row] for row in first_rows]


def _box_dict_to_array(box_dict):
    """Convert box dictionary to 3x3 numpy array."""
    if box_dict is None:
        return None
    if all(key in box_dict for key in ("v0", "v1", "v2")):
        return np.array([box_dict["v0"], box_dict["v1"], box_dict["v2"]], dtype=float)
    if all(
        key in box_dict
        for key in (
            "length_v0",
            "length_v1",
            "length_v2",
            "angle_v1_v2",
            "angle_v0_v2",
            "angle_v0_v1",
        )
    ):
        lengths = puw.quantity(
            np.array(
                [box_dict["length_v0"], box_dict["length_v1"], box_dict["length_v2"]],
                dtype=float,
            ),
            "nanometer",
        )
        angles = puw.quantity(
            np.array(
                [
                    box_dict["angle_v1_v2"],
                    box_dict["angle_v0_v2"],
                    box_dict["angle_v0_v1"],
                ],
                dtype=float,
            ),
            "radian",
        )
        box = get_box_from_lengths_and_angles(lengths, angles, skip_digestion=True)
        return np.asarray(puw.get_value(box, to_unit="nanometer"))
    return None


def _collect_coordinates(frames, n_atoms):
    if not frames:
        return None, None, None
    coords = []
    times = []
    boxes = []
    for frame in frames:
        positions = frame.get("coordinates", None)
        if positions is None:
            continue
        arr = np.array(positions, dtype=float)
        if arr.shape == (0,):
            arr = arr.reshape(0, 3)
        if n_atoms is not None:
            if arr.shape[0] < n_atoms:
                pad = np.full((n_atoms - arr.shape[0], 3), np.nan, dtype=float)
                arr = np.vstack((arr, pad))
            elif arr.shape[0] > n_atoms:
                arr = arr[:n_atoms]
        coords.append(arr)
        times.append(frame.get("time", None))
        boxes.append(_box_dict_to_array(frame.get("box", None)))
    if not coords:
        return None, None, None
    coords = np.stack(coords)
    times = np.array(times, dtype=float)
    box_array = None
    if boxes and all(box is not None for box in boxes):
        box_array = np.stack(boxes)
    return (
        puw.quantity(coords, "nanometer"),
        puw.quantity(times, "picosecond"),
        puw.quantity(box_array, "nanometer") if box_array is not None else None,
    )


@arg_digest(form="molsysmt.ViewerJSON")
def to_molsysmt_MolSys(
    item, skip_digestion=False, *, atom_indices="all", structure_indices="all"
):
    """
    Converting from molsysmt.ViewerJSON to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Unique atom indices (0-based) in the requested order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) in the requested order, including repetitions.

    Returns
    -------
    molsysmt.MolSys
        Native system with string ID labels and local positional indices.

    Raises
    ------
    ArgumentError
        If an index is out of range or atom indices repeat.
    FormatError
        If identity or bond metadata conflict, endpoints are invalid, or more
        than one bond set is declared without explicit selection.

    Notes
    -----
    Per-atom group_index, chain_index and entity_index columns distinguish
    elements with repeated labels. Present indices must be nonnegative integers
    or null; selected axes are compacted in source index order. Conflicting
    labels for one index are rejected. Without these columns, chain/entity IDs
    define identity and group IDs define identity within a chain. Such legacy
    payloads cannot distinguish repeated group IDs within one chain or repeated
    chain/entity IDs. Inconsistent group names or entity assignments are rejected.
    The graphics projection omits the component/molecule hierarchy. Components
    are rebuilt by the native connectivity tool from stored bonds; the reader
    supplies one synthetic molecule per represented group, with local string IDs.
    Bonds accept canonical atom_pairs or aligned legacy indexA/indexB columns.
    Empty collections and wrappers containing one bond definition are supported.
    Multiple bond sets are rejected; copy the payload and assign the intended
    set to data['bonds'] before native conversion. Sets do not declare a mapping
    to chemical states. Order/type columns use the existing native chemical-state
    translation; arbitrary graphics metadata do not become chemical assignments.

    Examples
    --------
    >>> from molsysmt.native import ViewerJSON
    >>> payload = ViewerJSON(data={"atoms": {"atom_id": ["007"],
    ...     "atom_name": ["C"], "group_id": ["L"], "chain_id": ["A"]}})
    >>> molsys = to_molsysmt_MolSys(payload)
    >>> molsys.topology.atoms["atom_id"].tolist()
    ['007']
    >>> molsys.topology.chains["chain_id"].tolist()
    ['A']

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.variables import is_all

    if not is_all(atom_indices) or not is_all(structure_indices):
        from .extract import extract

        item = extract(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )

    atoms = item.data.get("atoms", {}) or {}
    frames = (
        item.data.get(
            "structures", item.data.get("estructures", item.data.get("frames", []))
        )
        or []
    )

    # Atom-level fields
    atom_id = _safe_array(atoms.get("atom_id", None), None, dtype=object)
    atom_name = _safe_array(
        atoms.get("atom_name", None), len(atom_id) or None, dtype=object
    )
    formal_charge = _safe_array(
        atoms.get("formal_charge", None), len(atom_name) or None, dtype=object
    )
    partial_charge = _safe_array(
        atoms.get("partial_charge", None), len(atom_name) or None, dtype=object
    )

    n_atoms = len(atom_name) if atom_name is not None else len(atom_id)
    if n_atoms is None:
        n_atoms = 0

    bonds = _read_bonds(item.data.get("bonds"), n_atoms=n_atoms)

    chain_indices, chain_ids, _ = _axis(atoms, "chain", n_atoms)
    entity_indices, entity_ids, _ = _axis(atoms, "entity", n_atoms)
    # Keep the historical group_ig spelling as a read-only compatibility route.
    group_atoms = dict(atoms)
    if "group_id" not in group_atoms and "group_ig" in group_atoms:
        group_atoms["group_id"] = group_atoms["group_ig"]
    group_indices, group_ids, group_rows = _axis(
        group_atoms, "group", n_atoms, scope=chain_indices
    )
    group_names = _per_group(
        _labels(atoms.get("group_name"), n_atoms),
        group_indices,
        group_rows,
        "group_name",
    )
    group_entities = _per_group(
        entity_indices, group_indices, group_rows, "entity_index"
    )
    n_groups = len(group_ids)

    topo = Topology(
        n_atoms=n_atoms,
        n_groups=n_groups,
        n_components=0,
        n_molecules=n_groups,
        n_entities=len(entity_ids),
        n_chains=len(chain_ids),
        n_bonds=0,
        skip_digestion=True,
    )

    topo.atoms["atom_id"] = pd.Series(atom_id, dtype="string")
    topo.atoms["atom_name"] = pd.Series(atom_name, dtype=str)
    topo.atoms["atom_type"] = pd.Series(
        _labels(atoms.get("element_symbol"), n_atoms), dtype="string"
    )
    topo.atoms["group_index"] = pd.Series(group_indices, dtype="Int64")
    topo.atoms["chain_index"] = pd.Series(chain_indices, dtype="Int64")

    topo.groups["group_id"] = pd.Series(group_ids, dtype="string")
    topo.groups["group_name"] = pd.Series(group_names, dtype="string")
    topo.groups["group_type"] = pd.Series([""] * n_groups, dtype=str)
    topo.groups["molecule_index"] = pd.Series(np.arange(n_groups), dtype="Int64")

    topo.molecules["molecule_id"] = pd.Series(
        np.arange(n_groups).astype(str), dtype="string"
    )
    topo.molecules["molecule_name"] = pd.Series([""] * n_groups, dtype=str)
    topo.molecules["molecule_type"] = pd.Series([""] * n_groups, dtype=str)
    topo.molecules["entity_index"] = pd.Series(group_entities, dtype="Int64")

    topo.entities["entity_id"] = pd.Series(entity_ids, dtype="string")
    topo.entities["entity_name"] = pd.Series([""] * len(topo.entities), dtype=str)
    topo.entities["entity_type"] = pd.Series([""] * len(topo.entities), dtype=str)

    topo.chains["chain_id"] = pd.Series(chain_ids, dtype="string")
    topo.chains["chain_name"] = pd.Series([""] * len(chain_ids), dtype=str)
    topo.chains["chain_type"] = pd.Series([""] * len(chain_ids), dtype=str)

    if bonds["atom_pairs"]:
        atom_pairs = bonds["atom_pairs"]
        bond_orders = bonds.get("order", None)
        bond_types = bonds.get("type", None)
        if bond_orders is not None and len(bond_orders) == 0:
            bond_orders = None
        if bond_types is not None and len(bond_types) == 0:
            bond_types = None
        topo._append_chemical_state_bonds(
            atom_pairs,
            orders=bond_orders,
            types=bond_types,
            sort=False,
        )

    topo.rebuild_components(redefine_types=False, redefine_names=False)

    coordinates, times, boxes = _collect_coordinates(
        frames, n_atoms if n_atoms > 0 else None
    )
    structures = Structures(
        coordinates=coordinates,
        time=times,
        box=boxes,
        skip_digestion=True,
    )

    molsys = MolSys(skip_digestion=True)
    molsys.topology = topo
    molsys.structures = structures
    if formal_charge is not None or partial_charge is not None:
        from molsysmt.native import MolecularMechanics

        kwargs = {}
        if formal_charge is not None:
            kwargs["formal_charge"] = formal_charge.tolist()
        if partial_charge is not None:
            kwargs["partial_charge"] = partial_charge.tolist()
        molsys.molecular_mechanics = MolecularMechanics(**kwargs)
    else:
        molsys.molecular_mechanics = molsys.molecular_mechanics.copy()

    return molsys
