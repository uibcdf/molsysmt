from molsysmt.attribute.attributes import attributes as _all_attributes

attributes = {ii:False for ii in _all_attributes}

###
### MECHANICAL ATTRIBUTES
###

attributes['formal_charge'] = True
attributes['partial_charge'] = True
attributes['forcefield'] = True
attributes['non_bonded_method'] = True
attributes['cutoff_distance'] = True  
attributes['switch_distance'] = True                                        
attributes['dispersion_correction'] = True                                                                           
attributes['ewald_error_tolerance'] = True                                              
attributes['hydrogen_mass'] = True                                      
attributes['constraints'] = True                                    
attributes['flexible_constraints'] = True                                                                                           
attributes['water_model'] = True                                    
attributes['rigid_water'] = True                                    
attributes['implicit_solvent'] = True
attributes['solute_dielectric'] = True
attributes['solvent_dielectric'] = True
attributes['salt_concentration'] = True
attributes['kappa'] = True     

del(_all_attributes)
