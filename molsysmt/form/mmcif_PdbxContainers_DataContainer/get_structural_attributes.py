#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import types

form='mmcif.PdbxContainers.DataContainer'


## From atom

@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_coordinates_from_atom as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_occupancy_from_atom as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@arg_digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_atom as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_b_factor_from_atom as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, structure_indices='all', skip_digestion=True)

    return output

@arg_digest(form=form)
def get_formal_charge_from_atom (item, indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
    from molsysmt.form.molsysmt_MolecularMechanics import get_formal_charge_from_atom as aux_get

    tmp_item = to_molsysmt_MolecularMechanics(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_partial_charge_from_atom (item, indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanics import to_molsysmt_MolecularMechanics
    from molsysmt.form.molsysmt_MolecularMechanics import get_partial_charge_from_atom as aux_get

    tmp_item = to_molsysmt_MolecularMechanics(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        index_att = {jj: ii for ii, jj in enumerate(item.getObj('atom_site').getAttributeList())}
        model_nums = {row[index_att['pdbx_PDB_model_num']] for row in item.getObj('atom_site').data}
        return len(model_nums)
    else:
        return len(structure_indices)

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    from molsysmt.pbc import get_box_from_lengths_and_angles

    n_structures = get_n_structures_from_system(item, skip_digestion=True)

    check_if_cell = True
    if item.exists('exptl'):
        if 'NMR' in item.getObj('exptl').getValue('method'):
            check_if_cell = False

    if item.exists('cell') and check_if_cell:

        index_att = {jj: ii for ii, jj in enumerate(item.getObj('cell').getAttributeList())}
        cell_data = item.getObj('cell').data[0]

        cell_lengths = np.empty([n_structures, 3], dtype='float64')
        cell_angles = np.empty([n_structures, 3], dtype='float64')

        cell_lengths[:, 0] = float(cell_data[index_att['length_a']])
        cell_lengths[:, 1] = float(cell_data[index_att['length_b']])
        cell_lengths[:, 2] = float(cell_data[index_att['length_c']])

        cell_angles[:, 0] = float(cell_data[index_att['angle_alpha']])
        cell_angles[:, 1] = float(cell_data[index_att['angle_beta']])
        cell_angles[:, 2] = float(cell_data[index_att['angle_gamma']])

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles, skip_digestion=True)
        box = puw.standardize(box)

    else:

        box = None

    if not is_all(structure_indices):
        if box is not None:
            box = box[structure_indices, :, :]

    return box

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):

    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    return tmp_item.structures.bioassembly

@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):

    if item.exists('pdbx_struct_assembly_gen'):
        index_att = {jj: ii for ii, jj in enumerate(item.getObj('pdbx_struct_assembly_gen').getAttributeList())}
        assembly_ids = {row[index_att['assembly_id']] for row in item.getObj('pdbx_struct_assembly_gen').data}
        return len(assembly_ids)
    return 0

@arg_digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all', skip_digestion=False):

    from .to_molsysmt_Structures import to_molsysmt_Structures
    from molsysmt.form.molsysmt_Structures import get_alternate_location_from_system as aux_get

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output





# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

