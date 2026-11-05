"""Resolve sparse alternate-site records before writing their primary observations."""

import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentChoiceError,
    ArgumentError,
    ArgumentLengthError,
)
from molsysmt._private.variables import is_all

_CALLER = "molsysmt.build.solve_atoms_with_alternate_location"


def _invalid_site(reason):
    return ArgumentError("alternate_location", caller=_CALLER, message=reason)


def _site_columns(alternates):
    from molsysmt import pyunitwizard as puw

    labels = np.asarray(alternates.get("location_id"), dtype=object)
    if (
        labels.ndim != 1
        or labels.size == 0
        or not all(isinstance(label, str) and len(label) == 1 for label in labels)
        or len(set(labels)) != len(labels)
    ):
        raise _invalid_site(
            "Alternate location labels must be nonempty, unique one-character strings."
        )
    raw_occupancy = alternates.get("occupancy")
    if puw.is_quantity(raw_occupancy):
        raise _invalid_site("Alternate occupancies must be unit-free values.")
    try:
        occupancies = (
            np.full(labels.size, np.nan)
            if raw_occupancy is None
            else np.asarray(raw_occupancy, dtype=float)
        )
    except (TypeError, ValueError) as error:
        raise _invalid_site(
            "Alternate occupancies must be unit-free numeric values or unknown."
        ) from error
    if occupancies.shape != labels.shape:
        raise _invalid_site(
            "Alternate occupancies must be a unit-free vector aligned with location labels."
        )
    finite = np.isfinite(occupancies)
    if (
        np.isinf(occupancies).any()
        or ((occupancies[finite] < 0) | (occupancies[finite] > 1)).any()
    ):
        raise _invalid_site(
            "Finite alternate occupancies must be between zero and one; NaN means unknown."
        )
    return labels, occupancies


def _location_position(labels, occupancies, requested):
    if requested == "occupancy":
        if not np.isfinite(occupancies).any():
            raise ArgumentError(
                "location_id",
                value=requested,
                caller=_CALLER,
                message="Maximum-occupancy selection needs at least one finite occupancy; choose a location explicitly.",
            )
        position = int(np.nanargmax(occupancies))
        maximum = occupancies[position]
        # Preserve the documented half-occupancy tie rule, never favor a lower A.
        ties = np.isclose(occupancies, maximum, rtol=1e-5, atol=1e-8)
        matches = np.flatnonzero((labels == "A") & ties)
        if np.isclose(maximum, 0.5, rtol=1e-5, atol=1e-8) and matches.size:
            position = int(matches[0])
        return position
    matches = np.flatnonzero(labels == requested)
    if not matches.size:
        raise ArgumentChoiceError(
            "location_id", requested, choices=labels.tolist(), caller=_CALLER
        )
    return int(matches[0])


def _selected_observation(alternates, requested):
    from molsysmt import pyunitwizard as puw

    labels, occupancies = _site_columns(alternates)
    position = _location_position(labels, occupancies, requested)
    raw = alternates.get("coordinates")
    if not puw.is_quantity(raw) or not puw.check(
        puw.get_unit(raw), dimensionality={"[L]": 1}
    ):
        raise _invalid_site("Alternate coordinates require explicit length units.")
    coordinates = np.asarray(puw.get_value(raw, to_unit="nm"), dtype=float)
    if (
        coordinates.shape != (len(labels), 3)
        or not np.isfinite(coordinates[position]).all()
    ):
        raise _invalid_site(
            "Chosen alternate coordinates must be finite and aligned as (n_locations, 3)."
        )
    raw = alternates.get("b_factor")
    b_factor = np.nan
    if raw is not None:
        if not puw.is_quantity(raw) or not puw.check(
            puw.get_unit(raw), dimensionality={"[L]": 2}
        ):
            raise _invalid_site(
                "Alternate B factors require explicit squared-length units."
            )
        factors = np.asarray(puw.get_value(raw, to_unit="nm**2"), dtype=float)
        if factors.shape != labels.shape or np.isinf(factors[position]):
            raise _invalid_site(
                "Alternate B factors must align with location labels and be finite or unknown."
            )
        b_factor = factors[position]
    atom_id = None
    if alternates.get("atom_id") is not None:
        identifiers = np.asarray(alternates["atom_id"], dtype=object)
        if identifiers.shape != labels.shape:
            raise _invalid_site("Alternate atom IDs must align with location labels.")
        value = identifiers[position]
        if value is not None:
            if isinstance(value, (bool, np.bool_)) or not isinstance(
                value, (str, int, np.integer)
            ):
                raise _invalid_site(
                    "Alternate atom IDs must be string/integer labels or unknown."
                )
            atom_id = str(value)
    return coordinates[position].copy(), occupancies[position], b_factor, atom_id


