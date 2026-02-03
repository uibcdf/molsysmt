#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

form='molsysmt.MolecularMechanics'

###
### Atom
###

# Topology

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    if is_all(indices):

        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
        return np.arange(0,n_atoms)

    else:

        return indices

@arg_digest(form=form)
def get_n_atoms_from_atom (item, indices='all', skip_digestion=False):

    output = None

    if is_all(indices):

        if item.formal_charge is not None:
            output = len(item.formal_charge)
        elif item.partial_charge is not None:
            output = len(item.partial_charge)

    else:

        output = len(indices)

    return output


## Molecular Mechanics

@arg_digest(form=form)
def get_formal_charge_from_atom (item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.formal_charge
    else:
        output = item.formal_charge[indices]

    return output

@arg_digest(form=form)
def get_partial_charge_from_atom (item, indices='all', skip_digestion=False):

    if is_all(indices):
        output = item.partial_charge
    else:
        output = item.partial_charge[indices]

    return output

###
### System
###

# Topology

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return get_n_atoms_from_atom(item, skip_digestion=True)

## Molecular Mechanics

@arg_digest(form=form)
def get_forcefield_from_system(item, skip_digestion=False):          

    return item.forcefield

@arg_digest(form=form)
def get_non_bonded_method_from_system(item, skip_digestion=False):

    return item.non_bonded_method

@arg_digest(form=form)
def get_cutoff_distance_from_system(item, skip_digestion=False):

    return item.cutoff_distance

@arg_digest(form=form)
def get_switch_distance_from_system(item, skip_digestion=False):

    return item.switch_distance

@arg_digest(form=form)
def get_dispersion_correction_from_system(item, skip_digestion=False):

    return item.dispersion_correction

@arg_digest(form=form)
def get_ewald_error_tolerance_from_system(item, skip_digestion=False):

    return item.ewald_error_tolerance

@arg_digest(form=form)
def get_hydrogen_mass_from_system(item, skip_digestion=False):

    return item.hydrogen_mass

@arg_digest(form=form)
def get_constraints_from_system(item, skip_digestion=False):

    return item.constraints

@arg_digest(form=form)
def get_flexible_constraints_from_system(item, skip_digestion=False):

    return item.flexible_constraints

@arg_digest(form=form)
def get_water_model_from_system(item, skip_digestion=False):

    return item.water_model

@arg_digest(form=form)
def get_rigid_water_from_system(item, skip_digestion=False):

    return item.rigid_water

@arg_digest(form=form)
def get_implicit_solvent_from_system(item, skip_digestion=False):

    return item.implicit_solvent

@arg_digest(form=form)
def get_solute_dielectric_from_system(item, skip_digestion=False):

    return item.solute_dielectric

@arg_digest(form=form)
def get_solvent_dielectric_from_system(item, skip_digestion=False):

    return item.solvent_dielectric

@arg_digest(form=form)
def get_salt_concentration_from_system(item, skip_digestion=False):

    return item.salt_concentration

@arg_digest(form=form)
def get_kappa_from_system(item, skip_digestion=False):

    return item.kappa

