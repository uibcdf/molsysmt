import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


def _location_position(alternates, requested):
    if requested == "occupancy":
        occupancies = np.asarray(alternates["occupancy"], dtype=float)
        position = int(np.nanargmax(occupancies))
        if np.isclose(occupancies[position], 0.5):
            matches = np.flatnonzero(
                np.asarray(alternates["location_id"], dtype=object) == "A"
            )
            if len(matches):
                position = int(matches[0])
        return position

    matches = np.flatnonzero(
        np.asarray(alternates["location_id"], dtype=object) == requested
    )
    if not len(matches):
        from molsysmt._private.smonitor import ArgumentChoiceError

        raise ArgumentChoiceError(
            argument="location_id",
            value=requested,
            caller="molsysmt.build.solve_atoms_with_alternate_location",
        )
    return int(matches[0])


@arg_digest()
def solve_atoms_with_alternate_location(
    molecular_system,
    selection="all",
    structure_indices="all",
    location_id="occupancy",
    syntax="MolSysMT",
):
    """Resolving alternate-location atoms in selected structures.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system carrying alternate-location metadata.
    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atoms whose alternate locations are resolved.
    structure_indices : int, list of int, or 'all', default 'all'
        Structures in which coordinates and B factors are updated.
    location_id : str, list, tuple, or numpy.ndarray, default 'occupancy'
        Location identifier to choose. ``'occupancy'`` chooses independently
        in every structure. A sequence supplies one identifier per selected
        atom.
    syntax : str, default 'MolSysMT'
        Syntax used to interpret a string selection.

    Returns
    -------
    None
        The molecular system is modified in place.

    Notes
    -----
    Coordinates use the units already normalized by MolSysMT, normally nm.
    B factors are stored in nm². When occupancies tie at 0.5, location ``A``
    is preferred when available.

    See Also
    --------
    :func:`molsysmt.basic.get`
        Getting alternate-location metadata.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from importlib.resources import files
    >>> filename = str(files('molsysmt.data.pdb').joinpath('1bnf.pdb'))
    >>> molecular_system = msm.convert(
    ...     filename, to_form='molsysmt.MolSys', get_missing_bonds=False
    ... )
    >>> solve_atoms_with_alternate_location(
    ...     molecular_system, selection=[480], location_id='A'
    ... )
    >>> molecular_system.structures.coordinates.shape[0]
    1

    .. admonition:: Tutorial with more examples

       See :ref:`UserGuide_Tools_Build_SolveAtomsWithAlternateLocations`.

    .. versionadded:: 1.0.0
    """

    from molsysmt import get, pyunitwizard as puw, select, set as msm_set

    alternates_by_structure = get(
        molecular_system, alternate_location=True
    )
    if alternates_by_structure is None:
        return None

    if is_all(structure_indices):
        structure_indices = np.arange(
            get(molecular_system, n_structures=True), dtype=int
        )
    else:
        structure_indices = np.atleast_1d(structure_indices).astype(int)

    selected_atoms = {
        int(index)
        for index in select(
            molecular_system, selection=selection, syntax=syntax
        )
    }
    explicit_locations = None
    if not isinstance(location_id, str):
        explicit_locations = list(location_id)
        if len(explicit_locations) != len(selected_atoms):
            from molsysmt._private.smonitor import InternalAlgorithmError

            raise InternalAlgorithmError(
                "Unexpected number of alternate-location identifiers.",
                caller="molsysmt.build.solve_atoms_with_alternate_location",
            )
        explicit_locations = dict(zip(sorted(selected_atoms), explicit_locations))

    atom_ids_to_set = {}
    for structure_index in structure_indices:
        structure_alternates = alternates_by_structure[int(structure_index)]
        atom_indices = []
        coordinates = []
        b_factors = []
        has_b_factors = True
        for atom_index, alternates in structure_alternates.items():
            atom_index = int(atom_index)
            if atom_index not in selected_atoms:
                continue
            requested = (
                location_id
                if isinstance(location_id, str)
                else explicit_locations[atom_index]
            )
            position = _location_position(alternates, requested)
            atom_indices.append(atom_index)
            coordinates.append(alternates["coordinates"][position])
            atom_ids_to_set.setdefault(
                atom_index, alternates["atom_id"][position]
            )
            if alternates.get("b_factor") is None:
                has_b_factors = False
            else:
                b_factors.append(alternates["b_factor"][position])

        if not atom_indices:
            continue
        values = {
            "coordinates": puw.quantity(
                np.asarray(
                    [
                        puw.get_value(value, to_unit="nm")
                        for value in coordinates
                    ],
                    dtype=float,
                ),
                "nm",
            )
        }
        if has_b_factors:
            values["b_factor"] = puw.quantity(
                np.asarray(
                    [
                        puw.get_value(value, to_unit="nm**2")
                        for value in b_factors
                    ],
                    dtype=float,
                ),
                "nm**2",
            )
        msm_set(
            molecular_system,
            selection=atom_indices,
            structure_indices=[int(structure_index)],
            **values,
        )

    if atom_ids_to_set:
        ordered_indices = sorted(atom_ids_to_set)
        msm_set(
            molecular_system,
            selection=ordered_indices,
            atom_id=[atom_ids_to_set[index] for index in ordered_indices],
        )
    return None
