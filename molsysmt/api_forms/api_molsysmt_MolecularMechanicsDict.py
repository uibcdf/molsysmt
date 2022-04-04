from molsysmt._private.exceptions import *

from molsysmt.form.molsysmt_MolecularMechanicsDict.is_molsysmt_MolecularMechanicsDict import is_molsysmt_MolecularMechanicsDict as is_form
from molsysmt.form.molsysmt_MolecularMechanicsDict.extract import extract
from molsysmt.form.molsysmt_MolecularMechanicsDict.add import add
from molsysmt.form.molsysmt_MolecularMechanicsDict.merge import merge
from molsysmt.form.molsysmt_MolecularMechanicsDict.append_structures import append_structures
from molsysmt.form.molsysmt_MolecularMechanicsDict.concatenate_structures import concatenate_structures
from molsysmt.form.molsysmt_MolecularMechanicsDict.get import *
from molsysmt.form.molsysmt_MolecularMechanicsDict.set import *

form_name='molsysmt.MolecularMechanicsDict'
form_type='class'
form_info=["",""]


form_attributes = {

    'atom_index' : False,
    'atom_id' : False,
    'atom_name' : False,
    'atom_type' : False,

    'bond_index' : False,
    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

    'group_index' : False,
    'group_id' : False,
    'group_name' : False,
    'group_type' : False,

    'component_index' : False,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : False,
    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_index' : False,
    'chain_id' : False,
    'chain_name' : False,
    'chain_type' : False,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : False,
    'velocities' : False,
    'box' : False,
    'time' : False,
    'step' : False,

    'forcefield' : True,
    'non_bonded_method' : True,
    'non_bonded_cutoff' : True,
    'switch_distance' : True,
    'use_dispersion_correction' : True,
    'ewald_error_tolerance' : True,
    'hydrogen_mass' : True,
    'constraints' : True,
    'flexible_constraints' : True,
    'water_model' : True,
    'rigid_water' : True,
    'residue_templates' : True,
    'ignore_external_bonds' : True,
    'implicit_solvent' : True,
    'implicit_solvent' : True,
    'solute_dielectric' : True,
    'solvent_dielectric' : True,
    'implicit_solvent_salt_conc' : True,
    'implicit_solvent_kappa' : True,

    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_MolecularMechanics(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.molsysmt_MolecularMechanicsDict import to_molsysmt_MolecularMechanics as molsysmt_MolecularMechanicsDict_to_molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanicsDict_to_molsysmt_MolecularMechanics(item, check=False)

    return tmp_item

