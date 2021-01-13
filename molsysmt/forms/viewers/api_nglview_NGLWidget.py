from os.path import basename as _basename
from nglview import widget as _nglview_widget

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form = {
    _nglview_widget.NGLWidget: form_name
    }

info=["NGLView visualization native object","http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

with_topology=True
with_coordinates=True
with_box=True
with_parameters=False

def to_openmm_PDBFile(item, trajectory_item = None, atom_indices='all', frame_indices='all'):

    from io import StringIO
    from simtk.openmm.app import PDBFile
    try:
        structure_string = item.component_0.get_structure_string()
    except:
        structure_string = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']
    str_as_file = StringIO(structure_string)
    tmp_file = PDBFile(str_as_file)
    str_as_file.close()
    del(str_as_file)

    return tmp_file

def to_molsysmt_Topology(item, trajectory_item = None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.viewers import from_nglview_NGLWidget as nglview_NGLWidget_to_molsysmt_Topology
    return nglview_NGLWidget_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices='all')

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.forms.classes.api_openmm_PDBFile import select_with_MolSysMT as select_openmm_PDBFile_with_MolSysMT
    tmp_item = to_openmm_PDBFile(item)
    return select_openmm_PDBFile_with_MolSysMT(tmp_item, selection)

###### Get

## Atom

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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_comonents_from_atom as _get
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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_comopnent_type_from_group as _get
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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_group as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_component as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_comonents_from_molecule as _get
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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_molecule as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_chain as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

    from molsysmt.forms.classes.api_openmm_PDBFile import get_coordinates_from_entity as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

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

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_box_volume_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_time_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import get_n_frames_from_system as _get
    tmp_item = to_openmm_PDBFile(item)
    return _get(tmp_item, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name
