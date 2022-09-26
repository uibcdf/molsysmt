from molsysmt.form.molsysmt_MolecularMechanics.is_molsysmt_MolecularMechanics import \
    is_molsysmt_MolecularMechanics as is_form
from molsysmt.form.molsysmt_MolecularMechanics.extract import extract
from molsysmt.form.molsysmt_MolecularMechanics.add import add
from molsysmt.form.molsysmt_MolecularMechanics.append_structures import append_structures
from molsysmt.form.molsysmt_MolecularMechanics.get import *
from molsysmt.form.molsysmt_MolecularMechanics.set import *
from .form_attributes import form_attributes

form_name = 'molsysmt.MolecularMechanics'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['forcefield'] = True
form_attributes['non_bonded_method'] = True
form_attributes['non_bonded_cutoff'] = True
form_attributes['switch_distance'] = True
form_attributes['use_dispersion_correction'] = True
form_attributes['ewald_error_tolerance'] = True
form_attributes['hydrogen_mass'] = True
form_attributes['constraints'] = True
form_attributes['flexible_constraints'] = True
form_attributes['water_model'] = True
form_attributes['rigid_water'] = True
form_attributes['residue_templates'] = True
form_attributes['ignore_external_bonds'] = True
form_attributes['implicit_solvent'] = True
form_attributes['implicit_solvent'] = True
form_attributes['solute_dielectric'] = True
form_attributes['solvent_dielectric'] = True
form_attributes['implicit_solvent_salt_conc'] = True
form_attributes['implicit_solvent_kappa'] = True


def to_MolecularMechanicsDict(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.molsysmt_MolecularMechanics import \
        to_molsysmt_MolecularMechanicsDict as molsysmt_MolecularMechanics_to_molsysmt_MolecularMechanicsDict

    return molsysmt_MolecularMechanics_to_molsysmt_MolecularMechanicsDict(item)
