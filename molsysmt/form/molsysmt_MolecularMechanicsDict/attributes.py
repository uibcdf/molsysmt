from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

attributes['forcefield'] = True
attributes['non_bonded_method'] = True
attributes['non_bonded_cutoff'] = True
attributes['switch_distance'] = True
attributes['use_dispersion_correction'] = True
attributes['ewald_error_tolerance'] = True
attributes['hydrogen_mass'] = True
attributes['constraints'] = True
attributes['flexible_constraints'] = True
attributes['water_model'] = True
attributes['rigid_water'] = True
attributes['residue_templates'] = True
attributes['ignore_external_bonds'] = True
attributes['implicit_solvent'] = True
attributes['implicit_solvent'] = True
attributes['solute_dielectric'] = True
attributes['solvent_dielectric'] = True
attributes['implicit_solvent_salt_conc'] = True
attributes['implicit_solvent_kappa'] = True

del(_all_attributes)
