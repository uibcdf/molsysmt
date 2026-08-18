from molsysmt._private.argdigest import arg_digest

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def append_structures(item, structure_id=None, time=None, coordinates=None, velocities=None,
                      box=None, temperature=None, potential_energy=None, kinetic_energy=None,
                      atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Appending coordinate structures to an item of form molsysviewer.MolSysView.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_id : object, default=None
        Argument structure_id.
    time : object, default=None
        Argument time.
    coordinates : object, default=None
        Argument coordinates.
    velocities : object, default=None
        Argument velocities.
    box : object, default=None
        Argument box.
    temperature : object, default=None
        Argument temperature.
    potential_energy : object, default=None
        Argument potential_energy.
    kinetic_energy : object, default=None
        Argument kinetic_energy.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysviewer.MolSysView
        Resulting object in molsysviewer.MolSysView form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.append_structures import append_structures as molsys_append_structures

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    molsys_append_structures(
        tmp_item,
        structure_id=structure_id,
        time=time,
        coordinates=coordinates,
        velocities=velocities,
        box=box,
        temperature=temperature,
        potential_energy=potential_energy,
        kinetic_energy=kinetic_energy,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    item._molsys = tmp_item
    return None
