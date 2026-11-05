from importlib.resources import files

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.pbc_validation import validate_box_array


@signal(tags=["build", "solvation"])
@arg_digest()
def make_water_box(box, form="molsysmt.MolSys", skip_digestion=False):
    """
    Building a water box from the bundled SPC reference configuration.

    Replicate the bundled cubic ``spc216.gro`` tile to cover the Cartesian
    bounding box of one requested cell, including tilted or rotated boxes.
    Retain complete three-point waters whose oxygen lies inside that cell.
    Inventory and bonds are populated; no force-field parameters are assigned.


    Parameters
    ----------
    box : quantity
        One finite, nonsingular periodic box with vectors as rows, shaped
        ``(3, 3)`` or ``(1, 3, 3)``, in units of length. The origin is zero.
    form : str, default='molsysmt.MolSys'
        Requested output form, using public conversion when different from
        native MolSys. Its required information and optional providers must
        be available.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system
        Independent water system in the requested form. Default native output
        has coordinates ``(1, n_atoms, 3)`` and box ``(1, 3, 3)`` in canonical
        nanometers, with two O-H bonds per group. No retained waters gives
        coordinates ``(1, 0, 3)`` and zero atoms, groups and bonds.

    Raises
    ------
    ArgumentError
        If box units or array shape are invalid.
    StructuralInconsistencyError
        If the box is absent, nonfinite, numerically singular, or contains
        zero or multiple structure entries.

    Notes
    -----
    With box row vectors ``B``, Cartesian and fractional coordinates obey
    ``r = f @ B``. Keep a water if its oxygen satisfies ``0 <= f < 1`` on
    every axis. Hydrogens can extend beyond a face: each reference molecule
    is translated as a whole and is never wrapped atom by atom.

    The reference file labels its configuration SPC-MODEL at 300 K. Its reuse
    does not assign SPC/E or another force field, charges or an equilibrated
    state to the output. Finite clipping does not prescribe an exact density
    or guarantee the absence of overlaps at the new periodic boundaries.
    Assess packing before using the result for simulation.

    Native storage remains in nanometers without changing the application's
    unit policy. Use PyUnitWizard conversion or standardization for another
    presentation unit.

    See Also
    --------
    molsysmt.build.solvate
        Adding solvent around an existing molecular system.
    molsysmt.pbc.wrap_to_pbc
        Representing existing molecules in a periodic box.

    Examples
    --------
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> box = msm.pyunitwizard.quantity(2 * np.eye(3), 'nm')
    >>> molsys = msm.build.make_water_box(box)
    >>> msm.get(molsys, n_waters=True)
    268

    .. admonition:: User guide

       See :ref:`Tutorial_Make_water_box` for tilted cells and packing limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys

    box_values = None if box is None else puw.get_value(box, to_unit="nm")
    box_matrix = validate_box_array(
        box_values, 1, caller="molsysmt.build.make_water_box"
    )[0].copy()
    inv_box = np.linalg.inv(box_matrix)

    tile, length_tile = _load_reference_tile()

    Os_indices = np.arange(0, 216) * 3

    a_vec, b_vec, c_vec = box_matrix
    corners = np.array(
        [
            [0.0, 0.0, 0.0],
            a_vec,
            b_vec,
            c_vec,
            a_vec + b_vec,
            a_vec + c_vec,
            b_vec + c_vec,
            a_vec + b_vec + c_vec,
        ]
    )
    min_corner = corners.min(axis=0)
    max_corner = corners.max(axis=0)
    ortho_lengths = max_corner - min_corner

    n_tiles_x = np.ceil(ortho_lengths[0] / length_tile).astype(int)
    n_tiles_y = np.ceil(ortho_lengths[1] / length_tile).astype(int)
    n_tiles_z = np.ceil(ortho_lengths[2] / length_tile).astype(int)

    new_coors = []

    for ii in range(n_tiles_x):
        for jj in range(n_tiles_y):
            for kk in range(n_tiles_z):
                aux_tile = tile.copy()
                aux_tile[:, 0] += min_corner[0] + ii * length_tile
                aux_tile[:, 1] += min_corner[1] + jj * length_tile
                aux_tile[:, 2] += min_corner[2] + kk * length_tile

                coors_Os = aux_tile[Os_indices]
                fractional = coors_Os @ inv_box
                mask = np.all((fractional >= 0.0) & (fractional < 1.0), axis=1)
                new_coors.append(aux_tile[np.repeat(mask, 3), :])

    new_coors = np.concatenate(new_coors)

    del (tile, aux_tile, inv_box)

    n_atoms = new_coors.shape[0]
    n_waters = int(n_atoms / 3)

    output = MolSys(
        n_atoms=n_atoms,
        n_groups=n_waters,
        n_components=n_waters,
        n_molecules=n_waters,
        n_entities=1,
        n_chains=1,
        n_bonds=2 * n_waters,
        skip_digestion=True,
    )

    output.structures.box = puw.quantity(box_matrix[np.newaxis, :, :], "nm")
    output.structures.coordinates = puw.quantity(new_coors[np.newaxis, :, :], "nm")
    output.structures.box = puw.standardize(output.structures.box)
    output.structures.coordinates = puw.standardize(output.structures.coordinates)

    del (new_coors, box_matrix)

    output.topology.atoms["atom_id"] = np.arange(n_atoms)
    output.topology.atoms["atom_name"] = np.tile(["OW", "HW1", "HW2"], n_waters)
    output.topology.atoms["atom_type"] = np.tile(["O", "H", "H"], n_waters)
    output.topology.atoms["group_index"] = np.repeat(np.arange(n_waters), 3)
    output.chemical_states._set_component_indices(np.repeat(np.arange(n_waters), 3))
    output.topology.atoms["chain_index"] = 0
    output.topology.groups["group_id"] = np.arange(n_waters)
    output.topology.groups["group_name"] = "WAT"
    output.topology.groups["group_type"] = "water"
    output.topology.groups["molecule_index"] = np.arange(n_waters)
    output.chemical_states._resolve_chemical_state().components["component_id"] = (
        np.arange(n_waters)
    )
    output.chemical_states._resolve_chemical_state().components["component_name"] = (
        "water"
    )
    output.chemical_states._resolve_chemical_state().components["component_type"] = (
        "water"
    )
    output.topology.molecules["molecule_name"] = "water"
    output.topology.molecules["molecule_id"] = np.arange(n_waters)
    output.topology.molecules["molecule_type"] = "water"
    output.topology.molecules["entity_index"] = 0
    output.topology.entities["entity_name"] = "water"
    output.topology.entities["entity_id"] = 0
    output.topology.entities["entity_type"] = "water"
    output.topology.chains["chain_name"] = "A"
    output.topology.chains["chain_id"] = 0
    output.topology.chains["chain_type"] = "system"

    aux = np.zeros(n_waters * 2, dtype="int")
    mask = np.arange(0, n_waters * 2, 2)
    aux[mask] = np.arange(1, n_atoms, 3)
    mask = np.arange(1, n_waters * 2, 2)
    aux[mask] = np.arange(2, n_atoms, 3)

    bonds = output.chemical_states._get_chemical_state_bonds()
    bonds["atom1_index"] = np.repeat(np.arange(n_waters) * 3, 2)
    bonds["atom2_index"] = aux
    bonds._remove_empty_columns()

    del (aux, mask)

    output.topology._coerce_id_columns_to_string()
    output.chemical_states._resolve_chemical_state().components["component_id"] = (
        output.chemical_states._resolve_chemical_state()
        .components["component_id"]
        .astype("string")
    )
    if form == "molsysmt.MolSys":
        return output

    from molsysmt.basic import convert

    return convert(output, to_form=form)


def _load_reference_tile():
    """Read and translate the fixed SPC reference into its positive cubic tile."""
    from molsysmt.form.file_gro.to_molsysmt_Structures import to_molsysmt_Structures

    path = files("molsysmt.data.gro").joinpath("spc216.gro")
    reference = to_molsysmt_Structures(path)
    tile = puw.get_value(reference.coordinates[0], to_unit="nm").copy()
    length = 1.86206  # nm, as declared by the bundled reference box.
    tile += length / 2.0
    return tile, length
