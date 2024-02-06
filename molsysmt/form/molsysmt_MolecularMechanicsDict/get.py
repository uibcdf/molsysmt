#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

form='molsysmt.MolecularMechanicsDict'


## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
        return np.arange(0,n_atoms)

    else:

        return indices

@digest(form=form)
def get_n_atoms_from_atom (item, indices='all', skip_digestion=False):

    output = None

    if is_all(indices):

        for attribute in ['formal_charge', 'partial_charge']:
            if attribute in item:
                if item[attribute] is not None:
                    output = len(item[attribute])
                    break
    else:

        output = len(indices)

    return output

@digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        try:
            return item['formal_charge']
        except:
            return None
    else:
        try:
            return item['formal_charge'][indices]
        except:
            return None

@digest(form=form)
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):
        try:
            return item['partial_charge']
        except:
            return None
    else:
        try:
            return item['partial_charge'][indices]
        except:
            return None

## From system

@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return get_n_atoms_from_atom(item, skip_digestion=True)


@digest(form=form)
def get_forcefield_from_system(item, skip_digestion=False):

    try:
        return item['forcefield']
    except:
        return None

@digest(form=form)
def get_non_bonded_method_from_system(item, skip_digestion=False):

    try:
        return item['non_bonded_method']
    except:
        return None

@digest(form=form)
def get_cutoff_distance_from_system(item, skip_digestion=False):

    try:
        return item['cutoff_distance']
    except:
        return None

@digest(form=form)
def get_switch_distance_from_system(item, skip_digestion=False):

    try:
        return item['switch_distance']
    except:
        return None

@digest(form=form)
def get_dispersion_correction_from_system(item, skip_digestion=False):

    try:
        return item['dispersion_correction']
    except:
        return None

@digest(form=form)
def get_ewald_error_tolerance_from_system(item, skip_digestion=False):

    try:
        return item['ewald_error_tolerance']
    except:
        return None

@digest(form=form)
def get_hydrogen_mass_from_system(item, skip_digestion=False):

    try:
        return item['hydrogen_mass']
    except:
        return None

@digest(form=form)
def get_constraints_from_system(item, skip_digestion=False):

    try:
        return item['constraints']
    except:
        return None

@digest(form=form)
def get_flexible_constraints_from_system(item, skip_digestion=False):

    try:
        return item['flexible_constraints']
    except:
        return None

@digest(form=form)
def get_water_model_from_system(item, skip_digestion=False):

    try:
        return item['water_model']
    except:
        return None

@digest(form=form)
def get_rigid_water_from_system(item, skip_digestion=False):

    try:
        return item['rigid_water']
    except:
        return None

@digest(form=form)
def get_implicit_solvent_from_system(item, skip_digestion=False):

    try:
        return item['implicit_solvent']
    except:
        return None

@digest(form=form)
def get_solute_dielectric_from_system(item, skip_digestion=False):

    try:
        return item['solute_dielectric']
    except:
        return None

@digest(form=form)
def get_solvent_dielectric_from_system(item, skip_digestion=False):

    try:
        return item['solvent_dielectric']
    except:
        return None

@digest(form=form)
def get_salt_concentration_from_system(item, skip_digestion=False):

    try:
        return item['salt_concentration']
    except:
        return None

@digest(form=form)
def get_kappa_from_system(item, skip_digestion=False):

    try:
        return item['kappa']
    except:
        return None

