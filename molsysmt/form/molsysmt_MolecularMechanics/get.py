#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

form='molsysmt.MolecularMechanics'

###
### Atom
###

# Topology

@digest(form=form)
def get_atom_index_from_atom(item, indices='all'):

    if is_all(indices):

        n_atoms = get_n_atoms_from_system(item)
        return np.arange(0,n_atoms)

    else:

        return indices

@digest(form=form)
def get_n_atoms_from_atom (item, indices='all'):

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

@digest(form=form)
def get_formal_charge_from_atom (item, indices='all'):

    if is_all(indices):
        output = item.formal_charge
    else:
        output = item.formal_charge[indices]

    return output

@digest(form=form)
def get_partial_charge_from_atom (item, indices='all'):

    if is_all(indices):
        output = item.partial_charge
    else:
        output = item.partial_charge[indices]

    return output

###
### System
###

# Topology

@digest(form=form)
def get_n_atoms_from_system(item):

    return get_n_atoms_from_atom(item)

## Molecular Mechanics

@digest(form=form)
def get_forcefield_from_system(item):          

    return item.forcefield

@digest(form=form)
def get_non_bonded_method_from_system(item):

    return item.non_bonded_method

@digest(form=form)
def get_cutoff_distance_from_system(item):

    return item.cutoff_distance

@digest(form=form)
def get_switch_distance_from_system(item):

    return item.switch_distance

@digest(form=form)
def get_dispersion_correction_from_system(item):

    return item.dispersion_correction

@digest(form=form)
def get_ewald_error_tolerance_from_system(item):

    return item.ewald_error_tolerance

@digest(form=form)
def get_hydrogen_mass_from_system(item):

    return item.hydrogen_mass

@digest(form=form)
def get_constraints_from_system(item):

    return item.constraints

@digest(form=form)
def get_flexible_constraints_from_system(item):

    return item.flexible_constraints

@digest(form=form)
def get_water_model_from_system(item):

    return item.water_model

@digest(form=form)
def get_rigid_water_from_system(item):

    return item.rigid_water

@digest(form=form)
def get_implicit_solvent_from_system(item):

    return item.implicit_solvent

@digest(form=form)
def get_solute_dielectric_from_system(item):

    return item.solute_dielectric

@digest(form=form)
def get_solvent_dielectric_from_system(item):

    return item.solvent_dielectric

@digest(form=form)
def get_salt_concentration_from_system(item):

    return item.salt_concentration

@digest(form=form)
def get_kappa_from_system(item):

    return item.kappa

