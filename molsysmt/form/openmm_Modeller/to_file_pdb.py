from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from openmm.Modeller to file.pdb.

    Parameters
    ----------
    item : openmm.Modeller
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt.form.openmm_Topology.to_file_pdb import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename,
                                           skip_digestion=True)

    return tmp_item

