from molsysmt._private.digestion import digest
import h5py

@digest(form='openmm.Topology')
def to_file_msmh5(item, atom_indices='all', coordinates=None, output_filename=None):

    from molsysmt.native.file_msmh5 import version as msmh5_version

    fff = h5py.File(output_filename, "w")

    fff.attrs['version'] = "1.0"
    fff.attrs['type'] = "msmh5"
    fff.attrs['creator'] = "molsysmt"

    add_topology_to_msmh5(item, fff, atom_indices=atom_indices, coordinates=coordinates)

    fff.close()

    tmp_item = output_filename

    return tmp_item

@digest(form='openmm.Topology')
def add_topology_to_msmh5(item, file, atom_indices='all', coordinates=None):

    raise NotImplementedError
