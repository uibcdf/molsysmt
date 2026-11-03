from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["conversion"])
@arg_digest(form="molsysmt.MolSys")
def to_openmm_Topology(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from molsysmt.MolSys to openmm.Topology.


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
    openmm.Topology
        Resulting object in openmm.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology._from_native import export_native

    from . import get_box_from_system

    box = (
        None
        if item.structures is None
        else get_box_from_system(
            item, structure_indices=structure_indices, skip_digestion=True
        )
    )
    return export_native(
        item.topology,
        atom_indices=atom_indices,
        chemical_states=item.chemical_states,
        box=box,
        skip_digestion=True,
    )
