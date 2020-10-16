from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'pdb': form_name,
    'PDB': form_name
    }

info = ["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]
with_topology=True
with_trajectory=True

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_pdb as pdb_to_molsysmt_MolSys
    tmp_item = pdb_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.files import from_pdb as pdb_to_molsysmt_Topology
    tmp_item = pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_pdb as pdb_to_molsysmt_Trajectory
    tmp_item = pdb_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molsysmt.forms.classes.api_mdanalysis_Universe import extract as extract_universe
    tmp_item = mdanalysis_Universe(item)
    tmp_item = extract_universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdanalysis_topology_PDBParser import to_mdanalysis_Topology as mdanalysis_topology_PDBParser_to_mdanalysis_Topology

    tmp_item = to_mdanalysis_topology_PDBParser(item)
    tmp_item = mdanalysis_topology_PDBParser_to_mdanalysis_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_topology_PDBParser(item, atom_indices='all', frame_indices='all'):

    from MDAnalysis.topology import PDBParser

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.forms.classes.api_mdtraj_Topology import extract as extract_mdtraj_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_item = extract_mdtraj_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molsysmt.forms.classes.api_mdtraj_Trajectory import extract as extract_mdtraj_trajectory
    tmp_item = mdtraj_pdb_loader(item)
    tmp_item = extract_mdtraj_trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', frame_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    return PDBTrajectoryFile(item)

def to_mol2(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.save(output_filepath)

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology
    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from simtk.openmm.app.modeller import Modeller
    from molsysmt.forms.classes.api_openmm_Modeller import extract as extract_modeller
    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    tmp_item = extract_modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_PDBFile(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import extract as extract_pdbfile
    tmp_item = PDBFile(item)
    tmp_item = extract_pdbfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from pdbfixer.pdbfixer import PDBFixer
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import extract as extract_pdbfixer_PDBFixer
    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_pytraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from pytraj import load as pytraj_load
    from molsysmt.forms.classes.api_pytraj_Trajectory import extract as extract_pytraj_Trajectory
    tmp_item = pytraj_load(item)
    tmp_item = extract_pytraj_Trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_pytraj_Topology(item, atom_indices='all', frame_indices='all'):

    from pytraj import load_topology as pytraj_load_topology
    from molsysmt.forms.classes.api_pytraj_Topology import extract as extract_pytraj_Topology
    tmp_item = pytraj_load_topology(item)
    tmp_item = extract_pytraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from nglview import show_file as _nglview_show_file
    from os import remove
    tmp_file = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _nglview_show_file(tmp_file)
    remove(tmp_file)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_yank_Topography as openmm_to_yank_Topography
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_to_yank_Topography(tmp_item)
    return tmp_item

def select_with_MDTraj(item, selection):

    from mdtraj import load_topology as _dtraj_load_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_sel = tmp_item.select(selection)
    del(tmp_item)
    return tmp_sel

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_openmm_PDBFile import select_with_MolSysMT as select_openmm_PDBFile_with_MolSysMT
    tmp_item = to_openmm_PDBFile(item)
    return select_openmm_PDBFile_with_MolSysMT(tmp_item, selection)

def copy(item, output_filepath=None):

    from shutil import copy as copy_file
    from molsysmt.utils.files_and_directories import tmp_filename
    if output_filepath is None:
        output_filepath = tmp_filename(extension='pdb')
    copy_file(item, output_filepath)
    return output_filepath

def extract(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    if atom_indices is 'all' and frame_indices is 'all':

        return copy(item, output_filepath=output_filepath)

    else:

        from molsysmt.forms.classes.api_molsysmt_MolSys import to_pdb as molsysmt_MolSys_to_pdb
        tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
        return molsysmt_MolSys_to_pdb(tmp_item, output_filepath=output_filepath)

###### Get

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_bonded_atoms_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_frames_from_atom as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_atom_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_group_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_component_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_chain_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_molecule_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_index_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_id_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_name_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_entity_type_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_bonded_atoms_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_atoms_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_groups_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_components_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_chains_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_molecules_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_entities_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_bonds_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_aminoacids_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_nucleotides_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_ions_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_waters_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_cosolutes_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_small_molecules_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_peptides_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_proteins_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_dnas_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_rnas_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_mass_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_charge_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_box_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)


def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_box_shape_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)


def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_box_lengths_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)


def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_box_angles_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)


def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_time_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)


def get_step_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_step_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_frame_from_system(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_system(item, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_frames_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name


