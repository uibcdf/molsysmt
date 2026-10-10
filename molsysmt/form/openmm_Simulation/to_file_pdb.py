from molsysmt._private.argdigest import arg_digest


@arg_digest(form="openmm.Simulation")
def to_file_pdb(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from openmm.Simulation to file:pdb.


    Parameters
    ----------
    item : molecular system
        OpenMM Simulation supplying topology and the current context pose.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Requested PDB output path. The returned file belongs to the caller.

    Notes
    -----
    The single current context structure supplies coordinates and periodic box.
    MolSysMT box getters retain shape (1, 3, 3); this adapter selects that one box
    and converts it to nanometers in OpenMM units before updating a copied
    topology for writing. The source topology is unchanged. PDB coordinates and
    box lengths are serialized in angstroms by OpenMM, independently of session
    length units.


    .. versionadded:: 1.0.0
    """

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.openmm_Topology.to_file_pdb import (
        to_file_pdb as openmm_Topology_to_file_pdb,
    )
    from molsysmt.form.openmm_Topology.to_openmm_Topology import (
        to_openmm_Topology as openmm_Simulation_to_openmm_Topology,
    )

    from . import get_box_from_system, get_coordinates_from_atom

    topology = openmm_Simulation_to_openmm_Topology(
        item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
    coordinates = get_coordinates_from_atom(
        item,
        indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    box = get_box_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )
    topology.setPeriodicBoxVectors(
        None if box is None else puw.convert(box[0], "nm", to_form="openmm.unit")
    )

    tmp_item = openmm_Topology_to_file_pdb(
        topology,
        coordinates=coordinates,
        output_filename=output_filename,
        skip_digestion=True,
    )

    return tmp_item