@signal(tags=["api", "build", "alternate-location"])
@arg_digest()
def solve_atoms_with_alternate_location(
    molecular_system,
    selection="all",
    structure_indices="all",
    location_id="occupancy",
    syntax="MolSysMT",
    *,
    skip_digestion=False,
):
    """
    Resolving alternate-location atoms in selected structures.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atoms to resolve. A location vector follows the atom order returned by
        this selection; repeated atoms must request the same location.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structures to resolve, including nonconsecutive positions. Repeated
        positions are processed once; empty selections change nothing.
    location_id : str, list, tuple or numpy.ndarray, default='occupancy'
        One location label for all selected atoms, a one-dimensional vector of
        labels aligned with the selection, or 'occupancy' for the largest known
        occupancy. Labels are case-sensitive one-character strings.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Skip argument digestion only for already validated inputs. Scientific
        site validation still precedes publication.

    Returns
    -------
    None
        The molecular system is modified in place.

    Raises
    ------
    ArgumentChoiceError
        If a requested location is absent from a selected alternate site.
    ArgumentLengthError
        If the location vector does not align with the selected atoms.
    ArgumentError
        If selected sites, units or indices cannot support the request, or
        chosen structures disagree on a stable atom ID.
    NotWithThisFormError
        If a supplied domain cannot store a required primary attribute.

    Notes
    -----
    The primary coordinates, occupancy and B factor follow the chosen site.
    Occupancies are unit-free values between zero and one; NaN means unknown
    and no renormalization is performed. Unknown values are ignored by the
    occupancy criterion; at least one known value is required. An explicit
    label may select a site with unknown occupancy. Missing optional values
    become unknown rather than retaining the previous site's measurements.

    When the maximum is close to 0.5, A is preferred only if its occupancy is
    also close to that maximum (rtol=1e-5, atol=1e-8). Other exact ties retain
    source order. Coordinates and B factors carry explicit length and squared
    length units; native storage uses nm and nm**2 independently of the active
    display-unit policy. Atom IDs remain string labels on the stable atom axis:
    selected structures must agree on each updated label.

    All selected sites, quantity shapes and writer availability are checked
    before the first mutation. A rejected request preserves source observations
    and attached analysis identities. Unexpected failures inside a mutable form
    adapter retain that adapter's existing partial-write/invalidation behavior;
    this is not a transaction across arbitrary backends or files.

    Alternate records are retained unchanged. Native MolSys geometry edits make
    affected structures unevaluated in named interaction analyses; the other
    structures and previous analysis snapshots survive. Sparse updates are
    staged without copying the full coordinates. Creating an absent primary
    occupancy/B-factor field allocates its ordinary structure-by-atom series,
    leaving unassigned positions unknown.


    See Also
    --------
    :func:`molsysmt.basic.get`
        Getting alternate-location metadata.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from importlib.resources import files
    >>> filename = str(files('molsysmt.data.pdb').joinpath('1bnf.pdb'))
    >>> molsys = msm.convert(
    ...     filename, to_form='molsysmt.MolSys', get_missing_bonds=False
    ... )
    >>> solve_atoms_with_alternate_location(
    ...     molsys, selection=[480], location_id='A'
    ... )
    >>> molsys.structures.coordinates.shape[0]
    1


    .. admonition:: Tutorial with more examples

       See :ref:`Resolving alternate locations <Tutorial_Solve_atoms_with_alternate_locations>`.

    .. versionadded:: 1.0.0
    """

    from molsysmt import get, has_attribute, select, where_is_attribute
    from molsysmt import pyunitwizard as puw
    from molsysmt import set as msm_set
    from molsysmt.basic._index_validation import (
        validate_element_indices,
        validate_structure_indices,
    )
    from molsysmt.form import _dict_modules

    structures = validate_structure_indices(
        molecular_system, structure_indices, _CALLER
    )
    if structures is None:
        return None
    if is_all(structures):
        structures = range(get(molecular_system, n_structures=True))
    structures = list(dict.fromkeys(int(index) for index in structures))
    atoms = validate_element_indices(
        molecular_system,
        select(molecular_system, selection=selection, syntax=syntax),
        "atom",
        "selection",
        _CALLER,
    )
    atoms = [] if atoms is None else list(atoms)
    explicit_locations = {}
    if not isinstance(location_id, str):
        if len(location_id) != len(atoms):
            raise ArgumentLengthError(
                "location_id", len(atoms), len(location_id), caller=_CALLER
            )
        for atom, location in zip(atoms, location_id, strict=True):
            if atom in explicit_locations and explicit_locations[atom] != location:
                raise ArgumentError(
                    "location_id",
                    caller=_CALLER,
                    message="Repeated atoms cannot request different locations.",
                )
            explicit_locations[atom] = location
    if not structures or not atoms:
        return None
    selected_atoms = set(atoms)
    alternates_by_structure = get(
        molecular_system, structure_indices=structures, alternate_location=True
    )
    if alternates_by_structure is None:
        return None

    # Prepare every selected site and quantity before invoking a mutable adapter.
    plan = []
    atom_ids_to_set = {}
    for structure, structure_alternates in zip(
        structures, alternates_by_structure, strict=True
    ):
        indices, coordinates, occupancies, b_factors = [], [], [], []
        for atom, alternates in structure_alternates.items():
            if atom not in selected_atoms:
                continue
            requested = (
                location_id
                if isinstance(location_id, str)
                else explicit_locations[atom]
            )
            coordinate, occupancy, b_factor, atom_id = _selected_observation(
                alternates, requested
            )
            if atom_id is not None:
                if atom in atom_ids_to_set and atom_ids_to_set[atom] != atom_id:
                    raise _invalid_site(
                        "Chosen structures disagree on a stable atom ID; resolve them separately with explicit label handling."
                    )
                atom_ids_to_set[atom] = atom_id
            indices.append(int(atom))
            coordinates.append(coordinate)
            occupancies.append(occupancy)
            b_factors.append(b_factor)
        if indices:
            plan.append(
                (
                    structure,
                    indices,
                    {
                        "coordinates": puw.quantity(
                            np.asarray(coordinates, dtype=float)[None, :, :], "nm"
                        ),
                        "occupancy": np.asarray(occupancies, dtype=float)[None, :],
                        "b_factor": puw.quantity(
                            np.asarray(b_factors, dtype=float)[None, :], "nm**2"
                        ),
                    },
                )
            )
    if not plan:
        return None
    # Unknown optional observations remain unknown; do not invent measurements.
    has_b_factors = has_attribute(molecular_system, "b_factor")
    has_occupancies = has_attribute(molecular_system, "occupancy")
    for structure, indices, values in plan:
        if not has_b_factors and np.isnan(puw.get_value(values["b_factor"])).all():
            values.pop("b_factor")
        if not has_occupancies and np.isnan(values["occupancy"]).all():
            values.pop("occupancy")
    attributes = set().union(*(values.keys() for _, _, values in plan))
    if atom_ids_to_set:
        attributes.add("atom_id")
    for attribute in attributes:
        _, form = where_is_attribute(molecular_system, attribute, include_none=False)
        writer = (
            None
            if form is None
            else getattr(_dict_modules[form], f"set_{attribute}_to_atom", None)
        )
        if not callable(writer):
            from molsysmt._private.smonitor import NotWithThisFormError

            raise NotWithThisFormError(
                caller=_CALLER,
                requested_attribute=attribute,
                message=f"No supplied domain can store resolved {attribute!r}; supply the required native domains.",
            )
    for structure, indices, values in plan:
        msm_set(
            molecular_system, selection=indices, structure_indices=[structure], **values
        )
    if atom_ids_to_set:
        ordered = sorted(atom_ids_to_set)
        msm_set(
            molecular_system,
            selection=ordered,
            atom_id=[atom_ids_to_set[index] for index in ordered],
        )
    return None
